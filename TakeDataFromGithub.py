from requests import get
from tabulate import tabulate

# Input data
username = 'KentBeck'   # Change to take data from another user
access_key = ''         # Take personal token from github

# Crate headers to table
headers = ['Name', 'Size', 'Contributors Count', 'Branch', 'Is Protected']
table = []

# Take data from repository of chosen user
url_user_repository = f"https://api.github.com/users/{username}/repos"
user_data = get(url_user_repository, auth=(username, access_key)).json()
for project in user_data:
    # What if repository is empty
    if project['pushed_at'] is None:
        table.append([project['name'], project['size'], 0, "---", "---"])
    else:
        # If repository not empty check list of contributors
        count_of_contributors = 0
        repo_name = project['name']
        url_for_contributors = f"https://api.github.com/repos/{username}/{repo_name}/contributors?per_page=1&per_page=100"
        data_of_contributors = get(url_for_contributors, auth=(username, access_key)).json()
        for numbers_contributors in data_of_contributors:
            count_of_contributors = count_of_contributors + 1
            
        # Check if branch is protected
        url_for_check_private = f"https://api.github.com/repos/{username}/{repo_name}/branches"
        data_of_branches = get(url_for_check_private, auth=(username, access_key)).json()
        is_private = True
        for branch in data_of_branches:
            is_private = branch['protected']
            
        # Add data to table
        table.append([project['name'], project['size'], count_of_contributors, project['default_branch'], is_private])
print(tabulate(table, headers))