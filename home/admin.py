from django.contrib import admin

from .models import CustomUser
from .models import CoinData
from .models import UserSettingsData
from .models import UserNotifyData
from .models import CandleHourData


admin.site.register(CustomUser)

