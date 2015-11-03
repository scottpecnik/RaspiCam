import picamera
import threading
import io
from datetime import datetime, timedelta
from time import sleep

# Create a pool of image uploaders
lock = threading.Lock()
pool = []


class ImageUploader(threading.Thread):

    def __init__(self):
        super(ImageUploader, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.start()

    def run(self):
        # This method runs in a separate thread
        while not self.terminated:
            # Wait for an image to be written to the stream
            if self.event.wait(1):
                print("event set and reading pic info")
                try:
                    self.stream.seek(0)
                    with open('newImage.png', 'wb+') as f:
                        f.write(self.stream)
                finally:
                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    # Return ourselves to the pool
                    with lock:
                        pool.append(self)


def streams():
    print("streams")
    with lock:
        processor = pool.pop()
    yield processor.stream
    processor.event.set()



def loopuntilstart():
    runprocess = False
    while not runprocess:
        start = datetime.today()
        start = start.replace(hour=12, minute=00, second=00, microsecond=0)
        print('start: ' + str(start))
        global finish
        finish = start + timedelta(hours=12)
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
    with picamera.PiCamera() as camera:
    # camera = FakeCamera()
    # with FakeCamera() as camera:
        pool = [ImageUploader() for i in range(4)]
        while datetime.today() <= finish:
            print("Taking Pic and Uploading to BlueMix")
            camera.capture(streams(), 'png')
            camera.close()
            sleep(30)

    # Shut down the processors in an orderly fashion
    while pool:
        with lock:
            processor = pool.pop()
        processor.terminated = True
        processor.join()


def main():
    loopuntilstart()
    takephotos()

if __name__ == "__main__":
    main()
