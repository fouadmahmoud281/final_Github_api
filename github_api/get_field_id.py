from .execute_github_graphql_query import execute_github_graphql_query

def get_field_id(project_id, field_name, token):
    query = """
    query($projectId: ID!) {
      node(id: $projectId) {
        ... on ProjectV2 {
          fields(first: 100) {
            nodes {
              ... on ProjectV2FieldCommon {
                id
                name
              }
            }
          }
        }
      }
    }
    """
    variables = {
        "projectId": project_id
    }
    print(f"get_field_id query: {query}")
    print(f"get_field_id variables: {variables}")
    result = execute_github_graphql_query(query, variables, token)
    print(f"get_field_id result: {result}")
    for field in result['data']['node']['fields']['nodes']:
        if field['name'] == field_name:
            return field['id']
    raise Exception(f"Field '{field_name}' not found in project '{project_id}'")