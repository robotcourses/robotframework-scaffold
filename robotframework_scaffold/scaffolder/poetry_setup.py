import subprocess
import click

def init_poetry(info: dict):
    base_path = info["base_path"]
    project_name = info["name"]
    description = info.get("description", "")
    python_version = info.get("python_version", "^3.12")
    project_type = info.get("type", "").lower()

    click.echo("\n🚀 Initializing environment with Poetry...")

    # Define a lib extra com base no tipo de projeto
    if project_type == "web":
        web_library = info.get("web_library", "").lower()
        extra_lib = "robotframework-seleniumlibrary" if web_library == "seleniumlibrary" else "robotframework-browser"
    elif project_type == "api":
        extra_lib = "robotframework-requests"
    elif project_type == "mobile":
        extra_lib = "robotframework-appiumlibrary"
    else:
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

        subprocess.run(
            [
                "poetry", "install"
            ],
            cwd=base_path,
            check=True
        )

        click.secho("✅ Virtual environment created successfully!", fg="green")

    except subprocess.CalledProcessError:
        click.secho("❌ Error configuring environment with Poetry.", fg="red", bold=True)
