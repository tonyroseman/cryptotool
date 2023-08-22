import requests
from datetime import datetime, timedelta
import threading
import time
import json
from telethon import TelegramClient
import asyncio

from datetime import date, datetime, timedelta
import mysql.connector
import os

import telebot

# BOT_TOKEN = os.environ.get('BOT_TOKEN')
api_id = 20557393
api_hash = '7d9060762cc54b56f5851c1069bf3dab'

BOT_TOKEN = '6357010806:AAFXURf1_y1SV-xBH3KLdjGCUGgo6Tz7Mzk'
bot = telebot.TeleBot(BOT_TOKEN)
client = TelegramClient('anon', api_id, api_hash)
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)
def connect_mysql():
    
    cnx = mysql.connector.connect(user='root', password='root',
                                host='127.0.0.1',
                                database='cryptoadmin')
    return cnx
def insert_coindata(cnx, data, created_on=datetime.utcnow()):
    cursor = cnx.cursor()
    add_coindata = ("INSERT INTO home_coindata "
               "(data, created_on) "
               "VALUES (%(data)s, %(created_on)s)")

    # Insert salary information
    coindata = {
        'data': data,
        'created_on': created_on,
        }
    # Insert new employee
    cursor.execute(add_coindata, coindata)
    cnx.commit()
    cursor.close()
    print(created_on)
def insert_volumedata(cnx, data, created_on=datetime.utcnow()):
    cursor = cnx.cursor()
    add_volumedata = ("INSERT INTO home_volumedata "
               "(data, created_on) "
               "VALUES (%(data)s, %(created_on)s)")

    # Insert salary information
    volumedata = {
        'data': data,
        'created_on': created_on,
        }
    # Insert new employee
    cursor.execute(add_volumedata, volumedata)
    cnx.commit()
    cursor.close()
def insert_candledata(cnx, data, created_on=datetime.utcnow()):
    cursor = cnx.cursor()
    add_candledata = ("INSERT INTO home_candledata "
               "(data, created_on) "
               "VALUES (%(data)s, %(created_on)s)")

    # Insert salary information
    candledata = {
        'data': data,
        'created_on': created_on,
        }
    # Insert new employee
    cursor.execute(add_candledata, candledata)
    cnx.commit()
    cursor.close()
def insert_candlehourdata(cnx, data, created_on=datetime.utcnow()):
    cnx = connect_mysql()
    cursor = cnx.cursor()
    
    
    idkeys = data.keys()

    # Print the keys
    for coin_id in idkeys:
        cid = coin_id[3:]
        # Insert salary information
        candlehourdata = {
            'coin_id': int(cid),
            'data': str(data[coin_id]),
            'created_on': created_on,
            }
        query = f"SELECT * FROM home_candlehourdata WHERE coin_id = {int(cid)}"
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) > 0:
            
            candledata = str(result[0][2])
            
            # print(candledata)    
            rowdata = json.loads(candledata[2:len(candledata)-1].replace("'", "\"").replace("None","0.0"))

            open_prices = rowdata['open_price']
            close_prices = rowdata['close_price']
            volumes = rowdata['volume']
            if(len(data[coin_id]['open_price']) > 1):
                open_prices = data[coin_id]['open_price']
                close_prices = data[coin_id]['close_price']
                volumes = data[coin_id]['volume']
            elif len(data[coin_id]['open_price']) == 1:
                
                open_prices.insert(0,data[coin_id]['open_price'][0])   
                close_prices.insert(0,data[coin_id]['close_price'][0])   
                volumes.insert(0,data[coin_id]['volume'][0])
                open_prices = open_prices[0:24*14]
                close_prices = close_prices[0:24*14]
                volumes = volumes[0:24*14]
            else:
                open_prices = data[coin_id]['open_price']
                close_prices = data[coin_id]['close_price']
                volumes = data[coin_id]['volume']
            rowdata['open_price'] = open_prices
            rowdata['close_price'] = close_prices
            rowdata['volume'] = volumes
            query = """
                UPDATE home_candlehourdata
                SET data = %(data)s, created_on = %(created_on)s
                WHERE coin_id = %(coin_id)s
            """
            values = {'data': str(rowdata), 'created_on': created_on, 'coin_id': int(cid)}
            cursor.execute(query, values)
        
        else:
            add_candlehourdata = ("INSERT INTO home_candlehourdata "
               "(coin_id, data, created_on) "
               "VALUES (%(coin_id)s,%(data)s, %(created_on)s)")
            # Insert new employee
            cursor.execute(add_candlehourdata, candlehourdata)
        cnx.commit()
    cursor.close()
    
