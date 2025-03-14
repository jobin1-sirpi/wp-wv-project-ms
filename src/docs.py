# Custom OpenAPI schema metadata
import json
from typing import Any, Dict, Tuple

from .core.config import settings


docs_summary = (
    "MicroService to handle Project based functionalities in WindVista V2"
)
docs_description = (
    "`Apart from the response codes specified in each API, the API server may respond with other common "
    "responses based on standard API behavior.`"
)

docs_tags_metadata = [
    {
        "name": "Utility APIs",
        "description": (
            "The Utility APIs contain endpoints that serve operational or system-level purposes. "
            "These routes are not directly related to the core business logic of the API but "
            "are essential for overall functionality, monitoring, and accessibility."
        ),
    },
]


# Helper function to extract headers and payload from OpenAPI operation
def extract_headers_and_payload(
    operation: Dict[str, Any], components: Dict[str, Any]
) -> Tuple[Dict[str, str], Dict[str, Any]]:
    headers = {
        param["name"]: (
            param["schema"].get("type")
            or (
                "Bearer <token>"
                if param["name"] == "Authorization"
                else " | ".join(v["type"] for v in param["schema"].get("anyOf", []))
            )
        )
        for param in operation.get("parameters", [])
        if param.get("in") == "header"
    }

    payload_example = {}
    request_body = operation.get("requestBody", {}).get("content", {})
    for content_type, content in request_body.items():
        if content_type in ("application/json", "application/x-www-form-urlencoded"):
            headers["Content-Type"] = content_type
            schema_ref = content["schema"].get("$ref", "")
            schema_name = schema_ref.split("/")[-1] if schema_ref else None
            if schema_name:
                properties = (
                    components["schemas"].get(schema_name, {}).get("properties", {})
                )
                for key, value in properties.items():
                    if "anyOf" in value:
                        payload_example[key] = " | ".join(
                            v["type"] for v in value["anyOf"]
                        )
                    else:
                        payload_example[key] = value.get("type", "")
    return headers, payload_example


# Helper function to generate code samples
def generate_code_samples(
    path: str, method: str, operation: Dict[str, Any], components: Dict[str, Any]
) -> None:
    nl = "\n"
    tl = "    "
    base_url = settings.BASE_URL

    headers, payload_example = extract_headers_and_payload(operation, components)

    # Constructing query string
    query_params = [
        param for param in operation.get("parameters", []) if param.get("in") == "query"
    ]
    query_string = "&".join(f"{param['name']}={{value}}" for param in query_params)
    query_string = f"?{query_string}" if query_string else ""

    # Generating cURL example
    curl_headers = "".join(f"{tl}-H '{k}: {v}'{nl}" for k, v in headers.items())
    curl_payload = (
        f"{tl}-d '{json.dumps(payload_example)}'{nl}" if payload_example else ""
    )
    curl_sample = (
        f"curl -X {method.upper()} {base_url}{path}{query_string}{nl}"
        f"{curl_headers}{curl_payload}"
    ).strip()

    # Generating Python example
    python_sample = (
        f"import requests{nl}import json{nl}{nl}"
        f"url = '{base_url}{path}{query_string}'{nl}"
        f"payload = {json.dumps(payload_example) if payload_example else {}}{nl}"
        f"headers = {json.dumps(headers)}{nl}{nl}"
        f"response = requests.{method.lower()}(url, headers=headers, json=payload){nl}"
        f"print(response.text)"
    )

    # Generating JavaScript (fetch) example
    js_sample = (
        f"const url = '{base_url}{path}{query_string}';{nl}"
        f"const headers = {json.dumps(headers, indent=4)};{nl}"
        f"const payload = {json.dumps(payload_example, indent=4)};{nl}{nl}"
        f"fetch(url, {{method: '{method.upper()}', headers, body: JSON.stringify(payload)}}){nl}"
        f"    .then(response => response.json()){nl}"
        f"    .then(data => console.log(data)){nl}"
        f"    .catch(error => console.error('Error:', error));"
    )

    operation["x-code-samples"] = [
        {"lang": "curl", "source": curl_sample, "label": "Curl"},
        {"lang": "Python", "source": python_sample, "label": "Python3"},
        {"lang": "JavaScript", "source": js_sample, "label": "JavaScript (Fetch)"},
    ]
