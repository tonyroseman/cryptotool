from django.utils import timezone

import datetime
import json
from .models import CoinData
from .models import UserSettingsData






class CryptoModule:
    
        
    def get_top_coins(self, user,limit=1000):
        
        all_coindata= CoinData.objects.all()
        usersettingsdata = UserSettingsData.objects.filter(userid =user)
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
            if(len(coins) > 0):
                if(coindata['symbol'] in coins):

                    coindata['no'] = no+1
                    # coindata['vm'] = coindata['vol_24h']/coindata['market_cap']
                    retcoins.append(coindata)
                    no+=1
            else:
                coindata['no'] = no+1
                # coindata['vm'] = coindata['vol_24h']/coindata['market_cap']
                retcoins.append(coindata)
                no+=1

        
        return retcoins[0:limit]
    def get_user_coins(self, user, limit=1000):
        
        all_coindata= CoinData.objects.all()
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
            if(len(coins) > 0):
                if(coindata['symbol'] in coins):
                    coindata['no'] = no+1
                    retcoins.append(coindata)
                    no+=1
            else:

                
                coindata['no'] = no+1
                retcoins.append(coindata)
                no+=1
        
        return retcoins[0:limit]
    

# Example usage
