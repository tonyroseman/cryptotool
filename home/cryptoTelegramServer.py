import json
import time
import datetime

from telethon import TelegramClient

import threading
import mysql.connector

import telebot

# BOT_TOKEN = os.environ.get('BOT_TOKEN')


BOT_TOKEN = '6357010806:AAFXURf1_y1SV-xBH3KLdjGCUGgo6Tz7Mzk'
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    username = message.from_user.username
    bot.reply_to(message, f"{username}, Your Telegram notificaion function is activated. Thank you!")
    set_tlgactive(username)
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    username = message.from_user.username
    bot.reply_to(message, message.text)

def set_tlgactive(tlgname):
    cnx = connect_mysql()
    cursor = cnx.cursor()

    query = "SELECT * FROM home_telegramlist WHERE data=%s;"
    params = ("https://t.me/" + tlgname,)
    cursor.execute(query, params)
    result = cursor.fetchall()
    
    if(len(result) == 0):
        created_on=datetime.datetime.utcnow()
        add_data = ("INSERT INTO home_telegramlist "
                    "(data, created_on) "
                    "VALUES (%(data)s, %(created_on)s)")
        values = {'data': "https://t.me/" + tlgname, 'created_on': created_on}
        cursor.execute(add_data, values)
        cnx.commit()

    query = "SELECT * FROM home_customuser WHERE telegram = %s;"
    params = ("https://t.me/" + tlgname,)
    cursor.execute(query,params)
    result = cursor.fetchall()
    
    if(len(result) > 0):
        for user in result:
            query = """
                        UPDATE home_customuser
                        SET tlgactive = 1
                        WHERE id = %(id)s
                    """
            values = {'id': user[0]}
            cursor.execute(query, values)
            cnx.commit()

def get_user_info(user_id):
    cnx = connect_mysql()
    cursor = cnx.cursor()
    query = "SELECT * FROM home_customuser WHERE id = %s;"
    params = (user_id,)
    cursor.execute(query,params)
    result = cursor.fetchall()
    
    if(len(result) > 0):
        column_names = [desc[0] for desc in cursor.description]
        telegram_index = column_names.index('telegram')
        limit_index = column_names.index('limitcount')
        tlgact_index = column_names.index('tlgactive')
        if(int(result[0][tlgact_index]) == 1):
            cursor.close()
            return result[0], telegram_index, limit_index
        

    cursor.close()
    return None, None, None
def save_notifydata(user_id, data):
    cnx = connect_mysql()
    cursor = cnx.cursor()
    created_on=datetime.datetime.utcnow()
    add_data = ("INSERT INTO home_usernotifydata "
                    "(data, created_on, userid_id) "
                    "VALUES (%(data)s, %(created_on)s, %(userid_id)s)")
    values = {'data': str(data), 'created_on': created_on, 'userid_id': user_id}
    

    cursor.execute(add_data, values)
    cnx.commit()
    cursor.close()
    return None

def get_notifydatas():
    cnx = connect_mysql()
    cursor = cnx.cursor()
    
    query = "SELECT * FROM home_usernotifydata WHERE status = 0;"
    cursor.execute(query)
    result = cursor.fetchall()
    
    ret = []
    if(len(result) > 0):

        for notifydata in result:

            id = notifydata[0]
            user_id = notifydata[3]
            message = notifydata[1]
            
            userinfo, telegram_index, limit_index = get_user_info(user_id)
            if(userinfo is not None):
                
                notifydataobj = {}
                notifydataobj['user_id'] = user_id
                notifydataobj['message'] = message
                notifydataobj['telegram'] = userinfo[telegram_index]
                notifydataobj['id'] = id
                ret.append(notifydataobj)
            
    cursor.close()
    return ret

def get_tlg_users():
    cnx = connect_mysql()
    cursor = cnx.cursor()
    query = "SELECT * FROM home_usersettingsdata"
    
    cursor.execute(query)
    result = cursor.fetchall()
    userresult = []
    if(len(result) > 0):
        for usersetting in result:
            settingsdata = str(usersetting[1])
            
            data = json.loads(settingsdata[2:len(settingsdata)-1].replace("'", "\""))
            
            if data['tlg'] == '1':
                userresult.append(usersetting)
        
    cursor.close()
    if(len(usersetting) > 0):
        return userresult
    else:
        return None
def get_current_coindatas():
    cnx = connect_mysql()
    cursor = cnx.cursor()
    
    query = "SELECT * FROM home_coindata "
    cursor.execute(query)
    result = cursor.fetchall()
    if(len(result) > 0):
        column_names = [desc[0] for desc in cursor.description]
        coindataindex = column_names.index('data')
        cursor.close()
        return result, coindataindex
    cursor.close()
    return None, None

