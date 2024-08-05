from .execute_github_graphql_query import execute_github_graphql_query

def convert_draft_issue_to_issue(item_id, repository_id, token):
    query = """
    mutation($input: ConvertProjectV2DraftIssueItemToIssueInput!) {
      convertProjectV2DraftIssueItemToIssue(input: $input) {
        clientMutationId
        item {
          id
          content {
            ... on Issue {
              id
            }
          }
        }
      }
    }
    """
    variables = {
        "input": {
            "itemId": item_id,
            "repositoryId": repository_id
        }
    }
    print(f"convert_draft_issue_to_issue query: {query}")
    print(f"convert_draft_issue_to_issue variables: {variables}")
    result = execute_github_graphql_query(query, variables, token)
    print(f"convert_draft_issue_to_issue result: {result}")
    if 'data' in result and 'convertProjectV2DraftIssueItemToIssue' in result['data']:
        return result['data']['convertProjectV2DraftIssueItemToIssue']['item']['content']['id']
    elif 'errors' in result:
        raise Exception(result['errors'])
    else:
        raise Exception("Unexpected response format")