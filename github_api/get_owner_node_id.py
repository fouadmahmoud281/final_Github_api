from .execute_github_graphql_query import execute_github_graphql_query

def get_owner_node_id(owner, token):
    query = """
    query($owner: String!) {
      user(login: $owner) {
        id
      }
      organization(login: $owner) {
        id
      }
    }
    """
    variables = {"owner": owner}
    result = execute_github_graphql_query(query, variables, token)
    user = result['data'].get('user')
    organization = result['data'].get('organization')
    
    if user:
        return user['id']
    elif organization:
        return organization['id']
    else:
        raise Exception(f"Cannot find user or organization with login: {owner}")