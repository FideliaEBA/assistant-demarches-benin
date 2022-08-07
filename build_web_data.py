"""Convertit data/fiches.json en fiches.js pour que la page web fonctionne sans serveur.
À relancer après chaque modification de data/fiches.json."""
import json
from pathlib import Path

fiches = json.loads(Path("data/fiches.json").read_text(encoding="utf-8"))
Path("fiches.js").write_text("const FICHES = " + json.dumps(fiches, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")
print(f"{len(fiches)} fiches exportées dans fiches.js")
