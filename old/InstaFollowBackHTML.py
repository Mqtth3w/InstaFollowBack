'''
    @author Matteo Gianvenuti https://github.com/mqtth3w
    @license MIT License
    This software allow you to find who doesen't follow you back on Instagram
    through HTML parsing of your data dump already downloaded from Instagram.
'''

from bs4 import BeautifulSoup
from time import sleep
from sys import exit as sysexit
from os import makedirs, path

print("InstaFollowBackHTML")
print("Copyright (C) Matteo Gianvenuti. All rights reserved.\n")

def cleanup(txt:str) -> list[str]:
    soup = BeautifulSoup(txt, 'html.parser')
    link_texts = []
    for tag in soup.find_all('a'):
        link_texts.append(tag.text)
    return link_texts

def print_er(error:str):
    print(error)
    sleep(5)
    sysexit(1)

def print_instructions():
    instructions = """
    Instructions for using the software:
    1. On your Instagram account, navigate to Settings, then go to Your Activity and select Download Your Data.
    2. Choose Download or Transfer Your Information. Then, select some of your information.
    3. Select only Followers and Following (under Connections). Afterwards, choose Download to Device (HTML format).
    4. ATTENTION: Data range must be all time. Not last year as is by default.
    5. You will receive a link in your registered email to download your data.
    6. After downloading the data, extract the .zip folder and locate the paths to following.html and followers.html.
       (File names may include underscores or numbers)
       Examples:
       C:/Users/MATTEO/Downloads/mqtth3vv-2024-03-16-html/connections/followers_and_following/following.html
       C:/Users/MATTEO/Downloads/mqtth3vv-2024-03-16-html/connections/followers_and_following/followers_1.html
    """
    print(instructions)

def print_bad_friends(followers:list[str], following:list[str]):
    counter = 0
    for person in following:
        if person not in followers:
            print(person, end=" ")
            counter += 1
    print(f"\nTotal people who don't follow you back: {counter}.")

def main():
    print_instructions()
    FOLLOWING_PATH = input("Path to following file: ")
    try:
        with open(FOLLOWING_PATH, "r", encoding='utf-8') as f1:
            text = f1.read()
            following = cleanup(text)
    except:
        print_er("Error with following path.")
    FOLLOWERS_PATH = input("Path to followers file: ")
    try: 
        with open(FOLLOWERS_PATH, "r", encoding='utf-8') as f2:
            text = f2.read()
            followers = cleanup(text)
    except:
        print_er("Error with followers path.")
    print("\nWho doesn't follow you back on instagram? Loading results, wait.")
    print_bad_friends(followers, following)
    print("\nThis window will remain open for five minutes to give you time to check the results. You can also close it now.")
    sleep(300)
    
    
# Start here
if __name__ == "__main__":
    main()

