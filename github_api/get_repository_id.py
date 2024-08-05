from .execute_github_graphql_query import execute_github_graphql_query
from .config import GITHUB_TOKEN, REPO_OWNER, REPO_NAME
def get_repository_id(REPO_OWNER, REPO_NAME, GITHUB_TOKEN):
    query = """
    query($owner: String!, $repo_name: String!) {
      repository(owner: $owner, name: $repo_name) {
        id
      }
    }
    """
    variables = {"owner": REPO_OWNER, "repo_name": REPO_NAME}
    response = execute_github_graphql_query(query, variables, GITHUB_TOKEN)
    
    if 'errors' in response:
        raise Exception(f"Query returned errors: {response['errors']}")

    data = response.get("data", {}).get("repository")
    if data is None:
        raise Exception("Failed to retrieve repository information. Please check the repository details and try again.")
    
    return data["id"]