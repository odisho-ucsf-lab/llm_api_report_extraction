# LLM API Report Extraction

This tool is designed to extract structured data from MRI reports using a Large Language Model (LLM) API. It's part of a research project aimed at automating the extraction of relevant information from medical reports, with a specific focus on Prostate MRI reports.

## Features

- Reads MRI reports from a CSV file
- Applies predefined prompts to extract specific information
- Uses an LLM API to process the reports and generate structured responses
- Outputs the extracted data to a CSV file for further analysis
- Includes sample prompts specifically crafted for Prostate MRI reports

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/Vistian/llm_api_report_extraction.git
   cd llm_api_report_extraction
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Copy the `sample_config.json` file to `config.json`:
   ```
   cp sample_config.json config.json
   ```

2. Edit `config.json` to include your specific settings:
   - `prompt_file`: Path to your CSV file containing prompts
   - `report_file`: Path to your CSV file containing MRI reports
   - `output_dir`: Directory where output files will be saved
   - `iterations`: Number of times to process the entire dataset
   - `endpoint`: URL of the LLM API endpoint
   - `api-key`: Your API key for the LLM service
   - `api_version`: Version of the API you're using
   - `model`: Name of the LLM model to use
   - `log_level`: Logging level (0-5, where 0 is no logging and 5 is critical)
   - `log_file`: Path to the log file

## Usage

Run the main script:

```
python report_prompt_tool.py
```

The script will process the reports, apply the prompts, and save the extracted data to a CSV file in the specified output directory.

## Input File Formats

### Prompt File (CSV)
- A sample prompt file (`prompt_file_sample.csv`) is provided in the repository.
- This file contains prompts specifically crafted and refined for extracting information from Prostate MRI reports.
- Columns: "Prompt", "Field Name"
- Each row contains a prompt to extract a specific piece of information and the name of the field it corresponds to.
- **Important**: The column header names must remain consistent for the tool to function correctly.
- **Note for other use cases**: If you're using this tool for MRI reports other than Prostate, you will need to modify the prompts to suit your specific needs. The effectiveness of the data extraction heavily depends on the quality and specificity of these prompts.

### Report File (CSV)
- Columns: "ID", "MRN", "Date", "ReportText"
- Each row represents an MRI report with its metadata and the full text of the report.

## Output

The script generates a CSV file with the following columns:
- ID
- MRN
- ReportDate
- Prompt Number
- Expected Data Name
- Extracted Data Value

## Logging

The script logs its operations to a file specified in the config. The log level can be adjusted in the config file.

## Customization for Other Imaging Report Types

While this tool is optimized for Prostate MRI reports, it can be adapted for other types of imaging reports. To do so:

1. Create a new prompt file based on `prompt_file_sample.csv`.
2. Modify the prompts to extract relevant information for your specific MRI type.
3. Ensure that the new prompts maintain the same CSV structure (columns: "Prompt", "Field Name").
4. Update the `prompt_file` path in your `config.json` to point to your new prompt file.

Remember that the effectiveness of the data extraction depends on how well the prompts are tailored to your specific imaging report type and structure.

## Acknowledgments

This tool was developed as part of a UCSF Department of Urology research project: `Generative Artificial Intelligence Successfully Automates Data Extraction from Unstructured MRI Reports: Feasibility in Prostate Cancer Care`

## Contact

For questions or feedback, please open an issue in this repository, or contact Anobel Odisho, MD (anobel.odisho@ucsf.edu) or Matthew Cooperber, MD (matthew.cooperberg@ucsf.edu).
