import logging
import azure.functions as func 
from create_and_post import create_image_and_post_to_socials

app = func.FunctionApp()

@app.schedule(schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def eod_with_azure(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    create_image_and_post_to_socials()
    logging.info('Python timer trigger function executed.')