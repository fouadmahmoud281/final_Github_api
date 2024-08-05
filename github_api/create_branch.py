from .execute_github_graphql_query import execute_github_graphql_query

def create_branch(repository_id, base_oid, branch_name, GITHUB_TOKEN):
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