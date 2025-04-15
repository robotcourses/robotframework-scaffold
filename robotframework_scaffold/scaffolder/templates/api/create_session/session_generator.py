import os
import yaml
import click

def normalize_app_name(name: str) -> str:
    return name.strip().lower().replace(" ", "_")

def get_session_resource_content(app_name: str) -> str:
    """
    Gera o conteúdo do arquivo session.resource com base no nome da aplicação.
    """
    app_display_name = app_name.replace("_", " ").title().replace(" ", "")  # Ex: 'json_placeholder' -> 'JsonPlaceholder'
    return f"""*** Settings ***
Resource    ../../base.resource

*** Keywords ***
Create {app_display_name} Session
    Create Session
    ...  alias=${{{app_name}.alias}}
    ...  url=${{{app_name}.url}}
    ...  verify=${{False}}
    ...  disable_warnings=${{True}}
"""

def create_api_session_files(base_path: str):
    click.echo("\n🔧 Let's configure the API session creation files")

    # Coleta das informações da API
    app_name_raw = click.prompt("🔹 What is the name of the API under test?")
    app_name = normalize_app_name(app_name_raw)
    session_alias = click.prompt("🔹 What is the session alias?")

    sessions = {
        app_name: {
            "alias": session_alias
        }
    }

    while True:
        env = click.prompt("🌍 Which environment do you want to configure?", type=click.Choice(["dev", "hml", "sdx", "prd"]))
        url = click.prompt(f"🔗 What is the application's URL for environment '{env}'?")
        sessions[app_name][env] = {
            "url": url
        }

        add_more = click.confirm("➕ Do you want to add another environment?", default=False)
        if not add_more:
            break

    # Caminho do session_data.yml
    yml_path = os.path.join(base_path, "resources", "connections", "session_data.yml")
    os.makedirs(os.path.dirname(yml_path), exist_ok=True)

    with open(yml_path, "w", encoding="utf-8") as f:
        yaml.dump(sessions, f, default_flow_style=False, allow_unicode=True)

    click.secho(f"\n✅ File 'session_data.yml' successfully created at: {yml_path}", fg="green")

    # Criação do session.resource
    session_resource_path = os.path.join(base_path, "resources", "connections", "session.resource")
    os.makedirs(os.path.dirname(session_resource_path), exist_ok=True)

    content = get_session_resource_content(app_name)

    with open(session_resource_path, "w", encoding="utf-8") as f:
        f.write(content)

    click.secho(f"✅ File 'session.resource' successfully created at: {session_resource_path}\n", fg="green")

    return app_name
