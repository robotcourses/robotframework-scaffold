import os
import click

def create_suite_from_routes(project_path: str, keyword_files: list):
    suite_path = os.path.join(project_path, "tests", "test_all_endpoints.robot")
    tests = []

    for resource in keyword_files:
        filename = os.path.basename(resource)  # ex: post_pet_petid_uploadimage.robot
        raw_name = os.path.splitext(filename)[0]  # post_pet_petid_uploadimage
        keyword_name = raw_name.replace("_", " ").title()  # Post Pet Petid Uploadimage

        test_case = f"""Scenario: {keyword_name}
    {keyword_name}
    Log    Test executed"""
        tests.append(test_case)

    try:
        with open(suite_path, "w") as f:
            f.write("*** Settings ***\n")
            f.write("Documentation    Example Suite with Routes Execution\n")
            f.write("Resource    ../base.resource\n\n")
            f.write("*** Test Cases ***\n")
            f.write("\n\n".join(tests))
        click.secho(f"✅ Test suite created: {suite_path}", fg="green")
    except Exception as e:
        click.secho(f"❌ Failed to create test suite: {e}", fg="red")

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
        click.secho(f"✅ Arquivo '__init__.robot' criado em: {init_path}", fg="green")
    except Exception as e:
        click.secho(f"❌ Falha ao criar '__init__.robot': {e}", fg="red")
