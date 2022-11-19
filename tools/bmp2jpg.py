import cv2
import glob
import argparse
import os

parser = argparse.ArgumentParser(
                    prog = 'BMP2JPG',
                    description = 'Convert BMP2JPG',
                    epilog = 'Provide input and output')

parser.add_argument('-i', '--input',required=True)
parser.add_argument('-o','--output')   
args = parser.parse_args()
input_path = args.input 
dest_path = args.output

if(input_path[-1]=='/'):
    input_path=input_path[0:-1]
print(input_path)
if(dest_path is None):
    dest_path=input_path+"_jpg"
    from pathlib import Path
    Path(dest_path).mkdir(parents=True, exist_ok=True)

if(dest_path[-1]=='/'):
    dest_path=dest_path[0:-1]

print(f"Using input {input_path}")
print(f"Using dest_path {dest_path}")

arr = next(os.walk(f"{input_path}"))[2]
for item in arr:
    basefilename=item.split(".")[0]
    extention=item.split(".")[-1]
    #print(f"{extention == 'bmp'}")
    if(extention !="bmp" and extention != "BMP" ):
        print(f"ignore none bmp file:{item}")
        continue 
    print(f"from {input_path}/{item} \r\nto  {dest_path}/{basefilename}.jpg" )
    cv2.imwrite(f"{dest_path}/{basefilename}.jpg",cv2.imread(f"{input_path}/{item}"))
import shutil
basedir=os.path.dirname(dest_path)
archieve_filename=os.path.basename(dest_path)
print(f"{archieve_filename}")
print(f"{basedir}/{archieve_filename}")
shutil.make_archive(f"{basedir}/{archieve_filename}", 'zip', f"{dest_path}/")