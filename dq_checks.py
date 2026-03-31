import pandas as pd
from master_builder import build_master_df


def data_quality_checks(master_df: pd.DataFrame) -> pd.DataFrame:
    issues = []

    def add_issue(row, name, severity, message):
        issues.append({
            "TICKETID": row["TICKET_ID"],
            "CHECK_NAME": name,
            "RESULT": "NOT_OK",
            "SEVERITY": severity,
            "MESSAGE": message,
            "SYSTEM": row["SYSTEM"],
        })

    for i, row in master_df.iterrows():

        # 1. Missing Keys
        if pd.isna(row["CUSTOMER_ID"]) or str(row["CUSTOMER_ID"]).strip() == "":
            add_issue(row, "MISSING_CUSTOMER_ID", "HIGH", "Missing customer ID")

        if pd.isna(row["MATERIAL_ID"]) or str(row["MATERIAL_ID"]).strip() == "":
            add_issue(row, "MISSING_MATERIAL_ID", "HIGH", "Missing material ID")

        # 2. Missing Joins
        if pd.notna(row["CUSTOMER_ID"]) and pd.isna(row["CUSTOMER_NAME"]):
            add_issue(row, "CUSTOMER_NOT_FOUND", "HIGH", "Customer not found")

        if pd.notna(row["MATERIAL_ID"]) and pd.isna(row["MATERIAL_TYPE"]):
            add_issue(row, "MATERIAL_NOT_FOUND", "HIGH", "Material not found")

        # 3. Country Validation
        if pd.notna(row["COUNTRY_4"]) and str(row["COUNTRY_4"]).isdigit() and pd.isna(row["COUNTRY_NAME"]):
            add_issue(row, "COUNTRY_NOT_MAPPED", "MEDIUM", "Country not found")

        # 4. Date Logic
        if pd.isna(row["COMPLETION_DATE"]):
            add_issue(row, "MISSING_COMPLETION_DATE", "HIGH", "Missing completion date")
        elif row["COMPLETION_DATE"] < row["CREATED_DATE"]:
            add_issue(row, "COMPLETION_BEFORE_CREATED", "HIGH", "Completion date before creation")

        # 5. Status Normalization
        if "(R)" in row["STATUS"]:
            status_clean = "Finally Rejected"
        else:
            status_clean = row["STATUS"]

        if status_clean not in {"Completed", "Open", "Finally Rejected"}:
            add_issue(row, "UNKNOWN_STATUS", "MEDIUM", "Status is unknown")

        # 6. Customer Payer Rule
        if pd.notna(row["PAYER_TO"]) and row["PAYER_TO"] == row["CUSTOMER_ID"]:
            add_issue(row, "PAYER_TO_SELF", "MEDIUM", "Payer to self")

        # 7. Material Numeric Validation
        if pd.isna(row["NET_WEIGHT_KG"]):

            if row["MATERIAL_TYPE"] == "FG":
                add_issue(row, "NET_WEIGHT_MISSING", "MEDIUM", "Net weight is missing for FG material")

        else:
            try:
                float(row["NET_WEIGHT_KG"])
            except ValueError:
                add_issue(row, "NET_WEIGHT_NOT_NUMERIC", "MEDIUM", "Net weight is not numeric")


    return pd.DataFrame(issues)

# Production-only build master data and quality check
#
# master_df = build_master_df()
# issues_df = data_quality_checks(master_df)
# pd.set_option("display.max_rows", None)
# pd.set_option("display.max_columns", None)
#
# print(issues_df)
