import asyncio
import datetime
import json
import sqlite3
from telethon import TelegramClient, functions, types, events
from telethon.tl.functions.contacts import DeleteContactsRequest
from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.functions import PingRequest
from flask import Flask, request, jsonify
import os

from telethon.tl.types import InputUser

# LOAD configuration
# FIXME don't forget to link a <connections> entity when adapter will be created
db = sqlite3.connect(f'{os.getcwd()}/test.sqlite')
cur = db.cursor()
res = cur.execute('select value from configuration where key == "tg_api_id"')
api_id = res.fetchone()[0]
res = cur.execute('select value from configuration where key == "tg_api_hash"')
api_hash = res.fetchone()[0]
my_phone_number = '+998950500333'  # TODO get from db


# Initialize the client
client = TelegramClient('anon', api_id, api_hash)


@client.on(events.MessageRead())
async def handler(event):
    # Log when someone reads your messages
    print('Someone has read all your messages until', event.max_id)

@client.on(events.MessageRead(inbox=True))
async def handler(event):
    # Log when you read message in a chat (from your "inbox")
    print('You have read messages until', event.max_id)


async def create_and_check_contact(contact_phone_number):
    try:
        if not client.is_connected():
            await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(my_phone_number)
            code = '12345'
            await client.sign_in(my_phone_number, code)


        # Getting information about yourself
        me = await client.get_me()
        print(me.stringify())

        contacts = await client(functions.contacts.GetContactsRequest(hash=0))

        ## ADD CONTACT
        # Add the contact to your Telegram account
        result = await client(functions.contacts.ImportContactsRequest(
            contacts=[types.InputPhoneContact(
                client_id=0,
                phone=contact_phone_number,
                first_name='unknown',
                last_name='unknown'
            )]
        ))

        d = {}
        if result.users:
            user_id = result.users[0].id

            await client(DeleteContactsRequest(id=[user_id]))  # !! helps to give actual name of the user
            # get real name
            user = await client.get_entity(types.User(id=user_id))
            print(f"First Name: {user.first_name}")
            print(f"Last Name: {user.last_name}")
            d.update({
                "user_id": user_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": contact_phone_number,
                "login": user.username
            })

            # Verify if the chat is created
            if False:  # testing
                dialogs = await client.get_dialogs()
                for dialog in dialogs:
                    if dialog.entity.id == user_id:
                        # !! dialog.id == dialog.entity.id
                        await client.send_message(dialog.id, f'Testing {datetime.datetime.now()}!')

                        d["dialog_id"] = dialog.id
                        return json.dumps(d)
        else:
            return None

        return json.dumps(d)
    finally:
        # if client.is_connected():
        #     await client.disconnect()  # prevent to handlers to be called
        pass


async def import_contact(body):
    data = body
    contact_phone_number = data.get('contact_phone_number')
    # first_name = data.get('first_name', 'First Name')
    # last_name = data.get('last_name', 'Last Name')

    success = await create_and_check_contact(contact_phone_number)

    if success:
        return success
    else:
        raise ValueError(f"Contact {contact_phone_number} is not created")



