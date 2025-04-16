import os
import click

def create_test_init_file(base_path: str, app_name: str):
    """
    Cria o arquivo tests/__init__.robot com o setup global da suite.
    """
    init_path = os.path.join(base_path, "tests", "__init__.robot")

    app_keyword = f"Create {app_name.replace('_', ' ').title()} Session"

    content = f"""*** Settings ***
Resource    ../base.resource
Test Setup  {app_keyword}
"""

    try:
        with open(init_path, "w") as f:
            f.write(content)
        click.secho(f"✅ File '__init__.robot' created in:: {init_path}", fg="green")
    except Exception as e:
        click.secho(f"❌ Failed to create '__init__.robot': {e}", fg="red")
