import typer

app = typer.Typer(help="GenAI Evaluation Platform CLI")


@app.command()
def run(
    suite: str = typer.Option(..., help="Evaluation suite name"),
    model: str = typer.Option("mock", help="Model identifier"),
):
    """
    Run an evaluation suite.
    """
    typer.echo(f"Running suite={suite} model={model}")
    typer.echo("NOTE: runner not implemented yet")


@app.command()
def report(
    latest: bool = typer.Option(True, help="Generate report for latest run"),
):
    """
    Generate evaluation report.
    """
    typer.echo("Generating report (stub)")


@app.command()
def compare(
    baseline: str = typer.Option(..., help="Baseline run id"),
    candidate: str = typer.Option(..., help="Candidate run id"),
):
    """
    Compare two evaluation runs.
    """
    typer.echo(f"Comparing {baseline} vs {candidate} (stub)")


if __name__ == "__main__":
    app()
