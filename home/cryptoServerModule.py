import requests
import datetime
import threading
import json
import time
import mysql.connector
import urllib.parse


class cryptoServerModule():
    is_running_as_server = False
    taskcount = 0
    all_candles = []
    
    thread_count =2
    timeout = 10
    all_symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'NEOUSDT', 'LTCUSDT', 'QTUMUSDT', 'ADAUSDT', 'XRPUSDT', 'EOSUSDT',  'XLMUSDT', 'ONTUSDT', 'TRXUSDT', 'ETCUSDT', 'ICXUSDT', 'NULSUSDT', 'VETUSDT', 'LINKUSDT', 'WAVESUSDT', 'ONGUSDT', 'HOTUSDT', 'ZILUSDT', 'ZRXUSDT', 'FETUSDT', 'BATUSDT', 'XMRUSDT', 'ZECUSDT', 'IOSTUSDT', 'CELRUSDT', 'DASHUSDT', 'OMGUSDT', 'THETAUSDT', 'ENJUSDT', 'MATICUSDT', 'ATOMUSDT', 'TFUELUSDT', 'ONEUSDT', 'FTMUSDT', 'ALGOUSDT', 'DOGEUSDT', 'DUSKUSDT', 'ANKRUSDT', 'WINUSDT', 'COSUSDT', 'MTLUSDT', 'TOMOUSDT', 'PERLUSDT', 'DENTUSDT', 'KEYUSDT', 'DOCKUSDT', 'WANUSDT', 'FUNUSDT', 'CVCUSDT', 'CHZUSDT', 'BANDUSDT', 'XTZUSDT', 'RENUSDT', 'RVNUSDT', 'HBARUSDT', 'NKNUSDT', 'STXUSDT', 'KAVAUSDT', 'ARPAUSDT', 'IOTXUSDT', 'RLCUSDT', 'CTXCUSDT', 'BCHUSDT', 'TROYUSDT', 'VITEUSDT', 'OGNUSDT', 'DREPUSDT', 'WRXUSDT', 'BTSUSDT', 'LSKUSDT', 'BNTUSDT', 'LTOUSDT', 'MBLUSDT', 'COTIUSDT', 'STPTUSDT', 'WTCUSDT', 'DATAUSDT', 'SOLUSDT', 'CTSIUSDT', 'HIVEUSDT', 'CHRUSDT', 'ARDRUSDT', 'MDTUSDT', 'STMXUSDT', 'KNCUSDT', 'LRCUSDT', 'PNTUSDT', 'COMPUSDT', 'SCUSDT', 'ZENUSDT', 'SNXUSDT', 'VTHOUSDT', 'DGBUSDT', 'SXPUSDT', 'MKRUSDT', 'DCRUSDT', 'STORJUSDT', 'MANAUSDT', 'YFIUSDT', 'BALUSDT', 'BLZUSDT', 'IRISUSDT', 'KMDUSDT', 'JSTUSDT', 'ANTUSDT', 'CRVUSDT', 'SANDUSDT', 'OCEANUSDT', 'NMRUSDT', 'DOTUSDT', 'LUNAUSDT', 'RSRUSDT', 'PAXGUSDT', 'WNXMUSDT', 'TRBUSDT', 'SUSHIUSDT', 'YFIIUSDT', 'KSMUSDT', 'EGLDUSDT', 'DIAUSDT', 'RUNEUSDT', 'FIOUSDT', 'UMAUSDT', 'BELUSDT', 'WINGUSDT', 'UNIUSDT', 'OXTUSDT', 'SUNUSDT', 'AVAXUSDT', 'FLMUSDT', 'ORNUSDT', 'UTKUSDT', 'XVSUSDT', 'ALPHAUSDT', 'AAVEUSDT', 'NEARUSDT', 'FILUSDT', 'INJUSDT', 'AUDIOUSDT', 'CTKUSDT', 'AKROUSDT', 'AXSUSDT', 'HARDUSDT', 'STRAXUSDT', 'UNFIUSDT', 'ROSEUSDT', 'AVAUSDT', 'XEMUSDT', 'SKLUSDT', 'GRTUSDT', 'JUVUSDT', 'PSGUSDT', '1INCHUSDT', 'REEFUSDT', 'OGUSDT', 'ATMUSDT', 'ASRUSDT', 'CELOUSDT', 'RIFUSDT', 'TRUUSDT', 'CKBUSDT', 'TWTUSDT', 'FIROUSDT', 'LITUSDT', 'SFPUSDT', 'DODOUSDT', 'CAKEUSDT', 'ACMUSDT', 'BADGERUSDT', 'FISUSDT', 'OMUSDT', 'PONDUSDT', 'DEGOUSDT', 'ALICEUSDT', 'LINAUSDT', 'PERPUSDT', 'SUPERUSDT', 'CFXUSDT', 'TKOUSDT', 'PUNDIXUSDT', 'TLMUSDT', 'BARUSDT', 'FORTHUSDT', 'BAKEUSDT', 'BURGERUSDT', 'SLPUSDT', 'SHIBUSDT', 'ICPUSDT', 'ARUSDT', 'POLSUSDT', 'MDXUSDT', 'MASKUSDT', 'LPTUSDT', 'XVGUSDT', 'ATAUSDT', 'GTCUSDT', 'ERNUSDT', 'KLAYUSDT', 'PHAUSDT', 'BONDUSDT', 'MLNUSDT', 'DEXEUSDT', 'C98USDT', 'CLVUSDT', 'QNTUSDT', 'FLOWUSDT', 'TVKUSDT', 'MINAUSDT', 'RAYUSDT', 'FARMUSDT', 'ALPACAUSDT', 'QUICKUSDT', 'MBOXUSDT', 'FORUSDT', 'REQUSDT', 'GHSTUSDT', 'WAXPUSDT', 'GNOUSDT', 'XECUSDT', 'ELFUSDT', 'DYDXUSDT', 'IDEXUSDT', 'VIDTUSDT', 'GALAUSDT', 'ILVUSDT', 'YGGUSDT', 'SYSUSDT', 'DFUSDT', 'FIDAUSDT', 'FRONTUSDT', 'CVPUSDT', 'AGLDUSDT', 'RADUSDT', 'BETAUSDT', 'RAREUSDT', 'LAZIOUSDT', 'CHESSUSDT', 'ADXUSDT', 'AUCTIONUSDT', 'DARUSDT', 'BNXUSDT', 'MOVRUSDT', 'CITYUSDT', 'ENSUSDT', 'KP3RUSDT', 'QIUSDT', 'PORTOUSDT', 'POWRUSDT', 'VGXUSDT', 'JASMYUSDT', 'AMPUSDT', 'PLAUSDT', 'PYRUSDT', 'RNDRUSDT', 'ALCXUSDT', 'SANTOSUSDT', 'MCUSDT', 'BICOUSDT', 'FLUXUSDT', 'FXSUSDT', 'VOXELUSDT', 'HIGHUSDT', 'CVXUSDT', 'PEOPLEUSDT', 'OOKIUSDT', 'SPELLUSDT', 'JOEUSDT', 'ACHUSDT', 'IMXUSDT', 'GLMRUSDT', 'LOKAUSDT', 'SCRTUSDT', 'API3USDT', 'ACAUSDT', 'XNOUSDT', 'WOOUSDT', 'ALPINEUSDT', 'TUSDT', 'ASTRUSDT', 'GMTUSDT', 'KDAUSDT', 'APEUSDT', 'BSWUSDT', 'BIFIUSDT', 'MULTIUSDT', 'STEEMUSDT', 'MOBUSDT', 'NEXOUSDT', 'REIUSDT', 'GALUSDT', 'LDOUSDT', 'EPXUSDT', 'OPUSDT', 'LEVERUSDT', 'STGUSDT', 'LUNCUSDT', 'GMXUSDT', 'POLYXUSDT', 'APTUSDT', 'OSMOUSDT', 'HFTUSDT', 'PHBUSDT', 'HOOKUSDT', 'MAGICUSDT', 'HIFIUSDT', 'RPLUSDT', 'PROSUSDT', 'AGIXUSDT', 'GNSUSDT', 'SYNUSDT', 'VIBUSDT', 'SSVUSDT', 'LQTYUSDT', 'AMBUSDT', 'USTCUSDT', 'GASUSDT', 'GLMUSDT', 'PROMUSDT', 'QKCUSDT', 'UFTUSDT', 'IDUSDT', 'ARBUSDT', 'LOOMUSDT', 'OAXUSDT', 'RDNTUSDT', 'WBTCUSDT', 'EDUUSDT', 'SUIUSDT', 'AERGOUSDT', 'PEPEUSDT', 'FLOKIUSDT', 'ASTUSDT', 'SNTUSDT', 'COMBOUSDT', 'MAVUSDT', 'PENDLEUSDT', 'ARKMUSDT', 'WBETHUSDT', 'WLDUSDT', 'SEIUSDT', 'CYBERUSDT']
    future_symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'NEOUSDT', 'LTCUSDT', 'QTUMUSDT', 'ADAUSDT', 'XRPUSDT', 'EOSUSDT',  'XLMUSDT', 'ONTUSDT', 'TRXUSDT', 'ETCUSDT', 'ICXUSDT', 'NULSUSDT', 'VETUSDT', 'LINKUSDT', 'WAVESUSDT', 'ONGUSDT', 'HOTUSDT', 'ZILUSDT', 'ZRXUSDT', 'FETUSDT', 'BATUSDT', 'XMRUSDT', 'ZECUSDT', 'IOSTUSDT', 'CELRUSDT', 'DASHUSDT', 'OMGUSDT', 'THETAUSDT', 'ENJUSDT', 'MATICUSDT', 'ATOMUSDT', 'TFUELUSDT', 'ONEUSDT', 'FTMUSDT', 'ALGOUSDT', 'DOGEUSDT', 'DUSKUSDT', 'ANKRUSDT', 'WINUSDT', 'COSUSDT', 'MTLUSDT', 'TOMOUSDT', 'PERLUSDT', 'DENTUSDT', 'KEYUSDT', 'DOCKUSDT', 'WANUSDT', 'FUNUSDT', 'CVCUSDT', 'CHZUSDT', 'BANDUSDT', 'XTZUSDT', 'RENUSDT', 'RVNUSDT', 'HBARUSDT', 'NKNUSDT', 'STXUSDT', 'KAVAUSDT', 'ARPAUSDT', 'IOTXUSDT', 'RLCUSDT', 'CTXCUSDT', 'BCHUSDT', 'TROYUSDT', 'VITEUSDT', 'OGNUSDT', 'DREPUSDT', 'WRXUSDT', 'BTSUSDT', 'LSKUSDT', 'BNTUSDT', 'LTOUSDT', 'MBLUSDT', 'COTIUSDT', 'STPTUSDT', 'WTCUSDT', 'DATAUSDT', 'SOLUSDT', 'CTSIUSDT', 'HIVEUSDT', 'CHRUSDT', 'ARDRUSDT', 'MDTUSDT', 'STMXUSDT', 'KNCUSDT', 'LRCUSDT', 'PNTUSDT', 'COMPUSDT', 'SCUSDT', 'ZENUSDT', 'SNXUSDT', 'VTHOUSDT', 'DGBUSDT', 'SXPUSDT', 'MKRUSDT', 'DCRUSDT', 'STORJUSDT', 'MANAUSDT', 'YFIUSDT', 'BALUSDT', 'BLZUSDT', 'IRISUSDT', 'KMDUSDT', 'JSTUSDT', 'ANTUSDT', 'CRVUSDT', 'SANDUSDT', 'OCEANUSDT', 'NMRUSDT', 'DOTUSDT', 'LUNAUSDT', 'RSRUSDT', 'PAXGUSDT', 'WNXMUSDT', 'TRBUSDT', 'SUSHIUSDT', 'YFIIUSDT', 'KSMUSDT', 'EGLDUSDT', 'DIAUSDT', 'RUNEUSDT', 'FIOUSDT', 'UMAUSDT', 'BELUSDT', 'WINGUSDT', 'UNIUSDT', 'OXTUSDT', 'SUNUSDT', 'AVAXUSDT', 'FLMUSDT', 'ORNUSDT', 'UTKUSDT', 'XVSUSDT', 'ALPHAUSDT', 'AAVEUSDT', 'NEARUSDT', 'FILUSDT', 'INJUSDT', 'AUDIOUSDT', 'CTKUSDT', 'AKROUSDT', 'AXSUSDT', 'HARDUSDT', 'STRAXUSDT', 'UNFIUSDT', 'ROSEUSDT', 'AVAUSDT', 'XEMUSDT', 'SKLUSDT', 'GRTUSDT', 'JUVUSDT', 'PSGUSDT', '1INCHUSDT', 'REEFUSDT', 'OGUSDT', 'ATMUSDT', 'ASRUSDT', 'CELOUSDT', 'RIFUSDT', 'TRUUSDT', 'CKBUSDT', 'TWTUSDT', 'FIROUSDT', 'LITUSDT', 'SFPUSDT', 'DODOUSDT', 'CAKEUSDT', 'ACMUSDT', 'BADGERUSDT', 'FISUSDT', 'OMUSDT', 'PONDUSDT', 'DEGOUSDT', 'ALICEUSDT', 'LINAUSDT', 'PERPUSDT', 'SUPERUSDT', 'CFXUSDT', 'TKOUSDT', 'PUNDIXUSDT', 'TLMUSDT', 'BARUSDT', 'FORTHUSDT', 'BAKEUSDT', 'BURGERUSDT', 'SLPUSDT', 'SHIBUSDT', 'ICPUSDT', 'ARUSDT', 'POLSUSDT', 'MDXUSDT', 'MASKUSDT', 'LPTUSDT', 'XVGUSDT', 'ATAUSDT', 'GTCUSDT', 'ERNUSDT', 'KLAYUSDT', 'PHAUSDT', 'BONDUSDT', 'MLNUSDT', 'DEXEUSDT', 'C98USDT', 'CLVUSDT', 'QNTUSDT', 'FLOWUSDT', 'TVKUSDT', 'MINAUSDT', 'RAYUSDT', 'FARMUSDT', 'ALPACAUSDT', 'QUICKUSDT', 'MBOXUSDT', 'FORUSDT', 'REQUSDT', 'GHSTUSDT', 'WAXPUSDT', 'GNOUSDT', 'XECUSDT', 'ELFUSDT', 'DYDXUSDT', 'IDEXUSDT', 'VIDTUSDT', 'GALAUSDT', 'ILVUSDT', 'YGGUSDT', 'SYSUSDT', 'DFUSDT', 'FIDAUSDT', 'FRONTUSDT', 'CVPUSDT', 'AGLDUSDT', 'RADUSDT', 'BETAUSDT', 'RAREUSDT', 'LAZIOUSDT', 'CHESSUSDT', 'ADXUSDT', 'AUCTIONUSDT', 'DARUSDT', 'BNXUSDT', 'MOVRUSDT', 'CITYUSDT', 'ENSUSDT', 'KP3RUSDT', 'QIUSDT', 'PORTOUSDT', 'POWRUSDT', 'VGXUSDT', 'JASMYUSDT', 'AMPUSDT', 'PLAUSDT', 'PYRUSDT', 'RNDRUSDT', 'ALCXUSDT', 'SANTOSUSDT', 'MCUSDT', 'BICOUSDT', 'FLUXUSDT', 'FXSUSDT', 'VOXELUSDT', 'HIGHUSDT', 'CVXUSDT', 'PEOPLEUSDT', 'OOKIUSDT', 'SPELLUSDT', 'JOEUSDT', 'ACHUSDT', 'IMXUSDT', 'GLMRUSDT', 'LOKAUSDT', 'SCRTUSDT', 'API3USDT', 'ACAUSDT', 'XNOUSDT', 'WOOUSDT', 'ALPINEUSDT', 'TUSDT', 'ASTRUSDT', 'GMTUSDT', 'KDAUSDT', 'APEUSDT', 'BSWUSDT', 'BIFIUSDT', 'MULTIUSDT', 'STEEMUSDT', 'MOBUSDT', 'NEXOUSDT', 'REIUSDT', 'GALUSDT', 'LDOUSDT', 'EPXUSDT', 'OPUSDT', 'LEVERUSDT', 'STGUSDT', 'LUNCUSDT', 'GMXUSDT', 'POLYXUSDT', 'APTUSDT', 'OSMOUSDT', 'HFTUSDT', 'PHBUSDT', 'HOOKUSDT', 'MAGICUSDT', 'HIFIUSDT', 'RPLUSDT', 'PROSUSDT', 'AGIXUSDT', 'GNSUSDT', 'SYNUSDT', 'VIBUSDT', 'SSVUSDT', 'LQTYUSDT', 'AMBUSDT', 'USTCUSDT', 'GASUSDT', 'GLMUSDT', 'PROMUSDT', 'QKCUSDT', 'UFTUSDT', 'IDUSDT', 'ARBUSDT', 'LOOMUSDT', 'OAXUSDT', 'RDNTUSDT', 'WBTCUSDT', 'EDUUSDT', 'SUIUSDT', 'AERGOUSDT', 'PEPEUSDT', 'FLOKIUSDT', 'ASTUSDT', 'SNTUSDT', 'COMBOUSDT', 'MAVUSDT', 'PENDLEUSDT', 'ARKMUSDT', 'WBETHUSDT', 'WLDUSDT', 'SEIUSDT', 'CYBERUSDT']
    interval_mh = ['1m','3m', '5m', '15m', '1h','4h']



    sub_array_size = 100
    step = 3
    
    def runServer(self):
        
        print("Server start")
        proxyurl, cmckeys, h1_downdelta_s, h1_updelta_s, m3_downdelta_s,m3_updelta_s, priceperiod, h1period, m3period, lsperiod, cmperiod  = get_sys_settings()


        proxies = proxyurl
        cmcapis = cmckeys

        cryptoServerModule.all_candles = make_all_candles()
        get_fundingRate(0,proxies)
        check_thread = threading.Thread(target=check_user)
        check_thread.start()
        if len(cmcapis) > 0:
            cmc_thread = threading.Thread(target=get_top_symbols_current)
            cmc_thread.start()
        else:
            print("cmc key is None")

        if len(proxies) > 0:
            
            binance_thread = threading.Thread(target=get_candles_mh)
            binance_thread.start()
            ls_thread = threading.Thread(target=get_longshortrate)
            ls_thread.start()
        else:
            print("Proxy is None")

        save_coin_thread = threading.Thread(target=save_coindatas)
        save_coin_thread.start()



