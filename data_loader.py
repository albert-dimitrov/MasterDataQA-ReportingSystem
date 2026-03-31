import pandas as pd
import re


ID_COLUMNS = {"TICKETID", "CUSTOMERID", "MATERIALID"}
DATE_COLUMNS = {"CREATEDDATE", "COMPLETIONDATE"}

def to_snake(name: str) -> str:
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
    s2 = re.sub(r"(\D)(\d+)$", r"\1_\2", s2)
    return s2.upper()

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [to_snake(col.strip().replace(" ", "_")) for col in df.columns]
    return df

def strip_strings(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({"": None, "nan": None})
    return df

def normalize_country(country_value):
    if country_value is None:
        return None
    val = str(country_value).strip()
    if re.fullmatch(r"\d+", val):
        if len(val) == 3:
            return val.zfill(4)
        if len(val) == 4:
            return val
    return val

def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str)
    df = normalize_columns(df)
    df = strip_strings(df)
    return df

def load_tickets(path: str) -> pd.DataFrame:
    df = load_csv(path)
    # parse dates
    df["CREATED_DATE"] = pd.to_datetime(df.get("CREATED_DATE"), errors="coerce")
    df["COMPLETION_DATE"] = pd.to_datetime(df.get("COMPLETION_DATE"), errors="coerce")
    # add country columns
    df["COUNTRY_RAW"] = df.get("COUNTRY")
    df["COUNTRY_4"] = df["COUNTRY"].apply(normalize_country)
    return df

def load_customers(path: str) -> pd.DataFrame:
    return load_csv(path)

def load_materials(path: str) -> pd.DataFrame:
    return load_csv(path)

def load_country_map(path: str) -> pd.DataFrame:
    return load_csv(path)


# Production-only test -> ticket csv output
#
# tickets = load_tickets("data/tickets.csv")
# customers = load_customers("data/customers.csv")
# materials = load_materials("data/materials.csv")
# country_map = load_country_map("data/country_map.csv")
#
#
# with pd.option_context("display.max_rows", None, "display.max_columns", None):
#     print(tickets)
