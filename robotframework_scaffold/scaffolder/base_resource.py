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

        # Separa os arquivos por tipo
        route_resources = [r for r in resource_files if r.startswith("resources/routes")]
        custom_libraries = [r for r in resource_files if r.startswith("resources/contracts/")]

        # Adiciona os resources na seção Settings
        settings_end_index = 0
        for idx, line in enumerate(lines):
            if line.strip().startswith("*** Variables ***"):
                settings_end_index = idx
                break
        else:
            settings_end_index = len(lines)

        route_lines = ["\n## Routes\n"] + [f"Resource    {r}\n" for r in sorted(route_resources)]
        updated_lines = lines[:settings_end_index] + route_lines + lines[settings_end_index:]

        # Atualiza ou cria a seção de Variáveis com ENV
        env_line = f"${{ENV}}    {env}\n"
        if any("*** Variables ***" in line for line in updated_lines):
            for idx, line in enumerate(updated_lines):
                if line.strip().startswith("*** Variables ***"):
                    insert_idx = idx + 1
                    while insert_idx < len(updated_lines) and updated_lines[insert_idx].strip().startswith("${"):
                        insert_idx += 1
                    updated_lines.insert(insert_idx, env_line)
                    break
        else:
            updated_lines += ["\n*** Variables ***\n", env_line]

        # Adiciona Libraries customizadas logo após ## Custom Libraries
        for idx, line in enumerate(updated_lines):
            if "## Custom Libraries" in line:
                insert_at = idx + 1
                lib_lines = [f"Library    {lib}\n" for lib in sorted(set(custom_libraries))]
                updated_lines = updated_lines[:insert_at] + lib_lines + updated_lines[insert_at:]
                break

        # Salva arquivo final
        with open(base_file, "w") as f:
            f.writelines(updated_lines)

        click.secho("✅ base.resource updated with ENV, routes, and custom libraries.", fg="green")
    except Exception as e:
        click.secho(f"❌ Failed to update base.resource: {e}", fg="red")