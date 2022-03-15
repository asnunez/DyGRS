import json
import urllib.parse
import urllib.request
import http.client
import requests
import time
import config

attributes = 'mask'

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': config.config.API_KEY,
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
        conn = http.client.HTTPSConnection(config.config.API_FACE_DOMAIN)
        conn.request('POST', "/face/v1.0/detect?%s" % params, frame, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        result = identify_alert(str(data))

        return result
    except OSError as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def notify_alert(id_camera) -> None:
    alert = {
        "alert":
            {
                "type": "no mask",
                "camera": f"{id_camera}",
                "timestamp": f"{time.time()}"
            }
    }
    requests.post('http://' + config.config.HTTP_SERVER_IP + ':'
                  + str(config.config.HTTP_SERVER_PORT) + '/save-alert', json=alert)


def get_cameras() -> list:
    response = requests.get('http://' + config.config.HTTP_SERVER_IP + ':' +
                            str(config.config.HTTP_SERVER_PORT) + '/get-active-cameras')
    values = json.loads(response)
    aliases = list
    for entity in values:
        alias = entity["alias"]
        aliases.append(alias)

    return aliases


def identify_alert(result: str) -> int:
    if (result.find('faceMask')) > -1:
        return 0
    elif (result.find('noMask')) > -1:
        return 1
    else:
        return -1
