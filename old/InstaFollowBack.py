'''
    @author Matteo Gianvenuti https://github.com/mqtth3w
    @license MIT License
    This software allow you to connect to instagram with login (2FA supported)
    and automatically download following and followers to know who doesen't follow you back.
    Optionally you can automatically unfollow them.
'''

from instagrapi import Client
from instagrapi.exceptions import TwoFactorRequired, LoginRequired, ClientJSONDecodeError, ChallengeRequired
from time import sleep
from sys import exit as sysexit
from os import makedirs, path
import json
from Crypto.Cipher import AES
#from Crypto.Util.Padding import pad, unpad
# To see your ip "https://api.ipify.org/"
print("InstaFollowBack")
print("Copyright (C) Matteo Gianvenuti. All rights reserved.\n")

# Change this password!!!
KEY_32 = b"mqtt1507IlRe2000h3vvGianve23nuti"
# Is better to use the input so don't save the password in this program!!!
# KEY_32 = input("Password?").encode("utf-8")

def pad(data:bytes, blockSize:int) -> bytes:
    padLen = blockSize - (len(data) % blockSize)
    return data + (bytes([padLen])*padLen)

def unpad(data:bytes, blockSize:int) -> bytes:
    return data[:-ord(data[-1:])]

def encrypt_AES256(plaintext:str) -> bytes:
    plaintext = plaintext.encode()
    cipher = AES.new(KEY_32, AES.MODE_ECB)
    return cipher.encrypt(pad(plaintext,16))

def decrypt_AES256(ciphertext:bytes) -> str:
    cipher = AES.new(KEY_32, AES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)
    return unpad(plaintext,16).decode()

def print_er(error:str):
    print(error)
    sleep(5)
    sysexit(1)

def load_settings():
    try:
        with open("./data/alpha.txt", "rb") as f:
            ciphertext = f.read()
        plaintext = decrypt_AES256(ciphertext)
        try:
            settings = json.loads(plaintext)
            return settings
        except json.JSONDecodeError:
            pass
    except FileNotFoundError:
        pass
    except:
        print("Error loading session data.")
    return {}

def store_settings(settings):
    ciphertext = encrypt_AES256(json.dumps(settings))
    try:
        with open("./data/alpha.txt", "wb") as f:
            f.write(ciphertext)
    except:
        print("Error saving session data.")

def load_user() -> tuple[str, str]:
    try:
        with open("./data/beta.txt", "rb") as f:
            ciphertext = f.read()
        plaintext = decrypt_AES256(ciphertext)
        try:
            user, passw = plaintext.split(maxsplit=1)
            return user, passw
        except:
            pass
    except FileNotFoundError:
        pass
    except:
        print("Error loading login data.")
    return "",""

def store_user(user, passw):
    ciphertext = encrypt_AES256(user+" "+passw)
    try:
        with open("./data/beta.txt", "wb") as f:
            f.write(ciphertext)
    except:
        print("Error saving login data.")

def login() -> Client:
    settings = load_settings()
    user, passw = load_user()
    used_input = False
    session = False
    print("Login to Instagram to see who doesn't follow you back."
        "\nIt's done automatically if session is already saved.")
    cl = Client()
    cl.delay_range = [1, 3]
    if settings:
        if user == "" or passw == "":
            user = input("Enter your username: ")
            passw = input("Enter your password: ")
            used_input = True
        try:
            cl.set_settings(settings)
            cl.login(user, passw)
            # check if session is valid
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                old_session = cl.get_settings()
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])
                try:
                    cl.login(user, passw)
                    session = True
                except TwoFactorRequired:
                    auth_code = input("Enter your 2FA authentication code: ")
                    try: 
                        cl.login(user, passw, verification_code=auth_code)
                        session = True
                    except:
                        print_er("Wrong auth, missing internet connection or too much attempts.")
                except:
                    pass
            session = True
        except ClientJSONDecodeError:
            pass
        except:
            pass
    if not session:
        if not used_input:
            user = input("Enter your username: ")
            passw = input("Enter your password: ")
        try:
            cl.login(user, passw)
        except TwoFactorRequired:
            auth_code = input("Enter your 2FA authentication code: ")
            try: 
                cl.login(user, passw, verification_code=auth_code)
            except:
                print_er("Wrong auth, missing internet connection or too much attempts.")
        except:
            print_er("Wrong credentials, missing internet connection or too much attempts.")
        store_settings(cl.get_settings())
        store_user(user, passw)
    return cl

def get_followers_usernames(cl, amount:int = 0) -> list[str]: # amount 0 -> get all
    try:
        followers = cl.user_followers(cl.user_id, amount=amount) # Dict
    except ChallengeRequired:
        print_er("Error: ChallengeRequired. Solve the captcha in your account.")
    return [user.username for user in followers.values()]
    
def get_following_usernames(cl, amount:int = 0) -> list[str]:
    try: 
        following = cl.user_following(cl.user_id, amount=amount)
    except ChallengeRequired:
        print_er("Error: ChallengeRequired. Solve the captcha in your account.")
    return [user.username for user in following.values()]

def print_bad_friends(followers:list[str], following:list[str]) -> list[str]:
    counter = 0
    bad_friends = []
    for person in following:
        if person not in followers:
            print(person, end=" ")
            bad_friends.append(person)
            counter += 1
    print(f"\nTotal people who don't follow you back: {counter}.")
    return bad_friends

def auto_unfollow(bad_friends:list[str], cl:Client):
    print("\nAdvanced options:\n"
        "Enter \"0\" if you don't want to use advanced options.\n"
        "Enter \"unfollowall\" to automatically unfollow all users that doesn't follow you back.\n"
        "Enter \"user1 user2\" to automatically unfollow only those users (only if they doesn't follow you back).")
    opt = input("Enter an option: ")
    if opt == "0":
        return None
    try:
        following = [(user_id, user.username) for user_id, user in cl.user_following(cl.user_id, amount=0).items()]
    except ChallengeRequired:
        print_er("Error: ChallengeRequired. Solve the captcha in your account.")
    if opt == "unfollowall":
        unfollow = [(user_id, username) for user_id, username in following if username in bad_friends]
    else:
        unfollow = [(user_id, username) for user_id, username in following if username in opt.split()]
    print("Unfollowed:", end=" ")
    for user_id, username in unfollow:
        if cl.user_unfollow(user_id):
            print(username, end=" ")
    return None

def main():
    cl = login()
    print("Who doesn't follow you back on instagram? Dowloading content. "
        "Please wait.\nIt may take a few seconds/minutes depending by the total amount of followers and following.")
    followers_usurname = get_followers_usernames(cl)
    following_usurname = get_following_usernames(cl)
    bad_friends = print_bad_friends(followers_usurname, following_usurname)
    auto_unfollow(bad_friends, cl)
    print("\nThis window will remain open for five minutes to give you time to check the results. You can also close it now.")
    sleep(300)

# Start here
try:
    if not path.exists("./data"):
        makedirs("./data")
except:
    print_er("Error the data folder.")

if __name__ == "__main__":
    main()

