FROM nvidia/cuda:11.6.2-devel-ubuntu20.04

# Base scripts
RUN apt-get update --fix-missing
RUN apt install -y python3 python3-dev python3-pip

# Environment variables
ENV PATH=/usr/local/nvidia/bin:${PATH}
ENV PATH=/usr/local/cuda/bin:${PATH}
ENV LIBRARY_PATH=/usr/local/cuda/lib64:${LIBRARY_PATH}
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:${LD_LIBRARY_PATH}


##-----------AI TEMPLATE-----------------
ADD ./install/ /Install
# necessary package
RUN bash /Install/install_basic_dep.sh

# for test
RUN bash /Install/install_test_dep.sh

# for docs
RUN bash /Install/install_doc_dep.sh

# install Pytorch
# -----------pytorch support -----------------
RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113

# for detection
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN bash /Install/install_detection_deps.sh

# install detectron2

##-----------JOYCV-----------------
ADD ./joycv_install/install_apt_tools.sh /joycv_install/install_apt_tools.sh
RUN bash /joycv_install/install_apt_tools.sh

ADD ./joycv_install/install_detectron2.sh /joycv_install/install_detectron2.sh
RUN bash /joycv_install/install_detectron2.sh

ADD ./joycv_install/install_basler_driver_pypylon.sh /joycv_install/install_basler_driver_pypylon.sh
RUN bash /joycv_install/install_basler_driver_pypylon.sh
##-----------MM Classification -----
ADD ./mmclassification_install/install_mmclassification.sh /mmclassification_install/install_mmclassification.sh
RUN bash /mmclassification_install/install_mmclassification.sh
RUN apt-get install -y python-is-python3
# # Copy AITemplate to Docker
# RUN mkdir /AITemplate
# ADD ./COMMIT_INFO /AITemplate/COMMIT_INFO
# ADD ./python /AITemplate/python
# ADD ./3rdparty /AITemplate/3rdparty
# ADD ./examples /AITemplate/examples
# ADD ./tests /AITemplate/tests
# ADD ./docs /AITemplate/docs
# ADD ./static /AITemplate/static
# ADD ./licenses /AITemplate/licenses
# ADD ./docker/install/install_ait.sh /AITemplate/
#RUN bash /AITemplate/install_ait.sh

