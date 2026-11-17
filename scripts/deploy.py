"""Mock-деплой: имитирует выкладку и записывает версию в deployed/VERSION.

Использование:  python scripts/deploy.py [--target deployed]
Версия = содержимое файла VERSION + короткий SHA коммита (из GITHUB_SHA, если задан).
"""

import argparse
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def build_version(root: Path = ROOT, sha: str | None = None) -> str:
    base = (root / "VERSION").read_text(encoding="utf-8").strip()
    sha = sha if sha is not None else os.environ.get("GITHUB_SHA", "")
    return f"{base}+{sha[:7]}" if sha else base


def deploy(target: Path, root: Path = ROOT, sha: str | None = None) -> str:
    version = build_version(root, sha)
    print(f"[deploy] версия {version}")
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(root / "shortener", target / "shortener", ignore=shutil.ignore_patterns("__pycache__"))
    print(f"[deploy] скопирован пакет shortener -> {target / 'shortener'}")
    (target / "VERSION").write_text(version + "\n", encoding="utf-8")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"[deploy] записан {target / 'VERSION'} ({stamp})")
    print("[deploy] готово")
    return version


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default="deployed", type=Path)
    args = parser.parse_args(argv)
    deploy(args.target if args.target.is_absolute() else ROOT / args.target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
