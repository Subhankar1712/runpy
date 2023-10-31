import os
from github import Github

# Define your keywords and corresponding labels
keyword_label_mapping = {
    'bug': 'bug',
    'feature': 'feature',
    'enhancement': 'enhancement',
}

def main():
    # Create a GitHub API client
    github_token = os.getenv('GITHUB_TOKEN')
    github = Github(github_token)
    
    # Get the issue that triggered the workflow
    event_path = os.getenv('GITHUB_EVENT_PATH')
    with open(event_path, 'r') as f:
        event_data = json.load(f)
    
    issue_title = event_data['issue']['title'].lower()
    issue_body = event_data['issue']['body'].lower()
    
    # Check if any keywords match and add corresponding labels
    labels_to_add = []
    for keyword, label in keyword_label_mapping.items():
        if keyword in issue_title or keyword in issue_body:
            labels_to_add.append(label)
    
    # Get the repository and issue
    repo = github.get_repo(event_data['repository']['full_name'])
    issue = repo.get_issue(event_data['issue']['number'])
    
    # Add labels to the issue
    for label in labels_to_add:
        issue.add_to_labels(label)

if __name__ == '__main__':
    main()
