import json
import requests
# import telegram_send
import telebot
import datetime

# parameters = {'pincode': '834002', 'date': '06-08-2021'}
# response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin", params=parameters)
# print(json.loads(json.dumps(response.json(), sort_keys=True, indent=4))['sessions'])


API_KEY = '1907675657:AAF88lFvp-bZcwz0QUKFH3ABdZYSM0SqSI0'
bot = telebot.TeleBot(API_KEY)


def check_pin(message):
    request = message.text
    try:
        request = int(request)
        return True
    except:
        return False


def date_input(message):
    user_input = message.text
    day = user_input[0:2]
    month = user_input[3:5]
    year = user_input[6:]
    try:
        day = int(day)
        month = int(month)
        year = int(year)
        if day <= 31 and month <= 12 and year == 2021:
            return True
        else:
            return False
    except:
        return False


@bot.message_handler(commands=['find_by_pin'])
def find_by_pin(message):
    bot.reply_to(message, "Please enter your pin code")

@bot.message_handler(func=check_pin)
def pin_param(message):
    for p in range(2):
        today_date = f"{str(int(datetime.datetime.now().strftime('%d')) + p)}-{datetime.datetime.now().strftime('%m')}-{datetime.datetime.now().strftime('%Y')}"
        parameters = {'pincode': str(message.text), 'date': today_date}
        response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin",
                                params=parameters)
        req_data = json.loads(json.dumps(response.json()))
        bot.send_message(message.chat.id,
                         f"Following is the list of centres avaiable on {today_date} in pin code {message.text}")
        # if len(req_data['sessions']) != 0:
        Total_available_centres = 0
        for i in range(len(req_data['sessions'])):
            if req_data['sessions'][i]['available_capacity_dose1'] != 0 or req_data['sessions'][i]['available_capacity_dose2'] != 0:
                reply = f"{req_data['sessions'][i]['name']}\nAvailable first doses : {req_data['sessions'][i]['available_capacity_dose1']}\nAvailable second doses : {req_data['sessions'][i]['available_capacity_dose2']}\nVaccine Avaialable : {req_data['sessions'][i]['vaccine']}\nCost of vaccine : {req_data['sessions'][i]['fee']}\nDate : {req_data['sessions'][i]['date']}"
                bot.send_message(message.chat.id, reply)
                Total_available_centres += 1
        if Total_available_centres == 0:
            bot.send_message(message.chat.id, f"No vaccine centres available for booking on {today_date}")
        # else:
        #     bot.send_message(message.chat.id, f"No vaccine centres available for booking on {today_date}")


bot.polling()
