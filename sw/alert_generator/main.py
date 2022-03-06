import time
import tools
import cv2
from threading import Thread


def process_video(id_camera, number) -> None:
    print(id_camera)
    print('thread number %c', number)

    try:
        capture = cv2.VideoCapture(id_camera)
        while True:
            ret, frame = capture.read()
            if ret:
                result = tools.check_frame(frame)
                if result == 1:
                    tools.notify_alert('camera-X')
            time.sleep(1)
    finally:
        capture.release()


def main() -> None:
    videos = [
        r'C:\Users\danyk\Videos\Videos_Prueba\video_1.mp4',
        r'C:\Users\danyk\Videos\Videos_Prueba\video_2.mp4'
    ]

    threads = [Thread(target=process_video, args=(c, d)) for c in videos for d in range(0, len(videos))]

    [t.start() for t in threads]

    [t.join() for t in threads]


if __name__ == '__main__':
    main()
