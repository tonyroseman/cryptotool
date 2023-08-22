from django.utils import timezone

import datetime
import json
from .models import CoinData
from .models import CandleHourData
from .models import CustomUser




class CryptoModule:
    
        
    def get_top_coins(self,limit=1000):
        
        last_coindata_object= CoinData.objects.last()
        now = timezone.now()
        # now = datetime.datetime.utcnow()
        
        try:
            # threshold_time = now - datetime.timedelta(minutes=15)    
            threshold_time = now - timezone.timedelta(minutes=15)    
            ago15_data = CoinData.objects.filter(created_on__lte=threshold_time).order_by('-created_on').first()

            # threshold_time = now - datetime.timedelta(minutes=5)   
            threshold_time = now - timezone.timedelta(minutes=5)     
            ago5_data = CoinData.objects.filter(created_on__lte=threshold_time).order_by('-created_on').first()

            # threshold_time = now - datetime.timedelta(minutes=3) 
            threshold_time = now - timezone.timedelta(minutes=3)       
            ago3_data = CoinData.objects.filter(created_on__lte=threshold_time).order_by('-created_on').first()
            
            
        except CoinData.DoesNotExist:
            r = 0
        allcoins = json.loads(last_coindata_object.data.replace("'", "\""))
        retcoins = []
        m3BTC = m5BTC = m15BTC = h1BTC = h4BTC = 0
        fm3BTC = fm5BTC = fm15BTC = fh1BTC = fh4BTC = 0
        for coin in allcoins.keys():
            coin_id = int(coin[3:])
            cloned_json = json.loads(str(allcoins[coin]).replace("'", "\""))
            try:
                candlerecord = CandleHourData.objects.filter(coin_id=coin_id).latest('created_on')
            
                if(candlerecord is not None):
                    candledata = str(candlerecord.data)
                    
                    hdatas = json.loads(candledata.replace("'", "\"").replace("None","0.0"))
                    
                    if(len(hdatas['close_price']) > 0):                    
                        cloned_json['h1'] = round((allcoins[coin]['price'] - hdatas['close_price'][0])/hdatas['close_price'][0]*100,2)
                        if cloned_json['symbol'] == 'BTC':
                            h1BTC = cloned_json['h1']
                            fh1BTC = 1
                            cloned_json['h1BTC']  = ""
                        elif fh1BTC == 1:
                            cloned_json['h1BTC'] = round(cloned_json['h1'] - h1BTC,2)
                    if(len(hdatas['close_price']) > 3):
                        cloned_json['h4'] = round((allcoins[coin]['price'] - hdatas['close_price'][3])/hdatas['close_price'][3]*100,2)
                        if cloned_json['symbol'] == 'BTC':
                            h4BTC = cloned_json['h4']
                            fh4BTC = 1
                            cloned_json['h4BTC']  = ""
                        elif fh4BTC == 1:
                            cloned_json['h4BTC'] = round(cloned_json['h4'] - h4BTC,2)
                    c7 = c14 = 0
                    count = 0
                    sumvol = 0
                    for i in range(min(14*24,len(hdatas['close_price']))):
                        if (hdatas['close_price'][i] - hdatas['open_price'][i])/hdatas['open_price'][i]*100 >4 or (hdatas['close_price'][i] - hdatas['open_price'][i])/hdatas['open_price'][i]*100 < -4 :
                            if i<7*24:
                                c7+=1
                            c14+=1
                        
                        
                        if i < 48:
                            sumvol += hdatas['volume'][i]
                            count+=1
                    if count > 0 and sumvol > 0:
                        cloned_json['vol'] = round((allcoins[coin]['volume'] - sumvol/count)/(sumvol/count)*100,2)
                    else:
                        cloned_json['vol'] = 0
                    cloned_json['c7'] = c7
                    cloned_json['c14'] = c14
                if(ago3_data is not None):
                    
                    cdatas = json.loads(ago3_data.data.replace("'", "\""))
                    if coin in cdatas and cdatas[coin]['price'] > 0:
                        cloned_json['m3'] = round((allcoins[coin]['price'] - cdatas[coin]['price'])/cdatas[coin]['price']*100,2)
                        if cloned_json['symbol'] == 'BTC':
                            m3BTC = cloned_json['m3']
                            fm3BTC = 1
                            cloned_json['m3BTC']  = ""
                        elif fm3BTC == 1:
                            cloned_json['m3BTC'] = round(cloned_json['m3'] - m3BTC,2)
                if(ago5_data is not None):
                    
                    cdatas = json.loads(ago5_data.data.replace("'", "\""))
                    if coin in cdatas and cdatas[coin]['price'] > 0:
                        cloned_json['m5'] = round((allcoins[coin]['price'] - cdatas[coin]['price'])/cdatas[coin]['price']*100,2)
                        if cloned_json['symbol'] == 'BTC':
                            m5BTC = cloned_json['m5']
                            fm5BTC = 1
                            cloned_json['m5BTC']  = ""
                        elif fm5BTC == 1:
                            cloned_json['m5BTC'] = round(cloned_json['m5'] - m5BTC,2)
                if(ago15_data is not None):
                    
                    cdatas = json.loads(ago15_data.data.replace("'", "\""))
                    if coin in cdatas and cdatas[coin]['price'] > 0:
                        cloned_json['m15'] = round((allcoins[coin]['price'] - cdatas[coin]['price'])/cdatas[coin]['price']*100,2)
                        if cloned_json['symbol'] == 'BTC':
                            m15BTC = cloned_json['m15']
                            fm15BTC = 1
                            cloned_json['m15BTC']  = ""
                        elif fm15BTC == 1:
                            cloned_json['m15BTC'] = round(cloned_json['m15'] - m15BTC,2)
                retcoins.append(cloned_json)
                if(len(retcoins) == limit):
                    break
            except CandleHourData.DoesNotExist:
                
                r = 0
        return retcoins[0:limit]
    def get_user_coins(self, limit=1000):
        
        last_coindata_object= CoinData.objects.last()
        
        now = timezone.now()
        
        try:
            # threshold_time = now - datetime.timedelta(minutes=15)    
            threshold_time = now - timezone.timedelta(minutes=15)    
            ago15_data = CoinData.objects.filter(created_on__lte=threshold_time).order_by('-created_on').first()

            # threshold_time = now - datetime.timedelta(minutes=5)   
            threshold_time = now - timezone.timedelta(minutes=5)     
            ago5_data = CoinData.objects.filter(created_on__lte=threshold_time).order_by('-created_on').first()

            # threshold_time = now - datetime.timedelta(minutes=3) 
            threshold_time = now - timezone.timedelta(minutes=3)       
            ago3_data = CoinData.objects.filter(created_on__lte=threshold_time).order_by('-created_on').first()
            
            
        except CoinData.DoesNotExist:
            print("No candle")
            r = 0
        allcoins = json.loads(last_coindata_object.data.replace("'", "\""))
        retcoins = []
        m3BTC = m5BTC = m15BTC = h1BTC = h4BTC = 0
        fm3BTC = fm5BTC = fm15BTC = fh1BTC = fh4BTC = 0
        for coin in allcoins.keys():
            coin_id = int(coin[3:])
            cloned_json = json.loads(str(allcoins[coin]).replace("'", "\""))
            try:
                candlerecord = CandleHourData.objects.filter(coin_id=coin_id).latest('created_on')
            
                if(candlerecord is not None):
                    candledata = str(candlerecord.data)
                    
                    hdatas = json.loads(candledata.replace("'", "\"").replace("None","0.0"))
                    
                    if(len(hdatas['close_price']) > 0):                    
                        cloned_json['h1'] = round((allcoins[coin]['price'] - hdatas['close_price'][0])/hdatas['close_price'][0]*100,2)
                        if cloned_json['symbol'] == 'BTC':
                            h1BTC = cloned_json['h1']
                            fh1BTC = 1
                            cloned_json['h1BTC']  = ""
                        elif fh1BTC == 1:
                            cloned_json['h1BTC'] = round(cloned_json['h1'] - h1BTC,2)
                    if(len(hdatas['close_price']) > 3):
                        cloned_json['h4'] = round((allcoins[coin]['price'] - hdatas['close_price'][3])/hdatas['close_price'][3]*100,2)
                        if cloned_json['symbol'] == 'BTC':
                            h4BTC = cloned_json['h4']
                            fh4BTC = 1
                            cloned_json['h4BTC']  = ""
                        elif fh4BTC == 1:
                            cloned_json['h4BTC'] = round(cloned_json['h4'] - h4BTC,2)
                    c7 = c14 = 0
                    for i in range(min(14*24,len(hdatas['close_price']))):
                        if (hdatas['close_price'][i] - hdatas['open_price'][i])/hdatas['open_price'][i]*100 >4 or (hdatas['close_price'][i] - hdatas['open_price'][i])/hdatas['open_price'][i]*100 < -4 :
                            if i<7*24:
                                c7+=1
                            c14+=1
                        sumvol = 0
                        count = 0
                        if i < 48:
                            sumvol += hdatas['volume'][i]
                            count+=1
                        if count > 0 and sumvol > 0:
                            cloned_json['vol'] = round((allcoins[coin]['volume'] - sumvol/count)/(sumvol/count)*100,2)
                    cloned_json['c7'] = c7
                    cloned_json['c14'] = c14
                if(ago3_data is not None):
                    
                    cdatas = json.loads(ago3_data.data.replace("'", "\""))
                    if coin in cdatas and cdatas[coin]['price'] > 0:
                        cloned_json['m3'] = round((allcoins[coin]['price'] - cdatas[coin]['price'])/cdatas[coin]['price']*100,2)
                        if cloned_json['symbol'] == 'BTC':
                            m3BTC = cloned_json['m3']
                            fm3BTC = 1
                            cloned_json['m3BTC']  = ""
                        elif fm3BTC == 1:
                            cloned_json['m3BTC'] = round(cloned_json['m3'] - m3BTC,2)
                if(ago5_data is not None):
                    
                    cdatas = json.loads(ago5_data.data.replace("'", "\""))
                    if coin in cdatas and cdatas[coin]['price'] > 0:
                        cloned_json['m5'] = round((allcoins[coin]['price'] - cdatas[coin]['price'])/cdatas[coin]['price']*100,2)
                        if cloned_json['symbol'] == 'BTC':
                            m5BTC = cloned_json['m5']
                            fm5BTC = 1
                            cloned_json['m5BTC']  = ""
                        elif fm5BTC == 1:
                            cloned_json['m5BTC'] = round(cloned_json['m5'] - m5BTC,2)
                if(ago15_data is not None):
                    
                    cdatas = json.loads(ago15_data.data.replace("'", "\""))
                    if coin in cdatas and cdatas[coin]['price'] > 0:
                        cloned_json['m15'] = round((allcoins[coin]['price'] - cdatas[coin]['price'])/cdatas[coin]['price']*100,2)
                        if cloned_json['symbol'] == 'BTC':
                            m15BTC = cloned_json['m15']
                            fm15BTC = 1
                            cloned_json['m15BTC']  = ""
                        elif fm15BTC == 1:
                            cloned_json['m15BTC'] = round(cloned_json['m15'] - m15BTC,2)
            except CandleHourData.DoesNotExist:
                r = 0
            
            retcoins.append(cloned_json)
            if(len(retcoins) == limit):
                break
        
        
        return retcoins[0:limit]
    

# Example usage
