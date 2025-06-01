# Einbürgerungstest Fragen Scraper

A Python script that scrapes questions and answers from the German citizenship test (Einbürgerungstest) website and saves them to an organized Excel file. 

Feeling lazy? Just download the excel file from [here](Alle%20Fragen%20und%20Antworten%20zum%20Einbürgerungstest.xlsx).

## Features

- Scrapes questions and answers from all German states' citizenship test pages
- Saves data to a well-structured Excel file with separate sheets for each state
- Handles pagination automatically
- Includes error handling and retry mechanisms
- Randomizes user agents to avoid blocking
- Clean and organized output format

## Prerequisites

- Python 3.8+
- Required Python packages (see `pyproject.toml`)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/youpele52/leben_in_deutschland.git
   cd leben_in_deutschland
   ```

2. [Install uv (if not installed)](https://docs.astral.sh/uv/getting-started/installation/)

   

3. Create the Virtual Environment and Install Dependencies:
   ```bash
   uv venv
   uv sync
   ```

## Usage

1. Run the script:
   ```bash
   uv run main.py
   ```

2. The script will:
   - Scrape questions and answers from all German states' test pages
   - Save the data to an Excel file named "Alle Fragen und Antworten zum Einbürgerungstest.xlsx"
   - Create separate sheets for each state

## Configuration

You can modify the following in `constants.py`:
- `URLS`: List of URLs to scrape and their corresponding sheet names
- `FILE_NAME`: Name of the output Excel file (without extension)

## Output Format

The Excel file will contain:
- One sheet per German state
- Each sheet contains two columns:
  - `Frage`: The question text
  - `Antwort`: The correct answer

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This project is for educational purposes only. Please respect the website's terms of service and use responsibly.