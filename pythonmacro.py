import os
import webbrowser
from pynput import keyboard

LINKS = {
    "1": "https://classroom.google.com/u/1/c/ODI0ODM4MzczODI0",
    "2": "https://classroom.google.com/u/1/c/ODI0NTUzNjAzMzU2",
    "3": "https://classroom.google.com/u/1/c/ODI1MDU1NTg4Mjk3",
}

def get_chrome_browser():
    # Try to use Google Chrome explicitly across common OS locations.
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "google-chrome",
        "google-chrome-stable",
        "chromium",
        "chromium-browser",
    ]

    for path in chrome_paths:
        if os.path.isabs(path):
            if os.path.exists(path):
                webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(path))
                return webbrowser.get("chrome")
        else:
            try:
                return webbrowser.get(path)
            except webbrowser.Error:
                continue

    return webbrowser

CHROME = get_chrome_browser()

def on_press(key):
    try:
        key_char = key.char
        print(f"Alphanumeric key {key_char} pressed")
        url = LINKS.get(key_char)
        if url:
            CHROME.open_new_tab(url)
    except AttributeError:
        print(f'Special key {key} pressed')

def on_release(key):
    print(f'{key} released')
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
