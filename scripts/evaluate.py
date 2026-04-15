"""Run QueryForge evaluation suite from CLI."""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.eval.evaluator import run_evaluation


def main():
    version = sys.argv[1] if len(sys.argv) > 1 else "v1"
    print(f"Running QueryForge evaluation (prompt version: {version})...")

    results = run_evaluation(prompt_version=version)

    print(f"\n{'='*60}")
    print(f"Evaluation Complete — Prompt Version: {results['prompt_version']}")
    print(f"{'='*60}")
    print(f"Total Questions: {results['metrics']['total_questions']}")
    print(f"Total Tokens:    {results['metrics']['total_tokens']}")
    print(f"Avg Tokens/Query: {results['metrics']['avg_tokens_per_query']:.0f}")

    for r in results["results"]:
        print(f"\nQ: {r['question']}")
        print(f"  Generated: {r['generated_sql'][:80]}...")

    print(f"\nFull results logged to MLflow experiment: {version}")


if __name__ == "__main__":
    main()
