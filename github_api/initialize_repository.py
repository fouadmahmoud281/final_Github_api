from .create_file import create_file

def initialize_repository(repo_owner, repo_name, token):
    readme_content = f"# {repo_name}\n\nThis is the initial README file for the {repo_name} repository."
    license_content = "MIT License\n\nYour license text here."
    gitignore_content = "*.pyc\n__pycache__/\n.env\n"

    create_file(repo_owner, repo_name, "README.md", readme_content, "Add README.md", token)
    create_file(repo_owner, repo_name, "LICENSE", license_content, "Add LICENSE", token)
    create_file(repo_owner, repo_name, ".gitignore", gitignore_content, "Add .gitignore", token)