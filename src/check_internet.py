# So I've creted this because my ISP decide to have cut my internet a saturday at the 
# afternoon and I didn't have anything to do without internet so I just went out for a drive
# until I got the notification

import requests
from discord_webhook import DiscordWebhook
import time

def check_internet():
    try:
        requests.get('http://www.google.com', timeout=3)
        return True
    except:
        return False

def send_notification():
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/<TOKEN>')
    webhook.content = 'There is internet connection.'
    response = webhook.execute()

if __name__ == '__main__':
    while True:
        if check_internet():
            send_notification()
            break
        else:
            time.sleep(60)