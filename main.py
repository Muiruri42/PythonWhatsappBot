import logging
import os
import signal
import requests
import sys
from messages import *
from datetime import timedelta
from neonize.client import NewClient
from neonize.events import (
    ConnectedEv,
    MessageEv,
    PairStatusEv,
    event,
    ReceiptEv,
    CallOfferEv,
)
from neonize.types import MessageServerID
from neonize.utils import log
from neonize.utils.enum import ReceiptType

sys.path.insert(0, os.getcwd())


def interrupted(*_):
    event.set()


log.setLevel(logging.DEBUG)
signal.signal(signal.SIGINT, interrupted)


client = NewClient("db.sqlite3")
botnumber = "254754046165@s.whatsapp.net"

@client.event(ConnectedEv)
def on_connected(_: NewClient, __: ConnectedEv):
    log.info("⚡ Connected")


@client.event(ReceiptEv)
def on_receipt(_: NewClient, receipt: ReceiptEv):
     log.debug(receipt)


@client.event(CallOfferEv)
def on_call(_: NewClient, call: CallOfferEv):
    log.debug(call)


@client.event(MessageEv)
def on_message(client: NewClient, message: MessageEv):
    handler(client, message)

#Functions for Performing Different tasks.

def handler(client: NewClient, message: MessageEv):
    text = message.Message.conversation or message.Message.extendedTextMessage.text
    chat = message.Info.MessageSource.Chat
    cmd = text.split(' ')[0]
    testo = text.split(' ')[-1]
    match cmd:
        case "menu":
            client.send_image(
                chat,
                "https://download.samplelib.com/png/sample-boat-400x300.png",
                caption=menu,
                quoted=message,
            )
       
        case "repo":
             client.send_message(
                chat, "Test https://github.com/Muiruri42/PythonWhatsappBot/", link_preview=True
            )
        case "setgcname":
              client.set_group_name(chat, testo)
        case "ping":
            client.reply_message("pong", message)
        case "play":
            try:
                if len(text) == 0:
                    client.send_message(chat, "Usage: play dream ya kutoka kwa block buruklyn boyz")
                else:
                    url = f"https://spotify-mp3-downloader.vercel.app/get_download_link?search={testo}"
                    resp = requests.get(url)
                    if resp.status_code == 200:
                        music = resp.json()
                        song_url = music['download_link']
                        client.send_message(chat, client.build_audio_message(song_url, ptt=False, quoted=message),)
                    else:
                        client.send_message(chat, "An error occured with the Spotify API")
            except Exception as e:
                client.send_message(chat, f"ERROR: {e}", message)

        case "owner":
            client.send_contact(chat, "(^▽^) ＫＲＥＳＳＷＥＬＬ (✿^▽^)", "254798242085", quoted=message,)
            #client.reply_message("Thanks for trying to reach my owner. Contact Kresswell here +254798242085", message)
        case "gpt":
            if len(text) == 0:
                client.send_message(chat, "Hello, Please provide a query for me to process.", message)
            else:
                url = f"https://dev-the-dark-lord0.pantheonsite.io/wp-admin/js/Apis/Gemini.php?message={text}"
                response = requests.get(url)
                if response.status_code == 200:
                    answer = response.text
                    client.send_message(chat, answer, message)
                else:
                    client.send_message(chat, "An error occured while processing.", message)
        case "lyrics":
            try:
                song = text.split(' ')[-1]
                if len(song) == 0:
                    client.send_message(chat, "Please Provide a song for me to process its lyrics.")
                else:
                    url = f"https://lyrist.vercel.app/api/{song}"
                    response = requests.get(url)
                    if response.status_code == 200:
                        json_lyrics = response.json()
                        lyrics = json_lyrics.get("lyrics")
                        title = json_lyrics.get("title")
                        artist = json_lyrics.get("artist")
                        logo = json_lyrics.get("image")
                        client.send_message(chat, f"""
SONG TITLE: {title}
ARTIST: {artist}
_____________________________
{lyrics}
""", message)
            except Exception as e:
                client.send_message(chat, f"ERROR: {e}")



@client.event(PairStatusEv)
def PairStatusMessage(_: NewClient, message: PairStatusEv):
    log.info(f"logged as {message.ID.User}")


client.connect()
