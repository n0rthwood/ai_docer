'''
A simple Program for grabing video from basler camera and converting it to opencv img.
Tested on Basler acA1300-200uc (USB3, linux 64bit , python 3.5)

'''
from pypylon import pylon
import cv2
import torch, detectron2
TORCH_VERSION = ".".join(torch.__version__.split(".")[:2])
CUDA_VERSION = torch.__version__.split("+")[-1]
print("torch: ", TORCH_VERSION, "; cuda: ", CUDA_VERSION)
print("detectron2:", detectron2.__version__)

import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import os, json, cv2, random

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
import sys


import torch, detectron2
TORCH_VERSION = ".".join(torch.__version__.split(".")[:2])
CUDA_VERSION = torch.__version__.split("+")[-1]
print("torch: ", TORCH_VERSION, "; cuda: ", CUDA_VERSION)
print("detectron2:", detectron2.__version__)

import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import os, json, cv2, random

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog

import sys, getopt
argv=sys.argv[1:]
help_text=f"{__file__} -s <sn>"
try:
    opts, args = getopt.getopt(argv,"hs:e:",["sn=","ext="])
except getopt.GetoptError:
    print (help_text)
    sys.exit(2)
extention_name="bmp"
sn_to_use=None
for opt, arg in opts:
      if opt == '-h':
         print (help_text)
         sys.exit()
      elif opt in ("-s", "--sn"):
         sn_to_use = arg
      elif opt in ("-e", "--ext"):
         extention_name = arg
print(f"Collected args: sn:{sn_to_use} extention:{extention_name}")




def grab(camera,friendlyname):
    # conecting to the first available camera
    #pinstance = pylon.TlFactory.GetInstance()
    #camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

    friendlyname=friendlyname.replace(" ","_")    
    friendlyname=friendlyname.replace("(","_")
    friendlyname=friendlyname.replace(")","_")    
    # Grabing Continusely (video) with minimal delay
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
    converter = pylon.ImageFormatConverter()

    # converting to opencv bgr format
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
    counter=0
    import time
    time_start=time.time()
    timestr = time.strftime("%y%m%d-%H%M%S")
    batch_counter=0
    while camera.IsGrabbing():
        current_start_time=time.time()
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        cam_fps=0;
        #cam_fps= camera.ResultingFrameRateAbs.GetValue();
        counter=counter+1
        
        if grabResult.GrabSucceeded():
            cam_counter=grabResult.ImageNumber
            # Access the image data
            image = converter.Convert(grabResult)
            batch_counter=batch_counter+1
            img = image.GetArray()
            image_path=f"/opt/code/image/[{timestr}][{friendlyname}][{counter}][orig].{extention_name}"
            #write_result = cv2.imwrite(image_path,img)
            #print(f"write result {write_result} {image_path}")
            predict(img,f"/opt/code/image/[{timestr}][{friendlyname}][{counter}][marked].{extention_name}")
        grabResult.Release()
        current_end_time=time.time()
        current_timetook=current_end_time-current_start_time
        avg_timetook=(current_end_time-time_start)/counter
        current_fps=1/(current_timetook)
        avg_fps=1/(avg_timetook)
        print(f"{friendlyname} count:{counter} cam_counter:{cam_counter} camfps:{cam_fps} timetook:{current_timetook:.4f} current_fps:{current_fps:.1f} avg_timetook:{avg_timetook:.4f} avg_fps:{avg_fps:.1f}")
        if counter>999999:
            break
    # Releasing the resource    
    camera.StopGrabbing()




cfg = get_cfg()
    # add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
# Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")

predictor = DefaultPredictor(cfg)
def predict(im,save_name):
    
    print(f"image size:{im.shape}")
    outputs = predictor(im)

    v = Visualizer(im[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
    out = v.draw_instance_predictions(outputs["instances"].to("cpu"))

    #cv2.imwrite(save_name,out.get_image()[:, :, ::-1])
    

camera=None
print(f"selected camera sn:{sn_to_use} and save extention:{extention_name}")
print(f"Tring to list avaiable Cameras:")
for i in pylon.TlFactory.GetInstance().EnumerateDevices():
    print(f"i.GetFullName:{i.GetFullName()}\r\n \
            i.GetFriendlyName:{i.GetFriendlyName()}\r\n\
            i.GetAddress:{i.GetAddress()}\r\n\
            i.GetDeviceClass{i.GetDeviceClass()}\r\n\
            i.GetIpConfigCurrent:{i.GetIpConfigCurrent()}")
    if(i.GetSerialNumber()==sn_to_use):
        #camera = pylon.InstantCamera(i)
        print(f"Found match list:{i.GetSerialNumber()} expected:{sn_to_use}")
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(i))
        if(camera is None):
            print(f"No camera found!")
        else:        
            grab(camera,f"{i.GetDeviceClass()}-{i.GetSerialNumber()}")
