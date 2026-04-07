from __future__ import annotations

from pathlib import Path

import typer

from .compare.diff import compare_reports
from .dashboard import export_bi_views
from .gate import apply_gate
from .packs import compare_pack_artifacts, run_pack
from .pipeline import run_release_gate
from .runner import run_suite

app = typer.Typer(help="Release-grade GenAI evaluation platform CLI")


@app.command()
def run(
    suite: str = typer.Option(..., help="Evaluation suite name (e.g., rag_basic)"),
    model: str = typer.Option("mock", help="Model identifier"),
    out_dir: str = typer.Option(".", help="Output directory for artifacts"),
    max_workers: int = typer.Option(1, help="Max parallel workers"),
    timeout_seconds: float = typer.Option(10.0, help="Per-case timeout seconds"),
):
    dataset_path = f"datasets/{suite}/cases.jsonl"
    typer.echo(
        run_suite(
            suite_name=suite,
            dataset_path=dataset_path,
            model_name=model,
            out_dir=out_dir,
            max_workers=max_workers,
            timeout_seconds=timeout_seconds,
        )
    )


@app.command("run-pack")
def run_pack_cmd(
    suite: str = typer.Option(...),
    model: str = typer.Option("mock"),
    out_dir: str = typer.Option("."),
    repeat_count: int = typer.Option(5),
):
    dataset_path = f"datasets/{suite}/cases.jsonl"
    typer.echo(run_pack(suite_name=suite, dataset_path=dataset_path, model_name=model, out_dir=out_dir, repeat_count=repeat_count))


@app.command()
def compare(
    baseline: str = typer.Option(..., help="Baseline run id"),
    candidate: str = typer.Option(..., help="Candidate run id"),
    reports_dir: str = typer.Option("./reports", help="Reports directory"),
    out_dir: str = typer.Option(".", help="Output directory for compare artifacts"),
):
    baseline_report_path = Path(reports_dir) / f"{baseline}.json"
    candidate_report_path = Path(reports_dir) / f"{candidate}.json"
    typer.echo(compare_reports(str(baseline_report_path), str(candidate_report_path), out_dir=out_dir))


@app.command("compare-packs")
def compare_packs(
    baseline_pack_path: str = typer.Option(...),
    candidate_pack_path: str = typer.Option(...),
    out_dir: str = typer.Option("."),
):
    typer.echo(compare_pack_artifacts(baseline_pack_path=baseline_pack_path, candidate_pack_path=candidate_pack_path, out_dir=out_dir))


@app.command()
def gate(
 compare_artifact: str = typer.Option(..., help="Path to compare artifact JSON"),
 out_dir: str = typer.Option(".", help="Output directory for gate artifacts"),
 max_avg_score_drop: float = typer.Option(0.05, help="Maximum allowed avg score drop"),
 max_pass_rate_drop: float = typer.Option(0.10, help="Maximum allowed pass rate drop"),
 fail_on_any_regression_case: bool = typer.Option(False, help="Fail if any individual case regresses"),
 estimated_affected_query_pct: float = typer.Option(None, help="Estimated fraction of production queries affected, e.g. 0.12 for 12 percent"),
 max_affected_query_pct: float = typer.Option(0.10, help="Block if estimated affected query share exceeds this threshold"),
 daily_query_volume: int = typer.Option(None, help="Optional daily production query volume for impact estimation"),
 downstream_risk: str = typer.Option(None, help="Optional explicit downstream risk label: low, medium, high"),
 block_on_high_downstream_risk: bool = typer.Option(True, help="Block release if downstream risk is high"),
):
    typer.echo(
        apply_gate(
            compare_artifact_path=compare_artifact,
            out_dir=out_dir,
            max_avg_score_drop=max_avg_score_drop,
            max_pass_rate_drop=max_pass_rate_drop,
            fail_on_any_regression_case=fail_on_any_regression_case,
        )
    )


@app.command("export-dashboard")
def export_dashboard(out_dir: str = typer.Option(".", help="Artifact root to export from")):
    typer.echo(export_bi_views(root=out_dir))


@app.command("release-gate")
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
 fail_on_any_regression_case: bool = typer.Option(False, help="Fail if any individual case regresses"),
 estimated_affected_query_pct: float = typer.Option(None, help="Estimated fraction of production queries affected, e.g. 0.12 for 12 percent"),
 max_affected_query_pct: float = typer.Option(0.10, help="Block if estimated affected query share exceeds this threshold"),
 daily_query_volume: int = typer.Option(None, help="Optional daily production query volume for impact estimation"),
 downstream_risk: str = typer.Option(None, help="Optional explicit downstream risk label: low, medium, high"),
 block_on_high_downstream_risk: bool = typer.Option(True, help="Block release if downstream risk is high"),
):
    dataset_path = f"datasets/{suite}/cases.jsonl"
    typer.echo(run_release_gate(suite_name=suite, baseline_run_id=baseline, dataset_path=dataset_path, model_name=model, out_dir=out_dir, reports_dir=reports_dir))


if __name__ == "__main__":
    app()
