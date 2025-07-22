#!/usr/bin/env python3
"""Click integration example for Clicycle CLI framework."""

import time

import click

from clicycle import Clicycle, select_from_list

# Global Clicycle instance
cli = Clicycle(app_name="FileProcessor")


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.pass_context
def main(ctx, verbose):
    """File processing CLI tool with Clicycle integration."""
    # Ensure context object exists
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose

    # Display header
    cli.header("File Processor", "CLI tool with Click integration")

    if verbose:
        cli.debug("Verbose mode enabled")


@main.command()
@click.option("--input-dir", "-i", required=True, help="Input directory path")
@click.option("--output-dir", "-o", required=True, help="Output directory path")
@click.option(
    "--format",
    "-f",
    type=click.Choice(["json", "csv", "xml"]),
    default="json",
    help="Output format",
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without executing"
)
def process(input_dir, output_dir, output_format, dry_run):
    """Process files from input directory to output directory."""
    cli.section("File Processing")

    # Display configuration
    config_data = [
        {"label": "Input Directory", "value": input_dir},
        {"label": "Output Directory", "value": output_dir},
        {"label": "Output Format", "value": output_format.upper()},
        {"label": "Dry Run", "value": "Yes" if dry_run else "No"},
    ]
    cli.summary(config_data)

    if dry_run:
        cli.warning("Dry run mode - no files will be modified")

    # Simulate file processing
    files = [f"file_{i:03d}.txt" for i in range(1, 26)]  # 25 files

    cli.info(f"Found {len(files)} files to process")

    if not dry_run:
        confirmed = cli.confirm("Do you want to proceed with processing?")
        if not confirmed:
            cli.warning("Processing cancelled by user")
            return

    # Process files with progress bar
    with cli.progress("Processing files") as progress_cli:
        for i, filename in enumerate(files):
            progress_cli.update_progress(
                (i / len(files)) * 100, f"Processing {filename}"
            )
            time.sleep(0.1)  # Simulate processing time

    cli.success(f"Successfully processed {len(files)} files")

    # Display results
    results_data = [
        {"File Type": "Text Files", "Count": 20, "Status": "✓ Processed"},
        {"File Type": "Config Files", "Count": 3, "Status": "✓ Processed"},
        {"File Type": "Log Files", "Count": 2, "Status": "✓ Processed"},
    ]
    cli.table(results_data, title="Processing Results")


@main.command()
@click.option("--path", "-p", required=True, help="Path to validate")
@click.option("--rules", "-r", multiple=True, help="Validation rules to apply")
def validate(path, rules):
    """Validate files according to specified rules."""
    cli.section("File Validation")

    cli.info(f"Validating path: {path}")

    # If no rules specified, let user select
    if not rules:
        available_rules = [
            "syntax-check",
            "format-validation",
            "security-scan",
            "performance-check",
            "compliance-audit",
        ]

        cli.info("No validation rules specified")
        selected_rule = select_from_list(
            "validation rule", available_rules, default="syntax-check", cli=cli
        )
        rules = [selected_rule]

    cli.info(f"Applying {len(rules)} validation rule(s)")

    # Simulate validation with spinner
    for rule in rules:
        with cli.spinner(f"Running {rule}..."):
            time.sleep(2)

        # Simulate some validation results
        if rule == "syntax-check":
            cli.success("Syntax validation passed")
        elif rule == "security-scan":
            cli.warning("Found 2 potential security issues")
        else:
            cli.success(f"{rule} completed successfully")

    # Show validation summary
    cli.section("Validation Summary")
    validation_results = [
        {"Rule": rule.replace("-", " ").title(), "Status": "✓ Passed", "Issues": 0}
        for rule in rules
    ]
    cli.table(validation_results, title="Validation Results")


@main.command()
def status():
    """Show system status and configuration."""
    cli.section("System Status")

    # System info
    system_data = [
        {"Component": "File Processor", "Version": "1.0.0", "Status": "✓ Running"},
        {"Component": "Validation Engine", "Version": "2.1.3", "Status": "✓ Active"},
        {"Component": "Export Module", "Version": "1.5.0", "Status": "✓ Ready"},
        {"Component": "Security Scanner", "Version": "3.0.1", "Status": "⚠ Warning"},
    ]
    cli.table(system_data, title="System Components")

    # Show configuration
    cli.section("Configuration")
    config_data = [
        {"label": "Config File", "value": "~/.fileprocessor/config.json"},
        {"label": "Log Level", "value": "INFO"},
        {"label": "Max Concurrent", "value": "4"},
        {"label": "Temp Directory", "value": "~/.cache/fileprocessor"},
    ]
    cli.summary(config_data)

    # Recent activity
    cli.section("Recent Activity")
    with cli.block():
        cli.list_item("Processed 150 files in the last hour")
        cli.list_item("Validated 45 configurations today")
        cli.list_item("Exported 12 reports this week")


@main.command()
@click.option(
    "--format",
    "-f",
    type=click.Choice(["table", "json", "csv"]),
    default="table",
    help="Output format for the report",
)
def report(output_format):
    """Generate processing report."""
    cli.section("Generating Report")

    cli.info(f"Generating report in {output_format.upper()} format")

    # Simulate report generation
    with cli.spinner("Collecting data..."):
        time.sleep(1.5)

    with cli.spinner("Analyzing results..."):
        time.sleep(2)

    with cli.spinner("Formatting output..."):
        time.sleep(1)

    cli.success("Report generated successfully")

    # Show sample report data
    if output_format == "table":
        report_data = [
            {
                "Date": "2024-01-15",
                "Files Processed": 1250,
                "Errors": 5,
                "Success Rate": "99.6%",
            },
            {
                "Date": "2024-01-16",
                "Files Processed": 1180,
                "Errors": 2,
                "Success Rate": "99.8%",
            },
            {
                "Date": "2024-01-17",
                "Files Processed": 1340,
                "Errors": 8,
                "Success Rate": "99.4%",
            },
        ]
        cli.table(report_data, title="Processing Report (Last 3 Days)")

    elif output_format == "json":
        sample_json = {
            "report_date": "2024-01-17",
            "summary": {"total_files": 3770, "total_errors": 15, "success_rate": 0.996},
            "daily_stats": [
                {"date": "2024-01-15", "processed": 1250, "errors": 5},
                {"date": "2024-01-16", "processed": 1180, "errors": 2},
                {"date": "2024-01-17", "processed": 1340, "errors": 8},
            ],
        }
        cli.json(sample_json, title="Report JSON Output")

    else:  # CSV
        cli.code(
            "Date,Files Processed,Errors,Success Rate\\n"
            "2024-01-15,1250,5,99.6%\\n"
            "2024-01-16,1180,2,99.8%\\n"
            "2024-01-17,1340,8,99.4%",
            language="csv",
            title="Report CSV Output",
        )


if __name__ == "__main__":
    main()
