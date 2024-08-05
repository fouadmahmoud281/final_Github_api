from .execute_github_graphql_query import execute_github_graphql_query
from .config import GITHUB_TOKEN, REPO_OWNER, REPO_NAME
def list_branches(REPO_OWNER, REPO_NAME, GITHUB_TOKEN):
    query = """
    query($owner: String!, $repo_name: String!) {
      repository(owner: $owner, name: $repo_name) {
        refs(refPrefix: "refs/heads/", first: 100) {
          edges {
            node {
              name
            }
          }
        }
      }
    }
    """
    variables = {"owner": REPO_OWNER, "repo_name": REPO_NAME}
    response = execute_github_graphql_query(query, variables, GITHUB_TOKEN)
    
    if 'errors' in response:
        raise Exception(f"Query returned errors: {response['errors']}")

    branches = response.get("data", {}).get("repository", {}).get("refs", {}).get("edges", [])
    return [branch["node"]["name"] for branch in branches]