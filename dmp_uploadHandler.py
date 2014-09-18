#!/usr/bin/python
# DMP Upload handler
# Python 2.7.x
# Dependent on the watchdog library, see https://pypi.python.org/pypi/watchdog

import time, sys, uuid, os
import SimpleHTTPServer, SocketServer

from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler 

class uploadHandler(PatternMatchingEventHandler):
    patterns = ["*.3gp", "*.mp4", "*.webm","*.m4v", "*.flv", "*.f4v","*.ogv", "*.ogx", "*.3g2", "*.jpeg", "*.jpg", "*.png", "*.bmp"]
    newFileName = ""

    def rename(self, event):
        try:
            os.rename(event.src_path, tempDir + self.newFileName) #try to move the file
            print "File renamed & moved"
        except:
            time.sleep(1) #wait one second if we do not have access
        pass        

    def on_modified(self, event): #shoot if monitored files are modified
        print "File modified"
        while os.access(event.src_path, os.W_OK): #while the file still exist in upload dir...
            self.rename(event) #try to process it
        pass

    def on_created(self, event):
        print "File created"
        self.newFileName = self.generate_name(event.src_path) #on creation generate a unique filename
        pass 

    def generate_name(self, ofn):
        ts = str(time.time()).split('.')[0] #create the timestamp 
        tmpr = str(uuid.uuid4())[0:6].upper() #create a temporary random 6 char string 
        ts_tmpr = '{0}_{1}'.format(ts, tmpr) # assemble the prefix
        ext = ofn.split('.')[-1]  #strip the extention
        nfn = '{0}.{1}'.format(ts_tmpr, ext) #assemble the full file name
        return nfn
        pass   

 #For quick http tests only
def http_start(port, wdir):
    os.chdir(wdir)
    handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("localhost", port), handler)
    print "Serving at port ", port
    httpd.serve_forever()


if __name__ == '__main__':

    uploadDir = "upload" # For Linux, change to "upload/"
    tempDir = "temp\\" 
    wwwDir = "www\\"

    uploadObserver = Observer()
    tempObserver = Observer()
    
    uploadObserver.schedule(uploadHandler(), uploadDir)
    
    uploadObserver.start()
    tempObserver.start()

    print os.getcwd()
    print "It's on"

    #http_start(9998, wwwDir)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        uploadObserver.stop()
            
    uploadObserver.join()
