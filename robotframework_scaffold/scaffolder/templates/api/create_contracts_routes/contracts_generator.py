import click
import os
import requests
import json
import unicodedata
import re

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
            generate_keywords = click.confirm("⚙️  Do you want to auto-generate keyword files from Swagger?", default=True)
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
    routes_base = os.path.join(base_path, "resources", "routes")
    os.makedirs(routes_base, exist_ok=True)

    generated_files = []
    custom_libs = set()

    for path, methods in paths.items():
        for method, details in methods.items():
            try:
                raw_tag = details.get("tags", [None])[0]
                if raw_tag:
                    controller = normalize_tag(raw_tag)
                else:
                    parts = path.strip('/').split('/')
                    if len(parts) > 1:
                        controller = parts[1].capitalize()
                    elif parts:
                        controller = parts[0].capitalize()
                    click.secho(
                        f"⚠️ No tag found for '{path}'. Using fallback controller: '{controller}'",
                        fg="yellow"
                    )
            except Exception as e:
                click.secho(f"⚠️ Failed to extract controller for '{path}': {e}", fg="yellow")
                controller = "Unknown"

            # prepare directory per controller
            routes_dir = os.path.join(routes_base, controller)
            os.makedirs(routes_dir, exist_ok=True)

            keyword_name = f"{method.title()}{path}".replace("/", " ").replace("{", "").replace("}", "")
            filename = f"{method}_{path.strip('/').replace('/', '_').replace('{', '').replace('}', '')}.resource"

            # status code
            success_status = next((code for code in details.get("responses", {}) if str(code).startswith("2")), "200")

            # path parameters
            path_params = [p["name"] for p in details.get("parameters", []) if p.get("in") == "path"]

            # query parameters
            query_params = [p["name"] for p in details.get("parameters", []) if p.get("in") == "query"]

            # build URL
            parsed_url = path
            for p in path_params:
                parsed_url = parsed_url.replace(f"{{{p}}}", f"${{{p}}}")
            if query_params:
                qs = "&".join(f"{qp}=${{{qp}}}" for qp in query_params)
                parsed_url = f"{parsed_url}?{qs}"

            # request body schema
            schema = extract_request_schema(details, swagger_data)
            example_body = {}
            contract_args = []
            if schema:
                try:
                    example_body = generate_example_from_schema(schema, definitions or components)
                except Exception as e:
                    click.secho(f"⚠️ Failed to generate payload for {method.upper()} {path}: {e}", fg="yellow")

            # build arguments list
            robot_args = []
            for p in path_params:
                robot_args.append(f"${{{p}}}")
            for qp in query_params:
                robot_args.append(f"${{{qp}}}")
            if example_body:
                # generate contract module and args
                contract_path, contract_args = generate_python_contract_class(base_path, controller, method, path, example_body)
                custom_libs.add(contract_path)
                for arg in contract_args:
                    robot_args.append(f"${{{arg}}}")
            # expected status
            robot_args.append(f"${{expected_status}}={success_status}")

            # assemble keyword
            keyword_block = f"""*** Settings ***
Resource    ../../../base.resource

*** Keywords ***
{keyword_name}
    [Documentation]    Auto-generated keyword for endpoint {path} ({method.upper()})
    [Arguments]    {'    '.join(robot_args)}
"""

            if example_body:
                payload_args = '    '.join(f'${{{arg}}}' for arg in contract_args)
                keyword_block += f"""
    &{{payload}}    Contract {method.title()} {controller}    {payload_args}

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

            # write to controller subfolder
            file_path = os.path.join(routes_dir, filename.lower())
            with open(file_path, 'w') as f:
                f.write(keyword_block)
            generated_files.append(f"resources/routes/{controller}/{filename.lower()}")
            click.secho(f"✅ Keyword created: {file_path}", fg="green")

    return generated_files + sorted(custom_libs)



# 🔎 Detecta o schema de request para Swagger 2.0 e OpenAPI 3.x
def extract_request_schema(details: dict, swagger_data: dict) -> dict:
    schema = {}
    if 'requestBody' in details:
        content = details['requestBody'].get('content', {}).get('application/json', {})
        schema = content.get('schema', {})
    if not schema:
        for p in details.get('parameters', []):
            if p.get('in') == 'body':
                schema = p.get('schema', {})
                break
    if '$ref' in schema:
        ref = schema['$ref'].split('/')[-1]
        schema = swagger_data.get('definitions', {}).get(ref) or swagger_data.get('components', {}).get('schemas', {}).get(ref, {})
    return schema


# 🧠 Cria payloads de exemplo (com suporte a $ref aninhado)
def generate_example_from_schema(schema: dict, all_defs: dict) -> dict:
    if '$ref' in schema:
        ref = schema['$ref'].split('/')[-1]
        schema = all_defs.get(ref, {})
    if schema.get('type') == 'object':
        result = {}
        for prop, spec in schema.get('properties', {}).items():
            if '$ref' in spec:
                result[prop] = generate_example_from_schema(spec, all_defs)
            elif spec.get('type') == 'array':
                item = spec.get('items', {})
                if '$ref' in item:
                    result[prop] = [generate_example_from_schema(item, all_defs)]
                else:
                    result[prop] = [get_default_for_type(item.get('type', 'string'))]
            else:
                result[prop] = get_default_for_type(spec.get('type', 'string'))
        return result
    return {}


def get_default_for_type(prop_type: str):
    return {
        'string': 'example',
        'integer': 123,
        'number': 123.45,
        'boolean': True,
        'array': [],
        'object': {},
    }.get(prop_type, 'example')


def format_dict_for_robot(data: dict) -> str:
    return '    '.join(f"{k}={json.dumps(v)}" for k, v in data.items())


def generate_python_contract_class(base_path: str, controller: str, method: str, path: str, example_body: dict):
    from keyword import iskeyword

    class_name = controller
    method_name = f"{method.lower()}_{path.strip('/').replace('/', '_').replace('-', '_').replace('{', '').replace('}', '')}"
    keyword_name = f"Contract {method.title()} {controller}"

    controller_dir = os.path.join(base_path, 'resources', 'contracts', controller)
    os.makedirs(controller_dir, exist_ok=True)
    init_path = os.path.join(controller_dir, '__init__.py')

    variable_mapping = {}

    def flatten_dict(d, prefix=''):
        args = []
        for k, v in d.items():
            full_key = f"{prefix}.{k}" if prefix else k
            var_name = full_key.replace('.', '_').lower()
            if not iskeyword(var_name):
                variable_mapping[full_key] = var_name
                if isinstance(v, dict):
                    args.extend(flatten_dict(v, full_key))
                elif isinstance(v, list) and v and isinstance(v[0], dict):
                    args.extend(flatten_dict(v[0], full_key))
                else:
                    args.append(var_name)
        return args

    # get list of args for method signature
    args_list = flatten_dict(example_body)
    # build payload text
    def build_payload(d, prefix=''):
        if isinstance(d, dict):
            parts = []
            for k, v in d.items():
                full_key = f"{prefix}.{k}" if prefix else k
                var = variable_mapping.get(full_key)
                if isinstance(v, dict):
                    nested = build_payload(v, full_key)
                    parts.append(f"'{k}': {nested}")
                elif isinstance(v, list) and v and isinstance(v[0], dict):
                    nested = build_payload(v[0], full_key)
                    parts.append(f"'{k}': [{nested}]")
                elif isinstance(v, list):
                    parts.append(f"'{k}': [{variable_mapping.get(full_key)}]")
                else:
                    parts.append(f"'{k}': {variable_mapping.get(full_key)}")
            return '{' + ', '.join(parts) + '}'
        return '{}'

    payload = build_payload(example_body)

    method_code = f"""
    @keyword('{keyword_name}')
    def {method_name}(self, {', '.join(args_list)}):
        return {payload}
"""

    # write python contract class
    if not os.path.exists(init_path):
        with open(init_path, 'w') as f:
            f.write('from robot.api.deco import keyword\n\n')
            f.write(f'class {class_name}:\n')
            f.write('    def __init__(self):\n        pass\n')
            f.write(method_code)
    else:
        with open(init_path, 'a') as f:
            f.write(method_code)

    return f"resources/contracts/{controller}", args_list


def normalize_tag(tag: str) -> str:
    # Palavras para ignorar
    skip_words = {"de", "da", "do", "das", "dos", "e"}

    # Remove acentos
    nfkd = unicodedata.normalize('NFKD', tag)
    only_ascii = "".join(c for c in nfkd if not unicodedata.combining(c))

    # Separa em palavras e filtra as que devem permanecer
    words = re.findall(r'\w+', only_ascii)
    filtered = [word for word in words if word.lower() not in skip_words]

    # Junta mantendo capitalização original (como vem do Swagger)
    return ''.join(filtered)