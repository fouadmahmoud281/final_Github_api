from .create_file import create_file
from langchain_community.llms import OpenAI
import fitz  # PyMuPDF

pdf_path = "E:\Obelion.Ai\github_api\ToDo-BRD.pdf"
api_key = "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"
def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
        return text

def create_readme(text):
    llm = OpenAI(api_key="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")
    prompt = f"summarize the following Business Requirements Document (BRD) content and structure it into a professional README suitable for GitHub developers. The README should include sections such as Project Title, Description, Features, Installation, Usage, Contributing, License, and Contact Information. Ensure clarity, conciseness, and technical accuracy\n\n{text}\n\nREADME:"
    response = llm(prompt)
    return response


def initialize_repository(repo_owner, repo_name, token):
    brd_pdf_path = "E:\Obelion.Ai\github_api\ToDo-BRD.pdf"
    api_key = "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"
    text = extract_text_from_pdf(brd_pdf_path)
    readme_content = create_readme(text)
    license_content = "MIT License\n\nYour license text here."
    gitignore_content = "*.pyc\n__pycache__/\n.env\n"

    create_file(repo_owner, repo_name, "README.md", readme_content, "Add README.md", token)
    create_file(repo_owner, repo_name, "LICENSE", license_content, "Add LICENSE", token)
    create_file(repo_owner, repo_name, ".gitignore", gitignore_content, "Add .gitignore", token)