def get_top_symbols_current():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    proxyurl,cmckeys, h1_downdelta_s, h1_updelta_s, m3_downdelta_s,m3_updelta_s, priceperiod, h1period, m3period, lsperiod, cmperiod  = get_sys_settings()
    
    ki = 0
    while True:

        parameters = {
            "start": 1,         # Start index of coins
            "limit": 1000,      # Number of coins to retrieve (max is 5000)
            "convert": "USD",   # Currency to convert prices and market caps to
        }

        headers = {
            "X-CMC_PRO_API_KEY": cmckeys[ki],
            "Accepts": "application/json",
        }
        try:
            
            # proxies = {'http': "socks5://myproxy:9191"}
            # socks5://14a6f067eab2a:d4516c8c50@178.253.215.162:12324
            response = requests.get(url, params=parameters, headers=headers)
            
           
            
            if response.status_code == 200:
                data = response.json()
                
                
                oneflag = 0
                for coin in data["data"]:
                    if(coin["symbol"] == "ONE"):
                        if oneflag == 1:
                            continue
                        else:
                            oneflag = 1
                    try:
                        sindex = cryptoServerModule.all_symbols.index(coin["symbol"]+"USDT")
                        if(sindex > -1):
                            
                            
                            
                            cryptoServerModule.all_candles[sindex]['symbol'] = coin["symbol"]
                            cryptoServerModule.all_candles[sindex]['price'] = coin["quote"]["USD"]["price"]
                            cryptoServerModule.all_candles[sindex]['market_cap'] = coin["quote"]["USD"]["market_cap"]/1000000
                            cryptoServerModule.all_candles[sindex]['vol_24h'] = coin["quote"]["USD"]["volume_24h"]/1000000
                            
                            cryptoServerModule.all_candles[sindex]['vol'] = coin["quote"]["USD"]["volume_change_24h"]
                            cryptoServerModule.all_candles[sindex]['vm'] = cryptoServerModule.all_candles[sindex]['vol_24h']/cryptoServerModule.all_candles[sindex]['market_cap']
                            
                            # all_candles[index] =volumedata
                    except ValueError:
                        continue
                ki = (ki+1)%len(cmckeys)
                # print("price : ",all_candles[0])
                time.sleep(priceperiod)
            else:
                save_err_log(response.status_code,"CoinMarketCap API - " + cmckeys[ki],"Failed to retrieve data.")
                print("Failed to retrieve data. Status code:", response.status_code)
                ki = (ki+1)%len(cmckeys)

        except requests.exceptions.ConnectTimeout:
            save_err_log("Exception","CoinMarketCap API - " + cmckeys[ki],"Connection timed out.")
            print("Connection timed out - get_data_from_cmc")
            time.sleep(30)    
        except requests.exceptions.RequestException as e:
            save_err_log("Exception","CoinMarketCap API - " + cmckeys[ki],f"An error occurred: RequestException")
            print(f"An error occurred: {e}")
            time.sleep(60)    
            
    # return all_candles
