import pandas as pd
import math

# === PARAMETERS ===
INPUT_FILE = "export_NetTradeReport.csv"
OUTPUT_FILE = "filtered_assets.csv"
MIN_THRESHOLD = 5000  # optional filter


def get_round_base(value):
    """Return rounding base depending on value magnitude."""
    if value < 10:
        return 1
    magnitude = int(math.log10(abs(value)))
    if magnitude <= 2:
        return 10
    elif magnitude == 3:
        return 100
    elif magnitude == 4:
        return 1000
    elif magnitude == 5:
        return 10000
    elif magnitude == 6:
        return 100000
    else:
        return 10 ** (magnitude - 1)


def directional_adjust_and_round(value, direction, asset):
    """Apply ±10% and round by direction/magnitude. BTC gets ±0.1."""
    if str(asset).upper() == "BTC":
        if direction == "down":
            return round(value - 0.1, 1)
        elif direction == "up":
            return round(value + 0.1, 1)
        return round(value, 1)

    # Apply 10% adjustment
    if direction == "down":
        adjusted = value * 0.9
    elif direction == "up":
        adjusted = value * 1.1
    else:
        adjusted = value

    # Determine rounding base and apply rounding
    base = get_round_base(adjusted)
    if direction == "down":
        return math.floor(adjusted / base) * base
    elif direction == "up":
        return math.ceil(adjusted / base) * base
    else:
        return round(adjusted)


# === LOAD DATA ===
df = pd.read_csv(INPUT_FILE)
df["Native amount"] = pd.to_numeric(df["Native amount"], errors="coerce")

# === OPTIONAL FILTER ===
if MIN_THRESHOLD > 0:
    df = df[df["Nominal amount"] >= MIN_THRESHOLD]

# === APPLY LOGIC ===
def adjust_native(row):
    val = row["Native amount"]
    frm = str(row["from"]).upper()
    to = str(row["to"]).upper()
    asset = str(row["Asset"]).upper() if "Asset" in row else ""

    if frm == "CM" and to == "QF":
        return directional_adjust_and_round(val, "down", asset)
    elif frm == "QF" and to == "CM":
        return directional_adjust_and_round(val, "up", asset)
    else:
        return val


df["Adjusted Native"] = df.apply(adjust_native, axis=1)

# === KEEP ONLY REQUIRED COLUMNS ===
final_df = df[["Asset", "from", "to", "Adjusted Native"]]

# === SAVE OUTPUT ===
final_df.to_csv(OUTPUT_FILE, index=False)
print(f"Adjusted data saved to {OUTPUT_FILE}")
