import json
from github_api.create_repository import create_repository
from github_api.initialize_repository import initialize_repository
from github_api.create_project import create_project
from github_api.add_draft_issue import add_draft_issue_to_project
from github_api.convert_draft_issue import convert_draft_issue_to_issue
from github_api.link_project_to_repository import link_project_to_repository
from github_api.create_custom_field import create_custom_field
from github_api.invite_collaborators import invite_collaborators
from github_api.add_assignees import add_assignees_to_assignable
from github_api.get_owner_node_id import get_owner_node_id
from github_api.get_user_id_by_login import get_user_id_by_login
from github_api.get_branch_oid import get_branch_oid
from github_api.get_latest_commit_oid import get_latest_commit_oid
from github_api.get_repo_id import get_repo_id
from github_api.update_project_item_field_value import update_project_item_field_value
from github_api.update_issue_custom_status import update_issue_custom_status
from github_api.get_field_id import get_field_id
from github_api.create_file_structure import create_file_structure
from github_api.get_single_select_option_id import get_single_select_option_id
from github_api.update_file import update_file_on_github
from config import GITHUB_TOKEN, REPO_OWNER, REPO_NAME, PROJECT_NAME, branch_name,user_branch_name
import base64

def push_user_stories_to_project(github_token, repo_owner, repo_name, project_name, user_stories_json, collaborators_json, suggestions_json, status_field_name):
    try:
        repo_info = create_repository(repo_owner, repo_name, github_token)
        print(f"Successfully created repository '{repo_name}'")
    except Exception as e:
        print(f"Error creating repository '{repo_name}': {e}")
        return

    try:
        initialize_repository(repo_owner, repo_name, github_token)
        print(f"Successfully initialized repository '{repo_name}'")
    except Exception as e:
        print(f"Error initializing repository '{repo_name}': {e}")
        return

    try:
        owner_id = get_owner_node_id(repo_owner, github_token)
        print(f"Successfully fetched owner node ID: {owner_id}")
    except Exception as e:
        print(f"Error fetching owner node ID: {e}")
        return

    try:
        project_id = create_project(owner_id, project_name, github_token)
        print(f"Successfully created project '{project_name}' with ID: {project_id}")
    except Exception as e:
        print(f"Error creating project '{project_name}': {e}")
        return

    try:
        repo_id = get_repo_id(repo_owner, repo_name, github_token)
        link_project_to_repository(project_id, repo_id, github_token)
        print(f"Successfully linked project '{project_name}' to repository '{repo_name}'")
    except Exception as e:
        print(f"Error linking project to repository: {e}")
        return

    try:
        suggestions_field = create_custom_field(project_id, "Suggestions", "TEXT", github_token)
        suggestions_field_id = suggestions_field['id']
        print(f"Successfully created custom field 'Suggestions' with ID: {suggestions_field_id}")
    except Exception as e:
        print(f"Error creating custom field 'Suggestions': {e}")
        return

    try:
        status_field_id = get_field_id(project_id, status_field_name, github_token)
        print(f"Successfully fetched status field ID: {status_field_id}")
    except Exception as e:
        print(f"Error fetching status field ID: {e}")
        return

    try:
        user_stories = json.loads(user_stories_json)
        suggestions = json.loads(suggestions_json)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return

    assignable_ids = []
    story_to_draft_id = {}
    for idx, story in enumerate(user_stories, 1):
        note = story.get('note')
        role_action_reason = story.get('role_action_reason', '**As a user,**')
        acceptance_criteria = story.get('acceptance_criteria', [
            "Criteria 1: Describe the first acceptance criterion here.",
            "Criteria 2: Describe the second acceptance criterion here.",
            "Criteria 3: Describe additional criteria as needed."
        ])
        definition_of_done = story.get('definition_of_done', [
            "All acceptance criteria are met.",
            "Code is reviewed and approved.",
            "Necessary tests are written and pass.",
            "Documentation is updated, if applicable.",
            "Feature is deployed to the [environment name]."
        ])

        description = (f"{role_action_reason}\n"
                       f"**Acceptance Criteria:**\n")
        for criterion in acceptance_criteria:
            description += f"- [ ] {criterion}\n"

        description += "\n**Definition of Done:**\n"
        for done in definition_of_done:
            description += f"- [ ] {done}\n"

        if not note:
            print("Each user story must have a 'note' field")
            continue

        try:
            draft_issue_id = add_draft_issue_to_project(project_id, note, description, github_token)
            print(f"Successfully added draft issue '{note}' with ID: {draft_issue_id}")
            assignable_ids.append(draft_issue_id)
            story_to_draft_id[str(idx)] = draft_issue_id
        except Exception as e:
            print(f"Error creating draft issue for story '{note}': {e}")
            continue

    print(f"Successfully pushed {len(user_stories)} user stories to the '{project_name}' project")

    try:
        collaborators = json.loads(collaborators_json)
        assignee_ids = []
        for collaborator in collaborators:
            if 'login' in collaborator:
                collaborator['userId'] = get_user_id_by_login(collaborator['login'], github_token)
                assignee_ids.append(collaborator['userId'])
                del collaborator['login']
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return
    except Exception as e:
        print(f"Error fetching user IDs: {e}")
        return

    #try:
     #   invited_collaborators = invite_collaborators(project_id, collaborators, github_token)
      #  print(f"Successfully invited collaborators: {invited_collaborators}")
    #except Exception as e:
     #   print(f"Error inviting collaborators: {e}")
      #  return

    try:
        converted_issue_ids = []
        for draft_issue_id in assignable_ids:
            issue_id = convert_draft_issue_to_issue(draft_issue_id, repo_id, github_token)
            print(f"Successfully converted draft issue with ID: {draft_issue_id} to issue with ID: {issue_id}")
            converted_issue_ids.append(issue_id)
    except Exception as e:
        print(f"Error converting draft issues: {e}")
        return

    try:
        for issue_id in converted_issue_ids:
            add_assignees_to_assignable(issue_id, assignee_ids, github_token)
            print(f"Successfully assigned collaborators to issue with ID: {issue_id}")
    except Exception as e:
        print(f"Error assigning collaborators: {e}")
        return

    try:
        for story_id, data in suggestions.items():
            draft_issue_id = story_to_draft_id.get(story_id)
            if draft_issue_id:
                suggestions_text = "\n\n".join([f"***** {suggestion}" for suggestion in data['suggestions']])
                update_project_item_field_value(project_id, draft_issue_id, suggestions_field_id, {"text": suggestions_text}, github_token)
                print(f"Successfully updated custom field 'Suggestions' for issue with ID: {draft_issue_id}")
    except Exception as e:
        print(f"Error updating custom field 'Suggestions': {e}")
        return

    try:
        for draft_issue_id in assignable_ids:
            option_id = get_single_select_option_id(project_id, status_field_id, "Todo", github_token)
            update_issue_custom_status(project_id, draft_issue_id, status_field_id, option_id, github_token)
            print(f"Successfully updated issue status to 'Todo' for issue with ID: {draft_issue_id}")
    except Exception as e:
        print(f"Error updating issue status: {e}")
        return

