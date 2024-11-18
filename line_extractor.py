import os
import cv2
import numpy as np
from utils.parser_xml import XmlParser
import sys

class LineExtractor:
    def __init__(self, doc_root_dir, output_dir):
        self.doc_root_dir = doc_root_dir
        self.output_dir = output_dir

        # Ensure the output directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        elif os.path.isfile(self.output_dir):
            raise Exception(f"{self.output_dir} is a file, not a directory.")

    def extract_lines_from_page(self, image_path, xml_path, output_subdir):
        
        # Read the image
        image = cv2.imread(image_path)
        
        # # Check if the image was loaded successfully
        # if image is None:
        #     print(f"Error loading image: {image_path}")
        #     return  # Skip this image

        # Parse the XML
        parser = XmlParser(page_xml=xml_path)
        
        # Extract texts and coordinates from XML
        texts_coords = parser.extract_texts_and_coords()

        # Get the base name of the image file (without the extension)
        image_base_name = os.path.splitext(os.path.basename(image_path))[0]

        # Process each line
        for idx, (text, coords) in enumerate(texts_coords):
            # Adjusting the index to start from 1 instead of 0
            idx += 1
            rect = cv2.boundingRect(np.array(coords))
            x, y, w, h = rect

            # ######
            # # Ensure the cropping coordinates are within the image bounds
            # if w <= 0 or h <= 0:
            #     print(f"Invalid cropping coordinates for {image_path}: x={x}, y={y}, w={w}, h={h}")
            #     continue  # Skip this item

            cropped_image = image[y:y+h, x:x+w]

            ######
            # Check if the cropped image is empty
            if cropped_image.size == 0:
                print(f"Cropped image is empty for {image_path}: x={x}, y={y}, w={w}, h={h}")
                continue  # Skip this item

            # Correction
            #cropped_image_rgb = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)

            # Including the document name in the filename
            doc_name = os.path.basename(output_subdir)
            image_filename = os.path.join(output_subdir, f"{doc_name}_{image_base_name}_line_{idx}.png")
            
            # Save the cropped image
            # cv2.imwrite(image_filename, cropped_image_rgb)
            cv2.imwrite(image_filename, cropped_image)


            # Save the corresponding text if it's not None or empty
            if text:
                text_filename = os.path.join(output_subdir, f"{doc_name}_{image_base_name}_line_{idx}.txt")
                with open(text_filename, 'w', encoding='utf-8') as f:
                    f.write(text)

    def extract_lines(self):
        for root, dirs, files in os.walk(self.doc_root_dir):
            for dir_name in dirs:
                output_subdir = os.path.join(self.output_dir, dir_name)

                # Skip the entire document directory if it was already processed
                # A simple way to add new document folders and avoid reprocessing the same document
                # Can be better, but works for the purpose
                if os.path.exists(output_subdir) and os.listdir(output_subdir):
                    print(f"Skipping entire document directory {output_subdir}.")
                    continue  # Skip this directory

                # Construct paths for images and XML files
                images_dir = os.path.join(root, dir_name)
                xml_dir = os.path.join(images_dir, 'page')  # XML files are assumed to be in the 'page' subdirectory
                
                # Check if the 'page' directory exists
                if not os.path.exists(xml_dir):
                    continue  # Skip this directory if 'page' subdirectory does not exist

                # Process each image and corresponding XML file
                for image_name in os.listdir(images_dir):
                    if image_name.endswith(('.jpg', '.jpeg')):
                        image_path = os.path.join(images_dir, image_name)
                        xml_path = os.path.join(xml_dir, image_name.replace('.jpg', '.xml').replace('.jpeg', '.xml'))

                        # Check if the corresponding XML file exists
                        if os.path.exists(xml_path):
                            output_subdir = os.path.join(self.output_dir, dir_name)
                            if not os.path.exists(output_subdir):
                                os.makedirs(output_subdir)
                            self.extract_lines_from_page(image_path, xml_path, output_subdir)

# python line_extractor.py ./data ./output
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python line_extractor.py <dataset_root_directory> <output_directory>")
        sys.exit(1)

    doc_root_dir = sys.argv[1]
    output_dir = sys.argv[2]

    extractor = LineExtractor(doc_root_dir, output_dir)
    extractor.extract_lines()

    print("Done.")

