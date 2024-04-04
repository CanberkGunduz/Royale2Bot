import sys
import threading
import tkinter as tk
from io import BytesIO
from tkinter import messagebox

import mss
import numpy as np
import pyautogui as p
import keyboard
import cv2
import time
import requests as requests
import win32api
import win32con
from PIL import ImageGrab
import win32gui
import os
from datetime import datetime
import base64

p.useImageNotFoundException()

# Disable fail-safe
p.FAILSAFE = True

width = 1366
height = 768

class Mobile2Bot:
    fish_sens = 0.4
    bait_sens = 0.8
    bait_type_int = 0
    channel_number = 1
    character_number = 3
    inventory_count = 6
    auto_login = 1
    INVENTORY_FULL = False
    pelerin_var = False
    altin_yuzuk_var = False
    madalyon_var = False
    eldiven_var = False

    def __init__(self):
        # self.check_date()
        self.img_dict = self.read_images_in_folder()
        self.bait_type = "Hamur"
        self.is_running = False  # Flag to control the game cycle
        self.game_cycle_thread = None
        self.party_detection_running = False
        self.inventory_count = 6
        self.total_count = 0
        self.caught_count = 0
        self.valuable_count = 0
        self.delay_time = 0.8  # Default delay time



    def check_date(self):
        current_time = time.time()
        # print(current_time)
        target = 1807690193
        if current_time > target:
            root = tk.Tk()
            root.overrideredirect(True)
            root.withdraw()
            messagebox.showerror("Error", "Trial has ended.")
            root.destroy()
            sys.exit()

    def start_game_cycle(self):
        if not self.is_running:
            self.is_running = True
            self.starting_time = time.time()

            # # Create a thread to start the game
            # game_thread = threading.Thread(target=self.open_game)
            # game_thread.start()
            # self.open_game()

            self.game_cycle_thread = threading.Thread(target=self.game_cycle)
            self.mouse_click("left", 130, 15)
            self.game_cycle_thread.start()



    def stop_game_cycle(self):
        # if not self.check_bluestacks_is_open():
        #     self.open_game()
        #     return
        self.is_running = False
        # self.game_cycle_thread.join()
        # self.stop_party_detection()
        print("bot stopped")
        currentDateAndTime = datetime.now()
        with open(f"session_{self.delay_time}.txt", "a") as session_file:
            session_file.write(f"total tries: {self.total_count}\ncaught: {self.caught_count}\nvaluable: {self.valuable_count}\ncurrent date: {currentDateAndTime}\n-----------------------\n")



    def send_notification(self,message,send_screenshot=False):
        files=None
        if send_screenshot:
            # Take a screenshot using pyautogui
            screenshot = p.screenshot()

            # Convert the screenshot to BytesIO object
            screenshot_io = BytesIO()
            screenshot.save(screenshot_io, format='PNG')
            screenshot_io.seek(0)
            # Attach the screenshot to the request
            files = {'attachment': ('screenshot.png', screenshot_io, 'image/png')}

        requests.post("https://api.pushover.net/1/messages.json", data={

            "token": "a9qutshv8twt4tchs7rvnkqeofhgfk", # canberk
            # "token": "adyvnj3co61qo45opertrtyds6k8ee", # baris
            "user": "uofkgkwu6twdiptnjdi9kqkx616eqr",  # canberk
            # "user": "ugy4145hw2trh1kkwnw3w2ap3eegcn", # baris
            "message": message
        },files=files)

    def game_cycle(self):
        try:
            while self.is_running:
                while (not self.check_bluestacks_is_open()) or (not self.check_game_is_open()):
                    print("Opening the game...")
                    self.open_game()

                inv_full = self.check_inventory_full_by_empty_slots()
                print("Inventory full: ",inv_full)
                # if inv_full:
                #     self.open_fish()
                #     if self.check_inventory_full_by_empty_slots():
                #         self.send_notification("Inventory is full.",send_screenshot=True)
                #         self.stop_game_cycle()
                #         self.close_game()

                print("Game cycle is working")
                time.sleep(1)
                self.use_bait_new()
                # time.sleep(1)
                self.moving_rod_throw()
                time.sleep(3)
                self.fish_detector()
        except Exception as e:
            with open("log.txt", "a") as log_file:
                log_file.write(str(e))

    def mouse_click(self, button, x, y, delay=0.1):
        p.moveTo(x, y)
        time.sleep(0.3)
        p.mouseDown(button=button)
        time.sleep(delay)
        p.mouseUp(button=button)

    def mouse_drag(self, button, x1, y1, x2, y2,delay=0.1,move_speed=0.5):
        p.moveTo(x1, y1)
        time.sleep(delay)
        p.mouseDown(button=button)
        time.sleep(delay)
        p.moveTo(x2, y2, move_speed)
        time.sleep(delay)
        p.mouseUp(button=button)

    def mouse_carry(self, button, x1, y1, x2, y2, x3, y3, delay=0.1, move_speed=0.1):
        p.moveTo(x1, y1)
        time.sleep(delay)
        p.mouseDown(button=button)
        time.sleep(delay)
        p.moveTo(x2, y2, move_speed)
        time.sleep(0.7)
        p.moveTo(x3, y3)
        time.sleep(delay)
        p.mouseUp(button=button)

    def key_press(self, key, delay=0.3):
        time.sleep(0.1)
        keyboard.press(key)
        time.sleep(delay)
        keyboard.release(key)

    def moving_rod_throw(self):
        p.moveTo(300, 620)
        time.sleep(0.1)
        p.mouseDown(button="left")
        time.sleep(0.1)
        p.moveTo(300, 0)
        time.sleep(0.2)
        self.key_press("space")
        time.sleep(0.2)
        p.mouseUp(button="left")

    def choose_character(self):
        self.mouse_click("left",260,160+90*(self.character_number-1))
        time.sleep(0.5)
        self.mouse_click("left",1000,590)

    def start_bait_thread(self,func):
        if func == 0:
            self.bait_thread = threading.Thread(target=self.buy_bait)
        elif func == 1:
            self.bait_thread = threading.Thread(target=self.organize_bait)
        self.focus_game()
        self.bait_thread.start()
    def buy_bait(self):
        self.mouse_click("left",200,10)
        quantity = int(self.fish_quantity_spinbox.get())
        self.mouse_click("left",425,125)
        for _ in range(quantity*4):
            self.mouse_click("left",615,500)
        self.mouse_click("left",445,70)
        print("Baits bought...")

    def organize_bait(self):
        self.mouse_click("left",200,10)
        inv_coords = [(845, 150), (935, 150), (845, 180), (935, 180)]
        vault_coord = self.vault_coord
        inv_coord = self.inv_coordinates
        for index in range(12):
            self.mouse_carry("left", inv_coord[index][0], inv_coord[index][1],
                             inv_coords[self.inventory_count-1][0],inv_coords[self.inventory_count-1][1],
                             inv_coord[-index-1][0], inv_coord[-index-1][1])
            self.mouse_click("left",845,150)
        else:
            self.mouse_click("left", inv_coords[self.inventory_count-1][0],inv_coords[self.inventory_count-1][1])
            print("Baits are organized...")

    def open_inventory(self):
        self.mouse_click("left",890,80)
        inv_num = self.inventory_count
        inv_x, inv_y = 850 + (inv_num - 1) * 60, 260
        time.sleep(1)
        self.mouse_click("left", inv_x, inv_y)

    def is_inventory_open(self):
        time.sleep(1)
        detected,_,_ = self.locate_image_rgb_fs(self.img_dict["Inventory_text"])
        if not detected:
            self.open_inventory()
            return self.is_inventory_open()
        return True

    def use_bait_new(self):
        self.open_inventory()
        wallow_det, wallow_pos, _ = self.locate_image_rgb_fs(self.img_dict["Wallow"],(820, 280, 1180, 640), self.bait_sens)

        if wallow_det:
            self.mouse_click("left", wallow_pos[0] + 10 + 820, wallow_pos[1] + 10 + 280)
            time.sleep(0.1)
            self.mouse_click("left", 710, 590)
            # self.mouse_click("left",710,590)
            self.mouse_click("left", 1160, 210)
        else:

            detected, pos, located_precision = self.locate_image_rgb_fs(self.img_dict[self.bait_type], (820, 280, 1180, 640), self.bait_sens)
            if detected:
                self.mouse_click("left", pos[0] + 10 + 820, pos[1] + 10 + 280)
                time.sleep(0.1)
                self.mouse_click("left", 710,590)
                # self.mouse_click("left",710,590)
                self.mouse_click("left",1160,210)
            else:
                print("no bait left")
                self.stop_game_cycle()

    def rod_interact(self):
        self.key_press("space")

    def rod_interact_background(self):
        hwnd = win32gui.FindWindow(None, "BlueStacks App Player")
        print(hwnd)
        win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_SPACE, 0)
        # win32gui.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_SPACE, 0)

    def fish_detector(self):
        detection_threshold = 100
        key_to_press = 'space'
        count=0

        """
        Detects a red object within a specified screen area and simulates a key press when the object disappears (indicating it's time to 'get the fish').

        Parameters:
        - monitor_area: A dictionary with 'top', 'left', 'width', and 'height' keys defining the screen area to monitor.
        - lower_red_hsv: The lower bound of the HSV values to detect the red object.
        - upper_red_hsv: The upper bound of the HSV values to detect the red object.
        - detection_threshold: The threshold for detecting a significant change in red object presence.
        - key_to_press: The key to simulate pressing when the red object is detected to disappear.
        """
        with mss.mss() as sct:
            print("Monitoring for red object. Press Ctrl+C to stop.")
            try:
                while self.is_running:
                    # Capture the specified area of the screen
                    img = np.array(sct.grab({'top': 80, 'left': 460, 'width': 240, 'height': 100}))

                    # Convert the image from BGR to HSV
                    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

                    # Create a mask that only includes pixels within the specified red HSV range
                    mask = cv2.inRange(hsv_img, (0, 169, 157), (10, 189, 237))

                    # Use the mask to isolate the red parts of the image
                    # result_img = cv2.bitwise_and(img, img, mask=mask)

                    # Save the original and masked images for inspection
                    # cv2.imwrite('original_image.jpg', img)
                    # cv2.imwrite('masked_image.jpg', result_img)

                    # Sum the values in the mask to determine the amount of red detected
                    red_detected = np.sum(mask)
                    # print(red_detected)

                    # Check if the red object is detected based on the threshold
                    if red_detected < detection_threshold:
                        count+=1
                        if count>=4:
                            print("Red object possibly underwater, fetching the rod!")
                            time.sleep(1)
                            self.key_press("space")  # Simulate the key press to fetch the rod
                            self.key_press("space")  # Simulate the key press to fetch the rod
                            time.sleep(1)  # Wait a bit before continuing to monitor
                            break
                    else:
                        count=0

                    time.sleep(0.2)  # Short delay to avoid excessive CPU usage
            except KeyboardInterrupt:
                print("Stopped monitoring.")

    def open_fish(self):
        inv_coords = [(845, 150),(935, 150),(845, 180),(935, 180)]

        for i in range(self.inventory_count):

            self.mouse_click("left", inv_coords[i][0], inv_coords[i][1])
            x,x_gap,y,y_gap = 800,33,222,32
            inventory_coords = [(x+i*x_gap,y+j*y_gap) for i in range(6) for j in range(7)]

            for coords in inventory_coords:
                bbox = (coords[0]-x_gap//2-10,coords[1]-y_gap//2-10,coords[0]+x_gap//2+10,coords[1]+y_gap//2+10)
                if self.locate_image_rgb_fs(self.img_dict["altin_balik"],bbox)[0]:
                    continue

                self.mouse_click("right", coords[0], coords[1])


    def check_inventory_full_by_empty_slots(self):
        detected, _, _= self.locate_image_rgb_fs(self.img_dict["Empty_slot"],(815, 280, 1185, 650),0.7)
        if not detected:
            return True

    def check_bluestacks_is_open(self):
        bluestacks_is_open = None
        # Get the window handle (replace 'Your Window Title' with the actual window title)
        window_title = "BlueStacks App Player"
        hwnd = win32gui.FindWindow(None, window_title)

        if hwnd == 0:
            print('Window not found. (Check bluestacks)')
            bluestacks_is_open=False
        else:
            print("Bluestacks is open")
            bluestacks_is_open=True
        return bluestacks_is_open

    def check_game_is_open(self):
        game_is_open = self.locate_image_rgb_fs(self.img_dict["Helmet_logo"],(0,0,90,180))[0]
        print("Game is open:",game_is_open)
        return game_is_open

    def check_server_screen_is_open(self):
        server_screen_is_open = self.locate_image_rgb_fs(self.img_dict["Choose_channel"])[0]
        return server_screen_is_open

    def check_launch_screen_logo(self):
        launch_screen_logo = self.locate_image_rgb_fs(self.img_dict["Launch_screen_logo"])[0]
        return launch_screen_logo

    def check_game_freeze(self,capture_interval=5, tolerance=1):

        """
        Periodically captures the screen and compares it to the previous capture to assess if the screen is frozen.

        Parameters:
        - capture_interval: The time interval (in seconds) between screen captures.
        - tolerance: The tolerance level for changes in the pixel values to consider the screen as not frozen.
                     This accounts for minor fluctuations that might not indicate the screen is genuinely frozen.
        """
        with mss.mss() as sct:
            # Capture the initial screen state
            monitor = sct.monitors[1]  # Default to primary monitor
            prev_capture = np.array(sct.grab(monitor))

            try:
                while True:
                    time.sleep(capture_interval)  # Wait for the specified interval
                    # Capture the current screen state
                    current_capture = np.array(sct.grab(monitor))

                    # Compare the current capture to the previous one
                    if np.sum(np.abs(current_capture - prev_capture)) <= tolerance:
                        print("The screen might be frozen.")
                    else:
                        print("The screen is not frozen.")

                    # Update the previous capture
                    prev_capture = current_capture
            except KeyboardInterrupt:
                print("Stopped monitoring.")


    def focus_game(self):
        self.mouse_click("left",450,15)

    def close_game(self):
        self.mouse_click("left", 1250, 700)
        self.mouse_click("left", 850, 90)

    def close_bluestacks_x(self):
        hwnd= win32gui.FindWindow(None, 'BlueStacks X')
        win32gui.SendMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        self.mouse_click("left",1595,77)
        self.mouse_click("left",1595,77)

    def find_game_logo_on_bluestacks_and_click(self):
        _, pos, _ = self.locate_image_rgb_fs(self.img_dict["Game_logo_bluestacks"])  # game logo on bluestacks
        self.mouse_click("left", pos[0]+20, pos[1]+20)

    def find_game_logo_on_desktop_and_click(self):
        _, pos, _ = self.locate_image_rgb_fs(self.img_dict["Game_logo_desktop"])  # game logo on bluestacks
        self.mouse_click("left", pos[0]+10, pos[1]+10)
        self.key_press("enter")


    def connect_to_game(self):
        connect_button_pos = self.locate_image_rgb_fs(self.img_dict["Connect_button"])[1]
        x,y=connect_button_pos[0], connect_button_pos[1]
        self.mouse_click("left",x,y)
        connection_check_count = 0
        while not self.locate_image_rgb_fs(self.img_dict["Select_character"])[0]:
            connection_check_count+=1
            time.sleep(0.5)
            if connection_check_count>=50:
                print("Could not connect...")
                print("Closing the game...")
                self.close_game()
                return False
        else:
            return True

    def open_game(self,retry_count=0):
        if self.check_bluestacks_is_open() and not self.check_game_is_open():
            self.find_game_logo_on_bluestacks_and_click()
            time.sleep(10)
        else:
            while not self.check_bluestacks_is_open():
                self.find_game_logo_on_desktop_and_click()
                time.sleep(10)
                print("Desktop logo clicked and waited 10 seconds.")
            else:
                print("Trying to close bluestacks x")
                self.close_bluestacks_x()
        self.focus_game()
        launch_screen_counter=0
        while launch_screen_counter<30:
            time.sleep(2)
            launch_screen_counter+=1
            if self.check_launch_screen_logo():
                print("Launch screen logo detected.")
                time.sleep(5)
            if self.check_server_screen_is_open():
                break
        else:
            if self.locate_image_rgb_fs(self.img_dict["f8_games"])[0]:
                print("Stuck on initial launch...")
                print("Restarting...")
                self.close_game()
                return
        if self.check_server_screen_is_open():
            self.choose_server()
        else:
            print("Something went wrong while launching the game")
            self.close_game()
            return
        connection_successful = self.connect_to_game()
        if connection_successful:
            self.choose_character()
            self.mouse_click("left",1010,600) # position of start button
            self.set_ui()
        else:
            retry_count+=1
            if retry_count==4:
                self.send_notification("Could not start the game",True)
                self.stop_game_cycle()
            else:
                self.open_game(retry_count)



    def set_ui(self):
        while not self.locate_image_rgb_fs(self.img_dict["Hand_pick_logo"])[0]: # signaling the game is open
            time.sleep(1)
        else:
            self.mouse_drag("left", 400, 50, 640, 300, 0.1, 3)
        self.open_inventory()

    def choose_server(self):
        ch_num= self.channel_number-1
        ch_coords = [(600 + i * 200, 300 + j * 40) for j in range(3) for i in range(2)]
        print("Connecting to channel:",ch_num)
        self.mouse_click("left", ch_coords[ch_num][0], ch_coords[ch_num][1])

    def resize_window(self):

        # Get the window handle (replace 'Your Window Title' with the actual window title)
        window_title = "BlueStacks App Player"
        hwnd = win32gui.FindWindow(None, window_title)

        if hwnd != 0:
            # Get the current window position and size
            _, _, current_width, current_height = win32gui.GetClientRect(hwnd)
            _, _, _, _ = win32gui.GetWindowRect(hwnd)

            # Calculate the desired new width and height
            new_width = 1260
            new_height = 710
            # Set the new window size
            win32gui.SetWindowPos(hwnd, 0, 0, 0, new_width, new_height, 0x0000)  # SWP_NOSIZE flag

        else:
            print('Window not found. (Resize)')

    def create_gui(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.title('Royale2 Bot')

        # Set the position of the window
        self.root.geometry("+10+400")
        # Set window attributes to always stay on top but not focused
        self.root.attributes("-topmost", True)
        self.root.attributes("-toolwindow", True)

        # Create and place the UI components
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        row2_frame = tk.Frame(self.root)
        row2_frame.pack(pady=10)

        start_button = tk.Button(button_frame, text='Start', command=self.start_game_cycle)
        start_button.pack(side='left', padx=10)

        stop_button = tk.Button(button_frame, text='Stop', command=self.stop_game_cycle)
        stop_button.pack(side='left', padx=10)

        bait_menu_button = tk.Button(button_frame, text='Bait', command=self.open_bait_window)
        bait_menu_button.pack(side='left',padx=10)

        # trade_button = tk.Button(button_frame, text='Trade', command=self.trade)
        # trade_button.pack(side='left', padx=10)


        # # Char Slot label and value
        # char_slot_label = tk.Label(button_frame, text='Char Slot: ')
        # char_slot_label.pack(side='left')
        #
        # char_slot_value_label = tk.Label(button_frame, text=str(self.char_slot))
        # char_slot_value_label.pack(side='left')
        #
        # # Function to update the char_slot value
        # def update_char_slot(value):
        #     self.char_slot += value
        #     char_slot_value_label.config(text=str(self.char_slot))
        #
        # # Up arrow button to increase char_slot value
        # up_arrow_button = tk.Button(button_frame, text='▲', command=lambda: update_char_slot(1))
        # up_arrow_button.pack(side='left')
        #
        # # Down arrow button to decrease char_slot value
        # down_arrow_button = tk.Button(button_frame, text='▼', command=lambda: update_char_slot(-1))
        # down_arrow_button.pack(side='left')

        # Create a frame for delay time setting
        delay_frame = tk.Frame(self.root)
        delay_frame.pack(pady=10)

        # Delay time label and entry
        delay_label = tk.Label(delay_frame, text='Delay Time:')
        delay_label.pack(side='left', padx=10)

        delay_entry = tk.Entry(delay_frame, textvariable=tk.StringVar(value=str(self.delay_time)), width=5)
        delay_entry.pack(side='left', padx=10)

        # Function to update the delay time
        def update_delay_time():
            try:
                self.delay_time = float(delay_entry.get())
                print("new delay:", self.delay_time)
            except ValueError:
                messagebox.showerror("Error", "Invalid delay time. Please enter a valid numerical value.")

        # Update button to update the delay time
        update_delay_button = tk.Button(delay_frame, text='Update', command=update_delay_time)
        update_delay_button.pack(side='left')

        resize_button = tk.Button(row2_frame, text='Resize', command=self.resize_window)
        resize_button.pack(side="left", padx=10)

        set_sensitivity_button = tk.Button(row2_frame, text='Config', command=self.open_config_window)
        set_sensitivity_button.pack(side='left', padx=10)

        # Create a frame for bait type selection
        bait_frame = tk.Frame(self.root)
        bait_frame.pack(pady=10)

        # Bait type radio buttons
        bait_type_label = tk.Label(bait_frame, text='Bait Type:')
        bait_type_label.pack(side='left', padx=10)

        bait_type_var = tk.IntVar(value=self.bait_type_int)

        worm_button = tk.Radiobutton(bait_frame, text='Worm', variable=bait_type_var, value=0,
                                     command=lambda: self.update_bait_type(0))
        worm_button.pack(side='left', padx=10)

        dough_button = tk.Radiobutton(bait_frame, text='Dough', variable=bait_type_var, value=1,
                                      command=lambda: self.update_bait_type(1))
        dough_button.pack(side='left', padx=10)

    def update_bait_type(self, value):
        if value:
            self.bait_type = "Hamur"
        else:
            self.bait_type = "Solucan"

    def open_bait_window(self):
        config_window = tk.Toplevel(self.root)
        config_window.title('Bait')
        # Set the position of the window
        config_window.geometry("+10+400")
        # Set window attributes to always stay on top but not focused
        config_window.attributes("-topmost", True)
        config_window.attributes("-toolwindow", True)

        bait_frame = tk.Frame(config_window)
        bait_frame.pack(pady=10)

        buy_bait_frame = tk.Frame(bait_frame)
        buy_bait_frame.pack(pady=10)


        tk.Button(buy_bait_frame, text="Buy Fish", command=lambda:self.start_bait_thread(0)).pack(side="left",padx=10)
        self.fish_quantity_spinbox = tk.Spinbox(buy_bait_frame, from_=1, to=48, width=5)
        self.fish_quantity_spinbox.pack(side="left", pady=10)  # Add some padding between Spinbox and Button

        tk.Button(bait_frame, text="Organize Bait", command=lambda:self.start_bait_thread(1)).pack(pady=10)

        vault_frame=tk.Frame(config_window)
        vault_frame.pack()
        tk.Button(vault_frame, text="Put to Vault", command=lambda:self.start_bait_thread(2)).pack(side="left",padx=10,pady=10)
        tk.Button(vault_frame, text="Take from Vault", command=lambda:self.start_bait_thread(3)).pack(side="left",padx=10,pady=10)

    def open_config_window(self):
        # Create a new tkinter window for sensitivity settings
        config_window = tk.Toplevel(self.root)
        config_window.title('Config')

        # Add labels and entry fields for Fish and Bait sensitivity

        fish_frame = tk.Frame(config_window)
        fish_frame.pack(pady=10)

        fish_label = tk.Label(fish_frame, text='Fish Sensitivity:')
        fish_label.pack(side='left', padx=10)
        fish_entry = tk.Entry(fish_frame,width=7)
        fish_entry.insert(0, str(self.fish_sens))
        fish_entry.pack(side='left', padx=10)


        bait_label = tk.Label(fish_frame, text='Bait Sensitivity:')
        bait_label.pack(side='left', padx=10)
        bait_entry = tk.Entry(fish_frame,width=7)
        bait_entry.insert(0, str(self.bait_sens))
        bait_entry.pack(side='left', padx=10)

        # Channel number label and spinbox
        channel_frame = tk.Frame(config_window)
        channel_frame.pack(pady=10)
        channel_label = tk.Label(channel_frame, text='Channel Number:')
        channel_label.pack(side='left', padx=10)
        # Channel number spinbox
        channel_spinbox = tk.Spinbox(channel_frame, from_=1, to=6, increment=1, width=5)
        channel_spinbox.delete(0, "end")
        channel_spinbox.insert(0, str(self.channel_number))
        channel_spinbox.pack(side='left')

        # Channel number label and spinbox
        character_label = tk.Label(channel_frame, text='Character Number:')
        character_label.pack(side='left', padx=10)
        # Channel number spinbox
        character_spinbox = tk.Spinbox(channel_frame, from_=1, to=5, increment=1, width=5)
        character_spinbox.delete(0, "end")
        character_spinbox.insert(0, str(self.character_number))
        character_spinbox.pack(side='left')

        third_row_frame = tk.Frame(config_window)
        third_row_frame.pack(pady=10)

        # Channel number label and spinbox
        inventory_count_label = tk.Label(third_row_frame, text='Inventory Count:')
        inventory_count_label.pack(side='left', padx=10)
        # Channel number spinbox
        inventory_count_spinbox = tk.Spinbox(third_row_frame, from_=1, to=6, increment=1, width=5)
        inventory_count_spinbox.delete(0, "end")
        inventory_count_spinbox.insert(0, str(self.inventory_count))
        inventory_count_spinbox.pack(side='left')

        # Auto login checkbutton
        auto_login_var = tk.BooleanVar(value=True)
        auto_login_checkbox = tk.Checkbutton(third_row_frame, text="Auto Login", variable=auto_login_var)
        auto_login_checkbox.pack(side='left', padx=10)

        # Create a frame for the new rows of checkboxes
        row4_frame = tk.Frame(config_window)
        row4_frame.pack(pady=10)

        # Create checkboxes for the first row
        pelerin_var = tk.BooleanVar(value=False)
        pelerin_checkbox = tk.Checkbutton(row4_frame, text="Pelerin", variable=pelerin_var)
        pelerin_checkbox.pack(side='left', padx=20)

        altin_yuzuk_var = tk.BooleanVar(value=False)
        altin_yuzuk_checkbox = tk.Checkbutton(row4_frame, text="Altın Yüzük", variable=altin_yuzuk_var)
        altin_yuzuk_checkbox.pack(side='left', padx=10)

        # Create a frame for the second row of checkboxes
        row5_frame = tk.Frame(config_window)
        row5_frame.pack(pady=10)

        madalyon_var = tk.BooleanVar(value=False)
        madalyon_checkbox = tk.Checkbutton(row5_frame, text="Madalyon", variable=madalyon_var)
        madalyon_checkbox.pack(side='left', padx=10)

        eldiven_var = tk.BooleanVar(value=False)
        eldiven_checkbox = tk.Checkbutton(row5_frame, text="Eldiven", variable=eldiven_var)
        eldiven_checkbox.pack(side='left', padx=10)

        # Define a function to update the sensitivity values
        def update_config():
            self.fish_sens = float(fish_entry.get())
            self.bait_sens = float(bait_entry.get())
            self.channel_number = int(channel_spinbox.get())
            self.character_number = int(character_spinbox.get())
            self.inventory_count = int(inventory_count_spinbox.get())
            self.auto_login = auto_login_var.get()
            self.pelerin_var = pelerin_var.get()
            self.altin_yuzuk_var = altin_yuzuk_var.get()
            self.madalyon_var = madalyon_var.get()
            self.eldiven_var = eldiven_var.get()
            dont_take_dict = {"pelerin":self.pelerin_var,"altin_yuzuk":self.altin_yuzuk_var,"madalyon":self.madalyon_var,"eldiven":self.eldiven_var}
            self.update_dont_take_names(dont_take_dict)
            config_window.destroy()

        # Add an Update button to apply the sensitivity settings
        update_button = tk.Button(config_window, text='Update', command=update_config)
        update_button.pack()


    def start_gui(self):
        self.create_gui()
        self.root.mainloop()

    def locate_image_rgb_fs(self, template, bbox = (0,0,width,height), precision=0.9, pr=True):
        img = ImageGrab.grab(bbox=bbox)
        img_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        res = cv2.matchTemplate(img_cv2, template[0], cv2.TM_CCOEFF_NORMED)
        min_val, located_precision, min_loc, pos = cv2.minMaxLoc(res)
        detected = False
        if located_precision > precision:
            detected = True
        if pr:
            print("Searching",template[3],located_precision, pos)
        if detected:
            print("detected:",template[3])
        return detected, pos, located_precision,


    def read_images_in_folder(self):
        image_dict = {}
        folders = ["buttons","fish","misc"]
        for inner_folder in folders:
            folder_path = os.getcwd()
            images_path = os.path.join(folder_path, f"images/{inner_folder}")

            # List all files in the folder
            files = os.listdir(images_path)

            # Filter out only the JPG files
            jpg_files = [file for file in files if file.lower().endswith('.jpg')]

            # Iterate through JPG files and read them into the dictionary
            for jpg_file in jpg_files:
                file_path = os.path.join(images_path, jpg_file)

                # Read the image using OpenCV
                target = cv2.imread(file_path)

                # Ensure the image is not None
                if target is not None:
                    # Use the file name (without extension) as the key
                    key = os.path.splitext(jpg_file)[0]

                    # Get image dimensions
                    width, height = target.shape[::][0], target.shape[::][1]

                    # Append the tuple (target, width, height, name) to the dictionary with the file name as the key
                    image_dict[key] = (target, width, height, key)



        return image_dict

    def update_dont_take_names(self, dont_take_dict):

        try:
            # Iterate over the dictionary to update dont_take_names
            for variable_name, value in dont_take_dict.items():

                # Check if the variable is True and item_name is not in dont_take_names, then append
                if value and variable_name not in self.dont_take_names:
                    self.dont_take_names.append(variable_name)

                # Check if the variable is False and item_name is in dont_take_names, then remove
                elif not value and variable_name in self.dont_take_names:
                    self.dont_take_names.remove(variable_name)

        except Exception:
            pass



bot = Mobile2Bot()
bot.start_gui()
