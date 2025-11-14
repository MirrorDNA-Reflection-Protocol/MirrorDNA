"""
reflect command - Performs simple local reflection and logging.
"""

import click
import json
from pathlib import Path
from datetime import datetime
import os


def get_reflection_log_path() -> Path:
    """
    Get the path to the reflection log file.

    Returns:
        Path to ~/.mirrordna/logs/reflect.log
    """
    home = Path.home()
    log_dir = home / ".mirrordna" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / "reflect.log"


def generate_reflection(text: str) -> str:
    """
    Generate a simple reflective paraphrase of the input text.

    This is a basic reflection engine that rephrases the input
    in a reflective manner.

    Args:
        text: Input text to reflect upon

    Returns:
        Reflective paraphrase
    """
    # Simple reflection patterns
    text_lower = text.lower().strip()

    # Detect question patterns
    if text_lower.endswith('?'):
        return f"You're wondering: {text[:-1]}. That's an important question to explore."

    # Detect emotional/feeling statements
    feeling_words = ['feel', 'feeling', 'felt', 'emotion', 'happy', 'sad', 'angry',
                     'frustrated', 'excited', 'anxious', 'worried']
    if any(word in text_lower for word in feeling_words):
        return f"I notice you're expressing: \"{text}\". It's valuable to acknowledge these observations."

    # Detect achievement/progress statements
    achievement_words = ['completed', 'finished', 'done', 'achieved', 'accomplished',
                        'succeeded', 'built', 'created', 'made']
    if any(word in text_lower for word in achievement_words):
        return f"Reflecting on your progress: \"{text}\". This represents meaningful forward movement."

    # Detect planning/future statements
    future_words = ['will', 'going to', 'plan to', 'want to', 'need to', 'should']
    if any(word in text_lower for word in future_words):
        return f"Your intention: \"{text}\". Setting clear direction is an important step."

    # Default reflective response
    return f"Reflecting on: \"{text}\". This observation captures a moment in your journey."


def log_reflection(text: str, reflection: str) -> dict:
    """
    Log a reflection entry to the reflection log file.

    Args:
        text: Original input text
        reflection: Generated reflection

    Returns:
        Log entry dictionary
    """
    log_path = get_reflection_log_path()

    # Create log entry
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": "reflection",
        "original_text": text,
        "reflection": reflection,
        "source": "mirrordna_cli"
    }

    # Append to log file
    with open(log_path, 'a') as f:
        f.write(json.dumps(entry) + "\n")

    return entry


@click.command(name="reflect")
@click.argument("text")
@click.option("--no-log", is_flag=True, help="Don't write to log file")
@click.option("--show-log", is_flag=True, help="Show log file location")
def reflect(text, no_log, show_log):
    """
    Perform a simple local reflection on text.

    Takes a text string and returns a reflective paraphrase.
    By default, writes an entry to ~/.mirrordna/logs/reflect.log

    Examples:
        mirrordna reflect "Today's work was productive"
        mirrordna reflect "How can I improve my workflow?" --show-log
        mirrordna reflect "Quick note" --no-log
    """
    try:
        # Generate reflection
        reflection = generate_reflection(text)

        # Display reflection
        click.echo()
        click.secho("Original:", fg="cyan")
        click.echo(f"  {text}")
        click.echo()
        click.secho("Reflection:", fg="green", bold=True)
        click.echo(f"  {reflection}")
        click.echo()

        # Log reflection (unless --no-log)
        if not no_log:
            entry = log_reflection(text, reflection)
            log_path = get_reflection_log_path()

            if show_log:
                click.secho(f"✓ Logged to: {log_path}", fg="yellow")
                click.echo(f"  Entry: {entry['timestamp']}")
            else:
                click.secho(f"✓ Reflection logged", fg="yellow")

        if show_log and no_log:
            log_path = get_reflection_log_path()
            click.echo(f"Log location: {log_path}")

    except Exception as e:
        click.secho(f"Error during reflection: {e}", fg="red", err=True)
        raise click.Abort()
