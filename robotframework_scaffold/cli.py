import click
from robotframework_scaffold.scaffolder.prompts import collect_project_info
from robotframework_scaffold.scaffolder.preview import preview_structure
from robotframework_scaffold.scaffolder.creator import create_project
from robotframework_scaffold.scaffolder.poetry_setup import init_poetry
from robotframework_scaffold.scaffolder.venv_setup import init_venv


@click.group()
def main():
    pass

@main.command()
@click.option("--dry-run", is_flag=True, help="Preview the project structure without creating files.")
def init(dry_run):
    """Initialize a new Robot Framework project interactively."""
    info = collect_project_info()

    if dry_run:
        preview_structure(info)
        return

    create_project(info)

    if info["env_manager"] == "poetry":
        init_poetry(info)
    else:
        init_venv(info)

if __name__ == '__main__':
    main()