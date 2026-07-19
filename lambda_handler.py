from daily_sender import send_daily_reminder

def lambda_handler(event, context):
    send_daily_reminder()
    