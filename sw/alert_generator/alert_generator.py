import logging
import sys
import threading
import time
from typing import List

import cv2

from src.api_face import check_frame
from src.api_horus import get_active_cameras, notify_alert
from src.models import Camera


def main() -> None:
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(message)s")

    def proc_video(cam: Camera) -> None:

        logging.info(f"Starting new thread for {cam.host}")

        end = False

        def end_proc():
            nonlocal end
            end = True

        timer = threading.Timer(interval=30, function=end_proc)

        timer.start()

        video_cam = cv2.VideoCapture(f"{cam.host}/cam")

        logging.info(f"Starting video capture from {cam.host}")

        try:
            while not end:
                ret, frame = video_cam.read()
                if ret:
                    logging.info(f"Checking frame from {cam.host}, Alert?")
                    image_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
                    alert = check_frame(image_bytes)
                    logging.info(f"Alert checking ended. Result: {alert}")
                    if alert:
                        notify_alert(cam.alias)
                    time.sleep(1)
        finally:
            cv2.destroyAllWindows()
            video_cam.release()

        logging.info(f"Ending thread for {cam.host}")

    while True:
        cameras: List[Camera] = get_active_cameras()

        if not cameras:
            logging.info("Not cameras available from HTTP Server. Trying in 10 seconds")
            time.sleep(10)
            continue

        threads = [threading.Thread(target=proc_video, args=(camera,)) for camera in cameras]

        [thread.start() for thread in threads]
        [thread.join() for thread in threads]


if __name__ == '__main__':
    main()
