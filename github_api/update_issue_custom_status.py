from .execute_github_graphql_query import execute_github_graphql_query

def update_issue_custom_status(project_id, item_id, field_id, status, token):
    query = """
    mutation($input: UpdateProjectV2ItemFieldValueInput!) {
      updateProjectV2ItemFieldValue(input: $input) {
        clientMutationId
        projectV2Item {
          id
          fieldValues(first: 10) {
            nodes {
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                optionId
              }
              ... on ProjectV2ItemFieldTextValue {
                text
              }
              ... on ProjectV2ItemFieldNumberValue {
                number
              }
              ... on ProjectV2ItemFieldDateValue {
                date
              }
              ... on ProjectV2ItemFieldIterationValue {
                iterationId
              }
            }
          }
        }
      }
    }
    """
    variables = {
        "input": {
            "projectId": project_id,
            "itemId": item_id,
            "fieldId": field_id,
            "value": {"text": status}
        }
    }
    print(f"update_issue_custom_status query: {query}")
    print(f"update_issue_custom_status variables: {variables}")
    result = execute_github_graphql_query(query, variables, token)
    print(f"update_issue_custom_status result: {result}")
    if 'data' in result and 'updateProjectV2ItemFieldValue' in result['data']:
        return result['data']['updateProjectV2ItemFieldValue']['projectV2Item']
    elif 'errors' in result:
        raise Exception(result['errors'])
    else:
        raise Exception("Unexpected response format")