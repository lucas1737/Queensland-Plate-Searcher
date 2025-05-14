# Queensland Plate Searcher

A Python tool to quickly check Queensland vehicle registration details using the official Queensland Transport website.

## Overview

This script automates the process of checking vehicle registration details on the Queensland Transport website. It uses Selenium with the Edge browser to navigate the website, enter a plate number, and extract registration information.

## Features

- Automatically checks registration status for Queensland plate numbers
- Handles website navigation including terms acceptance
- Extracts detailed vehicle information
- Works with headless browser (no visible window)
- Command-line interface for easy use

## Requirements

- Python 3.6+
- Selenium
- Microsoft Edge browser

## Installation

1. Clone this repository:
```
git clone https://github.com/Galaxta/Queensland-Plate-Searcher.git
```

2. Navigate to the project directory:
```
cd Queensland-Plate-Searcher
```

The script will automatically install required packages if they're missing.

## Usage

Run the script with a plate number as an argument:
```
python Get-Registration.py ABC123
```

Or run without arguments to be prompted for input:
```
python Get-Registration.py
```

## Example Output

```
Registration details for plate number ABC123:
Registration status: Current
Registration expiry date: 01/01/2023
Vehicle make: TOYOTA
Vehicle model: COROLLA
Vehicle type: SEDAN
Vehicle color: WHITE
VIN/Chassis number: ABCD1234567890123
Engine number: 1AB2345678
```

## Planned Features

I'm planning to add these features in future updates:

- Batch Processing: Check multiple plate numbers from a text file
- Export Option: Save results to CSV or text files
- Retry Mechanism: Automatically retry failed requests
- Verbose/Silent Mode: Control the level of output detail
- Cleaner Results Display: Better formatted terminal output

## Disclaimer

This tool is for personal use only. Please ensure you comply with all relevant terms of service and privacy regulations when using this tool. This is not an official Queensland Transport product.

## License

This project is private and not licensed for public distribution.