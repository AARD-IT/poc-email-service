import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import Dict, Any

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(ROOT, "templates")


env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "xml"]),
)


def render_template(template_name: str, variables: Dict[str, Any] = None) -> str:
    variables = variables or {}
    template = env.get_template(template_name)
    return template.render(**variables)
