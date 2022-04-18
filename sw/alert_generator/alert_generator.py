import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List
import logging
import cv2

from src.api_horus import get_active_cameras, notify_alert
from src.models import Camera
from src.api_face import check_frame


def proc_video(cam: Camera) -> None:
    end = False

    def end_proc():
        nonlocal end
        end = True

    timer = threading.Timer(interval=30, function=end_proc)

    timer.start()

    video_cam = cv2.VideoCapture(cam.host)

    try:

        while not end:
            ret, frame = video_cam.read()
            if ret:
                alert = check_frame(frame)
                if alert:
                    notify_alert(cam.alias)
            time.sleep(1)
    finally:
        video_cam.release()


def main() -> None:
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(message)s")

    while True:
        cameras: List[Camera] = get_active_cameras()

        if not cameras:
            continue

        threads = [threading.Thread(target=proc_video, args=(camera,)) for camera in cameras]

        [thread.start() for thread in threads]
        [thread.join() for thread in threads]


if __name__ == '__main__':
    main()
