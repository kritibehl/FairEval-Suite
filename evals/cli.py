from pathlib import Path

import typer

from .runner import run_suite
from .compare.diff import compare_reports
from .gate import apply_gate
from .pipeline import run_release_gate

app = typer.Typer(help="GenAI Evaluation Platform CLI")


@app.command()
def run(
    suite: str = typer.Option(..., help="Evaluation suite name (e.g., rag_basic)"),
    model: str = typer.Option("mock", help="Model identifier"),
    out_dir: str = typer.Option(".", help="Output directory for artifacts"),
    max_workers: int = typer.Option(1, help="Max parallel workers"),
    timeout_seconds: float = typer.Option(10.0, help="Per-case timeout seconds"),
):
    dataset_path = f"datasets/{suite}/cases.jsonl"
    res = run_suite(
        suite_name=suite,
        dataset_path=dataset_path,
        model_name=model,
        out_dir=out_dir,
        max_workers=max_workers,
        timeout_seconds=timeout_seconds,
    )
    typer.echo(res)


@app.command()
def compare(
    baseline: str = typer.Option(..., help="Baseline run id"),
    candidate: str = typer.Option(..., help="Candidate run id"),
    reports_dir: str = typer.Option("./reports", help="Reports directory"),
    out_dir: str = typer.Option(".", help="Output directory for compare artifacts"),
):
    baseline_report_path = Path(reports_dir) / f"{baseline}.json"
    candidate_report_path = Path(reports_dir) / f"{candidate}.json"

    if not baseline_report_path.exists():
        raise typer.BadParameter(f"baseline report not found: {baseline_report_path}")

    if not candidate_report_path.exists():
        raise typer.BadParameter(f"candidate report not found: {candidate_report_path}")

    res = compare_reports(
        baseline_report_path=str(baseline_report_path),
        candidate_report_path=str(candidate_report_path),
        out_dir=out_dir,
    )
    typer.echo(res)


@app.command()
def gate(
    compare_artifact: str = typer.Option(..., help="Path to compare artifact JSON"),
    out_dir: str = typer.Option(".", help="Output directory for gate artifacts"),
    max_avg_score_drop: float = typer.Option(0.05, help="Maximum allowed avg score drop"),
    max_pass_rate_drop: float = typer.Option(0.10, help="Maximum allowed pass rate drop"),
    fail_on_any_regression_case: bool = typer.Option(
        False, help="Fail if any individual case regresses"
    ),
):
    res = apply_gate(
        compare_artifact_path=compare_artifact,
        out_dir=out_dir,
        max_avg_score_drop=max_avg_score_drop,
        max_pass_rate_drop=max_pass_rate_drop,
        fail_on_any_regression_case=fail_on_any_regression_case,
    )
    typer.echo(res)


@app.command()
def release_gate(
    suite: str = typer.Option(..., help="Evaluation suite name"),
    baseline: str = typer.Option(..., help="Baseline run id"),
    model: str = typer.Option("mock", help="Model identifier"),
    out_dir: str = typer.Option(".", help="Output directory for artifacts"),
    reports_dir: str = typer.Option("./reports", help="Reports directory for baseline lookup"),
    max_workers: int = typer.Option(1, help="Max parallel workers"),
    timeout_seconds: float = typer.Option(10.0, help="Per-case timeout seconds"),
    max_avg_score_drop: float = typer.Option(0.05, help="Maximum allowed avg score drop"),
    max_pass_rate_drop: float = typer.Option(0.10, help="Maximum allowed pass rate drop"),
    fail_on_any_regression_case: bool = typer.Option(
        False, help="Fail if any individual case regresses"
    ),
):
    dataset_path = f"datasets/{suite}/cases.jsonl"
    res = run_release_gate(
        suite_name=suite,
        baseline_run_id=baseline,
        dataset_path=dataset_path,
        model_name=model,
        out_dir=out_dir,
        reports_dir=reports_dir,
        max_workers=max_workers,
        timeout_seconds=timeout_seconds,
        max_avg_score_drop=max_avg_score_drop,
        max_pass_rate_drop=max_pass_rate_drop,
        fail_on_any_regression_case=fail_on_any_regression_case,
    )
    typer.echo(res)


if __name__ == "__main__":
    app()
