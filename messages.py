from datetime import datetime, timedelta
from utils import next_weekday

def dev_of_the_week_confirmed(data, lunch_tip=False):
    dotwList = data["dotwList"]
    backupList = data["backupList"]
    next_monday = next_weekday(datetime.now(),0).strftime("%b %d %Y")
    next_friday = next_weekday(datetime.now(),4).strftime("%b %d %Y")
    next_next_monday = next_weekday(datetime.now() + timedelta(days=7),0).strftime("%b %d %Y")
    next_next_friday = next_weekday(datetime.now() + timedelta(days=7),4).strftime("%b %d %Y")
    message = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":tada: The next *Legendary Defenders* are ready for battle!\n\n\n:date: {next_monday} - {next_friday}\n\n*Dev Of The Week*: {data['team'][dotwList[0]]['name']}\n*Backup*: {data['team'][backupList[0]]['name']}"
                },
                "accessory": {
                    "type": "image",
                    "image_url": "https://dvdmedia.ign.com/dvd/image/article/119/1199920/voltron-the-legend-begins-20111012014743151-000.jpg",
                    "alt_text": "voltron image"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"\n\n:date: {next_next_monday} - {next_next_friday} (tentative)"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Dev Of The Week*: {data['team'][dotwList[1]]['name']}\n*Backup*: {data['team'][backupList[1]]['name']}"
                }
            }
        ]
    if lunch_tip == True:
        message.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"* {data['team'][dotwList[0]]['name']} don't forget your lunch perk! Use the Engineering code, and *Voltron - Dev Of The Week Allowance* as the comment."
                }
            })
    return message

def dev_of_the_week(data):
    dotwList = data["dotwList"]
    backupList = data["backupList"]
    next_monday = next_weekday(datetime.now(),0).strftime("%b %d %Y")
    next_friday = next_weekday(datetime.now(),4).strftime("%b %d %Y")
    next_next_monday = next_weekday(datetime.now() + timedelta(days=7),0).strftime("%b %d %Y")
    next_next_friday = next_weekday(datetime.now() + timedelta(days=7),4).strftime("%b %d %Y")
    return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":mega: It's time to confrim the next *Legendary Defenders*!\n\n{data['team'][dotwList[0]]['name'] if dotwList[0] is not None else 'Somebody'} please check with the people below, then click 'Looks Good!' to confirm or choose others if needed."
                },
                "accessory": {
                    "type": "image",
                    "image_url": "https://dvdmedia.ign.com/dvd/image/article/733/733383/voltron-defender-of-the-universe-volume-1-20060918060709398-000.jpg",
                    "alt_text": "voltron image"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":date: {next_monday} - {next_friday}"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Dev Of The Week*:\n{data['team'][dotwList[1]]['name']}"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "pick someone else"
                    },
                    "value": "new_dotw_1"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Backup*:\n{data['team'][backupList[1]]['name']} "
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "pick someone else"
                    },
                    "value": "new_backup_1"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"\n\n"
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":date: {next_next_monday} - {next_next_friday} (tentative)"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Dev Of The Week*:\n{data['team'][dotwList[2]]['name']}"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "pick someone else"
                    },
                    "value": "new_dotw_2"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Backup*:\n{data['team'][backupList[2]]['name']} "
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "pick someone else"
                    },
                    "value": "new_backup_2"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"\n\n\n"
                },
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Looks good!",
                            "emoji": True
                        },
                        "value": "confirm_dotw",
                        "style": "primary",
                        "action_id": "actionId-0",
                        "confirm": {
                            "title": {
                                "type": "plain_text",
                                "text": "Are you sure?"
                            },
                            "text": {
                                "type": "mrkdwn",
                                "text": f"This will confirm {data['team'][dotwList[1]]['name']} and {data['team'][backupList[1]]['name']} as DOTW and Backup."
                            },
                            "confirm": {
                                "type": "plain_text",
                                "text": "Yes!"
                            },
                            "deny": {
                                "type": "plain_text",
                                "text": "Wait, let me double check."
                            }
                        }
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Go away bot",
                            "emoji": True
                        },
                        "style": "danger",
                        "value": "cancel_dotw",
                        "action_id": "actionId-1",
                        "confirm": {
                            "title": {
                                "type": "plain_text",
                                "text": "Are you sure?"
                            },
                            "text": {
                                "type": "mrkdwn",
                                "text": "This will delete this message, and you can manage the dev of the week all by yourself. I'm sure you'll do fine without me. No, I'm not pouting."
                            },
                            "confirm": {
                                "type": "plain_text",
                                "text": "Yes, go away!"
                            },
                            "deny": {
                                "type": "plain_text",
                                "text": "I've changed my mind."
                            }
                        }
                    }
                ]
            }
        ]