import urllib.parse
import urllib.request
from cv2 import cv2

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


def get_frame(id_camera, number):
    capture = cv2.VideoCapture(id_camera)
    ret, frame = capture.read()
    name = 'frame' + str(number) + '.png'

    if ret:
        cv2.imwrite(name, frame)
    else:
        pass

    capture.release()
    return name
