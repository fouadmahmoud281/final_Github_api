from .config import GITHUB_TOKEN, REPO_OWNER, REPO_NAME
from .execute_github_graphql_query import execute_github_graphql_query


def get_latest_commit_oid(repo_owner, repo_name, branch_name, token):
    query = """
    query($repoOwner: String!, $repoName: String!, $branchName: String!) {
      repository(owner: $repoOwner, name: $repoName) {
        ref(qualifiedName: $branchName) {
          target {
            oid
          }
        }
      }
    }
    """
    variables = {
        "repoOwner": repo_owner,
        "repoName": repo_name,
        "branchName": branch_name
    }
    response = execute_github_graphql_query(query, variables, token)
    if "errors" in response:
        raise Exception(f"Query returned errors: {response['errors']}")

    ref = response["data"]["repository"]["ref"]
    if ref is None:
        raise Exception(f"Branch '{branch_name}' does not exist")

    return ref["target"]["oid"]