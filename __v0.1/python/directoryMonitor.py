#!/usr/bin/python

import time
import sys
import uuid
import os

#sys.path.append('C:\\Program Files (x86)\\VideoLAN\\VLC')
#import vlc

from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler 

class uploadHandler(PatternMatchingEventHandler):
    patterns = ["*.3gp", "*.mp4", "*.webm","*.m4v", "*.flv", "*.f4v","*.ogv", "*.ogx", "*.3g2"]
    patterns = ["*.jpeg", "*.jpg", "*.png", "*.bmp"]
    newFileName = ""

    def process(self, event):
        """
        event.event_type 
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        try:
            os.rename(event.src_path, dirTEMP+self.newFileName) #try to move the file
        except:
            time.sleep(1) #wait one second if we do not have access
        pass        

    def on_modified(self, event): #shoot if monitored files are modified
        while os.access(event.src_path, os.W_OK): #while the file still exist in www dir...
            self.process(event) #try to process it
        pass

    def on_created(self, event):
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

class photoProcessor(PatternMatchingEventHandler):
        patterns = ["*.jpeg", "*.jpg", "*.png", "*.bmp"]

        def on_created(self, event):
            #ffmpeg -loop 1 -i ${filetmp} -c:v libx264 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -t 10  ${filetmp}.mp4
            #mv ${filetmp}.mp4 "${playerdir}/${datetime}".mp4

            #print(event.src_path+" moved")
            pass

class videoProcessor(PatternMatchingEventHandler):
        patterns = ["*.3gp", "*.mp4", "*.webm","*.m4v", "*.flv", "*.f4v","*.ogv", "*.ogx", "*.3g2"]

        def on_created(self, event):
            #mv ${filetmp}.mp4 "${playerdir}/${datetime}".mp4
            #print(event.src_path+" moved")
            pass
'''
class videoPlayer():
        def play_file():
            #for vid in videoQueue[]
            #setQueue(vid)
            #ffplay -t 5 -an -fs -autoexit "vid"            

        def queue_video(filename):
            #position = seek_queue+1
            #insert "filename" at videoQueue[position]

        def seek_queue():
            #return videoPlaying

        def set_queue(int):
            #videoPlaying = int
'''

if __name__ == '__main__':

    dirWWW = ".\\www\\"
    dirTEMP = ".\\temp\\"
    dirPROCESS = ".\\process\\"
    dirPLAYER = ".\\player\\"

    videoQueue = str
    videoPlaying = str

    uploadObserver = Observer()
    tempObserver = Observer()
    
    uploadObserver.schedule(uploadHandler(), dirWWW)
    tempObserver.schedule(photoProcessor(), dirTEMP)
    
    uploadObserver.start()
    tempObserver.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        uploadObserver.stop()

    uploadObserver.join()
