import csv
import json
import requests
import os
import logging
import datetime
import time
import pyodbc

def setup_logging(config):
    log_level = config.get("log_level", 0)
    log_file = config.get("log_file", "app.log")

    # Map config log_level to Python's logging level
    log_level_mapping = {
        0: logging.NOTSET,    # No logging at all
        1: logging.DEBUG,     # Debug messages
        2: logging.INFO,      # Informational messages
        3: logging.WARNING,   # Warnings/problems
        4: logging.ERROR,     # Error messages
        5: logging.CRITICAL   # Critical issues, system may be unable to continue
    }

    python_log_level = log_level_mapping.get(log_level, logging.NOTSET)

    # Configure logging to include line number and use the appropriate level
    logging.basicConfig(filename=log_file, level=python_log_level, 
                        format='%(asctime)s - %(levelname)s - %(message)s - %(lineno)d')

    logging.info("Logging started at level: {}".format(python_log_level))

def load_config(config_path):
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Error loading config file: {e}")
        exit(1)

def read_csv_prompt_file(prompt_file):
    try:
        prompts = []
        with open(prompt_file, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                prompts.append(row)
        logging.info(f"Loaded {len(prompts)} records from the prompt file.")
        return prompts
    except Exception as e:
        logging.error(f"Error reading file {prompt_file}: {e}")
        exit(1)

def read_csv_report_file(report_file):
    try:
        reports = []
        with open(report_file, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                reports.append(row)
        logging.info(f"Loaded {len(reports)} records from the reports file.")
        return reports
    except Exception as e:
        logging.error(f"Error reading file {report_file}: {e}")
        exit(1)

def post_to_endpoint(endpoint, api_key, api_version, payload, max_retries=3, backoff_factor=0.5):
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "api-key": api_key
    }
    params = {"api-version": f"{api_version}"}
    
    for attempt in range(max_retries):
        logging.debug(f"Attempt {attempt+1}: Request to {endpoint} with payload: {payload}")
        try:
            response = requests.post(endpoint, headers=headers, json=payload, params=params)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            if attempt < max_retries - 1:
                sleep_time = backoff_factor * (2 ** attempt)
                logging.warning(f"Request failed with error {e}. Retrying in {sleep_time} seconds.")
                time.sleep(sleep_time)
            else:
                logging.error(f"Request failed after {max_retries} attempts.")
                raise e

def main(config_path):
    config = load_config(config_path)
    setup_logging(config)  # Setup logging based on config
    prompt_file = config["prompt_file"]
    report_file = config["report_file"]
    output_dir = config["output_dir"]
    iterations = config["iterations"]
    endpoint = config["endpoint"]
    api_key = config["api-key"]
    api_version = config["api_version"]
    model = config["model"]

    # Generate a timestamp at the start of the run
    timestamp = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S') 

    prompts = read_csv_prompt_file(prompt_file)
    reports = read_csv_report_file(report_file)

    records = []
    total_processed = 0  # Track the total number of processed reports
    
    for i in range(iterations):
        for n, report_row in enumerate(reports, start=1):
            report = report_row["ReportText"]

            for m, prompt_row in enumerate(prompts, start=1):
                prompt = prompt_row["Prompt"]
                payload = {
                    "model": model,
                    "messages": [
                        {
                            "role": "user",
                            "content": f"{prompt}\n{report}"
                        }
                    ]
                }

                try:
                    response = post_to_endpoint(endpoint, api_key, api_version, payload)
                    content = response['choices'][0]['message']['content'].replace('\n', '').replace("'", '"')

                    try:
                        json_content = content.split('```json')[1].strip()
                        json_content = json_content.strip('```')
                        logging.debug(f"Response: {json_content}")
                    except Exception as e:
                        logging.error(f"Error parsing JSON content from response: {e} payload: {payload} content: {response}")
                        continue  # Skip to the next iteration of the inner loop if parsing fails
                    record = {
                        "ID": report_row["ID"],
                        "MRN": report_row["MRN"],
                        "ReportDate": report_row["Date"],
                        "Prompt Number": m,
                        "Expected Data Name": prompt_row["Field Name"],
                        "Extracted Data Value": content
                    }
                    records.append(record)
                except Exception as e:
                    logging.error(f"Error with endpoint communication or data handling: {e}")
                    continue  # Skip to the next iteration of the inner loop if API call or initial parsing fails

            total_processed += 1  # Increment after each report is fully processed

            # Print the progress for every 10th report processed
            if total_processed % 10 == 0:
                print(f"Cumulative reports processed so far: {total_processed}")

    output_file_path = os.path.join(output_dir, f"{timestamp}_output.csv")
    with open(output_file_path, 'w', newline='') as csvfile:
        fieldnames = ["ID", "MRN", "ReportDate", "Prompt Number", "Expected Data Name", "Extracted Data Value"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for record in records:
            writer.writerow(record)

    print(f"Total reports processed: {total_processed}")
    if logging.getLogger().level <= logging.INFO:
        logging.info(f"Total reports processed: {total_processed}")


if __name__ == "__main__":
    config_path = "./config.json"
    main(config_path)
