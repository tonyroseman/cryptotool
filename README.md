<pre>
- commit version 'update-5'
    -> updated app contents
        home\cryptoTelegramServer.py
        home\views.py
        home\coinmodule.py

        home\templates\admin\usermonitor.html
        home\templates\admin\index.html
        home\templates\admin\error_log.html
        home\templates\admin\user.html
        home\templates\includes\head.html
        home\templates\pages\setting.html
        home\templates\pages\usersettings.html
        home\templates\pages\admin_usernotify.html
        home\templates\pages\aboutus.html
        home\templates\pages\usernotify.html
        home\templates\pages\records.html
        home\templates\pages\index.html

    -> updated contents
        adjustments8.doc
            1, Error on “View setting” or “View Notify history” of any users
            3, Responsive table on page “Dashbroad” and “Records”
            4, Extend setting “Coin name” in “Settings” page
        adjustments9.doc
            1, Can not enable tlg function
            2, After removing the tlg URL on “User Profile” page. The data of user still remaining 

- commit version 'update-6'
    -> updated app contents
        home\cryptoTelegramServer.py
    -> updated contents
        tlg is not sending any noti => fixed

- commit version 'update-7'
    -> updated app contents
        home/cryptoServerModule.py
        home/templates/includes/sidebar.html
        home/templates/pages/records.html
        home/views.py
    -> updated contents
        adjustments10.doc 
            1, Wrong message when user is de-active
            2, This telegram link in here is not correct
            3, Error when starting server
            4, XRP marketcap is mapping wrong 
            5, Wrong result with setting “Coinname”
    -> Note
        To fix '1, Wrong message when user is de-active', add this statement at the end of core\settings.py

            AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.AllowAllUsersModelBackend']

- commit version 'update-8'
    -> updated app contents
        home/cryptoTelegramServer.py
        home/templates/admin/usermonitor.html
        home/urls.py
        home/views.py
    -> updated contents
        adjustments11.doc 
            1, Wrong result with setting “Coinname” and noti did not send
            2, When de-active an user on admin page -> they can still using all functions until they sign out

- commit version 'update-9'
    -> updated app contents
        home/models.py
        home/views.py
    -> updated contents
        fix usermonitor funtion error.
    -> Note
        After update app contents on pc or VPS, run follow commands in cmd of cryptotool directory.
            python .\manage.py makemigrations
            python manage.py migrate
        And then
            run "python .\manage.py runserver" on PC
            restart Web Server of our app on VPS.
- commit version 'update-10'
    -> updated app contents
        home/templates/includes/menu-list.html
        home/templates/includes/sidebar_admin.html
        home/urls.py
        static/assets/images/logo-dark.png
    -> updated contents
        fix dispaly warning on startup server
        display footer on admin page
        logo image on admin signin page

    -> additional updates
        home/templates/pages/admin_usernotify.html  // fix user notify history bug on admin page
        delete below files
            home/templates/pages/custom-index.html
            home/templates/pages/icon-feather.html
            home/templates/pages/tbl_allcoin.html
            static/assets/images/2.png        
            static/assets/images/3.png
            static/assets/images/logo-1.png
            static/assets/images/logo-dark-1.png
            static/assets/images/logo-docs.png
            static/assets/images/logo-icon.png
            static/assets/images/logo-thumb.png
            image.png
- commit version 'update-11'
    -> updated app contents
        home/cryptoServerModule.py
    -> updated contents
        update price, change module 1m, 3m, 5m
- commit version 'update-12'
    -> updated app contents
        home/cryptoServerModule.py
    -> updated contents
        update price, change module 1m, 3m, 5m
        update adjust12.doc
- commit version 'update-13'
    -> updated app contents
        home/cryptoServerModule.py
        home/templates/pages/admin_usernotify.html
        home/templates/pages/index.html
        home/templates/pages/records.html
        home/templates/pages/setting.html
        home/templates/pages/usernotify.html
        home/templates/pages/usersettings.html
    -> updated contents
        update 1m,3m,5m,15m with new way
        add change module 6h 12h 24h and 48h, remove 4h
        update all related pages
        update all h module refreshing data period

