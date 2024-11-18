import cv2
import os
# import numpy as np
from pathlib import Path
import argparse

# Preprocessing function
# TODO
def binarize_img(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    dst = cv2.fastNlMeansDenoising(img_gray, h=31, templateWindowSize=7, searchWindowSize=21)
    img_blur = cv2.medianBlur(dst, 3)
    img_thresh = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    return img_thresh

def binarize_scanned_img(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Histogram equalization
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img_gray = clahe.apply(img_gray)  # Corrected to apply CLAHE to grayscale image
    ret, img_thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return img_thresh

def process_directory(flag, source_dir, target_dir):
    # Check if the source directory exists
    if not os.path.exists(source_dir):
        print(f"Directory '{source_dir}' not found.")
        return  # Exit the function early if source_dir does not exist

    # Check if the source directory contains any files or subdirectories
    if not any(os.listdir(source_dir)):
        print(f"There are no files in {source_dir}.")
        return  # Exit the function early if source_dir is empty
    
    # Ensure the target directory structure mirrors the source
    Path(target_dir).mkdir(parents=True, exist_ok=True)

    # Process files and subdirectories
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        target_path = os.path.join(target_dir, item)

        # Check if it's a directory, recurse if so
        if os.path.isdir(source_path):
            process_directory(flag, source_path, target_path)
        else:
            # Process image files
            filename, file_ext = os.path.splitext(item)
            if file_ext.lower() in ['.png', '.jpg', '.jpeg']:
                img = cv2.imread(source_path)
                if flag == "scanned":
                    img_bin = binarize_scanned_img(img)
                    cv2.imwrite(target_path, img_bin)  # Save preprocessed image
                else:
                    img_bin = binarize_img(img)
                    cv2.imwrite(target_path, img_bin)
            elif file_ext.lower() == '.txt':
                # Copy text files
                with open(source_path, 'r', encoding='utf-8') as f_src:
                    content = f_src.read()
                with open(target_path, 'w', encoding='utf-8') as f_tgt:
                    f_tgt.write(content)

if __name__ == "__main__":

    # python pp.py <source_directory> <target_directory> [--flag FLAG]
    # python pp.py ./output ./output-pp
    parser = argparse.ArgumentParser(
        description="Pre-processing of images with an optional flag to indicate scanned images."
                    "eg. python pp.py ./output ./output-pp --flag scanned",
        usage="python pp.py ./output ./output-pp [--flag scanned]"   
    )
    # Define the source and target directories as positional arguments
    parser.add_argument("source_directory", type=str, help="Root directory")
    parser.add_argument("target_directory", type=str, help="Output directory")
    parser.add_argument("--flag", type=str, default=None, help="Optional flag for scanned images.")
    
    args = parser.parse_args()

    # Now args.source_directory and args.target_directory are used directly
    source_dir = args.source_directory
    target_dir = args.target_directory
    # args.flag will be None if not specified, or the provided value otherwise
    flag = args.flag
    
    process_directory(flag, source_dir, target_dir)
    print("Done.")
