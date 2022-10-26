#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo script located at: $SCRIPT_DIR
docker run --rm -it --privileged --network host -v /opt/workspace/mmclassification:/opt/mmclassification -v /opt/workspace/imagedb/input/DatasetId_1692766_1666577221:/opt/imagedb/train -v $SCRIPT_DIR/code/.torch:/root/.torch/  -v $SCRIPT_DIR/code/:/opt/code --runtime nvidia registry.cn-beijing.aliyuncs.com/joysort/training:latest python /opt/mmclassification/tools/train.py /opt/mmclassification/configs/joycv/resnet18_8xb16_freshchestnut.py 
