# Spreadsheet to Jira

## Config file
`config/__init__.py`
```
API_TOKEN = ""
ATLASSIAN_ACCOUNT = ""
JIRA_PROJECT = "TS" # project code in Jira
JIRA_MAX_ISSUES = 50
```

## Setup
```
python3 -m venv venv

pip install -r requirements.txt
```

## Process
 1. Write US in a spreadsheet. Template :
 
| Epic | En tant que... | Je peux... | Dans le but de... | Détails |
|--|--|--|--|--|
| | | | | |

2. Download as a CSV
3. Copy CSV at root of script
4. Run main.py
