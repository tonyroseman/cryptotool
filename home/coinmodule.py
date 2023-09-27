from django.utils import timezone

import datetime
import json
from .models import CoinData
from .models import UserSettingsData
from .settingsModule import SettingsModule
class CryptoModule:
    
    
    def get_top_coins(self, user,limit=1000):
        
        all_coindata= CoinData.objects.all()
       
       
        retcoins = []
        no=0
        for coin in all_coindata:
            coindata = json.loads(coin.data.replace("'", "\""))
        
            coindata['no'] = no+1
            # coindata['vm'] = coindata['vol_24h']/coindata['market_cap']
            retcoins.append(coindata)
            no+=1

        
        return retcoins[0:limit]
    def get_user_coins(self, user, sm,limit=1000):
        
        all_coindata= CoinData.objects.all()
        all_coindata = all_coindata[0:limit]
        
        usersettingsdata = UserSettingsData.objects.filter(userid=user)
        settings = []
        coins = []
        if(len(usersettingsdata) > 0):
            settings = json.loads(usersettingsdata[0].data.replace("'", "\""))
            
            if( 'coins' in settings):
                if(settings['coins'].strip() != ""):
                    coins = settings['coins'].split(',')
                
        
        retcoins = []
        no=0
        for coin in all_coindata:
            coindata = json.loads(coin.data.replace("'", "\""))
            coindata['no'] = no+1
            no+=1
            if(len(coins) > 0):
                if(coindata['symbol'] in coins):
                    
                    coindata['coinflag'] = True
                    retcoins.append(coindata)
                    
                elif (str("-")+coindata['symbol'] in coins):
                    continue
                elif len(settings.keys()) > 2:
                    
                    retcoins.append(coindata)
                    
                
            else:
                
                retcoins.append(coindata)
                
        
        return retcoins
    

# Example usage
