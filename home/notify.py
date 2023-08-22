


# Connect to Telegram
# client.start(phone_number)
from .models import UserNotifyData

class Notify:
    def __init__(self):
        self.api_id = 20557393
        
    def saveNotify(self, data, user):
        message = ""
        
        for k in data.keys():
            message = message + str(k) + ": " + str(data[k]) + "<br>"
        
        user_notify_data = UserNotifyData()
        user_notify_data.userid = user
        user_notify_data.data = message
        user_notify_data.status = '0'
        user_notify_data.save()
        