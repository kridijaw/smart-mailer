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