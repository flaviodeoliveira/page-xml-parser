import pandas as pd
import os

def generate_dataframe_from_directory(source_folder):
    # Initialize a list to store dictionaries for each row in the DataFrame
    data = []

    # Walk through each document directory in the source folder
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            # Filter out only text files
            if file.endswith('.txt'):
                # Construct the path to the text file
                text_path = os.path.join(root, file)
                try:
                    # Read the text content
                    with open(text_path, 'r', encoding='utf-8') as txt_file:
                        text_content = txt_file.read().strip()
                except Exception as e:
                    print(f"Erro ao ler {text_path}: {e}")
                    continue  # Skip to the next file
                
                # Get the base name for the image and text (without extension)
                base_name = os.path.splitext(file)[0]
                # Image file name based on text file name
                image_file = base_name + '.png'
                # Document name is extracted from the folder structure
                document_name = os.path.basename(root)
                
                # Add the gathered information to the data list
                data.append({
                    'Image File': image_file,
                    'Text': text_content,
                    'Document Name': document_name
                })

    # Convert the list of dictionaries into a DataFrame
    column_order = ['Image File', 'Text', 'Document Name']
    df = pd.DataFrame(data, columns=column_order)
    return df

if __name__ == "__main__":
    source_folder = 'output'
    df = generate_dataframe_from_directory(source_folder)
    # print(df.head())
    # print(df.shape)

    df.to_csv("dataframe.csv", index=False)