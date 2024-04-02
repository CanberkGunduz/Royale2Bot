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
    channel_number = 2
    character_number = 0
    inventory_count = 2
    auto_login = 1
    INVENTORY_FULL = False
    pelerin_var = False
    altin_yuzuk_var = False
    madalyon_var = False
    eldiven_var = False

    def __init__(self):
        # self.check_date()

        self.img_dict = self.read_images_in_folder()
        self.bait_type = "hamur"
        self.is_running = False  # Flag to control the game cycle
        self.game_cycle_thread = None
        self.party_detection_running = False
        self.inventory_count = 1
        self.total_count = 0
        self.caught_count = 0
        self.valuable_count = 0
        self.delay_time = 0.8  # Default delay time

        self.fish_detector()
        time.sleep(3)
        self.use_bait_new()
        time.sleep(3)
        self.moving_rod_throw()
        time.sleep(2)
        self.fish_detector()
        quit()

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
        # if not self.check_game_is_open():
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
                if self.auto_login:
                    if not self.check_game_is_open():
                        self.open_game()
                if not self.locate_image_rgb_fs(self.img_dict["menu"])[0]:
                    if self.locate_image_rgb_fs(self.img_dict["game_logo_white"],(10,60,40,100))[0]:
                        if self.locate_image_rgb_fs(self.img_dict["banned"])[0]:
                            self.send_notification("Account banned.",True)
                        if self.locate_image_rgb_fs(self.img_dict["connect"])[0]:
                            self.close_game()
                        self.resize_window()
                    if self.locate_image_rgb_fs(self.img_dict["server_closed"])[0]:
                        print("server is closed")
                        currentDateAndTime = datetime.now()
                        with open(f"session_{self.delay_time}.txt", "a") as session_file:
                            session_file.write(
                                f"SERVER IS CLOSED\ntotal tries: {self.total_count}\ncaught: {self.caught_count}\nvaluable: {self.valuable_count}\ncurrent date: {currentDateAndTime}\n-----------------------\n")
                        self.close_game()
                        time.sleep(120)
                    continue


                self.is_player_dead()
                inv_full = self.check_inventory_full_by_empty_slots()
                if inv_full:
                    self.open_fish()
                    if self.check_inventory_full_by_empty_slots():
                        self.send_notification("Inventory is full.",send_screenshot=True)
                        self.stop_game_cycle()
                        self.close_game()

                count = 0
                time.sleep(1)
                self.use_bait_new()
                self.moving_rod_throw()
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
        time.sleep(0.5)
        self.key_press("space")
        time.sleep(0.5)
        p.mouseUp(button="left")

    def choose_character(self,slot):
        self.mouse_click("left",260,160+90*slot)
        time.sleep(0.5)
        self.mouse_click("left",1000,590)

    def start_bait_thread(self,func):
        if func == 0:
            self.bait_thread = threading.Thread(target=self.buy_bait)
        elif func == 1:
            self.bait_thread = threading.Thread(target=self.organize_bait)
        elif func == 2:
            self.bait_thread = threading.Thread(target=self.put_bait_to_vault)
        elif func == 3:
            self.bait_thread = threading.Thread(target=self.take_bait_from_vault)
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

    def take_bait_from_vault(self):
        self.mouse_click("left",200,10)
        vault_coord = self.vault_coord
        for _ in range(12):
            det, pos, _ = self.locate_image_rgb_fs(self.img_dict["solucan"],bbox=(180,120,640,400),precision=0.5)
            if not det: break
            self.mouse_click("right", 180+pos[0], 120+pos[1])
            time.sleep(0.5)
        else:
            self.mouse_click("left",700,100)
            print("Baits are taken...")

    def put_bait_to_vault(self):
        self.mouse_click("left",200,10)
        vault_coord = self.vault_coord
        inv_coord = self.inv_coordinates
        for coord_index in range(len(vault_coord)):
            self.mouse_drag("left", inv_coord[coord_index][0],inv_coord[coord_index][1],vault_coord[coord_index][0], vault_coord[coord_index][1],move_speed=0.1)
        print("Baits are placed...")

    def trade(self):
        x1_1, y1_1, x2_1, y2_1 = 801, 222, 383, 315
        trade_window_squares = [(383, 315), (413, 315), (443, 315), (473, 315), (503, 315), (383, 345), (413, 345), (443, 345), (473, 345), (503, 345), (383, 375), (413, 375), (443, 375), (473, 375), (503, 375), (383, 405), (413, 405), (443, 405), (473, 405), (503, 405)]
        trade_count=0
        while True:
            if self.locate_image_rgb_fs(self.img_dict["trade"],precision=0.8)[0]:
                # detect trade window incrementally to decide coordinates
                if trade_count==2:
                    self.mouse_click("left",845,150)
                for i in range(3):
                    for j in range(6):
                        drag_loc = trade_window_squares[6*i+j][0],trade_window_squares[6*i+j][1]
                        self.mouse_drag("left", x1_1 + j * 33, trade_count%2*100+y1_1 + i * 33, drag_loc[0],drag_loc[1],0.1,0.1)
                time.sleep(2)
                while self.locate_image_rgb_fs(self.img_dict["trade"],precision=0.8)[0]:
                    time.sleep(3)
                trade_count += 1

            if trade_count==4:
                break


    def open_inventory(self):
        self.mouse_click("left",890,80)

    def is_inventory_open(self):
        detected,_,_ = self.locate_image_rgb_fs(self.img_dict["inventory_open"],bbox=(820,45,1000,72))
        if not detected:
            self.key_press("I")
            return self.is_inventory_open()
        return True

    def use_bait_new(self):
        self.open_inventory()
        time.sleep(0.5)
        detected, pos, located_precision = self.locate_image_rgb_fs(self.img_dict[self.bait_type], (820, 280, 1180, 640), self.bait_sens)
        if detected:
            self.mouse_click("left", pos[0] + 10 + 780, pos[1] + 10 + 380)
            self.mouse_click("left", pos[0] + 10 + 780, pos[1] + 10 + 380)
            # self.mouse_click("left",710,590)
            self.mouse_click("left",1160,210)
        else:
            print("no bait left")
            self.stop_game_cycle()
        time.sleep(0.4)

    def rod_interact(self):
        self.key_press("space")

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
                while True:
                    # Capture the specified area of the screen
                    img = np.array(sct.grab({'top': 80, 'left': 460, 'width': 240, 'height': 100}))

                    # Convert the image from BGR to HSV
                    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

                    # Create a mask that only includes pixels within the specified red HSV range
                    mask = cv2.inRange(hsv_img, (0, 169, 157), (10, 189, 237))

                    # Use the mask to isolate the red parts of the image
                    result_img = cv2.bitwise_and(img, img, mask=mask)

                    # Save the original and masked images for inspection
                    cv2.imwrite('original_image.jpg', img)
                    cv2.imwrite('masked_image.jpg', result_img)

                    # Sum the values in the mask to determine the amount of red detected
                    red_detected = np.sum(mask)
                    print(red_detected)

                    # Check if the red object is detected based on the threshold
                    if red_detected < detection_threshold:
                        count+=1
                        if count>=3:
                            print("Red object possibly underwater, fetching the rod!")
                            self.key_press("space")  # Simulate the key press to fetch the rod
                            self.key_press("space")  # Simulate the key press to fetch the rod
                            time.sleep(1)  # Wait a bit before continuing to monitor
                            break
                    else:
                        count=0

                    time.sleep(0.1)  # Short delay to avoid excessive CPU usage
            except KeyboardInterrupt:
                print("Stopped monitoring.")

    def detect_and_get_fish(self):

        img = ImageGrab.grab(bbox=(437, 230, 484, 276))
        img_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        current_dir = os.getcwd()
        file_name = "image.jpg"
        file_path = os.path.join(current_dir, file_name)
        cv2.imwrite(file_path, img_cv2)
        template = [cv2.imread(file_path),0,0,"captured"]

        time.sleep(1)
        for name in self.dont_take_names:
            detected, pos, located_precision = self.locate_image_rgb_fs(self.img_dict[name], (437, 230, 484, 276), 0.7)
            if detected:
                self.mouse_click("left", 585, 220)
                return True,False
        detected2, pos, located_precision = self.locate_image_rgb_fs(template, (440, 280, 560, 400), 0.1)
        print("searching item", located_precision, pos)
        if detected2:
            print("located item", located_precision, pos)
            self.mouse_click("left", pos[0] + 25 + 440, pos[1] + 25 + 280)
            return True,True

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
        detected, _, _= self.locate_image_rgb_fs(self.img_dict["empty_slot"],(780, 205, 985, 435),0.7)
        if not detected:
            return True

    def check_game_is_open(self):
        game_is_open = None
        # Get the window handle (replace 'Your Window Title' with the actual window title)
        window_title = "BlueStacks App Player"
        hwnd = win32gui.FindWindow(None, window_title)

        if hwnd == 0:
            print('Window not found.')
            game_is_open=False
        else:
            game_is_open=True
        return game_is_open

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

    def find_game_logo_and_click(self):
        _, pos, _ = self.locate_image_rgb_fs(self.img_dict["Game_logo"])  # game logo on desktop
        self.mouse_click("left", pos[0], pos[1])
    def open_game(self):
        retry_count = 0
        # if self.is_running:
        #     self.stop_game_cycle()
        if not self.check_game_is_open():
            # self.stop_image_detection() # so the auto login works

            self.find_game_logo_and_click()
            game_open_checker = 0
            while not self.check_game_is_open():
                time.sleep(0.5)
                game_open_checker+=1
                if game_open_checker >= 30:
                    self.find_game_logo_and_click()
                    game_open_checker=0
            self.resize_window()
            time.sleep(10)
            connected = False
            launch_start_time= time.time()
            while not connected:
                stuck_loading = time.time() - launch_start_time >= 60
                if stuck_loading:
                    self.close_game()
                    return
                time.sleep(1)
                self.choose_server()
                time.sleep(4)
                captcha_done = self.detect_bot_control()
                print(captcha_done)
                connected = self.check_is_connected()
                if not connected:
                    if self.locate_image_rgb_fs(self.img_dict["banned"])[0]:
                        print("account is banned")
                        with open(f"session_{self.delay_time}.txt", "a") as session_file:
                            session_file.write(
                                f"ACCOUNT IS BANNED\n")
                            self.stop_game_cycle()
                            self.close_game()
                            self.send_notification("Account is banned.",send_screenshot=True)
                            return
                    self.key_press("enter")
            time.sleep(1)
            self.focus_game()
            self.choose_character(self.character_number)
            if self.set_ui():

                time.sleep(1)
                p.hotkey('ctrl', 'f')
                self.focus_game()
                # if not self.party_detection_running:
                #     self.party_detection_running=True
                #     self.start_party_detection()
            else:
                print("something went wrong")
                retry_count+=1
                self.mouse_click("left", 993, 14)
                time.sleep(2)
                if retry_count<=6:
                    self.open_game()
                else:
                    sys.exit()

    def set_ui(self):
        trial_count = 0
        inv_coords = [(850, 260),(935, 150),(845, 180),(935, 180)]
        while True:
            detected, pos, _ = self.locate_image_rgb_fs(self.img_dict["connected_but_loading"])
            if not detected:
                detected, pos, _ = self.locate_image_rgb_fs(self.img_dict["menu"])
                if detected:
                    self.mouse_click("left", 890, 90) # open inventory
                    self.mouse_click("left",850+(self.inventory_count-1)*60, 260)
                    time.sleep(0.5)
                    return True
            time.sleep(1)
            trial_count += 1
            if trial_count == 30:
                trial_count = 0

                return False

    def choose_server(self):
        ch_num= self.channel_number-1
        ch_coords = [(600 + i * 200, 300 + j * 40) for j in range(3) for i in range(2)]
        print(ch_coords)
        print(ch_coords[ch_num])
        self.mouse_click("left", ch_coords[ch_num][0], ch_coords[ch_num][1])

    def check_is_connected(self):
        trial_count = 0
        while True:
            detected, pos, _ = self.locate_image_rgb_fs(self.img_dict["start"])
            if detected:
                return True
            time.sleep(1)
            trial_count += 1
            if trial_count == 8:
                trial_count = 0
                return False

    def attach_cheat_engine(self):
        detected, pos, _ = self.locate_image_rgb_fs(self.img_dict["ch_logo_bar"],bbox=(0,720,width,height))
        self.mouse_click("left",pos[0]+5,pos[1]+725)
        time.sleep(2)
        # detected, pos2, _ = self.locate_image_rgb_fs(self.img_dict["ch_menu_opener"])
        # self.mouse_click("left",pos2[0]+5,pos2[1]+5)
        # time.sleep(1)
        # det_white,pos3,_=  self.locate_image_rgb_fs(self.img_dict["game_logo_white"],bbox=(0,100,width,600),precision=0.7)
        # det_blue, pos4,_ =self.locate_image_rgb_fs(self.img_dict["game_logo_blue"],bbox=(0,0,width,600))
        p.hotkey('ctrl', 'p')
        time.sleep(1)
        self.key_press("enter")
        time.sleep(1)
        self.key_press("enter")
        # if det_blue:
        #     self.mouse_click("left",pos4[0]+2,pos4[1]+2)
        #     time.sleep(1)
        #     self.key_press("enter")
        #     time.sleep(1)
        #     self.key_press("enter")
        # elif det_white:
        #     self.mouse_click("left", pos3[0] + 2, pos3[1] + 100 +2)
        #     time.sleep(1)
        #     self.key_press("enter")
        #     time.sleep(1)
        #     self.key_press("enter")
        # else:
        #     self.key_press("enter")
        #     time.sleep(1)
        #     self.key_press("enter")

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
            print('Window not found.')

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
            self.bait_type = "hamur"
        else:
            self.bait_type = "solucan"

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
        channel_spinbox = tk.Spinbox(channel_frame, from_=1, to=9, increment=1, width=5)
        channel_spinbox.delete(0, "end")
        channel_spinbox.insert(0, str(self.channel_number))
        channel_spinbox.pack(side='left')

        # Channel number label and spinbox
        character_label = tk.Label(channel_frame, text='Character Number:')
        character_label.pack(side='left', padx=10)
        # Channel number spinbox
        character_spinbox = tk.Spinbox(channel_frame, from_=1, to=9, increment=1, width=5)
        character_spinbox.delete(0, "end")
        character_spinbox.insert(0, str(self.character_number))
        character_spinbox.pack(side='left')

        third_row_frame = tk.Frame(config_window)
        third_row_frame.pack(pady=10)

        # Channel number label and spinbox
        inventory_count_label = tk.Label(third_row_frame, text='Inventory Count:')
        inventory_count_label.pack(side='left', padx=10)
        # Channel number spinbox
        inventory_count_spinbox = tk.Spinbox(third_row_frame, from_=1, to=4, increment=1, width=5)
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
            print("fs",located_precision, pos)
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
