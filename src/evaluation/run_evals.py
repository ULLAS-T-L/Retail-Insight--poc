import argparse
import sys
from src.evaluation.rag_evaluator import evaluate_rag
from src.evaluation.agent_evaluator import evaluate_agent
from src.evaluation.memory_evaluator import evaluate_memory
from src.evaluation.report_generator import publish_reports

def run_evals():
    parser = argparse.ArgumentParser(description="Run advanced evaluations natively.")
    parser.add_argument("--mode", choices=["rag", "agent", "memory", "all"], required=True, help="Evaluation mode")
    args = parser.parse_args()

    results = []
    summary = {}
    failed_cases = []

    if args.mode in ["rag", "all"]:
        print("\n--- Running RAG Evaluation ---")
        rag_res, rag_sum, rag_fails = evaluate_rag()
        results.extend(rag_res)
        summary.update(rag_sum)
        failed_cases.extend(rag_fails)

    if args.mode in ["agent", "all"]:
        print("\n--- Running Agent Evaluation ---")
        agent_res, agent_sum, agent_fails = evaluate_agent()
        results.extend(agent_res)
        summary.update(agent_sum)
        failed_cases.extend(agent_fails)

    if args.mode in ["memory", "all"]:
        print("\n--- Running Memory Evaluation ---")
        mem_res, mem_sum, mem_fails = evaluate_memory()
        results.extend(mem_res)
        summary.update(mem_sum)
        failed_cases.extend(mem_fails)

    print("\n--- Generating Reports ---")
    publish_reports(results, summary, failed_cases)

if __name__ == "__main__":
    run_evals()