def make_all_candles():
    all_candles = []
    for symbol in cryptoServerModule.all_symbols:
        candel = {}
        candel['symbol'] = symbol[:len(symbol)-4]
        all_candles.append(candel)
    return all_candles
def save_coin(cnx,coin):
    
    created_on=datetime.datetime.utcnow()
    
    cursor = cnx.cursor()
    query = f"SELECT * FROM home_coindata WHERE symbol = '{coin['symbol']}'"
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) > 0:
        query = """
                UPDATE home_coindata
                SET data = %(data)s, created_on = %(created_on)s
                WHERE symbol = %(symbol)s
            """
        values = {'data': str(coin), 'created_on': created_on, 'symbol': coin['symbol']}
        cursor.execute(query, values)
    else:    

        add_coindata = ("INSERT INTO home_coindata "
                "(data, created_on, symbol) "
                "VALUES (%(data)s, %(created_on)s, %(symbol)s)")

        # Insert salary information
        coindata = {
            'data': str(coin),
            'created_on': created_on,
            'symbol': coin['symbol'],
            }
        # Insert new employee
        cursor.execute(add_coindata, coindata)
    cnx.commit()
    cursor.close()

def save_coindatas():
    while True:
        cnx = connect_mysql()
        
        updatequery = """
                        UPDATE home_coindata
                        SET data = %(data)s, created_on = %(created_on)s
                        WHERE symbol = %(symbol)s
                    """
        add_coindata = ("INSERT INTO home_coindata "
                        "(data, created_on, symbol) "
                        "VALUES (%(data)s, %(created_on)s, %(symbol)s)")
        updaterow = []
        insertrow = []
        cursor = cnx.cursor()
        for coindata in cryptoServerModule.all_candles:
            created_on=datetime.datetime.utcnow()
            # save_coin(cnx,coindata)# print(coindata_obj)   

            
            query = f"SELECT * FROM home_coindata WHERE symbol = '{coindata['symbol']}'"
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) > 0:
                
                values = {'data': str(coindata), 'created_on': created_on, 'symbol': coindata['symbol']}
                updaterow.append(values)
                
            else:    

            

                # Insert salary information
                coindata = {
                    'data': str(coindata),
                    'created_on': created_on,
                    'symbol': coindata['symbol'],
                    }
                # Insert new employee
                insertrow.append(coindata)
        if(len(insertrow) > 0):
            cursor.executemany(add_coindata, insertrow)
        if(len(updaterow) > 0):
            cursor.executemany(updatequery, updaterow)
        cnx.commit()
        cursor.close()
        time.sleep(0.5)
        
        # all_coindata.append(coindata_obj)
    
    
