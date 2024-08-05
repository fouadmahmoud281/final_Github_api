from .execute_github_graphql_query import execute_github_graphql_query

def add_assignees_to_assignable(assignable_id, assignee_ids, token):
    query = """
    mutation($input: AddAssigneesToAssignableInput!) {
      addAssigneesToAssignable(input: $input) {
        clientMutationId
        assignable {
          ... on Issue {
            id
            assignees(first: 10) {
              nodes {
                id
                login
              }
            }
          }
        }
      }
    }
    """
    variables = {
        "input": {
            "assignableId": assignable_id,
            "assigneeIds": assignee_ids
        }
    }
    print(f"add_assignees_to_assignable query: {query}")
    print(f"add_assignees_to_assignable variables: {variables}")
    result = execute_github_graphql_query(query, variables, token)
    print(f"add_assignees_to_assignable result: {result}")
    if 'data' in result and 'addAssigneesToAssignable' in result['data']:
        return result['data']['addAssigneesToAssignable']['assignable']
    elif 'errors' in result:
        raise Exception(result['errors'])
    else:
        raise Exception("Unexpected response format")