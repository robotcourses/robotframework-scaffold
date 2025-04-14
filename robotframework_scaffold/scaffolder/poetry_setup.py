import subprocess
import click


def init_poetry(info: dict):
    base_path = info["base_path"]
    project_name = info["name"]
    description = info.get("description", "")
    python_version = info.get("python_version", "^3.12")
    project_type = info.get("type", "").lower()
    web_library = info.get("web_library", "").lower()

    click.echo("\n🚀 Initializing environment with Poetry...")

    # Define a lib extra com base no tipo de projeto
    lib_map = {
        "api": "robotframework-requests",
        "web": "robotframework-seleniumlibrary" if web_library == "seleniumlibrary" else "robotframework-browser",
        "mobile": "robotframework-appiumlibrary"
    }

    extra_lib = lib_map.get(project_type)
    if not extra_lib:
        click.secho("❌ Unknown project type.", fg="red", bold=True)
        return

    try:
        subprocess.run(
            [
                "poetry", "init",
                "--name", project_name,
                "--description", description,
                "--python", python_version,
                "--dependency", "robotframework",
                "--dependency", extra_lib,
                "--no-interaction"
            ],
            cwd=base_path,
            check=True
        )

        click.secho("✅ Virtual environment created successfully!", fg="green")

    except subprocess.CalledProcessError:
        click.secho("❌ Error configuring environment with Poetry.", fg="red", bold=True)
