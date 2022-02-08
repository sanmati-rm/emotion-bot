from slack import WebClient
from emotionBot import emotionBot
from slackeventsapi import SlackEventAdapter
import os
from flask import Flask, Response
import logging

app = Flask(__name__)


SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']

# Create a slack client
slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))

slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events", app)  

def get_emotion(text,channel,user):
    # Get a new CoinBot
    emotion_bot = emotionBot(text,channel,user)

    # Get the onboarding message payload
    message = emotion_bot.get_message_payload()

    # Post the onboarding message in Slack
    #slack_web_client.chat_postMessage(**message)
    slack_web_client.chat_postEphemeral(**message)

    return Response(status=200)

@slack_events_adapter.on("message")
def get_message(payload):

    event = payload.get("event", {})
    message = payload["event"]

    if message.get('bot_id') is None:
        text = event.get("text")
        channel_id = event.get("channel")
        user=event.get("user")
    
    return get_emotion(text,channel_id,user)



if __name__ == "__main__":
    
    app.run(port=3000)
    
    # # Create the logging object
    # logger = logging.getLogger()

    # # Set the log level to DEBUG. This will increase verbosity of logging messages
    # logger.setLevel(logging.DEBUG)

    # # Add the StreamHandler as a logging handler
    # logger.addHandler(logging.StreamHandler())

    # # Run our app on our externally facing IP address on port 3000 instead of
    # # running it on localhost, which is traditional for development.
    # app.run(host='0.0.0.0', port=3001)
