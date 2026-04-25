import os
import json
import csv
from datetime import datetime
from config.settings import EVAL_RESULTS_DIR

def ensure_eval_dir():
    if not os.path.exists(EVAL_RESULTS_DIR):
        os.makedirs(EVAL_RESULTS_DIR)

def generate_json_report(results: list, summary_metrics: dict) -> str:
    path = os.path.join(EVAL_RESULTS_DIR, "latest_eval.json")
    payload = {
        "timestamp": datetime.now().isoformat(),
        "summary": summary_metrics,
        "results": results
    }
    with open(path, "w") as f:
        json.dump(payload, f, indent=4)
    return path

def generate_csv_report(results: list) -> str:
    if not results:
        return ""
    path = os.path.join(EVAL_RESULTS_DIR, "latest_eval.csv")
    keys = results[0].keys()
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)
    return path

def generate_md_report(summary_metrics: dict, failed_cases: list) -> str:
    path = os.path.join(EVAL_RESULTS_DIR, "summary.md")
    
    md_content = f"# Evaluation Summary Report\n"
    md_content += f"*Generated at {datetime.now().isoformat()}*\n\n"
    
    md_content += "## Aggregate Metrics\n"
    for metric, value in summary_metrics.items():
        if isinstance(value, float):
            md_content += f"- **{metric}**: {value:.2f}\n"
        else:
            md_content += f"- **{metric}**: {value}\n"
            
    md_content += "\n## Failed Cases\n"
    if failed_cases:
        for fc in failed_cases:
            md_content += f"### Test Case: {fc.get('id', 'unknown')}\n"
            md_content += f"- **Question**: {fc.get('question', 'N/A')}\n"
            md_content += f"- **Issue**: {fc.get('error', 'Mismatch validation')}\n\n"
    else:
        md_content += "No major failures detected across bounds! Perfect execution.\n"
        
    with open(path, "w") as f:
        f.write(md_content)
    return path
    
def publish_reports(results: list, summary_metrics: dict, failed_cases: list):
    ensure_eval_dir()
    generate_json_report(results, summary_metrics)
    generate_csv_report(results)
    generate_md_report(summary_metrics, failed_cases)
    print(f"Reports successfully generated in {EVAL_RESULTS_DIR}/")
