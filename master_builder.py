import pandas as pd
from data_loader import load_tickets, load_customers, load_materials, load_country_map


def build_master_df():
    tickets = load_tickets("data/tickets.csv")
    customers = load_customers("data/customers.csv")
    materials = load_materials("data/materials.csv")
    country_map = load_country_map("data/country_map.csv")

    master_df = tickets.merge(
        customers,
        how="left",
        left_on="CUSTOMER_ID",
        right_on="CUSTOMER_ID",
        suffixes=("", "_CUST")
    )

    master_df = master_df.merge(
        materials,
        how="left",
        left_on="MATERIAL_ID",
        right_on="MATERIAL_ID",
        suffixes=("", "_MAT")
    )

    master_df = master_df.merge(
        country_map,
        how="left",
        left_on="COUNTRY_4",
        right_on="COUNTRY_CODE_4",
        suffixes=("", "_CM")
    )

    return master_df

# Production-only build master data
#
# master_df = build_master_df()
# pd.set_option("display.max_rows", None)
# pd.set_option("display.max_columns", None)
# print(master_df)