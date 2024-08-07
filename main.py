import requests
import pandas as pd
import sqlite3
import json

# Replace with your repository details
owner = "oven-sh"
repo = "bun"

# GitHub API URL for issues
base_url = f"https://api.github.com/repos/{owner}/{repo}/issues"

# SQLite database setup
conn = sqlite3.connect("github_issues.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS issues (
    id INTEGER PRIMARY KEY,
    created_at TEXT,
    closed_at TEXT,
    state TEXT
)
"""
)


def fetch_issues(url):
    all_issues = []
    page = 1
    per_page = 100

    while True:
        params = {"state": "all", "per_page": per_page, "page": page}
        response = requests.get(url, params=params)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response content: {response.text}")
            break

        try:
            issues = response.json()
        except json.JSONDecodeError:
            print("Error: Unable to parse JSON response")
            print(f"Response content: {response.text}")
            break

        if not issues:
            break

        if isinstance(issues, dict) and "message" in issues:
            print(f"API Error: {issues['message']}")
            break
        
        print(f"Processing page {page}. all issues {len(all_issues)}")

        for issue in issues:
            if isinstance(issue, dict) and "pull_request" not in issue:
                try:
                    all_issues.append(
                        {
                            "id": issue["id"],
                            "created_at": issue["created_at"],
                            "closed_at": issue["closed_at"],
                            "state": issue["state"],
                        }
                    )
                except KeyError as e:
                    print(f"KeyError: {e}")
                    print(f"Issue data: {json.dumps(issue, indent=2)}")

        page += 1

    return all_issues


# Fetch all issues
all_issues = fetch_issues(base_url)

# Insert data into SQLite
for issue in all_issues:
    cursor.execute(
        """
    INSERT OR REPLACE INTO issues (id, created_at, closed_at, state)
    VALUES (?, ?, ?, ?)
    """,
        (issue["id"], issue["created_at"], issue["closed_at"], issue["state"]),
    )

# Commit changes and close connection
conn.commit()
conn.close()

# Convert to DataFrame for display
df = pd.DataFrame(all_issues)
print(df)

print(f"Total issues fetched and stored: {len(all_issues)}")
