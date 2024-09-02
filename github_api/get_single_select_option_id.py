from .execute_github_graphql_query import execute_github_graphql_query

def get_single_select_option_id(project_id, field_id, option_name, token):
    query = """
    query($projectId: ID!) {
      node(id: $projectId) {
        ... on ProjectV2 {
          fields(first: 100) {
            nodes {
              ... on ProjectV2SingleSelectField {
                id
                name
                options {
                  id
                  name
                }
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
    print(f"get_single_select_option_id query: {query}")
    print(f"get_single_select_option_id variables: {variables}")
    result = execute_github_graphql_query(query, variables, token)
    print(f"get_single_select_option_id result: {result}")
    for field in result['data']['node']['fields']['nodes']:
        if 'id' in field and field['id'] == field_id:
            for option in field.get('options', []):
                if option['name'] == option_name:
                    return option['id']
    raise Exception(f"Option '{option_name}' not found in field '{field_id}'")