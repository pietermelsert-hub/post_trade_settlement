import pandas as pd
import math

# === PARAMETERS ===
INPUT_FILE = "export.csv"
OUTPUT_FILE = "filtered_assets.csv"
MIN_THRESHOLD = 0  # Set to 7500 if you want to filter


def get_round_base(value):
    """Return rounding base depending on order of magnitude."""
    if value == 0:
        return 1
    magnitude = int(math.log10(abs(value)))
    # For example:
    # 100–999   → base 10
    # 1,000–9,999 → base 500
    # 10,000–99,999 → base 1,000
    # 100,000–999,999 → base 10,000
    # 1,000,000–9,999,999 → base 100,000
    if magnitude <= 2:
        return 5
    elif magnitude == 3:
        return 500
    elif magnitude == 4:
        return 1000
    elif magnitude == 5:
        return 10000
    elif magnitude == 6:
        return 100000
    elif magnitude == 7:
        return 1000000
    else:
        # default for large numbers
        return 10 ** (magnitude - 1)


def directional_round(value, direction):
    """Round value up or down depending on direction and magnitude."""
    base = get_round_base(value)
    if direction == "down":
        return math.floor(value / base) * base
    elif direction == "up":
        return math.ceil(value / base) * base
    return value


# === LOAD DATA ===
df = pd.read_csv(INPUT_FILE)
df["Nominal amount"] = pd.to_numeric(df["Nominal amount"], errors="coerce")

# Optional filtering
if MIN_THRESHOLD > 0:
    df = df[df["Nominal amount"] >= MIN_THRESHOLD]

# === APPLY ROUNDING ===
def adjust_nominal(row):
    value = row["Nominal amount"]

    if row["from"] == "CM" and row["to"] == "QF":
        return directional_round(value, "down")
    elif row["from"] == "QF" and row["to"] == "CM":
        return directional_round(value, "up")
    else:
        return value


df["Rounded number"] = df.apply(adjust_nominal, axis=1)

# === SAVE OUTPUT ===
df.to_csv(OUTPUT_FILE, index=False)
print(f"Rounded values saved to {OUTPUT_FILE}")
