from .execute_github_graphql_query import execute_github_graphql_query

def add_draft_issue_to_project(project_id, title, body, token):
    query = """
    mutation($projectId: ID!, $title: String!, $body: String) {
      addProjectV2DraftIssue(input: { projectId: $projectId, title: $title, body: $body }) {
        projectItem {
          id
        }
      }
    }
    """
    variables = {"projectId": project_id, "title": title, "body": body}
    result = execute_github_graphql_query(query, variables, token)
    print(f"add_draft_issue_to_project result: {result}")
    if 'data' in result and 'addProjectV2DraftIssue' in result['data']:
        return result['data']['addProjectV2DraftIssue']['projectItem']['id']
    elif 'errors' in result:
        raise Exception(result['errors'])
    else:
        raise Exception("Unexpected response format")