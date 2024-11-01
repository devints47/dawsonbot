# DawsonBot

`dawsonbot.py` is a Python script that uploads PNGs of an inventory table to the website XtraChef using Selenium.

## Prerequisites

- Python 3.x
- Selenium
- Google Chrome and ChromeDriver
- `convert_pdf.py` script

## Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Ensure you have Google Chrome installed and the corresponding ChromeDriver in your PATH.

## Usage

1. Prepare the PNGs:
    - Place the original PDFs in the `original_pdfs` directory.
    - Run the `convert_pdf.py` script to convert the PDFs to PNGs:
        ```sh
        python convert_pdf.py
        ```

2. Upload the PNGs using `dawsonbot.py`:
    ```sh
    python dawsonbot.py
    ```

## convert_pdf.py

The `convert_pdf.py` script handles the formatting of the original PDFs to get the tables in PNG format. It performs the following steps:
- Takes the original PDFs from the `original_pdfs` folder.
- Scales them up and converts them to PNGs.
- Saves the temporary PDFs in the `temp_pdfs` folder.
- Stores the final PNGs in the `fixed_pngs` folder.
