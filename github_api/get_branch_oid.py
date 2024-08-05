from .execute_github_graphql_query import execute_github_graphql_query
from config import GITHUB_TOKEN, REPO_OWNER, REPO_NAME, branch_name

def get_branch_oid():
    query = """
    query($owner: String!, $repo_name: String!, $branch_name: String!) {
      repository(owner: $owner, name: $repo_name) {
        ref(qualifiedName: $branch_name) {
          target {
            ... on Commit {
              oid
            }
          }
        }
      }
    }
    """
    variables = {"owner": REPO_OWNER, "repo_name": REPO_NAME, "branch_name": f"refs/heads/{branch_name}"}
    response = execute_github_graphql_query(query, variables, GITHUB_TOKEN)
    
    if 'errors' in response:
        raise Exception(f"Query returned errors: {response['errors']}")

    data = response.get("data", {}).get("repository", {}).get("ref")

    if data is None or data.get("target") is None:
        raise Exception(f"Failed to retrieve branch information for branch '{branch_name}'. Please check the branch name and try again.")

    return data["target"]["oid"]