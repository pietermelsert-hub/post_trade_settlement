import pandas as pd
import math

# === PARAMETERS ===
INPUT_FILE = "export.csv"
OUTPUT_FILE = "filtered_assets.csv"
MIN_THRESHOLD = 7500  # Minimum nominal amount threshold

# === LOAD DATA ===
df = pd.read_csv(INPUT_FILE)

# Ensure numeric type for nominal amounts
df["Nominal amount"] = pd.to_numeric(df["Nominal amount"], errors="coerce")

# === FILTER BY THRESHOLD ===
filtered_df = df[df["Nominal amount"] >= MIN_THRESHOLD].copy()

# === ROUNDING LOGIC ===
def adjust_nominal(row):
    nominal = row["Nominal amount"]

    if row["From"] == "CM" and row["To"] == "QF":
        adjusted = math.floor(nominal * 0.95)
    elif row["From"] == "QF" and row["To"] == "CM":
        adjusted = math.ceil(nominal * 1.05)
    else:
        adjusted = nominal  # leave unchanged

    # If the asset is BTC, round to whole number
    if str(row["Asset"]).upper() == "BTC":
        adjusted = round(adjusted)

    return adjusted

filtered_df["Adjusted Nominal"] = filtered_df.apply(adjust_nominal, axis=1)

# === SAVE OUTPUT ===
filtered_df.to_csv(OUTPUT_FILE, index=False)

print(f"Filtered and adjusted data saved to {OUTPUT_FILE}")
