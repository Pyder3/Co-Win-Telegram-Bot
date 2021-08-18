import shelve
import schedule
import telebot
import threading
import time
import requests
import datetime
import json
import os

# parameters = {'pincode': '834002', 'date': '06-08-2021'}
# response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin", params=parameters)
# print(json.loads(json.dumps(response.json(), sort_keys=True, indent=4))['sessions'])

no_of_days = 0
pin_code = 0
chat_id = ""
vaccine_type = ""
dose_type = ""
API_KEY = "1907675657:AAF88lFvp-bZcwz0QUKFH3ABdZYSM0SqSI0"
bot = telebot.TeleBot(API_KEY)

def dummy_func(message):
    dummy_message = message.text
    if "@VAX69420bot" in str(dummy_message):
        return True
    else:
        return False


def check_pin(message):
    request = message.text
    try:
        request = int(request)
        if len(str(request)) == 6:
            return True
        else:
            return False
    except:
        return False


def days_input(message):
    user_input = message.text
    try:
        user_input = int(user_input)
        return True
    except:
        return False


vaccine_name = ""


def brand_name(message):
    user_input = str(message.text)
    if user_input.casefold() == "covishield" or user_input.casefold() == "covaxin" or user_input.casefold() == "sputnik v" or user_input.casefold() == "all":
        return True
    else:
        return False


def dose(message):
    user_input = str(message.text)
    if user_input.casefold() == "first" or user_input.casefold() == "second" or user_input.casefold() == "both":
        return True
    else:
        return False


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Hey, {str(message.from_user.first_name)}, Welcome to VAN BOT!! Plss send the command /find_by_pin to begin!!")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "If you want to edit your preferences use the command /edit_details.\nIf you notice a bug, DM the admin at @vanbot_admin")



@bot.message_handler(commands=['find_by_pin', 'edit_details'])
def find_by_pin(message):
    bot.reply_to(message, "Please enter your pin code")


@bot.message_handler(func=check_pin)
def pin_param(message):
    global pin_code
    file = shelve.open("cust_data", flag='c')
    pin_code = str(message.text)
    file[str(message.chat.id)] = [pin_code, no_of_days, [], vaccine_type, dose_type]
    file.close()
    file = shelve.open("cust_data", flag='c')
    bot.send_message(message.chat.id, "How many days do you want to search for??")


@bot.message_handler(func=days_input)
def date_param(message):
    global chat_id
    global no_of_days
    file = shelve.open("cust_data", flag='c')
    no_of_days = int(message.text)
    chat_id = message.chat.id
    file[str(message.chat.id)] = [pin_code, no_of_days, [], vaccine_type, dose_type]
    file.close()
    file = shelve.open("cust_data", flag='c')
    bot.send_message(message.chat.id, "Enter the desired vaccine name (Covishield, Covaxin, Sputnik) and for no choice enter 'all'")


@bot.message_handler(func=brand_name)
def vaccine_name(message):
    file = shelve.open("cust_data", flag='c')
    global vaccine_type
    vaccine_type = str(message.text).casefold()
    file[str(message.chat.id)] = [pin_code, no_of_days, [], vaccine_type, dose_type]
    file.close()
    file = shelve.open("cust_data", flag='c')
    bot.send_message(message.chat.id, "If you wanna search for first dose, enter 'first', for second dose enter 'second' and for no filter enter 'both'")


@bot.message_handler(func=dose)
def fORs(message):
    global dose_type
    dose_type = str(message.text).casefold()
    file = shelve.open("cust_data", flag='c')
    file[str(message.chat.id)] = [pin_code, no_of_days, [], vaccine_type, dose_type]
    file.close()
    file = shelve.open("cust_data", flag='c')
    bot.send_message(message.chat.id, "Data recieved successfully!!")


@bot.message_handler(commands=["get_my_details"])
def fetch(message):
    file = shelve.open("cust_data", flag='r')
    bot.send_message(message.chat.id, f"Your pin code is {file[str(message.chat.id)][0]}\nYour are recieving notifications for {file[str(message.chat.id)][1]} days\nYour vaccine of choice is {file[str(message.chat.id)][3]}\nYou are searching for {file[str(message.chat.id)][4]} dose")
    file.close()