def get_coins_of_user(coindatas, usersettings, coindataindex):
    returns = []
    
    usersettingsdata = str(usersettings[1])
    settings = json.loads(usersettingsdata[2:len(usersettingsdata)-1].replace("'", "\""))
    count = len(settings.keys())-2
    for coin in coindatas:
        coindata = str(coin[coindataindex])
        data = json.loads(coindata[2:len(coindata)-1].replace("'", "\""))
        
        ok_count = 0
        rowflag = False
        for key in settings.keys():
            if key != 'tlg' and key[0:1] != 't' and key != 'mc' and key!='coins':
                operand = int(settings[key])
                flag = False
                if(key in data):
                    if operand == 1:
                        flag = data[key] > float(settings['t' + key])
                    elif operand == 2:
                        flag = data[key] < float(settings['t' + key])
                    elif operand == 3:
                        flag = data[key] >= float(settings['t' + key])
                    elif operand == 4:    
                        flag = data[key] <= float(settings['t' + key])

                if(flag):
                    
                    ok_count+=1
            if (key == 'mc'):
                operand = int(settings[key])
                flag = False
                if(key in data):
                    if operand == 1:
                        flag = data[key] > float(settings['t' + key])
                    elif operand == 2:
                        flag = data[key] < float(settings['t' + key])
                    elif operand == 3:
                        flag = data[key] >= float(settings['t' + key])
                    elif operand == 4:    
                        flag = data[key] <= float(settings['t' + key])

                if(flag):
                    
                    ok_count+=1
        
        
        if(ok_count == count/2):
            returns.append(data)
    if(len(returns) > 0):
        return returns
    else:
        return None
def get_notify_peroid():
    cnx = connect_mysql()
    cursor = cnx.cursor()
    
    query = "SELECT * FROM home_systemsettingsdata "
    cursor.execute(query)
    result = cursor.fetchall()
    if(len(result) > 0):
        try:
            syssettingsdata = str(result[0][1])
            settings = json.loads(syssettingsdata[2:len(syssettingsdata)-1].replace("'", "\""))
            
            cursor.close()
            return int(settings['tlgperiod'])*60
        except KeyError:
            cursor.close()
            return 60*10
    
    cursor.close()
    return 60*10
def make_message(data):
    message = "This " + data['symbol'] + " matched all settings.\n"
    # for key in data.keys():
    #     if key != 'symbol':
    #         message = message + key + ": " + str(data[key]) + "\n"
    return message
async def start_server(client):
    print('Telegram Server Start')
    tlg_user_coindata = {}
    
    while True:
        tlg_users = get_tlg_users()
        limitseconds = get_notify_peroid()
        if (tlg_users is not None):
            cur_coindatas, coindataindex = get_current_coindatas()
            if cur_coindatas is not None:
                for user in tlg_users:
                    userinfo,telegram_index, limit_index = get_user_info(user[2])
                    if(userinfo is not None):
                        coindatas = get_coins_of_user(cur_coindatas[0:int(userinfo[limit_index])], user, coindataindex)
                        if coindatas is not None:
                            
                            recipient_username = userinfo[telegram_index]
                            rcp = recipient_username
                            if(rcp != ""):
                                
                                
                                for coin in coindatas:
                                    message = make_message(coin)
                                    if rcp in tlg_user_coindata:
                                        user_data = tlg_user_coindata[rcp]
                                        if coin['symbol'] in user_data:
                                            coin_data = user_data[coin['symbol']]
                                            time_difference = datetime.datetime.now() - coin_data['time']
                                            if(time_difference.total_seconds() > limitseconds):
                                                await client.send_message(rcp, message)
                                                save_notifydata(userinfo[0],coin)
                                                new_coin_data = {}
                                                new_coin_data['data'] = coin
                                                new_coin_data['time'] = datetime.datetime.now()                                        
                                                user_data[coin['symbol']] = new_coin_data
                                                tlg_user_coindata[rcp] = user_data
                                                print(coin['symbol'])
                                            else:
                                                print(coin['symbol'], time_difference.total_seconds())
                                        else:
                                            await client.send_message(rcp, message)
                                            save_notifydata(userinfo[0],coin)
                                            new_coin_data = {}
                                            new_coin_data['data'] = coin
                                            new_coin_data['time'] = datetime.datetime.now()                                        
                                            user_data[coin['symbol']] = new_coin_data
                                            tlg_user_coindata[rcp] = user_data
                                            print(coin['symbol'])    
                                        
                                    else:
                                        await client.send_message(rcp, message)
                                        save_notifydata(userinfo[0],coin)
                                        new_coin_data = {}
                                        new_coin_data['data'] = coin
                                        new_coin_data['time'] = datetime.datetime.now()
                                        new_user_data = {}
                                        new_user_data[coin['symbol']] = new_coin_data
                                        tlg_user_coindata[rcp] = new_user_data
                                        print(coin['symbol'])
                                        time.sleep(3)
                                        
                                        
                                    # update_notifydata(notify['id'])
                            
        time.sleep(5)
        
 
def connect_mysql():
     cnx = mysql.connector.connect(user='root', password='root',
                                host='127.0.0.1',
                                database='cryptoadmin')
     return cnx
def start_bot():
    bot.polling()

class telegramServer():

    def startServer(self):
        api_id = 20557393
        api_hash = '7d9060762cc54b56f5851c1069bf3dab'
        client = TelegramClient('anon', api_id, api_hash)
        bot_thread = threading.Thread(target=start_bot)
        bot_thread.start()
        with client:
            client.loop.run_until_complete(start_server(client))


telegramserver = telegramServer()
telegramserver.startServer()



