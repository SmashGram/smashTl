import rsa

import telethon.crypto.rsa as telethon_rsa

from telethon import TelegramClient, events, functions
from telethon.sessions import SQLiteSession
from telethon.network.connection.tcpabridged import ConnectionTcpAbridged
from telethon.client.auth import AuthMethods

class SmashGramClient(TelegramClient):
    def __init__(self, session, api_id, api_hash, **kwargs):
        super().__init__(
            session,
            api_id,
            api_hash,
            connection=ConnectionTcpAbridged,
            **kwargs
        )

    async def send_message_to(self, target, message):
        if isinstance(target, str): # username provided
            if target.startswith("@"):
                target.lstrip("@")
            
            await self.send_message(target, message)
        elif isinstance(target, int): # id provided
            entity = await self.get_entity(target)

            await self.send_message(entity, message)

    async def log_in(self, phone):
        try:
            await self.connect()
        except IncompleteReadError:
            print("Server is down, unable to connect")

        if not await self.is_user_authorized():
            await self.send_code_request(phone)
            code = input('Введите код: ')

            try:
                await self.sign_in(phone, code)
            except Exception as e:

                if type(e).__name__ == "FloodWaitError":
                    message = e.split(" ")

                    seconds_total = int(message[3])
                    minutes = seconds_total // 60
                    seconds = seconds_total % 60
                    print(f"FloodWaitError: a wait of {minutes}m {seconds}s is required, please try again later")
                else:
                    print(f"Ошибка sign_in: {type(e).__name__}: {e}")
                return

    async def get_direct_messages(self):
        dialogs = await self.get_dialogs()

        for i in range(len(dialogs)):
            if (is_direct_message(dialogs[i].id)):
                print(f"chat_id: {dialogs[i].id}, user: {dialogs[i].name}")

    async def get_chats_and_channels(self):
        dialogs = await self.get_dialogs()

        for i in range(len(dialogs)):
            if (is_chat_or_channel_id(dialogs[i].id)):
                print(f"target_id: {dialogs[i].id}, user: {dialogs[i].name}")

def connect_to_server():
    API_ID      = 19434052
    API_HASH    = '4de79c3e2611b4a42131565e6602af54'
    SERVER_IP   = '109.107.181.246'
    SERVER_PORT = 20543

    RSA_KEY = b"""-----BEGIN RSA PUBLIC KEY-----
    MIIBCgKCAQEAu+3tvscWDAlEvVylTeMr5FpU2AjgqzoQHPjzp69r0YAtq0a8rX0M
    Ue78F/FRAqBaEbZW6WBzF3AjOlNYpOtvvwGhl9rGCgziunbd9nwcKJBMDWS9O7Mz
    /8xjz/swIB4V56XcjOhrjUHJ/GniFKoum00xeEcYnr5xnLesvpVMq97Ga6b+xt3H
    RftHY/Zy1dG5zs8upuiAOlEiKilhu1IthfMjFG3NF6TiGrO9YU3YixFbJy67jtHk
    v5FarscM2fC5iWQ2eP1y6jXR64sGU3QjncvozYOePrH9jGcnmzUmj42x/H28IjJQ
    9EjEc22sPOuauK0IF2QiCGh+TfsKCK189wIDAQAB
    -----END RSA PUBLIC KEY-----"""

    def patch_telethon(pem_key):
        key = rsa.PublicKey.load_pkcs1(pem_key)
        fingerprint = telethon_rsa._compute_fingerprint(key)
        telethon_rsa._server_keys.clear()
        telethon_rsa._server_keys[fingerprint] = (key, False)

    patch_telethon(RSA_KEY)

    async def _on_login_noop(self, user):
        pass

    # idk why patched
    AuthMethods._on_login = _on_login_noop

    session = SQLiteSession('mybot')
    session.set_dc(0, SERVER_IP, SERVER_PORT)

    return SmashGramClient(session, API_ID, API_HASH)

def get_schema_layer():
    from telethon.tl import alltlobjects

    print("current library schemaLayer: " + str(alltlobjects.LAYER))

def is_chat_or_channel_id(id):
    return id < 0

def is_direct_message(id):
    return not is_chat_or_channel_id(id)