import csv

import jira
from config import ATLASSIAN_ACCOUNT, API_TOKEN, JIRA_PROJECT
from jira import JIRA

jira_client = JIRA(
    "https://g-cloud.atlassian.net/", basic_auth=(ATLASSIAN_ACCOUNT, API_TOKEN)
)

fields = jira_client.fields()

story_points_field = None
for f in fields:
    if f.get("name") == "Story point estimate":
        story_points_field = f
        break

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
                epic = jira_client.create_issue(
                    project=JIRA_PROJECT,
                    summary=issue_data["Epic"],
                    description=issue_data["Epic"],
                    issuetype={"name": "Epic"},
                )
                created_epics[issue_data["Epic"]] = epic.id
                print(f"created epic {issue_data['Epic']}")
        # append Jira tmp issue to list
        issue_is_done = issue_data.get("Fait") == "TRUE"
        issue = {
            "project": {"key": JIRA_PROJECT},
            "summary": f"En tant que {issue_data.get('En tant que...')}, je peux {issue_data.get('Je peux...')} dans le but de {issue_data.get('Dans le but de...')}",
            "description": issue_data["Détails"],
            "issuetype": {"name": "Story"},
            "parent": {"id": created_epics[issue_data["Epic"]]},
        }
        if story_points_field and issue_data.get("Total"):
            try:
                issue[story_points_field.get("id")] = int(issue_data.get("Total", 0))
            except TypeError:
                print(f"could not parse {issue_data.get('Total')}")

        created_issue = jira_client.create_issue(fields=issue)
        print(f"issue {created_issue.id} created")
        if issue_is_done:
            jira_client.transition_issue(created_issue, 'Done')
            print(f"transitionned issue {created_issue.id} to done")

        # issue_list.append(issue)
        # Jira limits bulk creation to 50 issues per call, create pages of 50 issues
        # if len(tmp_issues) == JIRA_MAX_ISSUES:
        #     issue_list.append(tmp_issues)
        #     tmp_issues = []
    # append last page
    # issue_list.append(tmp_issues)

# bulk create in Jira
# for issue_page in issue_list:
#     issues = jira_client.create_issues(field_list=issue_page)
#     print(f"created {len(issue_page)} issues")


print("done")
