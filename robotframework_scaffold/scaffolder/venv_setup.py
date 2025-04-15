import os
import subprocess
import click


def init_venv(info: dict):
    base_path = info["base_path"]
    click.echo("\n🚀 Creating environment with venv...")

    venv_dir = os.path.join(base_path, ".venv")

    try:
        # Cria o ambiente virtual
        subprocess.run(["python", "-m", "venv", venv_dir], check=True)
        click.echo(f"✅ Virtual environment created at {venv_dir}")

        # Caminho para o executável python dentro do venv
        python_path = (
            os.path.join(venv_dir, "bin", "python") if os.name != "nt"
            else os.path.join(venv_dir, "Scripts", "python.exe")
        )

        # Atualiza o pip com segurança
        subprocess.run([python_path, "-m", "pip", "install", "--upgrade", "pip"], check=True)

        # Instala o Robot Framework
        subprocess.run([python_path, "-m", "pip", "install", "robotframework"], check=True)

        # Instala a biblioteca extra com base no tipo de projeto
        project_type = info.get("type")
        web_library = (info.get("web_library") or "").lower()

        lib_map = {
            "api": "robotframework-requests",
            "web": "robotframework-seleniumlibrary" if web_library == "seleniumlibrary" else "robotframework-browser",
            "mobile": "robotframework-appiumlibrary"
        }

        extra_lib = lib_map.get(project_type)
        if extra_lib:
            subprocess.run([python_path, "-m", "pip", "install", extra_lib], check=True)

        click.secho("✅ Environment ready to use!", fg="green")

        if os.name == "nt":
            activate_cmd = r".venv\Scripts\activate"
        else:
            activate_cmd = "source .venv/bin/activate"

        click.secho(f"👉 To activate the virtual environment, run:\n\n   {activate_cmd}\n", fg="yellow")
        click.secho("💡 If you're using VSCode, it might detect the .venv automatically.", fg="cyan")

    except subprocess.CalledProcessError:
        click.secho("❌ Failed to configure environment with venv.", fg="red", bold=True)
