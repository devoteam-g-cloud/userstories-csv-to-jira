import csv
from config import ATLASSIAN_ACCOUNT, API_TOKEN, JIRA_PROJECT, JIRA_URL, JIRA_MAX_ISSUES
from jira import JIRA

# init Jira client
jira_client = JIRA(
    JIRA_URL, basic_auth=(ATLASSIAN_ACCOUNT, API_TOKEN)
)
# fetch all fields, including custom fields
fields = jira_client.fields()
# find the field for the story points
story_points_field = None
for f in fields:
    if f.get("name") == "Story point estimate":
        story_points_field = f
        break
# init the list of epics
created_epics = {}
# init the list of issues
issue_list = []
# open and read the csv file
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
                # add epic id to the list of epics (to be used when creating issues for this epic)
                created_epics[issue_data["Epic"]] = epic.id
                print(f"created epic {issue_data['Epic']}")
        # add description to issue
        description = issue_data["Details"]
        # add quote details from quotation (can be removed)
        if "Front" in issue_data and "Back" in issue_data:
            description += f"""
            \n
            Front: {issue_data.get('Front', 0)}j\n
            Back: {issue_data.get('Back', 0)}j\n
            """
        # init Jira issue json
        issue = {
            "project": {"key": JIRA_PROJECT},
            "summary": f"As a {issue_data.get('As a...')}, I can {issue_data.get('I can...')} so that {issue_data.get('so that...')}",
            "description": description,
            "issuetype": {"name": "Story"},
            "parent": {"id": created_epics[issue_data["Epic"]]},
        }
        # add story point fields
        if story_points_field and issue_data.get("Total"):
            try:
                issue[story_points_field.get("id")] = float(issue_data.get("Total", 0))
            except TypeError:
                print(f"could not parse {issue_data.get('Total')}")

        # add issue to tmp list
        tmp_issues.append(issue)

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
