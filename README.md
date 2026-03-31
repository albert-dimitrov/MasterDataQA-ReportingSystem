# Master Data QA

## Overview

This project implements a **Master Data Quality** that ingests multiple CSV sources, 
normalizes and enriches the data, applies a defined set of data quality checks, 
and presents the results both as output files and through a simple web application.

The goal is to demonstrate clean data preparation, explicit and auditable data quality rules, 
and clear reporting suitable for operational monitoring — without using a database.

**Note:**  
This project uses **sample/demo data** inspired by realistic business scenarios. All data (including customer names, country codes, and agent names) is fictional and intended only for demonstration and portfolio purposes. No real company data or sensitive information is included.

## Environment Setup

### Python Version
- Python **3.10+** recommended

### Virtual Environment

Create and activate a virtual environment:

**Windows**

- python -m venv .venv
- .venv\Scripts\activate

**macOS/Linux**

- python3 -m venv .venv
- source .venv/bin/activate

### Install Dependencies

Before running the project, ensure your virtual environment is **activated**.

### Option 1 — Using requirements.txt

If the project includes a requirements.txt file, run:

- pip install -r requirements.txt

### Option 2 - Installing Manually
- pip install pandas
- pip install flask

## Project Files and Structure

### Data Folder — Source CSV Files

All input data files are stored in the `data` folder. 
These CSV files are used by the pipeline to build the 
master dataset and perform data quality checks.

#### Files

- **tickets.csv**  
  - Contains ticket information.

- **customers.csv**  
  - Customer master data.

- **materials.csv**  
  - Material master data.

- **country_map.csv**  
  - Reference table for mapping country codes to names and regions.

### Output Folder

The `output` folder contains all generated reports from the data quality pipeline. 
These files are created after running a scripts:

- **dq_issues.csv**  
  - Detailed list of all data quality issues from the master data.  
- **dq_summary.csv** 
  - Summary of issues by check name and severity.  
- **dq_overall_metrics.csv** 
  - Key metrics including total tickets, total issues, and tickets with at least one issue.  

### Static and Templates Folders

- `static` 
  - Contains CSS styles for the web app.
- `templates` 
  - Contains HTML templates used by Flask to render pages.  

### `data_loader.py`

This script handles **loading and normalizing all input CSV files** for the project.  

**Purpose:**
Loads and normalizes the CSV files from `data`.  
- Standardizes column names to `UPPER_SNAKE_CASE`  
- Strips whitespace  
- Ensures IDs are strings  
- Parses dates and normalizes country codes
- Normalizes the data

### `master_builder.py`

**Builds the master dataset** (`MASTER_DF`) by joining tickets, customers, materials, and country map.  
- Preserves all ticket rows  
- Normalizes and enriches data for further quality checks
- Uses `data_loader.py` to load and normalize the input CSV files

### `dq_checks.py`

Implements all **data quality checks** on the master dataset.  
- Detects missing keys, missing joins, invalid country codes, date logic errors, unknown statuses, payer rules, and numeric validation for materials etc.
- Produces a dataframe of **issues** (`NOT_OK` records) with standardized columns for reporting

### `reporting.py`

Generates the **output files** from the data quality checks:  

- `dq_issues.csv` 
  - all detected issues  
- `dq_summary.csv` 
  - counts of issues per check and severity  
- `dq_overall_metrics.csv` 
  - overall totals (tickets, issues, tickets with issues)  

This module is used after `dq_checks.py` to create files that the web app and reports consume.

### `output_creator.py`

This is the **main runner** script for **production use**.  

It performs the full pipeline:

1. Builds the master dataset using `master_builder.py`  
2. Runs data quality checks using `dq_checks.py`  
3. Generates CSV reports in the `output` folder using `reporting.py`  

**All steps are executed automatically when this script is run.**

**It will regenerate/generate the master data, data quality checks, and report files automatically.**

**If you want to test the reporting, make sure to delete the three files in `output` first and then run this script. This ensures you are generating fresh reports from the latest data.**

### `app.py`

This script launches the **Flask web application** to visualize the data quality results.  

Features:

- **Home page**: displays overall metrics and a summary table of issues.  
- **Issues page**: lists all data quality issues with case-insensitive filters by:
  - Ticket ID
  - Check Name
  - System
  - Severity  
- **CSV download links**: users can download the issue report and summary directly from the web UI.  

> Make sure the CSV files (`dq_issues.csv`, `dq_summary.csv`, `dq_overall_metrics.csv`) exist in the `output` folder before running the app.  
> If needed, regenerate them using `output_creator.py`.


#### Running the Flask Web App

To start the web application:

1. Make sure your virtual environment is activated and required packages are installed.
2. Ensure the `output/` folder contains the required CSV files:
   - `dq_issues.csv`
   - `dq_summary.csv`
   - `dq_overall_metrics.csv`
3. Run the app:
   - python app.py
4. Open your web browser and go to:
   - http://127.0.0.1:5000/









