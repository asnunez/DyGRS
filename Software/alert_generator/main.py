import http.client
import tools
from threading import Thread


def process_video(id_camera, number) -> None:
    print(id_camera)
    print('thread number %c', number)

    headers = tools.headers
    params = tools.params
    url_img = tools.get_frame(id_camera, number)

    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request('POST', "/face/v1.0/detect?%s" % params, url_img, headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except OSError as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


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
