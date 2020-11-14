#!/bin/bash

docker run --rm -it --gpus all --shm-size=8gb \
    -v $HOME/github/RealSenseTrainer/rst:/rst \
    -v $HOME/training-data:/training-data \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    --device=/dev/video0:/dev/video0 \
    --device=/dev/video1:/dev/video1 \
    --device=/dev/video2:/dev/video2 \
    -e DISPLAY=$DISPLAY \
    realsense:dev
