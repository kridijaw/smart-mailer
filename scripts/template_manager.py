from jinja2 import Template
from markupsafe import escape

def parse_template(template_path):
    with open(template_path, 'r') as file:
        content = file.read()

    # Split metadata and body
    parts = content.split('---\n', 2)
    if len(parts) == 3:
        metadata = {
            line.split(':', 1)[0].strip(): line.split(':', 1)[1].strip()
            for line in parts[1].strip().split('\n')
            if ':' in line
        }
        body = parts[2]
    else:
        metadata = {'subject': 'Your Subject'}  # Default subject
        body = content

    return metadata, body

def render_template(template_path, context):
    metadata, template_content = parse_template(template_path)
    safe_context = {k: escape(v) for k, v in context.items()}  # Sanitize context values
    template = Template(template_content)
    return metadata.get('subject'), template.render(safe_context)