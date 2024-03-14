import os
import requests

# Setup
ORG_NAME = os.getenv('INPUT_ORG_NAME')
REPO_NAME = os.getenv('INPUT_REPO_NAME')
GITHUB_TOKEN = os.getenv('INPUT_GITHUB_TOKEN')
SUMMARY_MD = "summary.md"  # File to save the markdown summary

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

# Define your functions here (fetch_org_owners, fetch_repo_admins, fetch_secret_scanning_alerts)

def generate_markdown_summary(org_name, repo_name, alerts, org_owners, repo_admins):
    markdown_lines = [
        "| S.No | Org/Repo Name | Org Owners | Repo Admins | Alert Number | Secret Type | State | Alert URL |",
        "| ---- | ------------- | ---------- | ----------- | ------------ | ----------- | ----- | --------- |"
    ]
    for index, alert in enumerate(alerts, start=1):
        org_repo_name = f"{org_name}/{repo_name}"
        joined_org_owners = ', '.join(org_owners)
        joined_repo_admins = ', '.join(repo_admins)
        markdown_lines.append(
            f"| {index} | {org_repo_name} | {joined_org_owners} | {joined_repo_admins} "
            f"| {alert.get('number', 'N/A')} | {alert.get('secret_type', 'Unknown')} "
            f"| {alert.get('state', 'Unknown')} | [Link]({alert.get('html_url', 'URL Not Available')}) |"
        )
    return "\n".join(markdown_lines)

def main():
    full_repo_name = f'{ORG_NAME}/{REPO_NAME}'
    alerts = fetch_secret_scanning_alerts(full_repo_name)
    org_owners = fetch_org_owners(ORG_NAME)
    repo_admins = fetch_repo_admins(full_repo_name)
    
    markdown_summary = generate_markdown_summary(ORG_NAME, REPO_NAME, alerts, org_owners, repo_admins)
    
    # Save the markdown summary to a file
    with open(SUMMARY_MD, 'w') as summary_file:
        summary_file.write(markdown_summary)
    
    # Print the path to the summary file for debugging
    print(f"Markdown summary saved to {SUMMARY_MD}")

if __name__ == '__main__':
    main()
