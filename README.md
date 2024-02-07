Factory Clawer
This script is designed to scrape data from the Ministry of Economic Affairs (MOEA) website. It collects data related to factories based on selected industry types and areas.

Prerequisites
Python 3.x
Selenium WebDriver
Firefox browser
pandas
Installation
Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/factoryclawer.git
```
Install the required Python packages:
```bash
pip install -r requirements.txt
```
Usage
Set up the Firefox browser preferences for downloads:

Downloads will be saved to the specified directory (download_path).
Downloads will not prompt for confirmation.
Run the script factory_clawer.py:

```bash
python factory_clawer.py
```
Upon execution, the script will:

Launch the Firefox browser.
Navigate to the MOEA website.
Select industry types and areas as specified in the script.
Download factory data for each selected industry type and area.
Rename the downloaded files to include the corresponding area and industry type.
Repeat the process for all combinations of industry types and areas.
The downloaded data will be saved to the specified download directory.

Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.
