import datetime
import numpy as np
import logging
import random
import requests
from requests.auth import HTTPBasicAuth
import os
from datetime import datetime

import azure.functions as func
from utils import get_github_api, post_message

GITLAB_TOKEN = os.environ['GITLAB_TOKEN']
SHORTCUT_TOKEN = os.environ['SHORTCUT_TOKEN']

def main(mytimer: func.TimerRequest) -> None:

    repos = ["cellar-utilities", "cellar-bootstrap", "cellar-ecom-fe", "cellar-ecom-html", "cellar-ecom-web", "cellar-getcellar-site", "cellar-ios", "cellar-mobile", "cellar-pos-html", "cellar-pos-ios", "core-api", "core-html", "customer-html", "therapy-html", "ecom-front"]
    link_count = 0
    links = ""

    for repo in repos:
        response = requests.get(f"https://gitlab.com/api/v4/projects/cellarco%2F{repo}/merge_requests?state=opened",
        headers={"Authorization": f"Bearer {GITLAB_TOKEN}"})

        merge_requests = list(response.json())

        show_repo = False
        for merge_request in merge_requests:        
            if 'Andrey Lykov' not in merge_request['author']['name'] and 'Sabina Ashrafova' not in merge_request['author']['name'] and 'Álvaro Lázaro' not in merge_request['author']['name']:
                show_repo = True

        if show_repo and len(merge_requests) > 0:
            links += f"\n*{repo}*"

        for merge_request in merge_requests:        
            if 'Andrey Lykov' not in merge_request['author']['name'] and 'Sabina Ashrafova' not in merge_request['author']['name'] and 'Álvaro Lázaro' not in merge_request['author']['name']:
                links += f"\n><{merge_request['web_url']}|{merge_request['author']['name']} - {merge_request['title'][:75] + '...' if len(merge_request['title']) > 78 else merge_request['title']}>"
                link_count = link_count + 1

    response = requests.get(f"https://api.app.shortcut.com/api/v3/workflows/500000005",
    headers={"Shortcut-Token": f"{SHORTCUT_TOKEN}"})

    workflow = response.json()

    blocks = [{
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"Barylka's Daily Bark"
            }
        }]
    
    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*:shortcut: <https://app.shortcut.com/cellar-1/stories/space/433/everything|Shortcut Board>*\n*{workflow['states'][2]['num_stories']}* items _In Progress_ | *{workflow['states'][4]['num_stories']}* items _In QA_ | *{workflow['states'][5]['num_stories']}* items _Blocked_\n\n\n{':blob_wave:' if link_count > 0 else ':blob_neutral:'} *{link_count} MR's are _Ready for Review_ today{'! :excited-dog:' if link_count > 0 else '.'}*\n{links}\n\n"
        },
        "accessory": {
            "type": "image",
            "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRbnZHJAEbcFxRub03cMAKT2oMNT8kkS5zYAz7z9Qgo1rZgnNSVjoIGGaPkaze5KHrkJuQ&usqp=CAU",
            "alt_text": "barylka"
        }
    })

    post_message("#team_barylka", text="Daily Bark", blocks=blocks)