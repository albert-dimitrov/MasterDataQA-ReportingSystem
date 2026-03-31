from flask import Flask, render_template, request, send_from_directory
import pandas as pd

app = Flask(__name__)

issues_df = pd.read_csv("output/dq_issues.csv")
summary_df = pd.read_csv("output/dq_summary.csv")
matrics_df = pd.read_csv("output/dq_overall_metrics.csv")

@app.route("/")
def home():
    metrics_dict = {
        row["METRIC"]: row["VALUE"]
        for _, row in matrics_df.iterrows()
    }

    return render_template(
        "home.html",
        metrics=metrics_dict,
        check_summary=summary_df.to_dict(orient="records")
    )
@app.route("/issues")
def issues():
    df = issues_df.copy()

    ticket_id = request.args.get("ticketid")
    check_name = request.args.get("check_name")
    system = request.args.get("system")
    severity = request.args.get("severity")

    if ticket_id:
        df = df[df["TICKETID"].astype(str).str.lower().str.contains(ticket_id, na=False)]

    if check_name:
        df = df[df["CHECK_NAME"].astype(str).str.lower() == check_name.lower()]

    if system:
        df = df[df["SYSTEM"].astype(str).str.lower() == system.lower()]

    if severity:
        df = df[df["SEVERITY"].astype(str).str.lower() == severity.lower()]

    return render_template(
        "issues.html",
        issues=df.to_dict(orient="records"),
        filters={
            "ticketid": ticket_id or "",
            "check_name": check_name or "",
            "system": system or "",
            "severity": severity or "",
        }
    )

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(
        directory="output",
        path=filename,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)

