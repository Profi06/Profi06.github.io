#!/usr/bin/env python3
from pathlib import Path
import re

def main():
    for p in Path.cwd().rglob("*.md"):
        if not p.is_file():
            continue

        new_path = Path(p.parent, p.stem + ".html")
        if new_path.exists():
            print(f"Could not convert {p} to {new_path} because {new_path} already exists.")
            continue

        m2h = p.read_text()
        # Blockquotes (need to be first)
        while re.search("^>+ ", m2h, flags=re.MULTILINE):
            m2h = re.sub(r"^(>*)>(.*)", r"\1<blockquote>\2</blockquote>", m2h, flags=re.MULTILINE)
            # Put consecutive lines in the same blockquote
            m2h = re.sub(r"</blockquote>\n(>*)<blockquote>", r"\n\1", m2h, flags=re.MULTILINE)

        # Headings: Hashtags at line start
        for i in range(6,0,-1):
            m2h = re.sub('^' + '#' * i + "(.*?)$", f"<h{i}>\\1</h{i}>", m2h, flags=re.MULTILINE)
        # Headings: Extra line with === or ---
        m2h = re.sub(r"^(.*?)\n=+$", r"<h1>\1</h1>", m2h, flags=re.MULTILINE)
        m2h = re.sub(r"^(.*?)\n-+$", r"<h2>\1</h2>", m2h, flags=re.MULTILINE)

        # Paragraphs
        m2h = re.sub(r"^((?:.+\n?)+)(?=\n\n)", r"<p>\1</p>", m2h, flags=re.MULTILINE)

        # Line Break with two trailing spaces
        m2h = re.sub(r"  $", r"<br>", m2h, flags=re.MULTILINE)

        # Text Formatting
        # Bold
        m2h = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", m2h, flags=re.MULTILINE)
        m2h = re.sub(r"(\s)__(.*?)__", r"\1<strong>\2</strong>", m2h, flags=re.MULTILINE)
        # Italic ( "(...|<strong>)" handles cases like ___this___ and **_that_** )
        m2h = re.sub(r"\*(.*?)\*", r"<em>\1</em>", m2h, flags=re.MULTILINE)
        m2h = re.sub(r"(\s|<strong>)_(.*?)_", r"\1<em>\2</em>", m2h, flags=re.MULTILINE)

        m2h = re.sub(r"", r"", m2h, flags=re.MULTILINE)
        m2h = re.sub(r"", r"", m2h, flags=re.MULTILINE)
        m2h = re.sub(r"", r"", m2h, flags=re.MULTILINE)
        m2h = re.sub(r"", r"", m2h, flags=re.MULTILINE)

        with new_path.open("x") as f:
            f.write(m2h)


if __name__ == "__main__":
    main()
