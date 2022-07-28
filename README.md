# CSV to Jira
Script to create issues and epics in Jira from a spreadsheet filled with User stories, converted to CSV. 
Format was initialized with English headers, can be changed in the code according to your need

## Config file
Copy the `config/__init__template.py` into `config/__init__.py` and fill in the variables required

## Config in Jira
Create a token, to be added to the config file mentionned above ([Documentation](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/)).

## Setup
```
python3 -m venv venv

pip install -r requirements.txt
```

## Process
 1. Write US in a spreadsheet. Template :
 
| Epic | As a... | I can... | so that... | Details | Total
|--|--|--|--|--|--|
| Login | User | log in to the app | I can access it | SSO Google | 1
| Home | User | list my todos | I can have a full view of them | See if we need pagination, mockup to be done | 3

2. Download as a CSV
3. Copy CSV at root of script, and name it `user_stories.csv`
4. Run main.py

## FYI: these are the supported headers, but you can add some more if you adapt the script. The order of the columns is not important as it is converted to JSON in the code.