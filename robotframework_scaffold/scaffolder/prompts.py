import os
import click
import sys

def collect_project_info():
    click.echo("🛠️  Welcome to the Robot Framework Scaffold!\n")

    # 1. Project name with default suggestion
    default_name = os.path.basename(os.getcwd())
    name = click.prompt("📦 Project names", default=default_name)
    base_path = os.path.abspath(name)

    # 2. Check if folder already exists
    if os.path.exists(base_path):
        overwrite = click.confirm(f"⚠️  The folder '{name}' already exists. Overwrite?", default=False)
        if not overwrite:
            click.echo("❌ Operation cancelled.")
            raise click.Abort()

    # 3. Ask for project type
    click.echo("📂 Choose your project type:")
    click.echo("  1 - API")
    click.echo("  2 - Web")
    click.echo("  3 - Mobile")
    type_choice = click.prompt("🔧 Your choice", type=click.Choice(["1", "2", "3"]), default="1")

    project_type_map = {
        "1": "api",
        "2": "web",
        "3": "mobile"
    }
    project_type = project_type_map[type_choice]

    # 3.1 If web, ask which library
    web_library = None
    if project_type == "web":
        click.echo("🌐 Choose your Web testing library:")
        click.echo("  1 - SeleniumLibrary")
        click.echo("  2 - BrowserLibrary")
        choice = click.prompt("🔧 Your choice", type=click.Choice(["1", "2"]), default="1")
        web_library = "SeleniumLibrary" if choice == "1" else "BrowserLibrary"

    # 4. Confirm creation
    if not click.confirm("🔧 Proceed with project creation?", default=True):
        click.echo("❌ Operation cancelled.")
        raise click.Abort()

    # 5. Ask about Poetry usage
    click.echo("⚙️  Choose the environment manager:")
    click.echo("  1 - Poetry")
    click.echo("  2 - venv")
    env_choice = click.prompt("🔧 Your choice", type=click.Choice(["1", "2"]), default="1")

    env_manager = "poetry" if env_choice == "1" else "venv"


    # 6. Project Description
    description = click.prompt("📝 Describe your project:")

    # Info Dict
    return {
        "name": name,
        "base_path": base_path,
        "type": project_type,
        "web_library": web_library,
        "description": description,
        "env_manager": env_manager,
        "python_version": ">=3.8,<3.14"
    }
