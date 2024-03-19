import os
import requests

# Setup
ORG_NAME = os.getenv('INPUT_ORG_NAME')
REPO_NAME = os.getenv('INPUT_REPO_NAME')
GITHUB_TOKEN = os.getenv('INPUT_GITHUB_TOKEN')

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def fetch_paginated_api_data(url):
    all_data = []
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            all_data.extend(response.json())
            if 'next' in response.links.keys():
                url = response.links['next']['url']
            else:
                url = None
        else:
            print(f'Failed to fetch data: {response.status_code}')
            break
    return all_data

def fetch_org_owners(org_name):
    return fetch_paginated_api_data(f'https://api.github.com/orgs/{org_name}/members?role=admin')

def fetch_repo_admins(full_repo_name):
    return fetch_paginated_api_data(f'https://api.github.com/repos/{full_repo_name}/collaborators?permission=admin')

def fetch_secret_scanning_alerts(full_repo_name):
    return fetch_paginated_api_data(f'https://api.github.com/repos/{full_repo_name}/secret-scanning/alerts')

def generate_markdown_summary(org_name, repo_name, alerts, org_owners, repo_admins):
    markdown_lines = [
        "## Secret Scanning Report",
        "| S.No | Org/Repo Name | Org Owners | Repo Admins | Alert Number | Secret Type | State | Alert URL |",
        "| ---- | ------------- | ---------- | ----------- | ------------ | ----------- | ----- | --------- |"
    ]
    for index, alert in enumerate(alerts, start=1):
        markdown_lines.append(
            f"| {index} | {org_name}/{repo_name} | {', '.join([o['login'] for o in org_owners])} | "
            f"{', '.join([a['login'] for a in repo_admins])} | {alert.get('number', 'N/A')} | "
            f"{alert.get('secret_type', 'Unknown')} | {alert.get('state', 'Unknown')} | "
            f"[Link]({alert.get('html_url', 'URL Not Available')}) |"
        )
    return "\n".join(markdown_lines)

def write_markdown_to_file(content, filename):
    with open(filename, 'w') as file:
        file.write(content)

def main():
    full_repo_name = f'{ORG_NAME}/{REPO_NAME}'
    alerts = fetch_secret_scanning_alerts(full_repo_name)
    org_owners = fetch_org_owners(ORG_NAME)
    repo_admins = fetch_repo_admins(full_repo_name)
    
    markdown_summary = generate_markdown_summary(ORG_NAME, REPO_NAME, alerts, org_owners, repo_admins)
    
    # Echo the markdown summary for GitHub Actions to capture
    print(markdown_summary)
    
    # Write the markdown summary to a file
    write_markdown_to_file(markdown_summary, "repo-secret_scanning_report.md")

if __name__ == '__main__':
    main()
