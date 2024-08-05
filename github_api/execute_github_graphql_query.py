import requests

def execute_github_graphql_query(query, variables, token):
    headers = {
        "Authorization": f"Bearer " + token,
        "Content-Type": "application/json"
    }
    response = requests.post("https://api.github.com/graphql",
                             headers=headers,
                             json={"query": query, "variables": variables})
    response.raise_for_status()
    return response.json()