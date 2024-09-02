from .execute_github_graphql_query import execute_github_graphql_query
from .list_branches import list_branches
from config import GITHUB_TOKEN, REPO_OWNER, REPO_NAME
def create_branch(repository_id, base_oid, branch_name, GITHUB_TOKEN):
    # List branches in the repository
    branches = list_branches(REPO_OWNER, REPO_NAME,GITHUB_TOKEN)

    if branch_name in branches:
        print(f"Branch '{branch_name}' already exists. Skipping creation.")
        return branch_name

    query = """
    mutation($input: CreateRefInput!) {
      createRef(input: $input) {
        ref {
          name
        }
      }
    }
    """
    variables = {
        "input": {
            "repositoryId": repository_id,
            "name": f"refs/heads/{branch_name}",
            "oid": base_oid
        }
    }
    print(f"create_branch query: {query}")
    print(f"create_branch variables: {variables}")

    response = execute_github_graphql_query(query, variables, GITHUB_TOKEN)
    
    if 'errors' in response:
        raise Exception(f"Mutation returned errors: {response['errors']}")

    return response["data"]["createRef"]["ref"]["name"]