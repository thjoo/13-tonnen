"""Gruppenspiel mit drei Geraeten gegen einen nachgebauten Speicher (tests/gruppe.js, ohne Firebase)."""
import pathlib, shutil, subprocess, pytest

HIER = pathlib.Path(__file__).resolve().parent

@pytest.mark.skipif(not shutil.which("node"), reason="node fehlt")
def test_gruppenspiel_drei_geraete():
    r = subprocess.run(["node", str(HIER / "gruppe.js"), str(HIER.parent / "index.html")], capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stdout + r.stderr
