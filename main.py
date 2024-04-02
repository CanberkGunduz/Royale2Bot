import sys
import threading
import tkinter as tk
from io import BytesIO
from tkinter import messagebox
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
        self.check_date()
        self.img_dict = self.read_images_in_folder()
        self.inv_coordinates = [(800, 220), (833, 220), (866, 220), (899, 220), (932, 220), (965, 220), (800, 253),
                                (833, 253), (866, 253), (899, 253), (932, 253), (965, 253), (800, 286), (833, 286),
                                (866, 286), (899, 286), (932, 286), (965, 286), (800, 319), (833, 319), (866, 319),
                                (899, 319), (932, 319), (965, 319), (800, 352), (833, 352), (866, 352), (899, 352),
                                (932, 352), (965, 352), (800, 385), (833, 385), (866, 385), (899, 385), (932, 385),
                                (965, 385), (800, 418), (833, 418), (866, 418), (899, 418), (932, 418), (965, 418),
                                (800, 451), (833, 451), (866, 451), (899, 451), (932, 451), (965, 451)]
        self.vault_coord = [(369, 170), (417, 170), (465, 170), (513, 170), (561, 170), (609, 170), (225, 218), (273, 218), (321, 218), (369, 218), (417, 218), (465, 218), (513, 218), (561, 218), (609, 218), (225, 266), (273, 266), (321, 266), (369, 266), (417, 266), (465, 266), (513, 266), (561, 266), (609, 266), (225, 314), (273, 314), (321, 314), (369, 314), (417, 314), (465, 314), (513, 314), (561, 314), (609, 314), (225, 362), (273, 362), (321, 362), (369, 362), (417, 362), (465, 362), (513, 362), (561, 362), (609, 362)]
        self.dont_take_names = ["beyaz_boya", "renkli_boya", "sari_boya", "siyah_boya", "kirmizi_boya", "pelerin",
                                "altin_yuzuk", "madalyon", "eldiven"]
        self.bait_type = "solucan"
        self.is_running = False  # Flag to control the game cycle
        self.game_cycle_thread = None
        self.party_detection_running = False
        self.inventory_count = 2
        self.total_count = 0
        self.caught_count = 0
        self.valuable_count = 0
        self.delay_time = 0.8  # Default delay time

        self.api_key = '2b0b48d582ce9683dc55066b1d4ebb12'
        self.comment_image_path = "comment_image.jpg"
        self.comment = ""  # Optional instruction for the worker

        # self.detect_bot_control()




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

    # def start_party_detection(self):
    #     self.party_detection_running = True
    #     self.party_detection_thread = threading.Thread(target=self.party_detection_function)
    #     self.party_detection_thread.start()
    #
    # def stop_party_detection(self):
    #     self.party_detection_running = False
    #     # self.party_detection_thread.join()
    #
    # def party_detection_function(self):
    #     # while self.is_running and self.party_detection_running:
    #     time.sleep(0.1)
    #     leader_disc = p.pixelMatchesColor(120,338,(58,56,58),10)
    #     # print(p.pixel(120,338))
    #     # print("leader is disconnected",leader_disc)
    #     if leader_disc:
    #         self.send_notification("Leader Disconnected",True)
    #         # Stop bot functionality
    #         self.stop_party_detection()
    #         self.close_game()
    #         self.stop_game_cycle()
    #         time.sleep(150)
    #         print("2.5 min passed")
    #         self.is_running=True


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

            # "token": "axkpeqe4nasi8avdohn4iwzmzroka8", # cemil
            "token": "a9qutshv8twt4tchs7rvnkqeofhgfk", # canberk
            # "token": "adyvnj3co61qo45opertrtyds6k8ee", # baris
            # "user": "uskopzecnkrn9vkq7duak9hmsno9ic", # cemil
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
                # self.key_press("w")
                # self.key_press("w")
                # self.key_press("w")
                # self.rod_interact()
                self.key_press("a")
                self.moving_rod_throw()

                # running false olsa da buraya kadar çalışıyo
                # stop için fonksiyon içine oyunu kapatma yerleştirilebilir
                while self.is_running:
                    # self.party_detection_function()
                    count += 1
                    if count%10==0:
                        # add image recog to see if char has disappeared
                        # if so, restart fishing cycle
                        self.key_press("w")
                    if self.is_fish_caught():
                        time.sleep(self.delay_time)
                        self.rod_interact()
                        time.sleep(2)
                        if self.is_fish_fetched():
                            done,valuable = self.detect_and_get_fish()
                            if done:
                                self.caught_count+=1
                                if valuable:
                                    self.valuable_count+=1
                                self.focus_game()
                                time.sleep(1)
                                break
                        else:
                            break
                    if self.is_fish_fetched():
                        done, valuable = self.detect_and_get_fish()
                        if done:
                            self.caught_count += 1
                            if valuable:
                                self.valuable_count += 1
                            self.focus_game()
                            time.sleep(1)
                            break
                    if count == 40:
                        break
                    time.sleep(0.4)
                    print(count)
                self.total_count+=1
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
        time.sleep(0.1)
        keyboard.press("w")
        time.sleep(1)
        self.rod_interact()
        time.sleep(0.5)
        keyboard.release("w")

    def choose_character(self,slot):
        move_right_button = 630,520
        for _ in range(slot):
            self.mouse_click("left",move_right_button[0],move_right_button[1])
            time.sleep(2)
        self.mouse_click("left",920,500)

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


    def check_states(self):
        server_closed = self.locate_image_rgb_fs(self.img_dict["server_closed"])
        banned = self.locate_image_rgb_fs(self.img_dict["banned"])
        connect = self.locate_image_rgb_fs(self.img_dict["connect"])
        start = self.locate_image_rgb_fs(self.img_dict["start"])
        connected_but_loading = self.locate_image_rgb_fs(self.img_dict["connected_but_loading"])
        menu = self.locate_image_rgb_fs(self.img_dict["menu"])
        respawn_here = self.locate_image_rgb_fs(self.img_dict["respawn_here"])
        game_logo_white = self.locate_image_rgb_fs(self.img_dict["game_logo_white"],(10,60,40,100))
        states_dict = {"server_closed":server_closed,"banned":banned,"connect":connect,"start":start,
                       "connected_but_loading":connected_but_loading,"menu":menu,"respawn_here":respawn_here,
                       "game_logo_white":game_logo_white}
        return states_dict

    def is_inventory_open(self):
        detected,_,_ = self.locate_image_rgb_fs(self.img_dict["inventory_open"],bbox=(820,45,1000,72))
        if not detected:
            self.key_press("I")
            return self.is_inventory_open()
        return True

    def detect_bot_control(self):
        detected,_,_ = self.locate_image_rgb_fs(self.img_dict["bot_control"],bbox = (570,35,700,70))
        count=0
        while detected:
            # count+=1
            # if count>=5:
            #     print("This is 5th Captcha in a Row. Restarting the Game Now...")
            #     self.close_game()
            #     return False
            print(f"Bot Control Detected...\nSolving Captcha Number {count}!")
            self.solve_captcha()
            time.sleep(5)
            detected, _, _ = self.locate_image_rgb_fs(self.img_dict["bot_control"], bbox=(570,35,700,70))
        else:
            return True

    def encode_image_to_base64(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # Function to send the CAPTCHA to 2Captcha using CoordinatesTask
    def send_captcha_for_solving(self, api_key, captcha_type, image_path, comment="", ):
        url = "https://api.2captcha.com/createTask"
        body = self.encode_image_to_base64(image_path)
        img_comment = self.encode_image_to_base64(self.comment_image_path)
        task = {
            "type": captcha_type,
            "body": body,
            "comment": "Check image instruction",
            "imgInstructions": img_comment
        }
        data = {
            'clientKey': api_key,
            'task': task,
            'json': 1,  # Request the response in JSON format
            'lang': 'en',
        }
        response = requests.post(url, json=data)  # Ensure to use json=data to send JSON payload
        return response.json()

    # Function to check for the solution
    def check_solution(self, api_key, captcha_id):
        url = "http://2captcha.com/res.php"
        params = {
            'key': api_key,
            'action': 'get',
            'id': captcha_id,
            'json': 1
        }
        while True:
            response = requests.get(url, params=params)
            result = response.json()
            print(result)
            if result.get('status') == 1:
                return result['request']  # The solution
            elif result.get('request') != 'CAPCHA_NOT_READY':
                print(f"Error: {result.get('request')}")
                return None
            time.sleep(5)  # Wait for a few seconds before checking again


    def screenshot_based_on_color(self):
        # Define the white threshold
        white_threshold = (230, 230, 230)  # Consider near white if R, G, and B are all above these values
        captcha_size = ""

        detected, pos, presicion = self.locate_image_rgb_fs(self.img_dict["captcha_logo"])
        print(detected, pos, presicion)

        is_big = p.pixelMatchesColor(pos[0]-240, pos[1]-530, white_threshold, tolerance=30)
        is_small_type_1 = p.pixelMatchesColor(pos[0]-180, pos[1]-550, white_threshold, tolerance=30)
        # is_small_type_2 = p.pixelMatchesColor(pos[0]-240, pos[1]-530, white_threshold, tolerance=30)

        # Check if the pixel at (440, 120) is near white
        if is_big:
            captcha_image_coordinates = pos[0]-160, pos[1]-440, pos[0] + 190, pos[1] - 100
            comment_image_coordinates = pos[0]-240, pos[1]-530, pos[0] + 270, pos[1] - 450
            p.screenshot('captcha_big.jpg', region=(captcha_image_coordinates[0], captcha_image_coordinates[1],
                                                    350, 340))
            p.screenshot('comment_image.jpg', region=(comment_image_coordinates[0], comment_image_coordinates[1],
                                                    510, 80))
            captcha_size = "big"

        elif is_small_type_1:
            captcha_image_coordinates = pos[0] - 180, pos[1] - 430, pos[0] + 210, pos[1] - 40
            comment_image_coordinates = pos[0] - 180, pos[1] - 550, pos[0] + 210, pos[1] - 440
            p.screenshot('captcha_small.jpg', region=(captcha_image_coordinates[0], captcha_image_coordinates[1],
                                                    390, 390))
            p.screenshot('comment_image.jpg', region=(comment_image_coordinates[0], comment_image_coordinates[1],
                                                      390, 120))
            captcha_size = "small_type_1"
        # elif p.pixelMatchesColor(380, 130, white_threshold, tolerance=30):
        #     # If not, and (595,125) is white, take a screenshot from (595,125) to (990,720)
        #     p.screenshot('captcha_small.jpg', region=(380, 130, 290, 360))
        #     p.screenshot('comment_image.jpg', region=(380, 130, 290, 360))
        #     captcha_size = "small_type_2"

        return captcha_size, captcha_image_coordinates

    def solve_captcha(self):
        self.focus_game()
        if self.locate_image_rgb_fs(self.img_dict["i_am_human"],precision=0.8)[0]:
            self.mouse_click("left", 430, 420, 1)
        # Call the function
        while not (self.locate_image_rgb_fs(self.img_dict["skip"])[0] or self.locate_image_rgb_fs(self.img_dict["verify"])[0]):
            time.sleep(1)
            print("Waiting for Captcha to Load...")
            if not self.locate_image_rgb_fs(self.img_dict["bot_control"])[0]:
                print("Bot Control is Already Done!")
                return
            if self.locate_image_rgb_fs(self.img_dict["i_am_human"])[0]:
                self.mouse_click("left", 430, 420, 1)
        else:
            self.focus_game()
        captcha_size, captcha_image_coordinates = self.screenshot_based_on_color()
        print("Captcha size:", captcha_size)

        # Main process

        if captcha_size == "big":
            image_path = "captcha_big.jpg"
            detected,pos,_ = self.locate_image_rgb_fs(self.img_dict["skip"])
            self.mouse_click("left",pos[0]+20,pos[1]+20)
            time.sleep(2)
            self.mouse_click("left",pos[0]+20,pos[1]+20)
        elif captcha_size == "small_type_1":
            image_path = "captcha_small.jpg"
            detected, pos, _ = self.locate_image_rgb_fs(self.img_dict["skip"])
            self.mouse_click("left",780,280)
            self.mouse_click("left",780,410)
            self.mouse_click("left",780,540)
            self.mouse_click("left",pos[0]+20,pos[1]+20)
        # api_key = self.api_key
        # comment = self.comment
        # image_path = self.comment_image_path
        #
        # # Sending the CAPTCHA
        # if captcha_size == "big":
        #     response = self.send_captcha_for_solving(api_key, "CoordinatesTask", image_path, comment)
        # elif captcha_size == "small_type_1":
        #     response = self.send_captcha_for_solving(api_key, "GridTask", image_path, comment)
        # if response.get('errorId') == 0:
        #     task_id = response.get('taskId')
        #     print(f"Captcha sent successfully. Task ID: {task_id}")
        #     # Polling for the solution
        #     solution = self.check_solution(api_key, task_id)
        #     if solution:
        #         print(f"Captcha Solved: {solution}")
        #         if captcha_size == "big":
        #             x = int(solution[0]['x']) + captcha_image_coordinates[0]
        #             y = int(solution[0]['y']) + captcha_image_coordinates[1]
        #             # Move the mouse to the coordinate and click
        #             self.mouse_click("left",x,y)
        #
        #         elif captcha_size == "small_type_1":
        #             grids_to_click = []
        #             for char in solution:
        #                 if char.isdigit():
        #                     grids_to_click.append(int(char))
        #             print(grids_to_click)
        #             if len(grids_to_click)<3:
        #                 return
        #             for num in grids_to_click:
        #                 x = 520+(num-1)%3*130
        #                 y = 280+((num+2)//3-1)*130
        #                 self.mouse_click("left",x,y,1)
        #                 print(x,y)
        #         _, pos, _ = self.locate_image_rgb_fs(self.img_dict["verify"])
        #         self.mouse_click("left", pos[0] + 30, pos[1] + 20)
        #     else:
        #         print("Failed to retrieve captcha solution")
        # else:
        #     print(f"Failed to send captcha: {response.get('errorDescription')}")

    def is_fish_caught(self):
        detected, pos, located_precision = self.locate_image_rgb_fs(self.img_dict["balik"], (490, 230, 530, 270), self.fish_sens)
        return detected

    def is_fish_fetched(self):
        detected, pos, located_precision = self.locate_image_rgb_fs(self.img_dict["x_button"], (570, 215, 590, 230), 0.8)
        return detected

    def is_player_dead(self,close_if_dead = True):
        detected, pos, located_precision = self.locate_image_rgb_fs(self.img_dict["respawn"], precision= 0.8)
        if close_if_dead and detected:
            print("Character died")
            self.close_game()
        return detected


    def use_bait_new(self):
        self.focus_game()
        detected, pos, located_precision = self.locate_image_rgb_fs(self.img_dict[self.bait_type], (780, 380, 980, 470), self.bait_sens)
        if detected:
            self.mouse_click("right", pos[0] + 10 + 780, pos[1] + 10 + 380)
        else:
            print("no bait left")
            self.stop_game_cycle()
        time.sleep(0.4)

    def rod_interact(self):
        self.key_press("space")

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
        window_title = "Mobile2 Global  "
        hwnd = win32gui.FindWindow(None, window_title)

        if hwnd == 0:
            print('Window not found.')
            game_is_open=False
        else:
            game_is_open=True
        return game_is_open


    def focus_game(self):
        self.mouse_click("left",50,15)

    def close_game(self):
        self.mouse_click("left", 1230, 15)


    def open_game(self):
        retry_count = 0
        # if self.is_running:
        #     self.stop_game_cycle()
        if not self.check_game_is_open():
            # self.stop_image_detection() # so the auto login works

            self.mouse_click("left",1315,630) # game logo on desktop
            self.key_press("enter")
            game_open_checker = 0
            while not self.check_game_is_open():
                time.sleep(0.5)
                game_open_checker+=1
                if game_open_checker >= 30:
                    self.mouse_click("left", 1315,630)
                    self.key_press("enter")
                    game_open_checker=0
            self.resize_window()
            time.sleep(10)
            # ch1 = 530,60
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
            self.attach_cheat_engine()
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
        inv_coords = [(845, 150),(935, 150),(845, 180),(935, 180)]
        while True:
            detected, pos, _ = self.locate_image_rgb_fs(self.img_dict["connected_but_loading"])
            if not detected:
                detected, pos, _ = self.locate_image_rgb_fs(self.img_dict["menu"])
                if detected:
                    self.mouse_click("left", 50, 10)
                    self.key_press("I")
                    for _ in range(4):
                        self.key_press("f")
                        self.key_press("g")
                    self.mouse_click("left",inv_coords[self.inventory_count-1][0],inv_coords[self.inventory_count-1][1])
                    time.sleep(0.5)
                    return True
            time.sleep(1)
            trial_count += 1
            if trial_count == 30:
                trial_count = 0

                return False

    def choose_server(self):
        ch_num= self.channel_number-1
        ch_coords = [(670 + i * 100, 70 + j * 30) for j in range(3) for i in range(3)]
        print(ch_coords)
        print(ch_coords[ch_num])
        self.mouse_click("left", ch_coords[ch_num][0], ch_coords[ch_num][1])
        self.mouse_click("left", 1155, 175)

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
        window_title = "Mobile2 Global  "
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
        self.root.title('Mobile2 Bot')

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
        folders = ["cheat_engine", "dont_take", "inv_items", "items", "misc", "states","captcha"]
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
