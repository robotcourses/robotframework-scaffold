from .constants import API_BASE_RESOURCE, SELENIUM_BASE_RESOURCE, BROWSER_BASE_RESOURCE, MOBILE_BASE_RESOURCE
from pathlib import Path
import click

def write_base_resource(project_path: Path, project_type: str, web_library: str = None):
    # Define default libraries
    libraries = {
        "api": "RequestsLibrary",
        "web": "SeleniumLibrary",  # será sobrescrito se web_library for definido
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
    elif project_type == 'web' and web_library != 'SeleniumLibrary':
        content = SELENIUM_BASE_RESOURCE
    elif project_type == 'web' and web_library != 'BrowserLibrary':
        content = BROWSER_BASE_RESOURCE
    elif project_type == 'mobile':
        content = MOBILE_BASE_RESOURCE

    try:
        base_resource_path.write_text(content)
        click.secho(f"[✓] base.resource created with {library}", fg="green")
    except Exception as e:
        click.secho(f"[!] Failed to write base.resource: {e}", fg="red", bold=True)
