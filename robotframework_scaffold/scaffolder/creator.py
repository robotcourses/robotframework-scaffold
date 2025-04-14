import os
import shutil
from .structure import PROJECT_TYPES
from .constants import GITIGNORE_CONTENT
from .base_resource import write_base_resource
import click
from pathlib import Path

def create_project(info):
    base_path = info["base_path"]
    project_type = info["type"]

    if os.path.exists(base_path):
        shutil.rmtree(base_path)

    os.makedirs(os.path.join(base_path, "tests"), exist_ok=True)
    os.makedirs(os.path.join(base_path, "resources"), exist_ok=True)

    for folder in PROJECT_TYPES[project_type]:
        os.makedirs(os.path.join(base_path, "resources", folder), exist_ok=True)

    # Gera o base.resource com a Library correta
    write_base_resource(
        Path(base_path),
        project_type,
        info.get("web_library")  # só será usado se o tipo for web
    )

    with open(os.path.join(base_path, ".gitignore"), "w") as gitignore:
        gitignore.write(GITIGNORE_CONTENT)

    click.secho("✅ Project scaffold created successfully!", fg="green")
