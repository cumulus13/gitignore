#!/usr/bin/env python
# gitignore.py
# A simple script to generate a .gitignore file with default entries, additional entries, or
# templates from gitignore.io. It uses rich for console output and supports reading existing .gitignore files.
# Requires Python 3.6+ and the rich library.
# Copyright (c) 2023, Hadi Cahyadi <cumulus13@gmail.com>
# Homepage: https://github.com/cumulus13/gitignore
# Licensed under the MIT License.
# SPDX-License-Identifier: MIT

import sys
import argparse
import urllib.request
from pathlib import Path
from typing import List, Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.syntax import Syntax
try:
    from licface import CustomRichHelpFormatter
except ImportError:
    class CustomRichHelpFormatter(argparse.HelpFormatter):
        """Fallback formatter if licface is not installed."""
        def __init__(self, prog):
            super().__init__(prog, max_help_position=30, width=120)
            
from rich import traceback as rich_traceback
import os
rich_traceback.install(show_locals=False, theme='fruity', width=os.get_terminal_size().columns, extra_lines=1, word_wrap=True)
console = Console()

class GitignoreGenerator:
    DEFAULT_ENTRIES = [
        "*.pyc", "*.bak", "*.zip", "*.rar", "*.7z", "*.mp3", "*.wav", "*.sublime-workspace",
        ".hg/", "build/", "*.hgignore", "*.hgtags", "*dist/", "*.egg-info/", "traceback.log",
        "__pycache__/", "*.log"
    ]

    ICONS = {
        "start": "🚀",
        "write": "📝",
        "done": "✅",
        "error": "❌",
        "prompt": "❔"
    }

    @classmethod
    def fetch_template(cls, templates: List[str]) -> List[str]:
        try:
            url = f"https://www.toptal.com/developers/gitignore/api/{','.join(templates)}"
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (compatible; GitignoreGenerator/1.0)"}
            )
            with urllib.request.urlopen(req) as res:
                content = res.read().decode()
                return content.strip().splitlines()
        except Exception as e:
            console.print(f"{cls.ICONS['error']} [bold red]Failed fetch template from gitignore.io:[/bold red] {e}")
            return []

    @classmethod
    def generate(
        cls,
        path: Path,
        extra_entries: Optional[List[str]] = None,
        append: bool = False,
        force: bool = False,
        templates: Optional[List[str]] = None
    ) -> None:
        entries = []

        if templates:
            entries += cls.fetch_template(templates)

        entries += cls.DEFAULT_ENTRIES

        if extra_entries:
            entries += extra_entries

        gitignore_path = path / ".gitignore"

        if gitignore_path.exists() and not force and not append:
            answer = input(f"{cls.ICONS['prompt']} .gitignore file is already on {gitignore_path}. Overwrite? [y/N] ").strip().lower()
            if answer != 'y':
                console.print("[yellow]Canceled.[/yellow]")
                return

        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
                console=console,
            ) as progress:
                task = progress.add_task("[cyan]Write a .gitigignore file...", total=None)

                content = "\n".join(entries) + "\n"

                if append and gitignore_path.exists():
                    with gitignore_path.open("a", encoding="utf-8") as f:
                        f.write("\n" + content)
                else:
                    gitignore_path.write_text(content, encoding="utf-8")

                progress.update(task, description="[green]After writing .gitignore")
                progress.stop()

            console.print(Panel.fit(
                f"{cls.ICONS['done']} [bold green].gitignore successfully stored on:[/bold green] {gitignore_path}",
                border_style="green"
            ))
        except Exception as e:
            console.print(
                f"{cls.ICONS['error']} [bold red]Failed to make .gitignore:[/bold red] {e}"
            )

    @classmethod
    def read_gitignore(cls, path: Path) -> None:
        """Read .gitignore with rich.syntax Syntax Coloring."""
        gitignore_path = path / ".gitignore"
        if not gitignore_path.exists():
            console.print(f"{cls.ICONS['error']} [bold red].gitignore file does not exist at {gitignore_path}[/bold red]")
            return

        try:
            content = gitignore_path.read_text(encoding="utf-8")
            syntax = Syntax(content, "gitignore", word_wrap=True)
            console.print(Panel.fit(
                syntax,
                title=f"{cls.ICONS['write']} [bold blue]Content of .gitignore[/bold blue]",
                border_style="blue"
            ))
        except Exception as e:
            console.print(f"{cls.ICONS['error']} [bold red]Failed to read .gitignore:[/bold red] {e}")
            
def main():
    parser = argparse.ArgumentParser(
        description="Generate .gitignore With default data, additional, or template.",
        formatter_class=CustomRichHelpFormatter,
    )
    parser.add_argument(
        "entries", nargs="?",
    )
    parser.add_argument(
        "-p", "--path", type=Path, default=Path("."),
        help="Path target .gitignore (default: current directory)"
    )
    parser.add_argument(
        "-d", "--data", action="append", default=[],
        help="Additional entry .gitignore (can be repeated)"
    )
    parser.add_argument(
        "-t", "--template", nargs="+", help="Use a template from gitignore.io (for example: python node java)"
    )
    parser.add_argument(
        "-a", "--append", action="store_true", help="Add to .gitignore without overwrite"
    )
    parser.add_argument(
        "-f", "--force", action="store_true", help="Pass the prompt if .gitignore already exists"
    )
    parser.add_argument('-r', '--read', action='store_true', help='Read .gitignore file and print its content')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
        
    args = parser.parse_args()

    if args.entries:
        args.append = True  # If entries are provided, we assume the user wants to append them
        # replace \ to /
        args.entries = args.entries.replace("\\", "/")
        if "," in args.entries:
            args.data.extend(args.entries.split(","))
        elif "\n" in args.entries:
            args.data.extend(args.entries.splitlines())
        elif ";" in args.entries:
            args.data.extend(args.entries.split(";"))
        elif ":" in args.entries:
            args.data.extend(args.entries.split(":"))
        elif "|" in args.entries:
            args.data.extend(args.entries.split("|"))
        elif " " in args.entries:
            args.data.extend(args.entries.split())
        elif args.entries.startswith("[") and args.entries.endswith("]"):
            args.data.extend(args.entries[1:-1].split(","))
        elif args.entries.startswith("{") and args.entries.endswith("}"):
            args.data.extend(args.entries[1:-1].split(","))
        elif args.entries.startswith('"') and args.entries.endswith('"'):
            args.data.append(args.entries[1:-1])
        elif args.entries.startswith("'") and args.entries.endswith("'"):
            args.data.append(args.entries[1:-1])
        elif args.entries.startswith("`") and args.entries.endswith("`"):
            args.data.append(args.entries[1:-1])
        elif args.entries.strip():
            args.data.append(args.entries.strip())
        else:
            args.data.append(args.entries)
            
    if args.read:
        GitignoreGenerator.read_gitignore(path=args.path)
        return
            
    console.print(f"{GitignoreGenerator.ICONS['start']} [bold blue]Starting to make .gitignore ...[/bold blue]")
    GitignoreGenerator.generate(
        path=args.path,
        extra_entries=args.data,
        append=args.append,
        force=args.force,
        templates=args.template
    )


if __name__ == "__main__":
    main()
