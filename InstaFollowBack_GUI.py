'''
    @author Matteo Gianvenuti https://github.com/mqtth3w
    @license GPL-3.0
    This software allow you to connect to instagram with login (2FA supported)
    and automatically download following and followers to know who doesen't follow you back.
    Optionally you can automatically unfollow them.
'''

import tkinter as tk
from tkinter import messagebox
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired
import json, os
from Crypto.Cipher import AES
#from Crypto.Util.Padding import pad, unpad
# To see your ip "https://api.ipify.org/"
#print("InstaFollowBack")
#print("Copyright (C) Matteo Gianvenuti. All rights reserved.\n")

# Change this password!!!
KEY_32 = b"mqtt1507IlRe2000h3vvGianve23nuti"
# Is better to use the input so don't save the password in this script!!!
#KEY_32 = input("Password?").encode("utf-8")

def pad(data: bytes, blockSize: int) -> bytes:
    padLen = blockSize - (len(data) % blockSize)
    return data + (bytes([padLen]) * padLen)

def unpad(data: bytes, blockSize: int) -> bytes:
    return data[:-ord(data[-1:])]

def encrypt_AES256(plaintext: str) -> bytes:
    plaintext = plaintext.encode()
    cipher = AES.new(KEY_32, AES.MODE_ECB)
    return cipher.encrypt(pad(plaintext, 16))

def decrypt_AES256(ciphertext: bytes) -> str:
    cipher = AES.new(KEY_32, AES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)
    return unpad(plaintext, 16).decode()

def print_er(error: str):
    messagebox.showerror("Error", error)
    
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
        print_er("Error loading session data.")
    return {}

def store_settings(settings):
    ciphertext = encrypt_AES256(json.dumps(settings))
    try:
        with open("./data/alpha.txt", "wb") as f:
            f.write(ciphertext)
    except:
        print_er("Error saving session data.")

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
    return "", ""

def store_user(user, passw):
    ciphertext = encrypt_AES256(user + " " + passw)
    try:
        with open("./data/beta.txt", "wb") as f:
            f.write(ciphertext)
    except:
        print("Error saving login data.")

def load_session() -> Client:
    cl = Client()
    cl.delay_range = [1, 3]
    settings = load_settings()
    user, passw = load_user()
    if settings and user and passw:
        try:
            cl.set_settings(settings)
            cl.login(user, passw)
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                old_session = cl.get_settings()
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])
                try:
                    cl.login(user, passw)
                except:
                    cl = None
        except:
            cl = None
    else:
        cl = None
    return cl

def get_followers_usernames(amount: int = 0) -> list[str]:
    global cl
    try:
        followers = cl.user_followers(cl.user_id, amount=amount)
    except ChallengeRequired:
        print_er("Error: ChallengeRequired. Solve the captcha in your account.")
    return [user.username for user in followers.values()]

def get_following_usernames(amount: int = 0) -> list[str]:
    global cl
    try:
        following = cl.user_following(cl.user_id, amount=amount)
    except ChallengeRequired:
        print_er("Error: ChallengeRequired. Solve the captcha in your account.")
    return [user.username for user in following.values()]

def print_bad_friends(followers: list[str], following: list[str]) -> list[str]:
    counter = 0
    bad_friends = []
    for person in following:
        if person not in followers:
            bad_friends.append(person)
            counter += 1
    result_text.insert("end", f"\nTotal people who don't follow you back: {counter}\n")
    return bad_friends

def auto_unfollow(bad_friends: list[str]):
    global cl
    opt = unfollow_option.get()
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
    for user_id, username in unfollow:
        if cl.user_unfollow(user_id):
            result_text.insert("end", f"Unfollowed: {username}\n")
    return None

def start_check():
    global cl
    result_text.insert("end", "Who doesn't follow you back on Instagram? Downloading content. "
                             "Please wait.\nIt may take a few seconds/minutes depending on the total amount of followers and following.\n")
    followers_username = get_followers_usernames()
    following_username = get_following_usernames()
    bad_friends = print_bad_friends(followers_username, following_username)
    auto_unfollow(bad_friends)
    result_text.insert("end", "\nThis window will remain open for five minutes to give you time to check the results. You can also close it now.")
    root.after(300000, root.quit)

def print_instructions():
    instructions = """
    Instructions for using the software:
    1. Insert username and password (and 2FA if enabled) to login.
    2. Wait some time for Instagram login and content download (following&followers).
    3. After you will see who doesn't follow you back.
    4. Optionally you can unfollow them.
    5. .
    """
    new_window = tk.Toplevel(root)
    new_window.title("Info")
    label = tk.Label(new_window, text=instructions)
    label.pack()

def main_window():
    global root, result_text, unfollow_option
    
    if not logged:
        root = tk.Tk()
        root.title("InstaFollowBack by Mqtth3w")
        root.resizable(False, False)
    
    for widget in root.winfo_children():
        widget.destroy()

    result_text = tk.Text(root, width=80, height=20)
    result_text.grid(row=0, column=0, columnspan=3)

    tk.Label(root, text="Unfollow Option:").grid(row=1, column=0)
    unfollow_option = tk.StringVar()
    unfollow_option.set("0")
    tk.Radiobutton(root, text="No Unfollow", variable=unfollow_option, value="0").grid(row=1, column=1)
    tk.Radiobutton(root, text="Unfollow All", variable=unfollow_option, value="unfollowall").grid(row=2, column=1)

    start_check()
    
    if not logged:
        root.mainloop()
    
def handle_login():
    user = username_entry.get()
    passw = password_entry.get()
    auth_code = twofa_entry.get()
    if user and passw:
        try:
            global cl, logged
            cl.login(user, passw, verification_code=auth_code)
            store_settings(cl.get_settings())
            store_user(user, passw)
            logged = True
            main_window()
        except:
            print_er("Wrong credentials, missing internet connection or too much attempts.")
    else:
        print_er("Missing username or/and password.")

def login_window():
    global cl, root, username_entry, password_entry, twofa_entry

    cl = Client()
    cl.delay_range = [1, 3]
    
    root = tk.Tk()
    root.title("InstaFollowBack by Mqtth3w")
    root.resizable(False, False)
       
    tk.Label(root, text="Instagram Username:").grid(row=0, column=0)
    username_entry = tk.Entry(root, width=50)
    username_entry.grid(row=0, column=1)

    tk.Label(root, text="Instagram Password:").grid(row=1, column=0)
    password_entry = tk.Entry(root, width=50, show="*")
    password_entry.grid(row=1, column=1)

    tk.Label(root, text="2FA Code:").grid(row=2, column=0)
    twofa_entry = tk.Entry(root, width=50)
    twofa_entry.grid(row=2, column=1)

    tk.Button(root, text="Login", command=handle_login).grid(row=3, column=1)
    
    print_instructions()

    root.mainloop()

# Start here
if not os.path.exists("./data"):
    os.makedirs("./data")
logged = False
cl = load_session()
if cl:
    main_window()
else:
    login_window()



