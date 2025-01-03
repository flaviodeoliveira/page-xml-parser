# page-xml-parser

PAGE XML parser for Handwritten Text Recognition (HTR). Creation of a dataset from line-to-text alignment in Transkribus

## Environment Setup (or venv etc.)

    conda create -n page-xml python=3.9

## Dependencies

    conda activate page-xml
    pip install -r requirements.txt

## Run

Place folder(s) with data extracted from Transkribus in the `data` directory.

### Parse files to create the dataset in `output` (line image - line transcription pairs)

    python line_extractor.py ./data ./output

### Create the `dataframe.csv` file with the following columns: `Image File`, `Text`, and `Document Name`

    python create_dataframe.py

### Create the pre-processed dataset in `output-pp`

Using the optional flag denoted by square brackets

    python pp.py ./output ./output-pp [--flag scanned]

Execution for scanned dataset:

    python pp.py ./output ./output-pp --flag scanned
