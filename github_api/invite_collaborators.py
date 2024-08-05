from .execute_github_graphql_query import execute_github_graphql_query

def invite_collaborators(project_id, collaborators, token):
    query = """
    mutation($input: UpdateProjectV2CollaboratorsInput!) {
      updateProjectV2Collaborators(input: $input) {
        clientMutationId
        collaborators(first: 100) {
          nodes {
            __typename
            ... on User {
              id
              login
            }
            ... on Team {
              id
              name
            }
          }
        }
      }
    }
    """
    variables = {
        "input": {
            "projectId": project_id,
            "collaborators": collaborators
        }
    }
    print(f"invite_collaborators query: {query}")
    print(f"invite_collaborators variables: {variables}")
    result = execute_github_graphql_query(query, variables, token)
    print(f"invite_collaborators result: {result}")
    if 'data' in result and 'updateProjectV2Collaborators' in result['data']:
        return result['data']['updateProjectV2Collaborators']['collaborators']
    elif 'errors' in result:
        raise Exception(result['errors'])
    else:
        raise Exception("Unexpected response format")