def get_coindata(symbol,coindata):
    
    allcoins = json.loads(coindata)
    for coin in allcoins:
        if coin['symbol'] == symbol:
            return coin
    return None
def get_coindatas(cnx, now,deltamin):
    
    cursor = cnx.cursor()
    target_time = now - timedelta(minutes=deltamin)
    query = "SELECT data FROM home_coindata WHERE YEAR(created_on) = %s AND MONTH(created_on) = %s AND DAY(created_on) = %s AND HOUR(created_on) = %s AND MINUTE(created_on) = %s ORDER BY created_on ASC LIMIT 1;"
    cursor.execute(query, (target_time.year, target_time.month, target_time.day, target_time.hour, target_time.minute))
    ret = None
    for (coin_data) in cursor:
        ret = str(coin_data)[3:]
        ret = ret[:len(ret)-3]
        ret = ret.replace("'", "\"").replace("\\", "_")
        break
    cursor.close()
    return ret

def get_volumedata(cnx):
    cursor = cnx.cursor()
    query = "SELECT data FROM home_volumedata ORDER BY created_on ASC LIMIT 1;"
    cursor.execute(query)
    ret = None
    for (vol_data) in cursor:
        ret = str(vol_data)[3:]
        ret = ret[:len(ret)-3]
        ret = ret.replace("'", "\"").replace("\\", "_")
        break
    cursor.close()
    return ret
def save_candlehour_data():
    history_api_key = '27c91633-22a0-4dbb-a4f1-149cd19adff8'
    
    ids, symbols, datas = get_coinMap()
    
    
    
    first  = 0
    candlecount = 0
    while(True):
        if first == 0:
            candlecount = 1 #14*24
        else:
            candlecount = 1
        now = datetime.utcnow()
        print("start save_candle" + "-----" + str(now))
        cnx = connect_mysql()
        url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/ohlcv/historical'
        if cnx is not None:
            
            now = datetime.utcnow()
            
            start_time = now - timedelta(hours=candlecount)
            start_timestamp = start_time.isoformat()
            for i in range(int(len(ids)/10)+1):
                ids_stringall = ','.join(map(str, ids[i*10:min((i+1)*10, len(ids))]))
                # Parameters for the API request
                parameters = {
                    'id': ids_stringall,  # Symbol of the cryptocurrency
                    'time_period':'hourly',
                    'interval': '1h',  # Time interval (1h, 1d, etc.)
                    'convert': 'USD',  # Convert prices to the specified currency
                    'count' : candlecount,
                }
                
                # Add your API key to the request headers
                headers = {
                    'X-CMC_PRO_API_KEY': history_api_key
                }
                
                # Send API request
                response = requests.get(url, headers=headers, params=parameters)
                
                # Check if the request was successful
                if response.status_code == 200:
                    # Retrieve the data from the response
                    data = response.json()
                    
                    # Extract the candle data for the desired time period (14 days)
                    candle_data = data['data']
                    # candles = candle_data['quotes']
                    
                    # Process the candle data as needed
                    for coin_id, coin_candles in candle_data.items():
                        candles = coin_candles['quotes']
                        
                        for candle in candles:
                            
                            
                            volume = candle['quote']['USD']['volume']
                            data = datas['id_' + str(coin_id)]
                            data['open_price'].insert(0,(candle['quote']['USD']['open']))
                            data['close_price'].insert(0,candle['quote']['USD']['close'])
                        
                            data['volume'].insert(0,volume)
                            datas['id_' + str(coin_id)] = data

                        
                else:
                    print('Error:', response.status_code)
                time.sleep(5)
            insert_candlehourdata(cnx=cnx,data=datas,created_on=now)
            now = datetime.utcnow()
            print("end save_candle" + "-----" + str(now))
            first = 1
            time.sleep(60*60)
    
    
