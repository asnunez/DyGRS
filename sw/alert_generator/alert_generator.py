import sys
import threading
import time
from typing import List
import logging
import cv2

from src.api_horus import get_active_cameras, notify_alert
from src.models import Camera
from src.api_face import check_frame, test


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
            time.sleep(10)
            continue

        threads = [threading.Thread(target=proc_video, args=(camera,)) for camera in cameras]

        [thread.start() for thread in threads]
        [thread.join() for thread in threads]


def tes1t():
    video_cap = cv2.VideoCapture(0)
    while True:
        # `success` is a boolean and `frame` contains the next video frame
        success, frame = video_cap.read()
        cv2.imshow("frame", frame)
        # wait 20 milliseconds between frames and break the loop if the `q` key is pressed
        if cv2.waitKey(20) == ord('q'):
            break

    # we also need to close the video and destroy all Windows
    video_cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
