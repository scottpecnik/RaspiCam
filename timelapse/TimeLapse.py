import picamera
import threading
import io
import cloudant
from datetime import datetime, timedelta
from time import sleep
from base64 import *

class ImageCapturer(threading.Thread):

    def __init__(self, camera, imageuploader):
        super(ImageCapturer, self).__init__()
        self.stream = io.BytesIO()
        self.camera = camera
        self.imageuploader = imageuploader

    def run(self):
        localtime = datetime.now()
        self.camera.capture(self.stream, 'png')
        self.stream.seek(0)
        self.imageuploader.storePic(localtime, self.stream)
        # self.stream.seek(0)
        # with io.open('newImage'+self.name+'.png', 'wb') as f:
        #     f.write(self.stream.read())
        # self.stream.seek(0)
        # self.stream.truncate()
        if pool.__contains__(self):
            pool.remove(self)
        exit()


class ImageUploader():

    def __init__(self):
        self.account = 'cloudant_account'
        self.username = 'cloudant_username'
        self.password = 'cloudant_password'
        self.database = None

    def login(self):
        self.account = cloudant.Account(self.account)
        self.account.login(self.username, self.password)
        self.database = self.account.database('timelapse')

    def storePic(self, timestamp, stream):
        uuid = self.account.uuids(1)
        _uuid = uuid.json()['uuids'].pop()
        document = self.database.document(_uuid)
        json = {
            'dateCreated': str(timestamp),
            'cameraType': 'raspberrypi',
            'cameraName': 'Scott\'s Raspberry Pi Camera',
            'location': 'Austin, TX',
            'caption': 'Scott\'s Apartment',
            '_attachments': {
                'picture': {
                    'content_type': 'image/png',
                    'data': b64encode(stream.read())
                }
            }
        }
        document.put(params=json)


def loopuntilstart():
    runprocess = False
    while not runprocess:
        start = datetime.today()
        start = start.replace(hour=22, minute=00, second=00, microsecond=0)
        print('start: ' + str(start))
        global finish
        finish = start + timedelta(hours=9)
        print('finish: ' + str(finish))
        print(datetime.today())
        if start <= datetime.today() <= finish:
            print("yes, within the interval")
            runprocess = True
        else:
            print("No, not within the interval.  Sleeping for 2 minutes")
            sleep(60*2)


def takephotos():
    global pool
    pool = []
    imageuploader = ImageUploader()
    imageuploader.login()
    with picamera.PiCamera() as camera:
        camera.exposure_mode = "night"
        camera.resolution = (1920, 1080)
        while datetime.today() <= finish:
            print("Taking Pic and Uploading to BlueMix")
            processor = ImageCapturer(camera, imageuploader)
            pool.append(processor)
            processor.start()
            sleep(30) #time to sleep before taking next picture

    while pool:
        processor = pool.pop()
        processor.join()

def main():
    loopuntilstart()
    takephotos()

if __name__ == "__main__":
    main()