if __name__ == "__main__":
    file_structure = {
        "frontend": {
            "components": {
                "SearchBar.js": "Content of SearchBar.js",
                "ProductListing.js": "Content of ProductListing.js",
                "ProductDetailsModal.js": "Content of ProductDetailsModal.js",
                "ShoppingCart.js": "Content of ShoppingCart.js",
                "Checkout.js": "Content of Checkout.js"
            },
            "pages": {
                "Home.js": "Content of Home.js"
            },
            "App.js": "Content of App.js"
        },
        "backend": {
            "controllers": {
                "ProductController.js": "Content of ProductController.js",
                "CartController.js": "Content of CartController.js",
                "OrderController.js": "Content of OrderController.js"
            },
            "models": {
                "Product.js": "Content of Product.js",
                "Cart.js": "Content of Cart.js",
                "Order.js": "Content of Order.js"
            },
            "routes": {
                "productRoutes.js": "Content of productRoutes.js",
                "cartRoutes.js": "Content of cartRoutes.js",
                "orderRoutes.js": "Content of orderRoutes.js"
            },
            "server.js": "Content of server.js"
        },
        "database": {
            "migrations": {
                "create_products_table.sql": "Content of create_products_table.sql",
                "create_cart_table.sql": "Content of create_cart_table.sql",
                "create_orders_table.sql": "Content of create_orders_table.sql"
            },
            "seeds": {
                "seed_products.sql": "Content of seed_products.sql",
                "seed_cart.sql": "Content of seed_cart.sql",
                "seed_orders.sql": "Content of seed_orders.sql"
            },
            "connection.js": "Content of connection.js"
        }
    }

    with open("user_stories.json", "r") as file:
        user_stories_json = file.read()
    with open("collaborators.json", "r") as file:
        collaborators_json = file.read()
    with open("suggestions.json", "r") as file:
        suggestions_json = file.read()

    status_field_name = "Status"  # Replace with your actual status field name

    push_user_stories_to_project(GITHUB_TOKEN, REPO_OWNER, REPO_NAME, PROJECT_NAME, user_stories_json, collaborators_json, suggestions_json, status_field_name)
    latest_commit_oid = create_file_structure(REPO_OWNER, REPO_NAME, user_branch_name, file_structure, GITHUB_TOKEN)
    latest_commit_oid = get_latest_commit_oid(REPO_OWNER, REPO_NAME, user_branch_name, GITHUB_TOKEN)



    # Test the update_file_on_github function
    file_path = "frontend/components/SearchBar.js"
    new_file_content = """
import React from 'react';

const SearchBar = () => {
  return (
    <div>
      <input type="text" placeholder="Search..." />
      <button>Search</button>
    </div>
  );
};

export default SearchBar;
"""
encoded_new_file_content = base64.b64encode(new_file_content.encode('utf-8')).decode('utf-8')

update_file_on_github(GITHUB_TOKEN, REPO_OWNER, REPO_NAME, user_branch_name, file_path, encoded_new_file_content,latest_commit_oid)