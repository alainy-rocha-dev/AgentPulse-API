"""
Live evaluation of the repair loop with a real LLM.

Runs the orchestrator (deterministic tool + LLM + Pydantic repair loop) on a fixed set of tasks and
counts how many answers passed on the first try, how many needed the repair loop, and how many
failed every attempt. No Docker, database or Celery needed: it calls the same code the worker runs.

Usage:
    export GROQ_API_KEY=...              # or OPENAI_API_KEY
    python -m eval.live_repair_eval --runs 3

Results are printed and saved to eval/results/repair_live_<timestamp>.json.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

from app.services.agent_orchestrator import AgentOrchestrator
from app.services.llm_client import LLMError, client_from_env
from app.services.repair_loop import SchemaValidationError

TASKS = [
    ("contract_analysis", [{"issue": "No late-payment penalty", "severity": "HIGH"}]),
    ("contract_analysis", [
        {"issue": "Auto-renewal without notice", "severity": "MEDIUM"},
        {"issue": "Unlimited liability for the supplier", "severity": "HIGH"},
        {"issue": "Jurisdiction clause missing", "severity": "MEDIUM"},
    ]),
    ("contract_analysis", []),
    ("compliance_review", [
        {"issue": "Personal data kept beyond retention period", "severity": "HIGH"},
        {"issue": "No data processing agreement with vendor", "severity": "HIGH"},
        {"issue": "Privacy policy last reviewed two years ago", "severity": "LOW"},
    ]),
    ("compliance_review", [{"issue": "Access logs not reviewed monthly", "severity": "MEDIUM"}]),
    ("vendor_risk", [
        {"issue": "Single supplier for a critical component", "severity": "HIGH"},
        {"issue": "No SLA for incident response", "severity": "MEDIUM"},
    ]),
    ("vendor_risk", [
        {"issue": "Supplier certification expired", "severity": "MEDIUM"},
        {"issue": "Payment terms of 90 days", "severity": "LOW"},
        {"issue": "No business continuity plan", "severity": "HIGH"},
        {"issue": "Shared admin credentials", "severity": "HIGH"},
    ]),
    ("support_ticket_triage", [
        {"issue": "Checkout fails for some card brands", "severity": "HIGH"},
        {"issue": "Typo on the pricing page", "severity": "LOW"},
    ]),
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Live repair-loop evaluation")
    parser.add_argument("--runs", type=int, default=3, help="runs per task")
    parser.add_argument("--pause", type=float, default=2.0, help="seconds between calls (free tiers)")
    args = parser.parse_args()
    logging.disable(logging.WARNING)

    client = client_from_env()
    if client is None:
        print("Set GROQ_API_KEY or OPENAI_API_KEY to run the live evaluation.")
        return 2

    samples, statuses, error_kinds = [], Counter(), Counter()
    total = len(TASKS) * args.runs
    print(f"Model: {client.label} | {len(TASKS)} tasks x {args.runs} runs = {total}\n")

    n = 0
    for run in range(args.runs):
        for task_type, items in TASKS:
            n += 1
            orchestrator = AgentOrchestrator(llm_client=client)
            sample = {"task_type": task_type, "items": len(items), "run": run + 1}
            try:
                result = orchestrator.run_task(task_type, {"items": items})
                attempts = result.metadata.repair_attempts + 1
                status = "first_try" if attempts == 1 else "repaired"
                sample.update(status=status, attempts=attempts,
                              seconds=result.metadata.execution_time_seconds)
            except SchemaValidationError:
                status = "failed"
                sample.update(status=status, attempts=len(orchestrator.last_attempt_errors))
            except LLMError as exc:
                status = "provider_error"
                sample.update(status=status, error=str(exc)[:200])
                if "HTTP 401" in str(exc):
                    print(f"Invalid API key: {exc}")
                    return 1
            sample["rejected"] = orchestrator.last_attempt_errors
            for err in orchestrator.last_attempt_errors:
                error_kinds[err.split(":", 1)[0]] += 1
            statuses[status] += 1
            samples.append(sample)
            print(f"[{n:>2}/{total}] {task_type:<22} {status}")
            time.sleep(args.pause)

    answered = total - statuses["provider_error"]
    rate = lambda k: round(statuses[k] / answered, 3) if answered else 0.0
    summary = {
        "mode": "live",
        "model": client.label,
        "tasks": len(TASKS),
        "runs_per_task": args.runs,
        "total": total,
        "answered": answered,
        "first_try": rate("first_try"),
        "repaired": rate("repaired"),
        "failed": rate("failed"),
        "provider_errors": statuses["provider_error"],
        "rejection_kinds": dict(error_kinds),
        "samples": samples,
    }

    print(f"\nAnswered: {answered}/{total}")
    for key in ("first_try", "repaired", "failed"):
        print(f"  {key:<10} {statuses[key]:>3}  ({summary[key]:.0%})")
    if error_kinds:
        print("Rejections by kind:", dict(error_kinds))

    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / f"repair_live_{datetime.now():%Y%m%d-%H%M%S}.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSaved to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
