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



</pre>
