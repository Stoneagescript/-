import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import json
import subprocess
import pyautogui
import time
import os
import sys
import requests

class DamageCalculator:
    def __init__(self, parent):
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        # Create labels and entry fields
        phy_attack_entry_label = tk.Label(self.parent, text="物理攻击力:")
        phy_attack_entry_label.pack()
        self.phy_attack_entry = tk.Entry(self.parent)
        self.phy_attack_entry.pack()

        fire_attack_label = tk.Label(self.parent, text="火焰攻击力:")
        fire_attack_label.pack()
        self.fire_attack_entry = tk.Entry(self.parent)
        self.fire_attack_entry.pack()

        freeze_attack_label = tk.Label(self.parent, text="寒冰攻击力:")
        freeze_attack_label.pack()
        self.freeze_attack_entry = tk.Entry(self.parent)
        self.freeze_attack_entry.pack()

        thunder_attack_label = tk.Label(self.parent, text="雷电攻击力:")
        thunder_attack_label.pack()
        self.thunder_attack_entry = tk.Entry(self.parent)
        self.thunder_attack_entry.pack()

        crit_chance_label = tk.Label(self.parent, text="暴击数值:")
        crit_chance_label.pack()
        self.crit_chance_entry = tk.Entry(self.parent)
        self.crit_chance_entry.pack()

        crit_damage_label = tk.Label(self.parent, text="暴击伤害（百分比写成小数）:")
        crit_damage_label.pack()
        self.crit_damage_entry = tk.Entry(self.parent)
        self.crit_damage_entry.pack()

        resistance_label = tk.Label(self.parent, text="抗性总和:")
        resistance_label.pack()
        self.resistance_entry = tk.Entry(self.parent)
        self.resistance_entry.pack()

        health_label = tk.Label(self.parent, text="生命值:")
        health_label.pack()
        self.health_entry = tk.Entry(self.parent)
        self.health_entry.pack()

        # Create calculate button
        calculate_button = tk.Button(self.parent, text="计算最终伤害", command=self.calculate)
        calculate_button.pack()

        # Create label to display the result
        self.damage_label = tk.Label(self.parent, text="最终伤害: ")
        self.damage_label.pack()

        image_path = "logo.png"  # Replace with your image path
        image = Image.open(image_path)
        image = image.resize((250, 250), resample=Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.image_label = tk.Label(self.parent, image=photo)
        self.image_label.image = photo  # Store reference to prevent garbage collection
        self.image_label.pack()


    def calculate(self):
        # Get user input data
        phy_attack = self.phy_attack_entry.get()
        fire_attack = self.fire_attack_entry.get()
        freeze_attack = self.freeze_attack_entry.get()
        thunder_attack = self.thunder_attack_entry.get()
        crit_chance = self.crit_chance_entry.get()
        crit_damage = self.crit_damage_entry.get()
        resistance = self.resistance_entry.get()
        health = self.health_entry.get()

        # Check if any input field is empty
        if not phy_attack or not fire_attack or not freeze_attack or not thunder_attack or not crit_chance or not crit_damage or not resistance or not health:
            messagebox.showwarning("提示", "请提供所有输入数据")
            return 0

        try:
            fire_attack = float(fire_attack)
            thunder_attack = float(thunder_attack)
            phy_attack = float(phy_attack)
            freeze_attack = float(freeze_attack)
            crit_chance = float(crit_chance)
            crit_damage = float(crit_damage)
            resistance = float(resistance)
            health = float(health)
        except ValueError:
            self.damage_label.configure(text="输入数据无效")
            return

        if fire_attack < 0 or thunder_attack < 0 or phy_attack < 0 or freeze_attack < 0 or crit_chance < 0 or crit_damage < 0 or resistance < 0 or health < 0:
            messagebox.showwarning("提示", "输入数据无效")
            return

        freeze_result = 1 if freeze_attack else 0
        fire_result = 1 if fire_attack else 0
        phy_result = 1 if phy_attack else 0
        thunder_result = 1 if thunder_attack else 0



        # Convert other input values to float

        crit_chance = float(crit_chance)
        crit_damage = float(crit_damage)
        resistance = float(resistance)
        health = float(health)

        # Damage calculation formula
        damage = phy_attack * 900 + fire_attack * 900 + freeze_attack * 744 + thunder_attack * 0 + (12.462 * freeze_result +14.4 * phy_result + 15 * fire_result + 0 * thunder_result ) * health + (446.4 * freeze_result + 540 * phy_result + 540 * fire_result) * resistance + 5088 * crit_chance
        final_damage = max(damage, 0) * 2.5 * ((1 - crit_chance / 28212.282) + crit_chance / 28212.282 * (1 + crit_damage))
        simple_damage = final_damage / 1000000


        # Display the result to the user
        self.damage_label.configure(text="一分半伤害: {}M".format(simple_damage))



class MacroTimer:
    def __init__(self, parent):
        self.parent = parent
        self.macro_type = tk.StringVar()  # Define macro_type as an attribute
        self.macro_type.set("keyboard")  # Set default value for macro_type
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.parent)  # Create a frame for the page

        macro_label = ttk.Label(frame, text="宏:")
        macro_label.pack()
        self.macro_entry = ttk.Entry(frame)  # Input field for macro
        self.macro_entry.pack()

        countdown_label = ttk.Label(frame, text="倒计时（小时）:")
        countdown_label.pack()
        self.countdown_entry = ttk.Entry(frame)  # Input field for countdown in hours
        self.countdown_entry.pack()

        self.macro_type.set("keyboard")  # Set default value for macro_type

        keyboard_radio = tk.Radiobutton(
            frame,
            text="键盘宏",
            variable=self.macro_type,  # Use self.macro_type as the variable
            value="keyboard"
        )
        keyboard_radio.pack()

        mouse_radio = tk.Radiobutton(
            frame,
            text="鼠标宏",
            variable=self.macro_type,  # Use self.macro_type as the variable
            value="mouse"
        )
        mouse_radio.pack()

        save_button = ttk.Button(frame, text="保存宏", command=self.save_macro)
        save_button.pack()

        load_button = ttk.Button(frame, text="加载宏", command=self.load_macro)
        load_button.pack()

        start_button = ttk.Button(frame, text="开始", command=self.start_macro)
        start_button.pack()

        stop_button = ttk.Button(frame, text="停止", command=self.stop_macro)
        stop_button.pack()

        frame.pack()

    def save_macro(self):
        # Save the macro to a local file
        macro = self.macro_entry.get()
        if not macro:
            messagebox.showwarning("提示", "请输入宏")
            return

        with open("macro_data.json", "w") as file:
            json.dump(macro, file)
            messagebox.showinfo("提示", "宏已保存")

    def load_macro(self):
        # 弹出文件选择对话框，让用户选择宏文件
        file_path = askopenfilename(filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")])

        if not file_path:
            messagebox.showwarning("提示", "请选择宏文件")
            return

        try:
            with open(file_path, "r") as file:
                macro = file.read()
                # 将加载的宏内容使用在你的应用程序中，例如设置输入字段的文本
                print("加载的宏内容：", macro)
                messagebox.showinfo("提示", "宏已加载")
        except FileNotFoundError:
            messagebox.showwarning("提示", "找不到宏文件")

    def check_network(self):
        try:
            # Use the ping command to check network connectivity
            output = subprocess.check_output(['ping', '-c', '1', 'www.google.com'])
            return True
        except subprocess.CalledProcessError:
            return False

    def shutdown(self):
        # Perform shutdown operation using OS command or other means
        subprocess.call(['shutdown', '-s', '-t', '0'])

    def start_macro(self):
        # Get the macro and countdown values
        macro = self.macro_entry.get()
        hours = self.countdown_entry.get()

        if not macro or not hours:
            messagebox.showwarning("提示", "请输入宏和倒计时")
            return

        try:
            hours = float(hours)
        except ValueError:
            messagebox.showwarning("提示", "无效的倒计时值")
            return

        countdown = int(hours * 3600)  # Convert hours to seconds

        # Execute operations related to macro and countdown
        # ...

        macro_type = self.macro_type.get()  # Access the macro_type instance variable

        # Check network connectivity and perform shutdown operation
        while countdown > 0:
            if not self.check_network():
                self.shutdown()
                break

            # Execute macro operation
            if macro_type == "keyboard":
                pyautogui.typewrite(macro)
            elif macro_type == "mouse":
                pyautogui.click()

            # Execute additional macro operation (keyboard or mouse)
            additional_macro = self.macro_entry.get()
            additional_macro_type = self.macro_type.get()  # Access the macro_type instance variable

            if additional_macro_type == "keyboard":
                pyautogui.typewrite(additional_macro)
            elif additional_macro_type == "mouse":
                pyautogui.click()

            # Decrement countdown by 1 second
            countdown -= 1

            # Wait for 1 second
            time.sleep(1)

    def stop_macro(self):
        # Stop the macro execution or perform necessary actions
        # ...
        pass

class JSONFileManager:
    def __init__(self, parent):
        self.server_url = "http://"  # 服务器url

    def create_widgets(self):
        upload_button = tk.Button(frame, text="上传JSON文件", command=self.upload_json)
        upload_button.pack()

        download_button = tk.Button(frame, text="浏览和下载JSON文件", command=self.download_json)
        download_button.pack()



    def upload_json(self):
        file_path = askopenfilename(filetypes=[("JSON Files", "*.json")])
        if not file_path:
            messagebox.showwarning("提示", "请选择要上传的JSON文件")
            return

        max_file_size = 1 * 1024 * 1024  # 1MB
        file_size = os.path.getsize(file_path)
        if file_size > max_file_size:
            messagebox.showwarning("提示", "文件大小超过1MB的限制，请选择较小的文件")
            return

        with open(file_path, "r") as file:
            json_data = file.read()

        upload_url = f"{self.server_url}/upload"
        response = requests.post(upload_url, data=json_data)

        if response.status_code == 200:
            messagebox.showinfo("提示", "文件上传成功")
        else:
            messagebox.showwarning("提示", "文件上传失败")

    def download_json(self):
        response = requests.get(f"{self.server_url}/json_files")

        if response.status_code == 200:
            file_list = response.json()  # Assuming the server returns a JSON array of file names
            if not file_list:
                messagebox.showinfo("提示", "服务器上没有可用的JSON文件")
                return

            selected_file = tk.StringVar()
            selected_file.set(file_list[0])  # Default selection

            # Create a file selection dialog
            dialog = tk.OptionMenu(root, selected_file, *file_list)
            dialog.pack()

            def download_selected_file():
                selected_file_name = selected_file.get()
                response = requests.get(f"{self.server_url}/download/{selected_file_name}")

                if response.status_code == 200:
                    save_path = asksaveasfilename(defaultextension=".json",
                                                  filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])

                    if save_path:
                        with open(save_path, "w") as file:
                            file.write(response.text)
                            messagebox.showinfo("提示", "JSON文件已下载成功")
                    else:
                        messagebox.showwarning("提示", "请选择保存路径")
                else:
                    messagebox.showwarning("提示", "无法下载选定的JSON文件")

            download_button = tk.Button(root, text="下载选定文件", command=download_selected_file)
            download_button.pack()
        else:
            messagebox.showwarning("提示", "无法获取服务器上的JSON文件列表")



if __name__ == "__main__":
    root = tk.Tk()
    root.title("幻塔工具")

    # Create an instance of the JSONFileManager class

    notebook = ttk.Notebook(root)
    notebook.pack()

    damage_calculator_frame = ttk.Frame(notebook)
    damage_calculator = DamageCalculator(damage_calculator_frame)
    damage_calculator_frame.pack()
    notebook.add(damage_calculator_frame, text="固伤计算器")

    macro_timer_frame = ttk.Frame(notebook)
    macro_timer = MacroTimer(macro_timer_frame)
    macro_timer_frame.pack()
    notebook.add(macro_timer_frame, text="宏计时器")

    root.mainloop()



