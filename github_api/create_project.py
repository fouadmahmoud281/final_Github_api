from .execute_github_graphql_query import execute_github_graphql_query

def create_project(owner_id, project_name, token):
    query = """
    mutation($ownerId: ID!, $title: String!) {
      createProjectV2(input: { ownerId: $ownerId, title: $title }) {
        projectV2 {
          id
        }
      }
    }
    """
    variables = {"ownerId": owner_id, "title": project_name}
    result = execute_github_graphql_query(query, variables, token)
    print(f"create_project result: {result}")
    if 'data' in result and 'createProjectV2' in result['data']:
        return result['data']['createProjectV2']['projectV2']['id']
    elif 'errors' in result:
        raise Exception(result['errors'])
    else:
        raise Exception("Unexpected response format")