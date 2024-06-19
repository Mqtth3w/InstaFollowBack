'''
    @author Matteo Gianvenuti https://github.com/mqtth3w
    @license MIT License
    This software allow you to find who doesen't follow you back on Instagram
    through HTML parsing of your data dump already downloaded from Instagram.
'''

import tkinter as tk
from bs4 import BeautifulSoup

#print("InstaFollowBack")
#print("Copyright (C) Matteo Gianvenuti. All rights reserved.\n")

def cleanup(txt: str) -> list[str]:
    soup = BeautifulSoup(txt, 'html.parser')
    link_texts = [tag.text for tag in soup.find_all('a')]
    return link_texts

def main(following_path, followers_path):
    try:
        with open(following_path, "r", encoding='utf-8') as f1:
            text = f1.read()
            following = cleanup(text)
    except Exception as e:
        messagebox.showerror("Error", f"Error with following path: {e}")
        return

    try:
        with open(followers_path, "r", encoding='utf-8') as f2:
            text = f2.read()
            followers = cleanup(text)
    except Exception as e:
        messagebox.showerror("Error", f"Error with followers path: {e}")
        return

    result_text.delete(1.0, "end")
    result_text.insert("end", "Who doesn't follow you back on Instagram?\n\n")
    
    counter = 0
    for person in following:
        if person not in followers:
            result_text.insert("end", person + "\n")
            counter += 1

    result_text.insert("end", f"\nTotal people who don't follow you back: {counter}\n")
    result_text.insert("end", "\nThis window will remain open for five minutes to give you time to check the results. You can also close it now.")
    result_text.update()
    root.after(300000, root.quit)

def select_file(entry):
    selected_file = filedialog.askopenfilename()
    if selected_file:
        entry.delete(0, 'end')
        entry.insert(0, selected_file)

def print_instructions():
    instructions = """
    Instructions for using the software:
    1. On your Instagram account, navigate to Settings, then go to Your Activity and select Download Your Data.
    2. Choose Download or Transfer Your Information. Then, select some of your information.
    3. Select only Followers and Following (under Connections). Afterwards, choose Download to Device (HTML format).
    4. You will receive a link in your registered email to download your data.
    5. After downloading the data, extract the .zip folder and locate (through the "Browse" option) the paths to following.html and followers.html.
       (File names may include underscores or numbers)
       Examples:
       C:/Users/MATTEO/Downloads/mqtth3vv-2024-03-16-html/connections/followers_and_following/following.html
       C:/Users/MATTEO/Downloads/mqtth3vv-2024-03-16-html/connections/followers_and_following/followers_1.html
    """
    new_window = tk.Toplevel(root)
    new_window.title("Info")
    label = tk.Label(new_window, text=instructions)
    label.pack()

def start_gui():
    global root, result_text
    root = tk.Tk()
    root.title("InstaFollowBackHTML by Mqtth3w")
    root.resizable(False, False)
    
    tk.Label(root, text="Path to following file:").grid(row=0, column=0)
    following_entry = tk.Entry(root, width=50)
    following_entry.grid(row=0, column=1)
    tk.Button(root, text="Browse", command=lambda: select_file(following_entry)).grid(row=0, column=2)

    tk.Label(root, text="Path to followers file:").grid(row=1, column=0)
    followers_entry = tk.Entry(root, width=50)
    followers_entry.grid(row=1, column=1)
    tk.Button(root, text="Browse", command=lambda: select_file(followers_entry)).grid(row=1, column=2)

    tk.Button(root, text="Check", command=lambda: main(following_entry.get(), followers_entry.get())).grid(row=2, column=1)

    result_text = tk.Text(root, width=80, height=20)
    result_text.grid(row=3, column=0, columnspan=3)

    print_instructions()

    root.mainloop()

# Start here
if __name__ == "__main__":
    start_gui()
