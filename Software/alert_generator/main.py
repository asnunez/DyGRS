import http.client
import urllib.error
import urllib.parse
import urllib.request
from threading import Thread


def process_video(id_camera) -> None:
    headers, params = url_define()

    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except OSError as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def url_define():
    attributes = 'mask,gender'
    subscription_key = 'key'

    headers = {
        # Request headers
        'Content-Type': 'application/jason',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': attributes,
        'recognitionModel': 'recognition_04',
        'returnRecognitionModel': 'false',
        'detectionModel': 'detection_03',
        'faceIdTimeToLive': '86400',
    })

    return [headers, params]


def main() -> None:
    camaras = [
        "rstp://camera1/dfdsf.mp4",
        "rstp://camera2/dfdsf.mp4",
        "rstp://camera3/dfdsf.mp4",
        "rstp://camera4/dfdsf.mp4",
        "rstp://camera5/dfdsf.mp4"
    ]

    threads = [Thread(target=process_video, args=(c,)) for c in camaras]

    [t.start() for t in threads]

    [t.join() for t in threads]


if __name__ == '__main__':
    main()
