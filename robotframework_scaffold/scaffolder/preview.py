from .structure import PROJECT_TYPES
import click

def preview_structure(info):
    project_type = info["type"]
    name = info["name"]

    click.secho("\n🧪 DRY RUN: The following structure would be created:\n", fg="cyan")
    click.echo(f"{name}/")
    click.echo(f"├── base.resource")
    click.echo(f"├── tests/")
    click.echo(f"├── .gitignore")
    click.echo(f"└── resources/")
    for folder in PROJECT_TYPES[project_type]:
        click.echo(f"    └── {folder}/")