def connect_mysql():
     cnx = mysql.connector.connect(user='root', password='root',
                                host='127.0.0.1',
                                database='cryptoadmin')
     return cnx
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


def get_candle(symbol, interval, start_time, end_time):
    
    api_url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": start_time,
        "endTime": end_time,
        "limit": 1000  # Fetch up to 1000 candles at a time
    }
    try:
        response = requests.get(api_url, params=params,timeout=cryptoServerModule.timeout)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            save_err_log(str(response.status_code),"Binance API - " + api_url + " Proxy : Local","Failed to fetch candles.")
            print("Failed to fetch candles")
            return []
    except requests.exceptions.ConnectTimeout:
        save_err_log("Exception","Binance API - " + api_url + " Proxy : Local","Connection timed out.")
        print("ConnectTimeout - get_candles")
        time.sleep(10)
        return []
    except requests.exceptions.RequestException as e:
        save_err_log("Exception","Binance API - " + api_url + " Proxy : " + "Local",f"An error occurred: RequestException")
        print(f"An error occurred: {e}")
        time.sleep(60)    
def get_all_candles_h(symbols):
    proxyurl, cmckeys, h1_downdelta_s, h1_updelta_s, m3_downdelta_s,m3_updelta_s, priceperiod, h1period, m3period, lsperiod, cmperiod  = get_sys_settings()
    
    
    threads = []
    for i in range(int(len(symbols)/cryptoServerModule.thread_count)+1):
        thread = threading.Thread(target=get_sub_candels_h, args=(symbols[min(i*cryptoServerModule.thread_count, len(symbols)):min((i+1)*cryptoServerModule.thread_count,len(symbols))], i,h1_downdelta_s, h1_updelta_s,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

def get_all_candles_3m(symbols):
    proxyurl,cmckeys, h1_downdelta_s, h1_updelta_s, m3_downdelta_s,m3_updelta_s, priceperiod, h1period, m3period, lsperiod, cmperiod  = get_sys_settings()
    
    
    threads = []
    for i in range(int(len(symbols)/cryptoServerModule.thread_count)+1):
        thread = threading.Thread(target=get_sub_candels_3m, args=(symbols[min(i*cryptoServerModule.thread_count, len(symbols)):min((i+1)*cryptoServerModule.thread_count,len(symbols))], i,m3_downdelta_s, m3_updelta_s,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
def get_sub_candels_h(symbols, index, down, up):
    for i in range(len(symbols)):
        cryptoServerModule.all_candles[index*cryptoServerModule.thread_count+i] = get_candles_h(symbols[i], down, up)
def get_sub_candels_3m(symbols, index, down, up):
    for i in range(len(symbols)):
        cryptoServerModule.all_candles[index*cryptoServerModule.thread_count+i] = get_candles_3m(symbols[i], down, up)
def get_sys_settings():
    cnx = connect_mysql()
    cursor = cnx.cursor()
    query = f"SELECT * FROM home_systemsettingsdata"
    
    cursor.execute(query)
    result = cursor.fetchall()
    h1_downdelta_s= -4
    h1_updelta_s = 4
    m3_downdelta_s= -1
    m3_updelta_s=1
    priceperiod = 150
    h1period = 60*60
    m3period = 60*60
    lsperiod = 60*60
    cmperiod = 0
    cmckeys=[]
    proxyurl= []
    if len(result) > 0:
        data = str(result[0][1])
        settings = json.loads(data[2:len(data)-1].replace("'", "\""))
        if "h1_downdelta" in settings:
            h1_downdelta_s = float(settings["h1_downdelta"])
        if "h1_updelta" in settings:
            h1_updelta_s = float(settings["h1_updelta"])
        if "m3_downdelta" in settings:
            m3_downdelta_s = float(settings["m3_downdelta"])
        if "m3_updelta" in settings:
            m3_updelta_s = float(settings["m3_updelta"])
        if "priceperiod" in settings:
            priceperiod = float(settings["priceperiod"])
        if "h1period" in settings:
            h1period = float(settings["h1period"])*60       
        if "m3period" in settings:
            m3period = float(settings["m3period"])*60
        if "lsperiod" in settings:
            lsperiod = float(settings["lsperiod"])*60
        if "cmperiod" in settings:
            cmperiod = float(settings["cmperiod"])
        for i in range(5):
            if "proxy" + str(i+1) in settings:
                proxyurl.append(settings["proxy" + str(i+1)])
        for i in range(10):
            if "cmckey" + str(i+1) in settings:
                cmckeys.append(settings["cmckey" + str(i+1)])
    return proxyurl, cmckeys, h1_downdelta_s, h1_updelta_s, m3_downdelta_s, m3_updelta_s, priceperiod, h1period, m3period, lsperiod, cmperiod
def get_candles_h(symbol, down, up):
    
    symbolstr = symbol['symbol']+'USDT'
   
    interval = "1h"
    duration = 14  # in days

    # Calculate start and end times
    end_time = int(datetime.datetime.now().timestamp() * 1000)
    start_time = end_time - ((duration * 24+1) * 60 * 60 * 1000)

    # Fetch the candles
    candles = get_candle(symbolstr, interval, start_time, end_time)

    # Process and print the fetched candles
    
    
    i=0
    c7=c14=0
    for candle in candles:
        
        open_price = float(candle[1])        
        close_price = float(candle[4])        
        if((close_price - open_price)/open_price*100 > up or (close_price - open_price)/open_price*100 < down):
            if i>=7*24:
                c7+=1
            c14+=1
        i+=1
    symbol['c7'] = c7
    symbol['c14'] = c14
    h_count = {}
    h_count['c7'] = c7
    h_count['c14'] = c14
    
    return symbol
def get_candles_3m(symbol, down, up):
    
    symbolstr = symbol['symbol']+'USDT'
   
    interval = "3m"
    duration = 2  # in days

    # Calculate start and end times
    end_time = int(datetime.datetime.now().timestamp() * 1000)
    start_time = end_time - ((duration * 24) * 60 * 60 * 1000 + 3*60*1000)

    # Fetch the candles
    candles = get_candle(symbolstr, interval, start_time, end_time)

    # Process and print the fetched candles
    
    
    i=0
    c1=c2=0
    for candle in candles:
        
        open_price = float(candle[1])        
        close_price = float(candle[4])        
        if((close_price - open_price)/open_price*100 > up or (close_price - open_price)/open_price*100 < down):
            if i>=24*20:
                c1+=1
            c2+=1
        i+=1
    symbol['c1'] = c1
    symbol['c2'] = c2
   
    
    return symbol
def get_sub_candels(subsymbol, interval,pi, proxiesarr, ipstr):
    url = "https://api.binance.com/api/v3/ticker"
    api_url = f"{url}?symbols={subsymbol}&windowSize={interval}"
    try:
    # Send the GET request
        
        response = None
        if (pi == 0):
            response = requests.get(api_url)
        
        else:
            proxies = {
                'http': proxiesarr[pi-1],
                'https': proxiesarr[pi-1]
            }
            response = requests.get(api_url, proxies=proxies)
        # Check the response status code
        if response.status_code == 200:
            # Successful API request
            ticker_data = response.json()
            for data in ticker_data:
            
                try:
                    sindex = cryptoServerModule.all_symbols.index(data["symbol"])
                    if(sindex > -1):
                        cryptoServerModule.all_candles[sindex][interval] = float(data['priceChangePercent'])
                        # all_candles[sindex][interval+'BTC'] = all_candles[sindex][interval] - all_candles[0][interval]
                except ValueError:
                    continue

            
            # Process or use the ticker data as per your requirements
            
            remaining_weight = response.headers.get('X-MBX-USED-WEIGHT')
            print(f"Remaining weight: {remaining_weight}", ipstr[pi-1])
        else:
            save_err_log(str(response.status_code),"Binance API - " + url + " Proxy : " + ipstr[pi-1],"Failed to fetch candles.")
            print(f"API request failed with status code: {response.status_code}")
            # Error in API request
            time.sleep(120)
    except requests.exceptions.Timeout:
        save_err_log("Exception","Binance API - " + url + " Proxy : " + ipstr[pi-1],"Request timed out. Please check your network connection or try again later.")
        print("Request timed out. Please check your network connection or try again later.")
    except requests.exceptions.RequestException as e:
        save_err_log("Exception","Binance API - " + url + " Proxy : " + ipstr[pi-1],f"An error occurred: RequestException")
        print(f"An error occurred: {e}")

def get_candles(symobls, pi, proxiesarr):
    
    # symbols = all_symbols[0:100]
    
    # Format the symbols parameter
    ipstr = ["Proxy1", "Proxy2", "Proxy3", "Proxy4", "Proxy5", "local"]
    symbols_param = "[" + ",".join(f'"{symbol}"' for symbol in symobls) + "]"
    encoded_symbols_param = urllib.parse.quote(symbols_param)
    can_threadings = []
    for interval in cryptoServerModule.interval_mh:
    # Set the windowSize
        can_thread = threading.Thread(target=get_sub_candels, args=(encoded_symbols_param,interval,pi,proxiesarr,ipstr,))
        can_thread.start()
        can_threadings.append(can_thread)
        pi = (pi+1)%(len(proxiesarr)+1)
    for tr in can_threadings:
        tr.join()
        # Set the API endpoint URL
        

def save_err_log(code, type, data):
    cnx = connect_mysql()
    cursor = cnx.cursor()
    add_logdata = ("INSERT INTO home_errorlog "
                    "(code, data, type,created_on) "
                    "VALUES (%(code)s, %(data)s, %(type)s, %(created_on)s)")
    created_on=datetime.datetime.utcnow()
    logdata = {
        'code': code,
        'data' : data,
        'created_on': created_on,
        'type': type,
    }
    cursor.execute(add_logdata, logdata)
    cnx.commit()
    cursor.close()
    
def get_candles_mh():
    proxyurl, cmckeys, h1_downdelta_s, h1_updelta_s, m3_downdelta_s,m3_updelta_s, priceperiod, h1period, m3period, lsperiod, cmperiod  = get_sys_settings()
    proxies = proxyurl
    get_all_candles_h(cryptoServerModule.all_candles)
    
    get_all_candles_3m(cryptoServerModule.all_candles)
    
    start_time = datetime.datetime.now()
    start_index = 0
    pi = 0
    while True:
        proxyurl, cmckeys, h1_downdelta_s, h1_updelta_s, m3_downdelta_s,m3_updelta_s, priceperiod, h1period, m3period, lsperiod, cmperiod  = get_sys_settings()
        proxies = proxyurl
        end_time = datetime.datetime.now()
        if((end_time - start_time).seconds > h1period):
            get_all_candles_h(cryptoServerModule.all_candles)
        if((end_time - start_time).seconds > m3period):            
            get_all_candles_3m(cryptoServerModule.all_candles)
            
        start_time = end_time
            
        sub_array = []
        for i in range(cryptoServerModule.sub_array_size):
            sub_array.append(cryptoServerModule.all_symbols[(start_index + i * cryptoServerModule.step) % len(cryptoServerModule.all_symbols)])
        
        get_fundingRate(pi, proxies)
        # pi = (pi+1)%(len(proxies)+1)
        get_candles(sub_array, pi, proxies)
        pi = (pi+len(cryptoServerModule.interval_mh))%(len(proxies)+1)
        
        start_index = (start_index + cryptoServerModule.sub_array_size + 1) % len(cryptoServerModule.all_symbols)
        time.sleep(cmperiod)
def check_user():
    while True:
        cnx = connect_mysql()
        cursor = cnx.cursor()
        query = f"SELECT * FROM home_customuser WHERE is_superuser = 0"
        
        cursor.execute(query)
        result = cursor.fetchall()
        now = datetime.datetime.now()
        if len(result) > 0:
            column_names = [desc[0] for desc in cursor.description]
            column_index = column_names.index('expired_time')
            for element in result:
                
                datetime_object = datetime.datetime.strptime(str(element[column_index]), "%Y-%m-%d %H:%M:%S")
                if datetime_object < now:
                    
                    query = """
                        UPDATE home_customuser
                        SET is_active = 0
                        WHERE id = %(id)s
                    """
                    values = {'id': element[0]}
                    cursor.execute(query, values)
                    cnx.commit()
                # else:
                    
                #     query = """
                #         UPDATE home_customuser
                #         SET is_active = 1
                #         WHERE id = %(id)s
                #     """
                #     values = {'id': element[0]}
                #     cursor.execute(query, values)
                #     cnx.commit()
        cursor.close()
        time.sleep(3)
def get_fundingRate(pi, proxiesarr):
    url = "https://fapi.binance.com/fapi/v1/premiumIndex"
    ipstr = ["Proxy1", "Proxy2", "Proxy3", "Proxy4", "Proxy5", "local"]
    nofundongSymbols = ['SCUSDT', 'CVCUSDT', 'RAYUSDT', 'BTSUSDT']
    response = None
    try:
        if (pi == 0):
            response = requests.get(url)
        else: 
            proxies = {
                'http': proxiesarr[pi-1],
                'https': proxiesarr[pi-1]
            }
            response = requests.get(url, proxies=proxies)
        
    
        
        
        if response.status_code == 200:
            
            print(f"Funding rate", ipstr[pi-1])
            # Parse the response JSON
            funding_rates = response.json()
            
            for coin in funding_rates:
                c1000 = False
                symbol = coin['symbol']
                
                if symbol[0:4] == '1000':
                    c1000 = True
                    symbol = symbol[4:]
                if(symbol[len(symbol)-4:] == 'USDT'):
                    if symbol in nofundongSymbols:
                        continue
                    try:
                        sindex = cryptoServerModule.all_symbols.index(symbol)
                        if(sindex > -1):
                            cryptoServerModule.all_candles[sindex]['fr'] = float(coin['lastFundingRate'])*100
                            if c1000 == True:
                                cryptoServerModule.all_candles[sindex]['c1000'] = 1
                                cryptoServerModule.future_symbols[sindex] = '1000' + symbol
                            else:
                                cryptoServerModule.all_candles[sindex]['c1000'] = 0
                    except ValueError:
                        
                        continue
            
        else:
            save_err_log(str(response.status_code),"Binance API - " + url + " Proxy : " + ipstr[pi-1],"Failed to retrieve funding rates.")
            print("Failed to retrieve funding rates. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        save_err_log("Exception","Binance API - " + url + " Proxy : " + ipstr[pi-1],f"An error occurred: RequestException")
        print(f"An error occurred: {e}")
        time.sleep(60)    
def get_longshortrate():
    piindex = 0
    url = "https://fapi.binance.com/futures/data/globalLongShortAccountRatio"
    ipstr = ["local", "Proxy1", "Proxy2", "Proxy3", "Proxy4", "Proxy5", "Proxy6"]
    while True:
        proxyurl, cmckeys, h1_downdelta_s, h1_updelta_s, m3_downdelta_s,m3_updelta_s, priceperiod, h1period, m3period, lsperiod, cmperiod  = get_sys_settings()
        proxiesarr = proxyurl
        for symbol in cryptoServerModule.future_symbols:

            params = {
                "symbol": symbol,
                "period": "5m",
                
                "limit": 1  # Fetch only one candle
            }
            response = None
            if (piindex == 0):
                response = requests.get(url, params=params)
           
            else:
                proxies = {
                    'http': proxiesarr[piindex-1],
                    'https': proxiesarr[piindex-1]
                }
                response = requests.get(url, proxies=proxies, params=params)
            if response.status_code == 200:
                data = response.json()
                if(len(data) > 0):
                    
                    long_short_ratio = data[0]['longShortRatio']
                    try:
                        
                            
                        sindex = cryptoServerModule.future_symbols.index(symbol)
                        if(sindex > -1):
                            cryptoServerModule.all_candles[sindex]['ls'] = float(long_short_ratio)
                            
                    except ValueError:
                        
                        continue
                    
                piindex = (piindex+1)%(len(proxiesarr)+1)
            else:
                save_err_log(str(response.status_code),"Binance API - " + url + " Proxy : " + ipstr[piindex-1],"Failed to retrieve long/short ratio.")
                print("Failed to retrieve long/short ratio. Status code:", response.status_code)
        time.sleep(lsperiod)


server = cryptoServerModule()
server.runServer()
        
        




    

    
    

    


