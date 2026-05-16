# import my library
import lib_smashgram as smashgram
# import module to run project
import asyncio

# conect to server
client = smashgram.connect_to_server()
# current user phone
phone = "+your number without spaces here"

async def main():
    # log in to client
    await client.log_in(phone)

    # send message by username
    await client.send_message_to('me', 'bbbcc')
    # send message by id
    await client.send_message_to(74, 'bb#cc')

    # get list of direct messages on account
    await client.get_direct_messages()
    # get list of chast and channels on account
    await client.get_chats_and_channels()

    # poll infinitely
    await client.run_until_disconnected()

# run program
if __name__ == '__main__':
    asyncio.run(main())