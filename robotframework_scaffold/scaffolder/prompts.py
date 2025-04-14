import os
import click
import sys

def collect_project_info():
    click.echo("🛠️  Welcome to the Robot Framework Scaffold!\n")

    # 1. Project name with default suggestion
    default_name = "robot-tests"
    name = click.prompt("📦 Project name", default=default_name)
    base_path = os.path.abspath(name)

    # 2. Check if folder already exists
    if os.path.exists(base_path):
        overwrite = click.confirm(f"⚠️  The folder '{name}' already exists. Overwrite?", default=False)
        if not overwrite:
            click.echo("❌ Operation cancelled.")
            raise click.Abort()

    # 3. Ask for project type
    project_type = ""
    while project_type not in ("api", "web", "mobile"):
        project_type = click.prompt("📂 Project type (api/web/mobile)").lower()

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
    use_poetry = click.confirm("🐍 Create a virtual environment using Poetry?", default=True)

    # 6. Project Description
    description = click.prompt("📝 Describe your project:")

    return {
        "name": name,
        "base_path": base_path,
        "type": project_type,
        "web_library": web_library,
        "description": description,
        "use_poetry": use_poetry,
        "python_version": ">=3.8,<3.14"
    }
