from pathlib import Path
from .constants import API_STRUCTURE, WEB_STRUCTURE, MOBILE_STRUCTURE

def create_readme(info: dict):
    base_path = Path(info["base_path"])
    readme_path = base_path / "README.md"

    project_name = info["name"]
    description = info.get("description", "")
    project_type = info["type"]

    if project_type == 'api':
        structure = API_STRUCTURE
    elif project_type == 'web':
        structure = WEB_STRUCTURE
    elif project_type == 'mobile':
        structure = MOBILE_STRUCTURE

    content = f"# {project_name}\n\n" \
              f"{description}\n\n" \
              f"## Project Structure\n{structure}"

    readme_path.write_text(content, encoding="utf-8")