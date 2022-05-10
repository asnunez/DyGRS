#! /bin/sh


IP=$(hostname  -I | cut -f1 -d' ')
CAMERA_ALIAS="CameraTest"


wget https://github.com/aler9/rtsp-simple-server/releases/download/v0.18.0/rtsp-simple-server_v0.18.0_linux_amd64.tar.gz
mkdir camera-dir
tar -xvzf rtsp-simple-server_v0.18.0_linux_amd64.tar.gz -C camera-dir/
cd camera-dir
docker run --rm -d -v $PWD/rtsp-simple-server.yml:/rtsp-simple-server.yml -p 8554:8554 aler9/rtsp-simple-server
sudo nohup ffmpeg -nostdin -framerate 24 -video_size 480x480 -i /cam.mp4 -f rtsp -rtsp_transport tcp rtsp://$IP:8554/cam &
sudo avahi-publish-address -s $CAMERA_ALIAS _rtsp._tcp 8554 &