@bot.message_handler(commands=['end'])
def stop(message):
    file = shelve.open("cust_data", flag='r')
    del file[str(message.chat.id)]
    file.close()
    file = shelve.open("cust_data", flag='r')
    bot.send_message(message.chat.id, "You will no longer receive notifications!!")


# @bot.message_handler(func=dummy_func)
# def send_reply(message):
#     file = shelve.open("cust_data", flag='r')
#     for i in file[message.text][2]:
#         bot.send_message(int(str(message.text)[:-13]), i)
#     file.close()
#     bot.reply_to(message, "message recieved!!")
reply_date = ""

def send_reply():
    file = shelve.open("cust_data", flag='c')
    for p in list(file.keys()):
        if p != '' and len(str(file[p][0])) != 0 and len(str(file[p][1])) != 0 and len(str(file[p][3])) != 0 and len(str(file[p][4])) != 0:
            reply = []
            file = shelve.open("cust_data", flag='c')
            pin_code = file[p][0]
            no_of_days = file[p][1]
            vaccine_type = file[p][3]
            dose = file[p][4]
            # print(file[p])
            for l in range(no_of_days):
                today_date = f"{str(int(datetime.datetime.now().strftime('%d')) + l)}-{datetime.datetime.now().strftime('%m')}-{datetime.datetime.now().strftime('%Y')}"
                parameters = {'pincode': str(pin_code), 'date': today_date}
                response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin",
                                        params=parameters)
                req_data = json.loads(json.dumps(response.json()))
                # if len(req_data['sessions']) != 0:
                Total_available_centres = 0
                for i in range(len(req_data['sessions'])):
                    if (dose == "both" and (req_data['sessions'][i]['available_capacity_dose1'] != 0 or req_data['sessions'][i]['available_capacity_dose2'] != 0)) or (dose == "first" and req_data['sessions'][i]['available_capacity_dose1'] != 0) or (dose == "second" and req_data['sessions'][i]['available_capacity_dose2'] != 0):
                        if req_data['sessions'][i]['vaccine'].casefold() == vaccine_type or vaccine_type == "all":
                            reply.append(f"{req_data['sessions'][i]['name']}\nAvailable first doses : {req_data['sessions'][i]['available_capacity_dose1']}\nAvailable second doses : {req_data['sessions'][i]['available_capacity_dose2']}\nVaccine Avaialable : {req_data['sessions'][i]['vaccine']}\nCost of vaccine : {req_data['sessions'][i]['fee']}\nDate : {req_data['sessions'][i]['date']}\n")
                            # bot.send_message(chat_id, reply)
                            Total_available_centres += 1
                if Total_available_centres == 0:
                    # bot.send_message(chat_id, f"No vaccine centres available for booking on {today_date}")
                    reply.append(f"No vaccine centres available for booking on {today_date}")
            if str(file[p][2]) != str(reply):
                file[p] = [pin_code, no_of_days, reply, vaccine_type, dose]
                file.close()
                file = shelve.open("cust_data", flag='c')
                if len(str(p)) != 0:
                    bot.send_message(int(p), "SLOTS UPDATED!!!!")
                    for k in file[p][2]:
                        # bot.send_message(int(p), f"Following is the list of centres avaiable on {} in pin code {pin_code}")
                        bot.send_message(int(p), k)
                        print(k)
                        print(pin_code)
                    bot.send_message(int(p), "To book a slot, log on to https://selfregistration.cowin.gov.in")


schedule.every(15).seconds.do(send_reply)


def forever():
    while True:
        schedule.run_pending()
        time.sleep(1)


t1 = threading.Thread(target=forever)
t1.start()


def polling_thread():
    while True:
        try:
            bot.polling(none_stop=False)
        except Exception:
            time.sleep(15)


t2 = threading.Thread(target=polling_thread)
t2.start()
