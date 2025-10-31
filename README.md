Here’s a clear and professional README.md for your project — written so someone new could immediately understand what the script does and how to use it.

Post-Trade Settlement Rounding Script

This Python script filters asset data based on a nominal amount threshold, then applies direction-based rounding adjustments to the native amounts. It’s designed for post-trade settlement processes where small differences between systems (e.g., CM vs. QF) need to be normalized and rounded according to consistent rules.

🔍 What It Does

Reads a CSV file containing trade data with at least these columns:

Asset

from

to

Nominal amount

Native amount

Filters the dataset to include only rows where
Nominal amount >= MIN_THRESHOLD (default: 7500).

Adjusts and rounds the Native amount:

From CM → QF → rounds down 10% and to the nearest magnitude (e.g., thousands, hundreds).

From QF → CM → rounds up 10% and to the nearest magnitude.

BTC assets are handled specially: ±0.1 instead of ±10%.

All values under 10 are rounded to whole numbers.

Outputs a new CSV file (filtered_assets.csv) containing only:

Asset, from, to, Adjusted Native

⚙️ Requirements

Python 3.10+

pandas
 library

Install dependencies:

pip install pandas

🚀 How to Use

Place your input CSV file in the same directory as the script, named export.csv.

Adjust the parameters at the top of the script if needed:

INPUT_FILE = "export.csv"
OUTPUT_FILE = "filtered_assets.csv"
MIN_THRESHOLD = 7500


Run the script:

python post_trade_settlement.py


The script will output:

Filtered and adjusted data saved to filtered_assets.csv

📄 Example

Input:

Asset	from	to	Nominal amount	Native amount
USD	CM	QF	9328499	710293
USD	QF	CM	32487	2104
BTC	CM	QF	2100	2.4

Output (filtered_assets.csv):

Asset	from	to	Adjusted Native
USD	CM	QF	9000000
USD	QF	CM	2300
BTC	CM	QF	2.3
🧠 Logic Summary
Range (approx)	Rounded To	Adjustment (Direction)
< 10	whole number	±10% (±0.1 for BTC)
10 – 999	10s	±10%
1,000 – 9,999	100s	±10%
10,000 – 99,999	1,000s	±10%
100,000 – 999,999	10,000s	±10%
1,000,000+	Next lower order	±10%
🧾 Output

File: filtered_assets.csv

Columns: Asset, from, to, Adjusted Native

Example message:

Filtered and adjusted data saved to filtered_assets.csv

📬 Notes

The script assumes consistent capitalization for “from” and “to” values (CM / QF).

Modify MIN_THRESHOLD to include smaller or larger trades.

Works best with clean CSV input; invalid or missing numeric values are ignored.
