from master_builder import build_master_df
from dq_checks import data_quality_checks
from reporting import generate_reports

# PRODUCTION_ONLY_FILE
# build master df
# check the quality of master data
# generate csv file reports in output folder

master_df = build_master_df()
issues_df = data_quality_checks(master_df)

generate_reports(master_df, issues_df)