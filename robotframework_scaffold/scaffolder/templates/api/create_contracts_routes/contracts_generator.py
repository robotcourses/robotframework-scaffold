import click
import os
import requests
import json

def ask_about_swagger():
    has_swagger = click.confirm("🔹 Do you have a Swagger (OpenAPI) URL available?", default=False)
    if not has_swagger:
        click.echo("🚫 Swagger not provided. Skipping automatic generation.")
        return None, False

    while True:
        base_url = click.prompt("🔗 Please enter the Swagger base URL")
        data, resolved_url = try_resolve_swagger_json(base_url)
        if data:
            click.secho(f"✅ Swagger JSON found at: {resolved_url}", fg="green")
            generate_keywords = click.confirm("⚙️ Do you want to auto-generate keyword files from Swagger?", default=True)
            return resolved_url, generate_keywords
        else:
            click.secho("❌ Could not find a valid Swagger JSON from the provided base URL.", fg="red")
            retry = click.confirm("🔁 Do you want to try another URL?", default=True)
            if not retry:
                return None, False

def try_resolve_swagger_json(base_url: str):
    possible_paths = [
        "", "/swagger.json", "/v2/swagger.json", "/v3/api-docs", "/openapi.json",
        "/api-docs", "/docs/swagger.json", "/swagger/v1/swagger.json"
    ]
    for path in possible_paths:
        test_url = base_url.rstrip("/") + path
        try:
            response = requests.get(test_url, timeout=5)
            response.raise_for_status()
            json_data = response.json()
            if "paths" in json_data or "swagger" in json_data or "openapi" in json_data:
                return json_data, test_url
        except Exception:
            continue
    return None, None

def generate_keywords_from_swagger(swagger_url: str, base_path: str, app_name: str):
    click.echo(f'swagger_url: {swagger_url}')
    try:
        response = requests.get(swagger_url)
        response.raise_for_status()
        swagger_data = response.json()
    except Exception as e:
        click.secho(f"❌ Error accessing Swagger: {e}", fg="red")
        return []

    paths = swagger_data.get("paths", {})
    if not paths:
        click.secho("⚠️ No endpoints found in Swagger.", fg="yellow")
        return []

    definitions = swagger_data.get("definitions", {})
    components = swagger_data.get("components", {}).get("schemas", {})
    routes_dir = os.path.join(base_path, "resources", "routes")
    os.makedirs(routes_dir, exist_ok=True)

    generated_files = []

    for path, methods in paths.items():
        for method, details in methods.items():
            keyword_name = f"{method.title()}{path}".replace("/", " ").replace("{", "").replace("}", "")
            filename = f"{method}_{path.strip('/').replace('/', '_').replace('{', '').replace('}', '')}.robot"

            success_status = next(
                (code for code in details.get("responses", {}) if str(code).startswith("2")), "200"
            )

            path_params = [
                param["name"] for param in details.get("parameters", [])
                if param.get("in") == "path"
            ]

            parsed_url = path
            for param in path_params:
                parsed_url = parsed_url.replace(f"{{{param}}}", f"${{{param}}}")

            schema = extract_request_schema(details, swagger_data)
            example_body = {}
            if schema:
                try:
                    example_body = generate_example_from_schema(schema, definitions or components)
                except Exception as e:
                    click.secho(f"⚠️ Failed to generate body for {method.upper()} {path}: {e}", fg="yellow")

            args = "    ".join([f"${{{p}}}" for p in path_params])
            args += f"    ${{expected_status}}={success_status}"

            keyword_block = f"""*** Settings ***
Resource    ../../base.resource

*** Keywords ***
{keyword_name}
    [Documentation]    Auto-generated keyword for endpoint {path} ({method.upper()})
    [Arguments]    {args}
"""

            if example_body:
                keyword_block += f"""
    &{{payload}}    Create Dictionary    {format_dict_for_robot(example_body)}

    ${{response}}  {method.title()} On Session
    ...  alias=${{{app_name}.alias}}
    ...  url={parsed_url}
    ...  json=${{payload}}
    ...  expected_status=${{expected_status}}

    RETURN  ${{response}}
"""
            else:
                keyword_block += f"""
    ${{response}}  {method.title()} On Session
    ...  alias=${{{app_name}.alias}}
    ...  url={parsed_url}
    ...  expected_status=${{expected_status}}

    RETURN  ${{response}}
"""

            file_path = os.path.join(routes_dir, filename.lower())
            with open(file_path, "w") as f:
                f.write(keyword_block)

            generated_files.append(f"resources/routes/{filename.lower()}")
            click.secho(f"✅ Keyword criada: {file_path}", fg="green")

    return generated_files


def extract_request_schema(details: dict, swagger_data: dict) -> dict:
    schema = {}
    request_body = details.get("requestBody")
    if request_body:
        content = request_body.get("content", {}).get("application/json", {})
        schema = content.get("schema", {})

    if not schema:
        for param in details.get("parameters", []):
            if param.get("in") == "body":
                schema = param.get("schema", {})
                break

    if "$ref" in schema:
        ref = schema["$ref"]
        ref_name = ref.split("/")[-1]
        definitions = swagger_data.get("definitions", {})
        components = swagger_data.get("components", {}).get("schemas", {})
        schema = definitions.get(ref_name) or components.get(ref_name, {})

    return schema

def generate_example_from_schema(schema: dict, all_defs: dict) -> dict:
    if "$ref" in schema:
        ref = schema["$ref"].split("/")[-1]
        schema = all_defs.get(ref, {})

    if schema.get("type") == "object":
        result = {}
        for prop, spec in schema.get("properties", {}).items():
            if "$ref" in spec:
                result[prop] = generate_example_from_schema(spec, all_defs)
            elif spec.get("type") == "array":
                item = spec.get("items", {})
                if "$ref" in item:
                    result[prop] = [generate_example_from_schema(item, all_defs)]
                else:
                    result[prop] = [get_default_for_type(item.get("type", "string"))]
            else:
                result[prop] = get_default_for_type(spec.get("type", "string"))
        return result
    return {}

def get_default_for_type(prop_type: str):
    return {
        "string": "example",
        "integer": 123,
        "number": 123.45,
        "boolean": True,
        "array": [],
        "object": {},
    }.get(prop_type, "example")

def format_dict_for_robot(data: dict) -> str:
    return "    ".join(f"{k}={json.dumps(v)}" for k, v in data.items())
