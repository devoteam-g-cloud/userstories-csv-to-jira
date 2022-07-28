from config import ATLASSIAN_ACCOUNT, API_TOKEN, JIRA_PROJECT, JIRA_URL
from jira import JIRA

jira_client = JIRA(JIRA_URL, basic_auth=(ATLASSIAN_ACCOUNT, API_TOKEN))


def get_all_issues(project_name=JIRA_PROJECT, fields=["id"]):
    """
    Removes all issues from a jira project
    """
    issues = []
    i = 0
    chunk_size = 100
    while True:
        chunk = jira_client.search_issues(f'project = {project_name}', startAt=i, maxResults=chunk_size, fields=fields)
        i += chunk_size
        issues += chunk.iterable
        if i >= chunk.total:
            break
    return issues

issues = get_all_issues()
for i in issues:
    i.delete()
    print(f"deleted {i.key}")

