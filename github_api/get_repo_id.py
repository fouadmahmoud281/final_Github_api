from .execute_github_graphql_query import execute_github_graphql_query

def get_repo_id(repo_owner, repo_name, token):
    query = """
    query($owner: String!, $name: String!) {
      repository(owner: $owner, name: $name) {
        id
      }
    }
    """
    variables = {"owner": repo_owner, "name": repo_name}
    result = execute_github_graphql_query(query, variables, token)
    if 'data' in result and 'repository' in result['data']:
        return result['data']['repository']['id']
    else:
        raise Exception(f"Cannot find repository with owner: {repo_owner} and name: {repo_name}")