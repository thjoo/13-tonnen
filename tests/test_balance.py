"""Balance mit Bots (tests/balance.js): starke, mittlere und schwache Spielweise, je 150 Partien pro Version."""
import pathlib, shutil, subprocess, pytest

HIER = pathlib.Path(__file__).resolve().parent

@pytest.mark.skipif(not shutil.which("node"), reason="node fehlt")
def test_balance_mit_bots():
    r = subprocess.run(["node", str(HIER / "balance.js"), str(HIER.parent / "index.html")], capture_output=True, text=True, timeout=180)
    assert r.returncode == 0, r.stdout + r.stderr
