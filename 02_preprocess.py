from PIL import Image
import h5py
import cv2
from os import listdir
from os.path import isfile, join
from typing import List, Union
from pathlib import Path
from pyprojroot import here
from tqdm import tqdm

def img_to_hdf5(cxr_paths: List[Union[str, Path]], out_filepath: str, resolution=320): 
    """
    Convert directory of images into a .h5 file given paths to all 
    images. 
    """
    dset_size = len(cxr_paths)
    failed_images = []
    with h5py.File(out_filepath,'w') as h5f:
        img_dset = h5f.create_dataset('cxr', shape=(dset_size, resolution, resolution))    
        for idx, path in enumerate(tqdm(cxr_paths)):
            try: 
                # read image using cv2
                img = cv2.imread(str(path))
                # convert to PIL Image object
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img_pil = Image.fromarray(img)
                # preprocess
                img = preprocess(img_pil, desired_size=resolution)     
                img_dset[idx] = img
            except Exception as e: 
                failed_images.append((path, e))
    print(f"{len(failed_images)} / {len(cxr_paths)} images failed to be added to h5.", failed_images)

'''
This function resizes and zero pads image 
'''
def preprocess(img, desired_size=320):
    old_size = img.size
    ratio = float(desired_size)/max(old_size)
    new_size = tuple([int(x*ratio) for x in old_size])
    img = img.resize(new_size, Image.LANCZOS)
    # create a new image and paste the resized on it

    new_img = Image.new('L', (desired_size, desired_size))
    new_img.paste(img, ((desired_size-new_size[0])//2,
                        (desired_size-new_size[1])//2))
    return new_img

if __name__ == "__main__":
    cxr_dir = here('raw_images')
    cxr_paths = [join(cxr_dir, f) for f in listdir(cxr_dir) if f.endswith('.jpg')]
    out_path = here('data/cxr.h5')
    img_to_hdf5(cxr_paths, out_path)