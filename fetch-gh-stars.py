import requests
import pandas as pd
import os
from datetime import datetime
import dotenv
from utils import find_latest_file

dotenv.load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", None)
GITHUB_API_URL = "https://api.github.com"

def get_starred_repos(user_id, existing_repos):
    """
    Fetch the list of all starred repositories by a GitHub user, handling pagination.
    Stops fetching when an existing repo is found.
    """
    starred_repos = []
    page = 1
    per_page = 100

    while True:
        url = f"{GITHUB_API_URL}/users/{user_id}/starred"
        params = {
            "per_page": per_page,
            "page": page
        }
        headers = {
            "Accept": "application/vnd.github.v3.star+json",
            "Authorization": f"token {GITHUB_TOKEN}",
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            print(f"Fetched page {page} of starred repositories for {user_id}")
            repos = response.json()
            if not repos:
                break  # Exit if no more repositories are available
            
            for repo_info in repos:
                repo_name = repo_info['repo']['name']
                if repo_name in existing_repos:
                    print(f"Encountered existing repo '{repo_name}', stopping fetch.")
                    return starred_repos  # Stop if an existing repo is found
                starred_repos.append(repo_info)

            page += 1
        else:
            print(f"Failed to fetch starred repositories for {user_id}. Status code: {response.status_code}")
            break

    return starred_repos

def get_repo_readme(owner, repo):
    """
    Fetch the README file content of a given repository.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/readme"
    headers = {
        "Accept": "application/vnd.github.v3.raw",
        "Authorization": f"token {GITHUB_TOKEN}",
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch README for {owner}/{repo}. Status code: {response.status_code}")
        return None


def save_readmes_to_csv(user_id):
    """
    Fetch all starred repos' README and save them to a CSV file.
    """
    # Load previously saved repositories if available
    latest_file = find_latest_file(user_id)
    existing_repos = set()

    if latest_file:
        existing_df = pd.read_csv(latest_file)
        existing_repos = set(existing_df["repo_name"])
        print(f"Loaded existing data from {latest_file} with {len(existing_repos)} repositories.")
    else:
        print("No existing data found. Fetching all starred repositories.")

    # Fetch new starred repositories
    starred_repos = get_starred_repos(user_id, existing_repos)
    readme_data = []
    new_repos_count = 0

    for repo_info in starred_repos:
        owner = repo_info['repo']['owner']['login']
        repo_name = repo_info['repo']['name']

        # Stop fetching if repo already exists
        if repo_name in existing_repos:
            print(f"Already processed {repo_name}, stopping to avoid duplicates.")
            break

        repo_url = repo_info['repo']['html_url']
        topics = ', '.join(repo_info['repo']['topics'])
        readme_url = f"https://github.com/{owner}/{repo_name}/blob/main/README.md"
        readme_content = get_repo_readme(owner, repo_name)

        readme_data.append({
            "repo_owner": owner,
            "repo_name": repo_name,
            "repo_url": repo_url,
            "topics": topics,
            "readme_url": readme_url,
            "readme_content": readme_content if readme_content else "Failed to fetch"
        })
        new_repos_count += 1

    # Combine new data with old data
    if latest_file:
        existing_df = pd.read_csv(latest_file)
        new_df = pd.DataFrame(readme_data)
        combined_df = pd.concat([new_df, existing_df], ignore_index=True)
    else:
        combined_df = pd.DataFrame(readme_data)

    # Save to a new CSV file
    fetch_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{user_id}_starred_repos-{fetch_date}.csv"
    combined_df.to_csv(filename, index=False)
    print(f"Saved README contents to {filename} with {new_repos_count} new repositories.")

if __name__ == "__main__":
    user_id = input("Enter the GitHub user ID: ")
    assert GITHUB_TOKEN, "GITHUB_TOKEN environment variable is required to fetch starred repositories."
    save_readmes_to_csv(user_id)