- commit version 'update-14'
    -> updated app contents
        home/cryptoServerModule.py
        home/templates/pages/admin_usernotify.html
        home/templates/pages/index.html
        home/templates/pages/records.html
        home/templates/pages/setting.html
        home/templates/pages/usernotify.html
        home/templates/pages/usersettings.html
    -> updated contents
        update adjusts13.doc
    -> additional app updated contents
        home/templates/admin/systemsetting.html
- commit version 'update-15'
    -> updated app contents
        home/cryptoServerModule.py
        home/templates/admin/systemsetting.html
    -> updated contents
        update cmc error

- commit version 'update-16'
    -> updated app contents
        home/models.py
        home/settingsModule.py
        home/templates/includes/head.html
        home/templates/pages/aboutus.html
        home/templates/pages/admin_usernotify.html
        home/templates/pages/index.html
        home/templates/pages/records.html
        home/templates/pages/setting.html
        home/templates/pages/usernotify.html
        home/urls.py
        home/views.py
        static/assets/css/style.css
        static/assets/js/treeview.js
    -> updated contents
        update advanced settings demo
    -> Notes
        After update app contents on pc or VPS, run follow commands in cmd of cryptotool directory.
            python .\manage.py makemigrations
            python manage.py migrate
        And then
            run "python .\manage.py runserver" on PC
            restart Web Server of our app on VPS.
        advanced settings demo can test on About us page.

- commit version 'update-17'
    -> updated app contents
        home/coinmodule.py
        home/settingsModule.py
        home/templates/includes/head.html
        home/templates/includes/menu-list.html
        home/templates/pages/aboutus.html
        home/templates/pages/advanced_settings.html
        home/templates/pages/records.html
        home/templates/pages/setting.html
        home/urls.py
        home/views.py
    -> updated contents
        update advanced settings and record page
    
- commit version 'update-18'
    -> updated app contents
       home/cryptoServerModule.py
       home/cryptoTelegramServer.py
       home/models.py
       home/settingsModule.py
       home/templates/pages/advanced_settings.html
       home/templates/pages/records.html
       home/templates/pages/setting.html
       home/templates/pages/usernotify.html
       home/urls.py
       home/views.py
       home/templates/pages/usersettings.html
    -> updated contents
        update advanced settings tlg function
    -> Notes
        After update app contents on pc or VPS, run follow commands in cmd of cryptotool directory.
            python .\manage.py makemigrations
            python manage.py migrate
        And then
            run "python .\manage.py runserver" on PC
            restart Web Server of our app on VPS.    
- commit version 'update-19'
    -> updated app contents
        home/cryptoTelegramServer.py
        home/models.py
        home/settingsModule.py
        home/templates/pages/advanced_settings.html
        home/urls.py
        home/views.py
    -> updated contents
        update of coin name setting of advanced settings page

- commit version 'update-20'
    -> updated app contents
        home/settingsModule.py
        home/views.py
    -> updated contents
        update of adjust_18.doc

- commit version 'update-21'
    -> updated app contents
        home/cryptoServerModule.py
        home/settingsModule.py
        home/templates/admin/systemsetting.html
        home/templates/pages/admin_usernotify.html
        home/templates/pages/advanced_settings.html
        home/templates/pages/index.html
        home/templates/pages/records.html
        home/templates/pages/setting.html
        home/templates/pages/usernotify.html
        home/templates/pages/usersettings.html
        home/views.py
    -> updated contents
        update all bugs and new updating requirments
- commit version 'update-22'
    -> updated app contents
        home/cryptoServerModule.py
        home/templates/admin/systemsetting.html
    -> updated contents
        update cc error
- commit version 'update-23'
    -> updated app contents
        home/cryptoServerModule.py
        home/cryptoTelegramServer.py
    -> updated contents
        update cc refresh error
- commit version 'update-24'
    
    -> updated contents
        update without tlg noti delay


        
</pre>
