import logging
import json

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Unimplimented Slack command called.')
    return func.HttpResponse(
            "This HTTP triggered function executed successfully.",
            status_code=200
    )
