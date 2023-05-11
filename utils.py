
import requests
import logging
import json
import datetime
import random
import os

from urllib.parse import unquote
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from ghapi.core import GhApi

STORAGE_URL = os.environ['STORAGE_URL']
STORAGE_TOKEN = os.environ['STORAGE_TOKEN']
BOT_TOKEN = os.environ['BOT_TOKEN']
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']

client = WebClient(token=BOT_TOKEN)

def get_github_api():
    api = GhApi(owner='thinkific', repo='thinkific', token=GITHUB_TOKEN)
    return api

def get_data():    
    logging.info(STORAGE_URL)
    logging.info(STORAGE_TOKEN)
    response = requests.get(STORAGE_URL, headers={"Content-Type": "application/json","X-Master-Key": STORAGE_TOKEN})
    return response.json()["record"]

def update_data(data):
    response = requests.put(STORAGE_URL, data=json.dumps(data), headers={"Content-Type": "application/json","X-Master-Key": STORAGE_TOKEN, "X-Bin-Versioning": "false"})

def pick_teammember(team, sort_by_attribute, exclude_team_index=None):
    team_pool = sorted(team, key=lambda item: item[sort_by_attribute])[:round(len(team)/2)]
    picked_teammember = random.choice(team_pool)
    return picked_teammember if team.index(picked_teammember) != exclude_team_index else pick_teammember(team, sort_by_attribute, exclude_team_index)

def unwrap_payload(req):
    return json.loads(unquote(req.get_body().decode('utf-8')).removeprefix("payload="))

def update_message(channel, ts, text=None, blocks=None):
    try:
        client.chat_update(
            channel=channel,
            ts=ts,
            text=text,
            blocks=blocks
        )
    except SlackApiError as e:
        logging.info(e.response["error"])
        assert e.response["error"] 

def delete_message(channel, ts):
    try:
        client.chat_delete(
            channel=channel,
            ts=ts
        )
    except SlackApiError as e:
        logging.info(e.response["error"])
        assert e.response["error"] 

def post_message(channel, text=None, blocks=None):
    logging.info(BOT_TOKEN)
    try:
        client.chat_postMessage(
            channel=channel,
            text=text,
            blocks=blocks,
            link_names=True
        )
    except SlackApiError as e:
        assert e.response["error"] 

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)