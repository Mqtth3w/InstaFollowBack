# InstaFollowBack

Discover who doesn't follow you back on Instagram and optionally auto-unfollow them.

## InstaFollowBackHTML_GUI
It works offline with manually downloaded data (the download require just 5min). No Instagram login required. I personally prefer this version.

### Requirements
bs4, tkinter.

### Usage
 1. On your Instagram account, navigate to Settings, then go to Your Activity and select Download Your Data.
 2. Choose Download or Transfer Your Information. Then, select some of your information.
 3. Select only Followers and Following (under Connections). Afterwards, choose Download to Device (HTML format).
 4. You will receive a link in your registered email to download your data.
 5. After downloading the data, extract the .zip folder and locate (through the "Browse" option) the paths to following.html and followers.html.

## InstaFollowBack_GUI
(this version is not yet completed, I have to test)
Automatically logs in (if you already logged) to Instagram and downloads data to check who doesn't follow you back. It also allows you to automatically unfollow those individuals.
All data is saved offline on your computer, encrypted with 256-bit AES, ensuring their safety. It's necessary to save the session so that you won't have to log in with your credentials every time, similar to the Instagram app. If you log in many times with your credentials, Instagram will think you are a bot. You should look at the code and change the encryption password. 
If you use InstaFollowBack several times a day, Instagram may suspect you are a bot and will ask you to solve a captcha. Simply solve it. It's safe. I have used it more than 20 times a day during testing (for the no GUI version), but it's always better not to abuse this feature. It's a good idea to consistently use the same IP address (for at least eight hours). Alternatively, you can use InstaFollowBackHTML anytime you want because it works offline.

### Requirements
instagrapi, pillow, pycryptodome, tkinter.

### Usage
 0. If the session is already saved wait for login.
 1. Insert username and password (and 2FA if enabled) to login.
 2. Wait some time for Instagram login and content download (following&followers).
 3. After you will see who doesn't follow you back.
 4. Optionally you can unfollow them.

## old
This folder contain an equal version but without the GUI. So doesn't require tkinter.
