from jinja2 import Template
from markupsafe import escape
from scripts.parse_template import parse_template


def render_template(template_path, context):
    metadata, template_content = parse_template(template_path)
    safe_context = sanitize_template(context)
    template = Template(template_content)
    return metadata.get('subject'), template.render(safe_context), metadata.get('reply-to')


def sanitize_template(context):
    safe_context = {k: escape(v) for k, v in context.items()}
    return safe_context
