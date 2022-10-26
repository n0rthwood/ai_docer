#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo script located at: $SCRIPT_DIR
docker run --rm -it --privileged --network host -v /opt/images/:/opt/images/ -v $SCRIPT_DIR/code/.torch:/root/.torch/  -v $SCRIPT_DIR/code/:/opt/code --runtime nvidia ai_docker /bin/bash