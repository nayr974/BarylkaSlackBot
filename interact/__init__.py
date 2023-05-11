import logging
import azure.functions as func

from utils import post_message, unwrap_payload, update_message, delete_message, get_data, update_data, pick_teammember
from messages import dev_of_the_week, dev_of_the_week_confirmed

def confirm_dotw(data, payload):
    dotwList = data["dotwList"]
    backupList = data["backupList"]

    dotwList.pop(0)
    dotwList.append(None)
    backupList.pop(0)
    backupList.append(None)

    data["team"][dotwList[0]]["dotwCount"] += 1
    data["team"][backupList[0]]["backupCount"] += 1
    
    update_message(payload["channel"]["id"], payload["message"]["ts"], text="The dev of the week for next week has been picked!", blocks=dev_of_the_week_confirmed(data, lunch_tip=True))
    post_message("#project-tech-team_daily", text="The dev of the week for next week has been picked!", blocks=dev_of_the_week_confirmed(data))
    post_message("#project-dotw_sync", text="The dev of the week for next week has been picked!", blocks=dev_of_the_week_confirmed(data))
    update_data(data)

def delete_post(data, payload):
    data["dotwList"] = None
    data["backupList"] = None

    delete_message(payload["channel"]["id"], payload["message"]["ts"])	
    update_data(data)

def new_dotw(data, payload, dotw_index):
    current_choice = data["dotwList"][dotw_index]
    data["dotwList"][dotw_index] = data["team"].index(pick_teammember(data["team"], "dotwCount", current_choice))

    update_message(payload["channel"]["id"], payload["message"]["ts"], blocks=dev_of_the_week(data))
    update_data(data)

def new_backup(data, payload, backup_index):
    current_choice = data["backupList"][backup_index]
    data["backupList"][backup_index] = data["team"].index(pick_teammember(data["team"], "backupCount", current_choice))

    update_message(payload["channel"]["id"], payload["message"]["ts"], blocks=dev_of_the_week(data))
    update_data(data)

def main(req: func.HttpRequest) -> func.HttpResponse:
    payload = unwrap_payload(req)
    data = get_data()

    if payload["actions"][0]["value"] == "confirm_dotw":
        confirm_dotw(data, payload)

    if payload["actions"][0]["value"] == "cancel_dotw":
        delete_post(data, payload)

    if payload["actions"][0]["value"].startswith("new_dotw"):
        dotw_index = int(payload["actions"][0]["value"][-1])
        new_dotw(data, payload, dotw_index)

    if payload["actions"][0]["value"].startswith("new_backup"):
        backup_index = int(payload["actions"][0]["value"][-1])
        new_backup(data, payload, backup_index)

    return func.HttpResponse(
            "This HTTP triggered function executed successfully.",
            status_code=200
    )