from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, ChatAdminRequiredError, \
    ChannelPrivateError, UserKickedError, InputUserDeactivatedError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.channels import JoinChannelRequest
import sys
import csv
import traceback
import time
import random

api_id =1188591
api_hash = '9f1fd643fa73d4320b22d7643ce0d60b'
phone = '+972527373474'
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    phone = input("Enter your phone: ")
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

ForwarderChannel = -1001363030854

channelList = {
   -1893480242:-1612670449,
-1598345276:-1513230619,
-1682521156:-1612670449,
-1716080812:-1761360264,
-1819569132:-1648396817,
-1703044653:-1355230118,
-1617372317:-1612670449,
-1792983211:-1606632080,
-1817718661:-1502228530,
-1885997371:-1608979643,


}


@client.on(events.NewMessage)
async def my_event_handler(event):
    # Ignore Outgoing Message Updates
    if event.out:
        return
    is_group = event.is_group
    is_channel = event.is_channel
    is_private = event.is_private
    message = event.message.message
    has_media = event.media
    sender_id = None

    if is_channel:
        sender_id = event.chat_id
        if sender_id in channelList:
            await client.send_message(
                channelList[sender_id],  # to which entity you are forwarding the messages
                event.message  # the messages (or message) to forward
            )
    elif is_group:
        print('\n# Group Message')
        sender_id = event.message.to_id.chat_id
    elif is_private:
        await client.send_message(
            ForwarderChannel,  # to which entity you are forwarding the messages
            event.message  # the messages (or message) to forward
        )
    else:
        print('Invalid Sender Type', event)
        print('Message : {}'.format(message))
        print('Sender : {}'.format(sender_id))
    # Mark as read
    try:
        user_entity = await client.get_input_entity(sender_id)
        await  client.send_read_acknowledge(user_entity, max_id=event.original_update.pts)
    except Exception as e:
        print(e)


client.start()
client.run_until_disconnected()