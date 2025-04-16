from .constants import API_BASE_RESOURCE, SELENIUM_BASE_RESOURCE, BROWSER_BASE_RESOURCE, MOBILE_BASE_RESOURCE
from pathlib import Path
import click
import os

def write_base_resource(project_path: Path, project_type: str, web_library: str = None, env: str = "dev"):
    # Define default libraries
    libraries = {
        "api": "RequestsLibrary",
        "web": "SeleniumLibrary",
        "mobile": "AppiumLibrary"
    }

    # Sobrescreve se for projeto web e o usuário escolheu outra lib
    if project_type.lower() == "web" and web_library:
        library = web_library
    else:
        library = libraries.get(project_type.lower())

    if not library:
        click.secho(f"[!] Unknown project type: {project_type}", fg="red", bold=True)
        return

    base_resource_path = project_path / "base.resource"
    base_resource_path.parent.mkdir(parents=True, exist_ok=True)

    if project_type == 'api':
        content = API_BASE_RESOURCE
    elif project_type == 'web' and web_library == 'BrowserLibrary':
        content = BROWSER_BASE_RESOURCE
    elif project_type == 'web':
        content = SELENIUM_BASE_RESOURCE
    elif project_type == 'mobile':
        content = MOBILE_BASE_RESOURCE
    else:
        content = ""

    try:
        base_resource_path.write_text(content)
        click.secho(f"[✓] base.resource created with {library} and ENV={env}", fg="green")
    except Exception as e:
        click.secho(f"[!] Failed to write base.resource: {e}", fg="red", bold=True)

def append_resources_to_base(project_path: str, resource_files: list, env: str):
    base_file = os.path.join(project_path, "base.resource")

    try:
        with open(base_file, "r") as f:
            lines = f.readlines()

        # Inserir routes na seção de Settings
        settings_end_index = 0
        for idx, line in enumerate(lines):
            if line.strip().startswith("*** Variables ***"):
                settings_end_index = idx
                break
        else:
            # Se não encontrar, adiciona no final
            settings_end_index = len(lines)

        route_lines = ["\n## Routes\n"] + [f"Resource    {r}\n" for r in sorted(resource_files)]

        # Inserir ENV na seção de Variables, ou criar uma nova se não existir
        env_line = f"${{ENV}}    {env}\n"
        if any("*** Variables ***" in line for line in lines):
            for idx, line in enumerate(lines):
                if line.strip().startswith("*** Variables ***"):
                    # Encontrou a seção Variables
                    insert_idx = idx + 1
                    while insert_idx < len(lines) and lines[insert_idx].strip().startswith("${"):
                        insert_idx += 1
                    lines.insert(insert_idx, env_line)
                    break
        else:
            # Se não tiver seção Variables, adiciona ao final
            lines += ["\n*** Variables ***\n", env_line]

        # Adiciona os Resources na seção de Settings
        lines = lines[:settings_end_index] + route_lines + lines[settings_end_index:]

        with open(base_file, "w") as f:
            f.writelines(lines)

        click.secho("✅ base.resource updated with routes and ENV", fg="green")
    except Exception as e:
        click.secho(f"❌ Failed to update base.resource: {e}", fg="red")