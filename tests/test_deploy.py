import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import deploy  # noqa: E402


def make_root(tmp_path, version="1.2.3"):
    tmp_path.mkdir(parents=True, exist_ok=True)
    (tmp_path / "VERSION").write_text(version + "\n", encoding="utf-8")
    pkg = tmp_path / "shortener"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    return tmp_path


def test_build_version_with_sha(tmp_path):
    root = make_root(tmp_path)
    assert deploy.build_version(root, sha="abcdef1234567") == "1.2.3+abcdef1"


def test_build_version_without_sha(tmp_path, monkeypatch):
    monkeypatch.delenv("GITHUB_SHA", raising=False)
    assert deploy.build_version(make_root(tmp_path)) == "1.2.3"


def test_deploy_writes_version_file_and_copies_package(tmp_path):
    root = make_root(tmp_path / "src")
    target = tmp_path / "deployed"
    version = deploy.deploy(target, root=root, sha="deadbeefcafe")
    assert version == "1.2.3+deadbee"
    assert (target / "VERSION").read_text(encoding="utf-8").strip() == "1.2.3+deadbee"
    assert (target / "shortener" / "__init__.py").exists()
