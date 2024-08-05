import requests

def create_repository(owner, repo_name, token, description="", private=True):
    url = f"https://api.github.com/user/repos"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "name": repo_name,
        "description": description,
        "private": private
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()