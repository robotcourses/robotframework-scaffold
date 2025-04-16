import click
from robotframework_scaffold.scaffolder.prompts import collect_project_info
from robotframework_scaffold.scaffolder.preview import preview_structure
from robotframework_scaffold.scaffolder.creator import create_project
from robotframework_scaffold.scaffolder.poetry_setup import init_poetry
from robotframework_scaffold.scaffolder.venv_setup import init_venv
from robotframework_scaffold.scaffolder.templates.api.create_session.session_generator import create_api_session_files
from robotframework_scaffold.scaffolder.templates.api.create_contracts_routes.contracts_generator import ask_about_swagger, generate_keywords_from_swagger
from robotframework_scaffold.scaffolder.base_resource import append_resources_to_base
from robotframework_scaffold.scaffolder.suite_generator import create_test_init_file


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

    if info["type"] == "api":
        app_name, env = create_api_session_files(info["base_path"])
        swagger_url, wants_auto_generate = ask_about_swagger()
        if swagger_url and wants_auto_generate:
            generated_files = generate_keywords_from_swagger(swagger_url, info["base_path"], app_name)
            if generated_files:
                append_resources_to_base(info["base_path"], generated_files, env)
                create_test_init_file(info["base_path"], app_name)
    
    click.secho("\n")
    click.secho("🎉  Project successfully created", fg="blue", bold=True)
    click.secho("⚠️  ATTENTION: Robot Scaffold is intended to speed up your coding work and not replace it completely.\nErrors in generating Keywords may occur.\nSo, please review all generated code before committing to the remote repository.", fg="yellow")

if __name__ == '__main__':
    main()