import csv
from config import ATLASSIAN_ACCOUNT, API_TOKEN, JIRA_PROJECT, JIRA_MAX_ISSUES
from jira import JIRA

jira_client = JIRA("https://g-cloud.atlassian.net/", basic_auth=(ATLASSIAN_ACCOUNT, API_TOKEN))

project = jira_client.project(JIRA_PROJECT)
created_epics = {}
issue_list = []

with open("user_stories.csv", "r") as f:
    reader = csv.reader(f)
    headers = None
    data = []
    tmp_issues = []
    for row in reader:
        # for each row
        if headers is None:
            # init headers
            headers = row
            continue
        issue_data = {}
        # csv to json
        for idx, elt in enumerate(row):
            issue_data[headers[idx]] = elt
        
        if issue_data["Epic"] not in created_epics:
            # if epic was not created during execution, create in Jira
            if len(issue_data["Epic"]) > 0:
                epic = jira_client.create_issue(project=JIRA_PROJECT, summary=issue_data["Epic"], description=issue_data["Epic"], issuetype={"name": "Epic"})
                created_epics[issue_data["Epic"]] = epic.id
                print(f"created epic {issue_data['Epic']}")
        # append Jira tmp issue to list
        tmp_issues.append(
            {
                "project": {"key": JIRA_PROJECT},
                "summary": f"En tant que {issue_data.get('En tant que...')}, je peux {issue_data.get('Je peux...')} dans le but de {issue_data.get('Dans le but de...')}",
                "description": issue_data["Détails"],
                "issuetype": {"name": "Story"},
                "parent": {"id": created_epics[issue_data["Epic"]]}
            }
        )
        # Jira limits bulk creation to 50 issues per call, create pages of 50 issues
        if len(tmp_issues) == JIRA_MAX_ISSUES:
            issue_list.append(tmp_issues)
            tmp_issues = []
    # append last page
    issue_list.append(tmp_issues)

# bulk create in Jira
for issue_page in issue_list:
    issues = jira_client.create_issues(field_list=issue_page)
    print(f"created {len(issue_page)} issues")

print("done")
