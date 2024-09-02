from .get_repository_id import get_repository_id
from .list_branches import list_branches
from .get_branch_oid import get_branch_oid
from .create_branch import create_branch
from .create_commit import create_commit
from .process_structure import process_structure
from .get_latest_commit_oid import get_latest_commit_oid
from config import GITHUB_TOKEN, REPO_OWNER, REPO_NAME, branch_name ,user_branch_name

def create_file_structure(REPO_OWNER, REPO_NAME, branch_name, structure, GITHUB_TOKEN):
        # Get repository ID
        repository_id = get_repository_id(REPO_OWNER, REPO_NAME, GITHUB_TOKEN)

        # List branches in the repository
        branches = list_branches(REPO_OWNER, REPO_NAME,GITHUB_TOKEN)
        print("Branches: ", branches)

        if branch_name not in branches:
            raise Exception(f"Branch '{branch_name}' does not exist. Available branches: {', '.join(branches)}")

        # Get branch OID (base commit OID)
        base_commit_oid = get_branch_oid()

        # Create a new branch
        new_branch_name = create_branch(repository_id, base_commit_oid, user_branch_name,GITHUB_TOKEN)

        # Get the OID of the new branch
        new_branch_oid = get_latest_commit_oid(REPO_OWNER, REPO_NAME, new_branch_name, GITHUB_TOKEN)
        # Process the structure and create file additions
        file_additions = process_structure(structure)

        # Create a commit with the new file additions
        commit_oid = create_commit(GITHUB_TOKEN,REPO_OWNER, REPO_NAME, new_branch_name, file_additions, "Create file structure", new_branch_oid)


        print("File structure created successfully!")
        
        return new_branch_oid
