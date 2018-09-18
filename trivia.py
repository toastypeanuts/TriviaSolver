#pylint:disable=E1101

from PIL import Image
import pytesseract
import argparse
import cv2
import os
import time
import googSearch
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
import pyscreenshot as ImageGrab
import time

imageName = ""


class Watcher:
    DIRECTORY_TO_WATCH = (r'''C:\Users\mjoh0\Desktop\Projects\TriviaPhotos''')

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_created(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)
            imageName = event.src_path[45:]
            print(imageName)
            time.sleep(0.1)
            runOCR(event.src_path, '')

def restartScript():
    
    w = Watcher()
    w.run()

def runOCR(imageName, preprocessType) :
    	
    # load the example image and convert it to grayscale
    image = cv2.imread(imageName)
    gray = image

    # check to see if we should apply thresholding to preprocess the
    # image
    if preprocessType == "thresh":
        gray = cv2.threshold(gray, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # make a check to see if median blurring should be done to remove
    # noise
    elif preprocessType == "blur":
        gray = cv2.medianBlur(gray, 3)

    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)
    #print(text)
    os.remove(imageName)
    start = time.time()
    googSearch.findResults(text)
    end = time.time()
    print('time elasped = ' + str(end - start))
    print('-----------------------------------------------------')
    print("Starting...")
    restartScript()



def snapImage():
    
    #part of the screen
    im=ImageGrab.grab(bbox=(10,220,500,695))
    
    #to file
    im.save(r'''C:\Users\mjoh0\Desktop\Projects\TriviaPhotos\pic1.png''')
    #print('image saved!')
    #print('------------------------------------------')
    #print(' ')



def main():
    print("Starting...")
    #inputVar = input('type \'run\' to run trivia script or \'quit\' to exit: ')
    #if(inputVar == 'run'):
    #print('Running...')
    w = Watcher()
    w.run()
    #elif (inputVar == 'quit'):
    #    sys.exit()
    #else:
    #    print("please type either \'run\' or \'quit\'")

if __name__ == '__main__':	
    main()
	
