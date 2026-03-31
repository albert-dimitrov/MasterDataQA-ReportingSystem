import os
import pandas as pd


def generate_reports(master_df: pd.DataFrame, issues_df: pd.DataFrame):
    os.makedirs("output", exist_ok=True)

    issues_df.to_csv("output/dq_issues.csv", index=False)

    check_summary = (
        issues_df
        .groupby(["CHECK_NAME", "SEVERITY"])
        .size()
        .reset_index(name="ISSUE_COUNT")
        .sort_values(["SEVERITY", "CHECK_NAME"])
    )
    check_summary.to_csv("output/dq_summary.csv", index=False)

    overall_metrics = pd.DataFrame([
        {"METRIC": "TOTAL_TICKETS", "VALUE": master_df["TICKET_ID"].nunique()},
        {"METRIC": "TOTAL_ISSUES", "VALUE": len(issues_df)},
        {"METRIC": "TICKETS_WITH_ISSUES", "VALUE": issues_df["TICKETID"].nunique()},
    ])

    overall_metrics.to_csv("output/dq_overall_metrics.csv", index=False)

    return check_summary, overall_metrics
