import os
import json
import sys
import time
from fbchat import Client
from fbchat.models import *
import requests
import ua_generator
from commands.gemini import get_gemini_response
from commands.chat4o import get_webgpt4o_response
from commands.pinterest import get_pinterest_images
from commands.binary import TextEncoder
import re
import random

try:
    with open('configuration.json') as f:
        configuration = json.load(f)
except FileNotFoundError:
    print("\033[1m\033[91mSORRY, AN ERROR ENCOUNTERED WHILE FINDING 'CONFIGURATION.JSON'.\033[0m")
    sys.exit()
except json.decoder.JSONDecodeError:
    print("\033[1m\033[91mSORRY, AN ERROR ENCOUNTERED WHILE READING THE JSON FILE.\033[0m")
    sys.exit()

def print_slow(str):
    for char in str:
        time.sleep(.1)
        sys.stdout.write(char)
        sys.stdout.flush()
    sys.exit()

class MessBot(Client):
    add_token = []
    

    def get_token(self):
        global configuration
        os.system('clear')
        accounts = configuration['CONFIG']['PAGE_ACCOUNTS']['ACCOUNTS']
        for account in accounts:
            account_data = account.split('|')
            url = 'https://b-api.facebook.com/method/auth.login'
            form = {
                'adid': 'e3a395f9-84b6-44f6-a0ce-fe83e934fd4d',
                'email': account_data[0],
                'password': account_data[1],
                'format': 'json',
                'device_id': '67f431b8-640b-4f73-a077-acc5d3125b21',
                'cpl': 'true',
                'family_device_id': '67f431b8-640b-4f73-a077-acc5d3125b21',
                'locale': 'en_US',
                'client_country_code': 'US',
                'credentials_type': 'device_based_login_password',
                'generate_session_cookies': '1',
                'generate_analytics_claim': '1',
                'generate_machine_id': '1',
                'currently_logged_in_userid': '0',
                'irisSeqID': 1,
                'try_num': '1',
                'enroll_misauth': 'false',
                'meta_inf_fbmeta': 'NO_FILE',
                'source': 'login',
                'machine_id': 'KBz5fEj0GAvVAhtufg3nMDYG',
                'meta_inf_fbmeta': '',
                'fb_api_req_friendly_name': 'authenticate',
                'fb_api_caller_class': 'com.facebook.account.login.protocol.Fb4aAuthHandler',
                'api_key': '882a8490361da98702bf97a021ddc14d',
                'access_token': '350685531728%7C62f8ce9f74b12f84c123cc23437a4a32'
            }
            headers = {
                'content-type': 'application/x-www-form-urlencoded',
                'x-fb-friendly-name': 'fb_api_req_friendly_name',
                'x-fb-http-engine': 'Liger',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            }
            response = requests.post(url, data=form, headers=headers)
            try:
                response_data = response.json()
                if 'access_token' in response_data:
                    self.add_token.append(response_data['access_token'])
                    print("\033[1m[\033[91m\033[1m/\033[0m\033[1m] PAGES SUCCESSFULLY LOADED!\033[0m")
                else:
                    print("\033[1m[\033[91m\033[1mx\033[0m\033[1m] PAGES FAILED TO LOAD!\033[0m")
            except ValueError as e:
                print("\033[1m[\033[91m\033[1mx\033[0m\033[1m] Error decoding JSON for {} {}: {}\033[0m".format(
                    account_data[0], account_data[1], e))

    def send_message(self, thread_id, thread_type, message):
        self.send(Message(text=message), thread_id=thread_id, thread_type=thread_type)

    def send_image(self, thread_id, thread_type, image_path):
     self.sendLocalFiles(
        [image_path], thread_id=int(thread_id), thread_type=thread_type
    )

    def onMessage(self, mid=None, author_id=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        try:
            if author_id == self.uid:
                return

            global follow_in_progress, reaction_in_progress
            with open('configuration.json') as f:
                configuration = json.load(f)
            msg = message_object.text.lower()
           
            rainbow_light_text_print("[ [ MESSAGE ] ] " + msg)
            
            prefix = configuration['CONFIG']['BOT_INFO']['PREFIX']
             
            
             
            if prefix.lower() in ["prefix", "prefix", "prefix"]:  # Check for the exact word "prefix" in various cases
                prefix = configuration['CONFIG']['BOT_INFO']['PREFIX']

            if prefix.lower() in ["prefix", "prefix", "prefix"]:
                self.send(Message(text=f"The prefix is: {prefix}"), thread_id=thread_id, thread_type=thread_type)
                return

            if msg.lower() == prefix.lower():
                self.send(Message(text="Hey! That's me, what can i help you?"), thread_id=thread_id, thread_type=thread_type)
                return

            greetings = ("hi", "hi!", "hello", "hello!")
            if any(msg.lower().startswith(greeting) for greeting in greetings):
                try:
                    user_info = self.fetchUserInfo(author_id)
                    sender_name = user_info[author_id].name
                    greeting_message = f"Hello, {sender_name}!"
                    self.sendMessage(thread_id=thread_id, message=greeting_message, thread_type=thread_type)
                except Exception as e:
                    print(f"An error occurred while sending a greeting message: {e}")
            if msg.lower() == (prefix + "help"):
                help_message = f"""
𝙴𝚎𝚊𝚟𝚎 
─── ⋆⋅☆⋅⋆ ── ─── ⋆⋅☆⋅⋆ ── 
𝙳𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚍 𝚋𝚢: 𝚂𝚞𝚜𝚑𝚒

𝙳𝚎𝚜𝚌𝚛𝚒𝚙𝚝𝚒𝚘𝚗: 𝙴𝚎𝚊𝚟𝚎 𝚒𝚜 𝚊𝚗 𝚒𝚗𝚝𝚎𝚕𝚕𝚒𝚐𝚎𝚗𝚝 𝚋𝚘𝚝, 𝚊𝚞𝚝𝚘𝚖𝚊𝚝𝚎𝚍 𝚊𝚗𝚍 𝚍𝚎𝚜𝚒𝚐𝚗𝚎𝚍 𝚊𝚜𝚜𝚒𝚜𝚝𝚊𝚗𝚝 𝚍𝚎𝚜𝚒𝚐𝚗𝚎𝚍 𝚝𝚘 𝚜𝚝𝚛𝚎𝚊𝚖𝚕𝚒𝚗𝚎 𝚌𝚘𝚖𝚖𝚞𝚗𝚒𝚌𝚊𝚝𝚒𝚘𝚗 𝚊𝚗𝚍 𝚎𝚗𝚌𝚑𝚊𝚗𝚌𝚎 𝚞𝚜𝚎𝚛 𝚒𝚗𝚝𝚎𝚛𝚊𝚌𝚝𝚒𝚘𝚗

─── ⋆⋅☆⋅⋆ ── ─── ⋆⋅☆⋅⋆ ── 
    𝙲𝚘𝚖𝚖𝚊𝚗𝚍𝚜٩(◕‿◕｡)۶

─── ⋅⋆☆⋅ ── ─── ⋅⋆☆⋅ ── 
 ╰┈➤({prefix})𝚊𝚜𝚔4𝚘
 -𝙰𝚗 𝚊𝚒 𝚊𝚜𝚜𝚒𝚜𝚝𝚊𝚗𝚝 𝚝𝚑𝚊𝚝 𝚌𝚊𝚗  𝚊𝚗𝚜𝚠𝚎𝚛 𝚊𝚗𝚢𝚝𝚑𝚒𝚗𝚐 𝚢𝚘𝚞 𝚊𝚜𝚔
─── ⋅⋆☆⋅ ── ─── ⋅⋆☆⋅ ── 
 ╰┈➤({prefix})𝚊𝚜𝚔𝚐𝚎𝚖
-𝙰𝚗 𝚊𝚒 𝚊𝚜𝚜𝚒𝚜𝚝𝚊𝚗𝚌𝚎 𝚌𝚛𝚎𝚊𝚝𝚎𝚍 𝚋𝚢 𝙶𝚘𝚘𝚐𝚕𝚎 𝚝𝚘  𝚑𝚎𝚕𝚙 𝚢𝚘𝚞 

─── ⋅⋆☆⋅ ── ─── ⋅⋆☆⋅ ── 
 ╰┈➤({prefix})𝚓𝚘𝚔𝚎
-𝙶𝚎𝚝 𝚊 𝚛𝚊𝚗𝚍𝚘𝚖 𝚓𝚘𝚔𝚎

─── ⋅⋆☆⋅ ── ─── ⋅⋆☆⋅ ── 
 ╰┈➤({prefix})𝚢𝚘𝚞𝚝𝚞𝚋𝚎 (𝚜𝚎𝚊𝚛𝚌𝚑)
-𝙶𝚎𝚝 𝚊 𝚟𝚒𝚍𝚎𝚘 𝚏𝚛𝚘𝚖 𝚢𝚘𝚞𝚝𝚞𝚋𝚎 

─── ⋅⋆☆⋅ ── ─── ⋅⋆☆⋅ ── 
 ╰┈➤({prefix})𝚙𝚒𝚗𝚝𝚎𝚛𝚎𝚜𝚝 (𝚜𝚎𝚊𝚛𝚌𝚑)
-𝙶𝚎𝚝 𝚊 𝚙𝚒𝚌𝚝𝚞𝚛𝚎 𝚏𝚛𝚘𝚖 𝚙𝚒𝚗𝚝𝚎𝚛𝚎𝚜𝚝

─── ⋅⋆☆⋅ ── ─── ⋅⋆☆⋅ ── 
 ╰┈➤({prefix})𝚜𝚑𝚘𝚝𝚒
-𝙶𝚎𝚝 𝚊 𝚟𝚒𝚍𝚎𝚘 𝚏𝚛𝚘𝚖 𝙱𝚎𝚊𝚞𝚝𝚒𝚏𝚞𝚕 𝚐𝚒𝚛𝚕𝚜 𝚏𝚛𝚘𝚖 𝚝𝚒𝚔𝚝𝚘𝚔 𝚖𝚊𝚐𝚓𝚊𝚔𝚘𝚕 𝚔𝚊𝚗𝚊 𝚊𝚕𝚕 𝚢𝚘𝚞 𝚠𝚊𝚗𝚝.
─── ⋅⋆☆⋅ ── ─── ⋅⋆☆⋅ ── 
 ╰┈➤({prefix})𝚌𝚊𝚝𝚏𝚊𝚌𝚝𝚜
-𝙶𝚎𝚝 𝚊 𝚏𝚊𝚌𝚝𝚜 𝚏𝚛𝚘𝚖 𝚊 𝚌𝚊𝚝

𝙴𝚗𝚓𝚘𝚢 !
                """
                help_message = help_message.replace("(prefix)", prefix)
                self.send(Message(text=help_message), thread_id=thread_id, thread_type=thread_type)
                
                
                image_path = "/home/spade/Desktop/botai/commands/image/ren.jpeg"  # Replace with your image path
                self.send_image(thread_id=thread_id, thread_type=thread_type, image_path=image_path)

                return
         

            if msg.startswith(f"{prefix}ask4o"):
                question = msg[len(f"{prefix}ask4o"):].strip()
                reply = "Typing..."
                self.send(message=Message(text=reply), thread_id=thread_id, thread_type=thread_type)
                try:
                    ask2 = get_webgpt4o_response(question)
                    ask2_text = ask2['response']
                    reply = f"𝗖𝗵𝗮𝘁𝗚𝗽𝘁 4𝗼 𝗔𝗶:\n\n{ask2_text}\n\n\n"
                    self.send(message=Message(text=reply), thread_id=thread_id, thread_type=thread_type)
                except Exception as e:
                    error_reply = f"An error occurred: {str(e)}"
                    self.send(message=Message(text=error_reply), thread_id=thread_id, thread_type=thread_type)
                return
            if msg.startswith(f"{prefix}binary"):
               message = msg[len(f"{prefix}binary"):].strip()
               encoded_message = TextEncoder.encode_text(message)
               message1 = encoded_message
               if encoded_message:
                   self.send_message(message1=Message(text=message1), thread_id=thread_id, thread_type=thread_type)
               else:
                   self.send(Message(text="Failed to encode text."), thread_id=thread_id, thread_type=thread_type)
                   return
            if msg.startswith(f"{prefix}facts"):
                
                facts = requests.get('https://api.popcat.xyz/fact').json()['fact']
                
                reply = f"RANDOM FACT: \n{facts}"
                
                self.send(Message(text=reply), thread_id=thread_id, thread_type=thread_type)
                
            if msg.startswith(f"{prefix}askgem"):
                question = msg[len(f"{prefix}askgem"):].strip()
                reply1 = "Typing..."
                self.send(message=Message(text=reply1), thread_id=thread_id, thread_type=thread_type)
                try:
                    ask2 = get_gemini_response(question)
                    ask2_text = ask2['response']
                    reply = f"𝗚𝗲𝗺𝗶𝗻𝗶 𝗔𝗶:\n\n{ask2_text}\n\n\n"
                    reply += " dev: https://www.facebook.com/100025265961414"
                    self.send(message=Message(text=reply), thread_id=thread_id, thread_type=thread_type)
                except Exception as e:
                    error_reply = f"An error occurred: {str(e)}"
                    self.send(message=Message(text=error_reply), thread_id=thread_id, thread_type=thread_type)
                return
        except Exception as e:
            print("An error occurred:", str(e))

def rainbow_light_text_print(text, end='\n'):
    colors = [
        "\033[91m",  
        "\033[93m",  
        "\033[92m",  
        "\033[96m",  
        "\033[94m",  
        "\033[95m",  
    ]
    num_steps = len(colors)
    for i, char in enumerate(text):
        color_index = i % num_steps
        print(f"{colors[color_index]}{char}", end="")
    print("\033[0m", end=end)

def convert_cookie(session):
    return '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in session])

if __name__ == '__main__':
    with open('configuration.json') as f:
        configuration = json.load(f)
    try:
        form = {
            'adid': 'e3a395f9-84b6-44f6-a0ce-fe83e934fd4d',
            'email': str(configuration['CONFIG']['BOT_INFO']['EMAIL']),
            'password': str(configuration['CONFIG']['BOT_INFO']['PASSWORD']),
            'format': 'json',
            'device_id': '67f431b8-640b-4f73-a077-acc5d3125b21',
            'cpl': 'true',
            'locale': 'en_US',
            'client_country_code': 'US',
            'credentials_type': 'device_based_login_password',
            'generate_session_cookies': '1',
            'generate_analytics_claim': '1',
            'generate_machine_id': '1',
            'currently_logged_in_userid': '0',
            'irisSeqID': 1,
            'try_num': '1',
            'enroll_misauth': 'false',
            'meta_inf_fbmeta': 'NO_FILE',
            'source': 'login',
            'machine_id': 'KBz5fEj0GAvVAhtufg3nMDYG',
            'meta_inf_fbmeta': '',
            'fb_api_req_friendly_name': 'authenticate',
            'fb_api_caller_class': 'com.facebook.account.login.protocol.Fb4aAuthHandler',
            'api_key': '882a8490361da98702bf97a021ddc14d',
            'access_token': '181425161904154|95a15d22a0e735b2983ecb9759dbaf91'
        }

        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'x-fb-friendly-name': form['fb_api_req_friendly_name'],
            'x-fb-http-engine': 'Liger',
            'user-agent': str(ua_generator.generate())
        }

        url = 'https://b-graph.facebook.com/auth/login'
        response = requests.post(url, data=form, headers=headers)
        response_data = response.json()
        if "access_token" in response_data:
            access_token = response_data['access_token']
            cookie = convert_cookie(response_data['session_cookies'])
            key_value_pairs = [pair.strip() for pair in cookie.split(";")]
            session_cookies = {key: value for key, value in (pair.split("=") for pair in key_value_pairs)}
            rainbow_light_text_print("[ [ NAME ] ] Eeave Facebook Bot")
            rainbow_light_text_print("[ [ VERSION ] ] Version 1.0.0")
            time.sleep(0.5)
            rainbow_light_text_print("[ [ DESCRIPTION ] ] Eeave is a Messenger bot that interacts with people")
            if str(configuration['CONFIG']['BOT_INFO']['PREFIX']) == "" or " " in configuration['CONFIG']['BOT_INFO']['PREFIX'] or len(configuration['CONFIG']['BOT_INFO']['PREFIX']) != 1:
                sys.exit("\033[91m[ [ ERROR ] ] PLEASE CHECK THE PREFIX, PREFIX MUST HAVE VALUE AND DOESN'T HAVE SPACE AND ONLY ONE SYMBOL/LETTER. \033[0m")
            else:
                try:
                    bot = MessBot(' ', ' ', session_cookies=session_cookies)
                    rainbow_light_text_print("[ [ CONNECTING ] ] {}".format(str(bot.isLoggedIn()).upper()))
                except:
                    sys.exit("\033[91m[ [ ERROR ] ] FAILED TO CONNECT TO SERVER, TRY TO RERUN TO PROGRAM. \033[0m")
                try:
                    bot.listen()
                except:
                    bot.listen()
        else:
            rainbow_light_text_print("[ [ ERROR ] ] {}".format(str(response_data['error']['message'])))
    except requests.exceptions.ConnectionError:
        print("\033[1m\033[91mPLEASE CHECK YOUR INTERNET CONNECTION AND TRY AGAIN.\033[0m")
