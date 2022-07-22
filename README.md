# Spreadsheet to Jira

## Config file
`config/__init__.py`
```
API_TOKEN = ""
ATLASSIAN_ACCOUNT = "test@test.com"
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
 
| Epic | En tant que... | Je peux... | Dans le but de... | Détails | Total | Fait
|--|--|--|--|--|--|--|
| Login | Utilisateur | me connecter à l'application | y accéder | Connexion avec Google | 1 | TRUE |
| Accueil | Utilisateur | lister mes todos | les voir | Liste paginée | 3 | FALSE |

2. Download as a CSV
3. Copy CSV at root of script, and name it `user_stories.csv`
4. Run main.py

### FYI: these are the supported headers, but you can add some more, or change the order