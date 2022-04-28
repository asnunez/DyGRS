import http.client
import logging
import re
import urllib.parse
import urllib.request

from .config import config

attributes = 'mask'

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': config.API_KEY,
}

params = urllib.parse.urlencode({
    # Request parameters
    'returnFaceId': 'false',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': attributes,
    'recognitionModel': 'recognition_04',
    'returnRecognitionModel': 'false',
    'detectionModel': 'detection_03',
    'faceIdTimeToLive': '86400',
})


def is_alert(result: str) -> bool:

    if result.find('faceMask') > -1:
        return False
    elif result.find('noMask') > -1:
        return True
    else:
        return False


def check_frame(frame: bytes) -> bool:
    try:
        conn = http.client.HTTPSConnection(config.API_FACE_DOMAIN)
        conn.request('POST', "/face/v1.0/detect?%s" % params, frame, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()

        return is_alert(str(data))

    except OSError as e:
        logging.error(e)


def test():
    img = "aaa.png"

    data = ""

    with open(img, "rb") as fd:
        data = fd.read()

    print(check_frame(data))


