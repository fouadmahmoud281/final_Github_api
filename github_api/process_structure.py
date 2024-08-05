import base64

def process_structure(structure, path=""):
    file_additions = []
    for name, content in structure.items():
        if isinstance(content, dict):
            # Process subfolder
            subfolder_additions = process_structure(content, f"{path}/{name}" if path else name)
            file_additions.extend(subfolder_additions)
        else:
            # Create file addition
            file_additions.append({
                "path": f"{path}/{name}" if path else name,
                "contents": base64.b64encode(content.encode()).decode()
            })
    return file_additions