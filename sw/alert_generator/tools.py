import urllib.parse
import urllib.request
import http.client
import requests

attributes = 'mask'
subscription_key = '9c2fe1a150ff4ec298a101f4495e19fa'

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
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


def check_frame(frame: bytes) -> int:
    try:
        conn = http.client.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
        conn.request('POST', "/face/v1.0/detect?%s" % params, frame, headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        conn.close()
        result = identify_alert(data)

        return result
    except OSError as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def notify_alert(id_camera) -> None:
    # Manda la notificacion al cliente diciendo que no tiene mascarilla
    requests.post('http://10.254.14.117:80/save-alert', json={"alert": "no mask", "camera": f"{id_camera}"})


def identify_alert(result: str) -> int:
    if (result.find('faceMask')) > -1:
        return 0
    elif (result.find('noMask')) > -1:
        return 1
    else:
        return -1


