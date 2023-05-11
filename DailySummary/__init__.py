import datetime
import numpy as np
import logging
import random
import requests
from requests.auth import HTTPBasicAuth
import os
from datetime import datetime

JIRA_TOKEN = os.environ['JIRA_TOKEN']

import azure.functions as func
from utils import get_github_api, post_message

def main(mytimer: func.TimerRequest) -> None:
    ############ PRS
    api = get_github_api()
    github_results = api.search.issues_and_pull_requests(q='is:open is:pr label:"Ready for Review" archived:false author:nayr974 author:ColbySong author:ashleyyy author:Karanveer-singh671 author:nasser-31 author:irishic author:mmrlivingstone', order='desc')

    links = ""
    for item in github_results["items"]:
        links += f"\n><{item.pull_request.html_url}|{item.title[:75] + '...' if len(item.title) > 78 else item.title}>"

    ############ Sprint Data
    response = requests.get("https://thinkific.atlassian.net/rest/agile/1.0/board/422/sprint",
	headers={"Authorization": f"Basic {JIRA_TOKEN}"})
    sprint_id = list(response.json()["values"])[-1]["id"]
    sprint_name = list(response.json()["values"])[-1]["name"]
    sprint_goal = list(response.json()["values"])[-1]["goal"].replace('\n', ' ')
    sprint_start = datetime.strptime(list(response.json()["values"])[-1]["startDate"], "%Y-%m-%dT%H:%M:%S.%fZ")
    sprint_end = datetime.strptime(list(response.json()["values"])[-1]["endDate"], "%Y-%m-%dT%H:%M:%S.%fZ")
    days_remaining = np.busday_count(datetime.utcnow().date(), sprint_end.date()) +1

    #response = requests.get(f"https://thinkific.atlassian.net/rest/greenhopper/1.0/rapid/charts/scopechangeburndownchart?rapidViewId=421&sprintId={sprint_id}",
	#headers={"Authorization": f"Basic {JIRA_TOKEN}"})
    #scopeChangeBurndownChart = response.json()

    response = requests.get(f"https://thinkific.atlassian.net/rest/agile/1.0/sprint/{sprint_id}/issue",
    headers={"Authorization": f"Basic {JIRA_TOKEN}"})
    issues = list(response.json()["issues"])
    totalIssues = response.json()["total"]
    totalPoints = 0
    totalPointsDone = 0
    totalIssuesDone = 0

    for issue in issues:
        if issue["fields"]["status"]["name"] == "Done" or issue["fields"]["status"]["name"] == "Not today, Satan." :
            totalIssuesDone = totalIssuesDone + 1
            if issue["fields"]["customfield_10026"]:
                totalPointsDone = int(totalPointsDone + issue["fields"]["customfield_10026"])
        if issue["fields"]["customfield_10026"]:
            totalPoints = totalPoints + int(issue["fields"]["customfield_10026"])


    ############### BUILD MESSAGE
    blocks = [{
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"Totoro Daily Summary"
            }
        }]

    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f":run: *{sprint_name}*\n>Goal: {sprint_goal}\n>\n><https://thinkific.atlassian.net/jira/software/c/projects/TOTO/boards/422|Sprint Board>   <https://thinkific.atlassian.net/jira/software/c/projects/TOTORO/boards/422/reports/burnup-char|Burnup Chart>    <https://thinkific.atlassian.net/jira/software/c/projects/TOTORO/boards/422/reports/velocity-chart|Velocity Report>\n>{days_remaining} work days remaining    {totalIssuesDone}/{totalIssues} items done    {totalPointsDone}/{totalPoints} story points done"
        }
    })

    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f":pencil: *Huddle notes in this thread!*\n>Please add your notes by 10am PT."
        }
    })
        
    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f":blob_wave: *{github_results.total_count} PR's are _Ready for Review_ today!*{links}\n\n<!subteam^S032EF67EUS>"
        },
        "accessory": {
            "type": "image",
            "image_url": "https://soranews24.com/wp-content/uploads/sites/3/2020/08/My-Neighbor-Totoro-anime-storyboard-book-Hayao-Miyazaki-art-Japanese-neighbour-Japan-pictures-news-1.jpg",
            "alt_text": "totoro"
        }
    })

    post_message("#team-totoro-test", text="Totoro Daily Summary", blocks=blocks)
 