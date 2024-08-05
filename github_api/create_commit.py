import requests
import base64

GITHUB_API_URL = "https://api.github.com/graphql"

def create_commit(token, repo_owner, repo_name, branch_name, file_additions, commit_message, expected_head_oid):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # No need to create additions, as file_additions is already in the correct format
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
                "branchName": branch_name
            },
            "message": {
                "headline": commit_message
            },
            "fileChanges": {
                "additions": file_additions
            },
            "expectedHeadOid": expected_head_oid
        }
    }
    response = requests.post(GITHUB_API_URL, headers=headers, json={"query": query, "variables": variables})
    response.raise_for_status()
    response_data = response.json()

    if "errors" in response_data:
        raise Exception(f"Mutation returned errors: {response_data['errors']}")

    return response_data["data"]["createCommitOnBranch"]["commit"]["oid"]