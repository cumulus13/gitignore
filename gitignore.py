#!/usr/bin/env python

import argparse
import urllib.request
from pathlib import Path
from typing import List, Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

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
            console.print(f"{cls.ICONS['error']} [bold red]Gagal fetch template dari gitignore.io:[/bold red] {e}")
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
            answer = input(f"{cls.ICONS['prompt']} File .gitignore sudah ada di {gitignore_path}. Overwrite? [y/N] ").strip().lower()
            if answer != 'y':
                console.print("[yellow]Dibatalkan.[/yellow]")
                return

        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
                console=console,
            ) as progress:
                task = progress.add_task("[cyan]Menulis file .gitignore...", total=None)

                content = "\n".join(entries) + "\n"

                if append and gitignore_path.exists():
                    with gitignore_path.open("a", encoding="utf-8") as f:
                        f.write("\n" + content)
                else:
                    gitignore_path.write_text(content, encoding="utf-8")

                progress.update(task, description="[green]Selesai menulis .gitignore")
                progress.stop()

            console.print(Panel.fit(
                f"{cls.ICONS['done']} [bold green].gitignore berhasil disimpan di:[/bold green] {gitignore_path}",
                border_style="green"
            ))
        except Exception as e:
            console.print(
                f"{cls.ICONS['error']} [bold red]Gagal membuat .gitignore:[/bold red] {e}"
            )


def main():
    parser = argparse.ArgumentParser(
        description="Generate .gitignore dengan data default, tambahan, atau template."
    )
    parser.add_argument(
        "-p", "--path", type=Path, default=Path("."),
        help="Path target .gitignore (default: current directory)"
    )
    parser.add_argument(
        "-d", "--data", action="append", default=[],
        help="Tambahan entri .gitignore (bisa diulang)"
    )
    parser.add_argument(
        "-t", "--template", nargs="+", help="Gunakan template dari gitignore.io (contoh: python node java)"
    )
    parser.add_argument(
        "-a", "--append", action="store_true", help="Tambahkan ke .gitignore tanpa overwrite"
    )
    parser.add_argument(
        "-f", "--force", action="store_true", help="Lewati prompt jika .gitignore sudah ada"
    )

    args = parser.parse_args()

    console.print(f"{GitignoreGenerator.ICONS['start']} [bold blue]Memulai pembuatan .gitignore...[/bold blue]")
    GitignoreGenerator.generate(
        path=args.path,
        extra_entries=args.data,
        append=args.append,
        force=args.force,
        templates=args.template
    )


if __name__ == "__main__":
    main()
