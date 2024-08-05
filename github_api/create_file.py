import requests
import base64

def create_file(repo_owner, repo_name, path, content, message, token):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "message": message,
        "content": base64.b64encode(content.encode()).decode(),
        "branch": "main"
    }
    response = requests.put(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()