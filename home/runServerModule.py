import os
import threading



def execute_script(name):
    os.system('python ' + name)

class serverModule():
    
    def runServer(self):
        
        b = threading.Thread(target=execute_script, args=('cryptoServerModule.py',))
        b.start()
        a = threading.Thread(target=execute_script, args=('cryptoTelegramServer.py',))
        a.start()
        print("All Server start")
        a.join()

        b.join()

server = serverModule()
server.runServer()