from .execute_github_graphql_query import execute_github_graphql_query
from .get_repository_id import get_repository_id
from .get_branch_oid import get_branch_oid


def update_file_on_github(token, repo_owner, repo_name, user_branch_name, file_path, file_content, latest_commit_oid):
    # Create a new commit with the updated file
    query = """
    mutation($input: CreateCommitOnBranchInput!) {
      createCommitOnBranch(input: $input) {
        commit {
          oid
          url
        }
      }
    }
    """
    variables = {
        "input": {
            "branch": {
                "repositoryNameWithOwner": f"{repo_owner}/{repo_name}",
                "branchName": user_branch_name
            },
            "message": {
                "headline": "Update file"
            },
            "fileChanges": {
                "additions": [
                    {
                        "path": file_path,
                        "contents": file_content
                    }
                ]
            },
            "expectedHeadOid": latest_commit_oid
        }
    }
    response = execute_github_graphql_query(query, variables, token)
    if "errors" in response:
        raise Exception(f"Mutation returned errors: {response['errors']}")

    return response["data"]["createCommitOnBranch"]["commit"]["oid"]