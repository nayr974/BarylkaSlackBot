import logging
import json
import azure.functions as func
from datetime import datetime
from utils import get_data, update_data, pick_teammember, post_message
from messages import dev_of_the_week


def main(mytimer: func.TimerRequest) -> None:
    return 
    data = get_data()
    logging.info(json.dumps(data))

    dotwList = data["dotwList"]
    backupList = data["backupList"]
    
    if dotwList is None or len(dotwList) != 3:
        dotwList = [None,None,None]
    if dotwList[1] is None:
        dotwList[1] = data["team"].index(pick_teammember(data["team"], "dotwCount"))
    dotwList[2] = data["team"].index(pick_teammember(data["team"], "dotwCount", dotwList[1]))
    data["dotwList"] = dotwList

    if backupList is None or len(backupList) != 3:
        backupList = [None,None,None]
    if backupList[1] is None:
        backupList[1] = data["team"].index(pick_teammember(data["team"], "backupCount", dotwList[1]))
    backupList[2] = data["team"].index(pick_teammember(data["team"], "backupCount", dotwList[2]))
    data["backupList"] = backupList
    
    post_message("#team-totoro", text="It's time to pick the *Dev Of The Week* for next week!", blocks=dev_of_the_week(data))
    update_data(data)
