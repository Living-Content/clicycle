"""Prompts for the CLI."""

import click

from .core import Clicycle


def select_from_list(
    item_name: str,
    options: list[str],
    default: str | None = None,
    cli: Clicycle | None = None,
) -> str:
    """Renders a list of options and prompts the user to select one."""
    # Use provided Clicycle instance or create a new one
    if cli is None:
        cli = Clicycle()

    cli.info(f"Available {item_name}s:")
    for i, option in enumerate(options, 1):
        cli.info(f"  {i}. {option}")

    prompt_text = f"Select a {item_name}"
    if default and default in options:
        try:
            default_index = options.index(default) + 1
            prompt_text += f" (default: {default_index})"
        except ValueError:
            default_index = None  # Should not happen, but for safety
    else:
        default_index = None

    choice = cli.prompt(prompt_text, type=int, default=default_index)

    if not 1 <= choice <= len(options):
        raise click.UsageError(
            f"Invalid selection. Please choose a number between 1 and {len(options)}."
        )

    return options[choice - 1]