def get_coinMap():
    free_api_key = '27c91633-22a0-4dbb-a4f1-149cd19adff8'
    
    # CoinMarketCap API endpoint
    base_url = "https://pro-api.coinmarketcap.com/v1/"
    url = base_url + 'cryptocurrency/listings/latest'
    stable_coins = ['USDT', 'USDC', 'DAI', 'BUSD', 'TUSD', 'USDD', 'USDP', 'GUSD', 'USTC', 'FRAX', 'FDUSD', 'USDJ', 'LUSD', 'TRIBE', 'EURS', 'USDX', 'VAI', 'EUROC', 'XSGD', 'CUSD', 'EURt', 'SUSD', 'FEI', 'RSV', 'USDK', 'SBD', 'OUSD', 'GYEN', 'KRT', 'CEUR', 'BIDR', 'HUSD', 'IDRT', 'DJED', 'ZUSD', 'EOSDT', 'BAC', 'ESD', 'USDP', 'AGEUR', 'USDZ', 'GHO', 'BRZ', 'MIM', 'xDAI', 'DUSD', 'HAY', 'DOLA', 'MIMATIC', 'BITCNY', 'USDH', 'IST', 'JPYC', 'PAR', 'TRYB', 'USDs', 'WEMIX$', 'mCUSD', 'DUSD', 'WANUSDT', 'PYUSD', 'ONC', 'XCHF', 'MTR', 'CUSD', 'DAI+', 'TOR', 'mCEUR', 'XSTUSD', 'USX', 'JPYC', 'MUSD', 'MXNt', 'DGX', 'USDB', 'BRCP', 'USDS', 'USDEX', 'USDR', 'QCAD', 'CUSDT', 'YUSD', 'FUSD', 'XUSD', 'IRON', 'FUSD', 'DGD', 'KBC', 'DPT', '1GOLD', 'MUSD', 'CADC', 'XIDR', 'STATIK', 'MONEY', 'USN', 'BITUSD', 'USNBT', 'BITGOLD', 'BITEUR','HGT', 'QC', 'ITL', 'USDS', 'CONST', 'USDQ', 'XEUR', 'BGBP', 'EBASE', 'BKRW', 'USDEX', 'USDL', 'UETH', 'vUSDT', 'vUSDC', 'vBUSD', 'BVND', 'BSD', 'DSD', 'SAC', 'vDAI', 'USDEX', 'ZUSD', 'USDFL', 'MDS', 'MDO', 'ALUSD', 'FLOAT', 'fUSDT', 'FLUSD', 'SEUR', 'ARTH', 'USDAP', 'BEAN', 'COFFIN', 'COUSD', 'DUSD', 'nUSD', 'XUSD', 'AUSD', 'fUSDT', 'H2O', 'IUSDS', 'ONEICHI', 'USDI', 'GBPT', 'EUROS', 'SBC']
    stable_coin_map = {}
    for stable_coin in stable_coins:
        stable_coin_map[stable_coin] = 1
    params = {
        'start': 1,
        'limit': 1000,
        'convert': 'USD',
        
    }
    headers = {
        'X-CMC_PRO_API_KEY': free_api_key
    }
    
    response = requests.get(url, params=params, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Retrieve the data from the response
        data = response.json()

        # Extract the coin details (ID and symbol)
        coins = data['data']

        # Process the coin details as needed
        ids = []
        symbols = []
        datas = {}
        for coin in coins:
            if stable_coin_map.get(coin['symbol']) is None:

                ids.append(coin['id'])
                symbols.append(coin['symbol'])    
                data = {}
                data['symbol'] = coin['symbol']
                data['open_price'] = []
                data['close_price'] = []                
                data['volume'] = []
                datas['id_' + str(coin['id'])] = data

        return ids, symbols, datas     
    else:
        print('Error:', response.status_code)
def delete_coin():
    cnx = connect_mysql()
    cursor = cnx.cursor()
    query = "DELETE FROM home_coindata WHERE created_on < NOW() - INTERVAL 30 MINUTE;"
    cursor.execute(query)
    cursor.close()
def delete_coindata():
    while(True):
        delete_coin()
        time.sleep(20*60)
def get_user_info(user_id):
    cnx = connect_mysql()
    cursor = cnx.cursor()
    query = "SELECT * FROM home_customuser WHERE id = %s;"
    params = (user_id,)
    cursor.execute(query,params)
    result = cursor.fetchall()
    
    if(len(result) > 0):
        cursor.close()
        return result[0]
    cursor.close()
    return None
def update_notifydata(id):
    cnx = connect_mysql()
    cursor = cnx.cursor()
    
    query = "UPDATE home_usernotifydata SET status = 1 WHERE id = %s"
    params = (id,)

    cursor.execute(query, params)
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
            
            userinfo = get_user_info(user_id)
            if(userinfo is not None):
                
                notifydataobj = {}
                notifydataobj['user_id'] = user_id
                notifydataobj['message'] = message
                notifydataobj['telegram'] = userinfo[11]
                notifydataobj['id'] = id
                ret.append(notifydataobj)
            
    cursor.close()
    return ret
async def start_bot():
    start_thread()
    print('Bot Start')
    
    while(True):
        notifydtas = get_notifydatas()
        
        for notify in notifydtas:
            recipient_username = notify['telegram']
            message = str(notify['message'])
            message = message[2:len(message)-1]
            print(message)
            await client.send_message(recipient_username, message.replace("<br>","\n"))
            update_notifydata(notify['id'])
            time.sleep(3)
        time.sleep(5)
def save_coindata():
    api_keys = ['8c4befae-ef2c-4613-a156-ef8024d95461','27c91633-22a0-4dbb-a4f1-149cd19adff8','157e0cb6-b422-40ea-8fa2-eb77c3b0c5fd','9847eba5-a2f4-435a-8800-26aeaab6036d','57eb3750-0113-44a3-8530-fcf2c64d3f8e','02d3c3a8-da3f-4a33-abbb-936bcd251106']
    # api_key = '27c91633-22a0-4dbb-a4f1-149cd19adff8'
    cnx = connect_mysql()
    stable_coins = ['USDT', 'USDC', 'DAI', 'BUSD', 'TUSD', 'USDD', 'USDP', 'GUSD', 'USTC', 'FRAX', 'FDUSD', 'USDJ', 'LUSD', 'TRIBE', 'EURS', 'USDX', 'VAI', 'EUROC', 'XSGD', 'CUSD', 'EURt', 'SUSD', 'FEI', 'RSV', 'USDK', 'SBD', 'OUSD', 'GYEN', 'KRT', 'CEUR', 'BIDR', 'HUSD', 'IDRT', 'DJED', 'ZUSD', 'EOSDT', 'BAC', 'ESD', 'USDP', 'AGEUR', 'USDZ', 'GHO', 'BRZ', 'MIM', 'xDAI', 'DUSD', 'HAY', 'DOLA', 'MIMATIC', 'BITCNY', 'USDH', 'IST', 'JPYC', 'PAR', 'TRYB', 'USDs', 'WEMIX$', 'mCUSD', 'DUSD', 'WANUSDT', 'PYUSD', 'ONC', 'XCHF', 'MTR', 'CUSD', 'DAI+', 'TOR', 'mCEUR', 'XSTUSD', 'USX', 'JPYC', 'MUSD', 'MXNt', 'DGX', 'USDB', 'BRCP', 'USDS', 'USDEX', 'USDR', 'QCAD', 'CUSDT', 'YUSD', 'FUSD', 'XUSD', 'IRON', 'FUSD', 'DGD', 'KBC', 'DPT', '1GOLD', 'MUSD', 'CADC', 'XIDR', 'STATIK', 'MONEY', 'USN', 'BITUSD', 'USNBT', 'BITGOLD', 'BITEUR','HGT', 'QC', 'ITL', 'USDS', 'CONST', 'USDQ', 'XEUR', 'BGBP', 'EBASE', 'BKRW', 'USDEX', 'USDL', 'UETH', 'vUSDT', 'vUSDC', 'vBUSD', 'BVND', 'BSD', 'DSD', 'SAC', 'vDAI', 'USDEX', 'ZUSD', 'USDFL', 'MDS', 'MDO', 'ALUSD', 'FLOAT', 'fUSDT', 'FLUSD', 'SEUR', 'ARTH', 'USDAP', 'BEAN', 'COFFIN', 'COUSD', 'DUSD', 'nUSD', 'XUSD', 'AUSD', 'fUSDT', 'H2O', 'IUSDS', 'ONEICHI', 'USDI', 'GBPT', 'EUROS', 'SBC']
    stable_coin_map = {}
    for stable_coin in stable_coins:
        stable_coin_map[stable_coin] = 1
    i = 0
    if cnx is not None:
        
        while(True):
            i=i+1
            now = datetime.utcnow()
            print("start save_coin" + "-----" + str(now))
            
            
            base_url = "https://pro-api.coinmarketcap.com/v1/"
            url = base_url + 'cryptocurrency/listings/latest'
                
            params = {
                'start': 1,
                'limit': 1000,
                'convert': 'USD',
            
            }
            headers = {
                'X-CMC_PRO_API_KEY': api_keys[i%6]
            }
            
            response = requests.get(url, params=params, headers=headers)
            
            data = response.json()
            now = datetime.utcnow()
            
            
            top_coins = data['data']
            allcoins = {}
            
            
            no = 0
            
            for coin in top_coins:
                if stable_coin_map.get(coin['symbol']) is None:
                
                    coinobj = {}
                    coinobj['no'] = no+1                
                    coinobj['symbol'] = coin['symbol']
                    coinobj['price'] = round(coin['quote']['USD']['price'], 3)            
                    coinobj['market_cap'] = round(coin['quote']['USD']['market_cap']/1000000,5)
                    coinobj['volume'] = coin['quote']['USD']['volume_24h']
                    allcoins['id_' + str(coin['id'])] = coinobj
                    
                            
                    no+=1
                    if no > 1000:
                        break
            
            
            insert_coindata(cnx=cnx, data=str(allcoins),created_on=now)
            
            
            now = datetime.utcnow()
            
            print("end save_coin" + "----" + str(now))
            time.sleep(60)
def start_thread():
    # 
    # bot_thread = threading.Thread(target=start_bot)
    # bot_thread.start()
    # candle_thread = threading.Thread(target=save_candlehour_data)
    # candle_thread.start()
    coin_thread = threading.Thread(target=save_coindata)
    coin_thread.start()
    del_coin_thread = threading.Thread(target=delete_coindata)    
    del_coin_thread.start()

    # candle_thread.join()
    # coin_thread.join()
    # del_coin_thread.join()
    # bot_thread.join()
# save_coindata()
# bot.infinity_polling()
# start_thread()
with client:
    client.loop.run_until_complete(start_bot())


# start_thread()



