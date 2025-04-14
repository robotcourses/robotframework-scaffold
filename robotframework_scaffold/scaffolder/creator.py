import os
import shutil
from .structure import PROJECT_TYPES
from .constants import GITIGNORE_CONTENT
from .base_resource import write_base_resource
from .readme import create_readme
from .create_common_resource import create_common_resources
import click
from pathlib import Path

def create_project(info):
    base_path = info["base_path"]
    project_type = info["type"]

    # Se o diretório já existir, remove
    if os.path.exists(base_path):
        shutil.rmtree(base_path)

    # Cria as pastas principais
    os.makedirs(os.path.join(base_path, "tests"), exist_ok=True)
    os.makedirs(os.path.join(base_path, "resources"), exist_ok=True)

    # Cria subpastas específicas conforme o tipo de projeto
    for folder in PROJECT_TYPES[project_type]:
        os.makedirs(os.path.join(base_path, "resources", folder), exist_ok=True)

    # Gera o base.resource com a Library correta
    write_base_resource(
        Path(base_path),
        project_type,
        info.get("web_library")  # só será usado se o tipo for web
    )

    # Cria os arquivos commons (web e mobile) e connection (api)
    create_common_resources(Path(base_path), project_type, info.get("web_library"))

    # Cria o .gitignore
    with open(os.path.join(base_path, ".gitignore"), "w") as gitignore:
        gitignore.write(GITIGNORE_CONTENT)

    # Cria o README.md
    create_readme(info)

    click.secho("✅ Project scaffold created successfully!", fg="green")
