"""Assistant sur les démarches administratives béninoises (moteur de recherche TF-IDF).

L'assistant ne « devine » jamais : il retrouve la fiche la plus proche de la question
dans data/fiches.json et la présente. S'il ne trouve rien de pertinent, il le dit.

Utilisation :
    python assistant.py                     # mode conversation
    python assistant.py "comment avoir mon casier ?"
"""
import json
import sys
import unicodedata
import re
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SEUIL = 0.10
MOTS_VIDES = {"le", "la", "les", "un", "une", "des", "de", "du", "d", "l", "et", "ou", "a", "au", "aux", "en",
              "pour", "par", "sur", "je", "j", "mon", "ma", "mes", "me", "moi", "ce", "cette", "ces", "est", "sont",
              "c", "quoi", "comment", "quel", "quelle", "quels", "quelles", "que", "qu", "qui", "dans", "avoir", "obtenir",
              "faire", "veux", "voudrais", "besoin", "peut", "puis", "il", "faut", "se", "sa", "son", "ses", "y"}


def normaliser(texte: str) -> str:
    texte = unicodedata.normalize("NFD", texte.lower())
    texte = "".join(c for c in texte if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", texte).strip()


def texte_fiche(f: dict) -> str:
    # Les mots-clés sont répétés pour qu'ils pèsent plus que le reste du texte
    return " ".join([f["titre"], f["mots_cles"], f["mots_cles"], f["resume"], " ".join(f["etapes"])])


class Assistant:
    def __init__(self, chemin: str = "data/fiches.json"):
        self.fiches = json.loads(Path(chemin).read_text(encoding="utf-8"))
        self.vec = TfidfVectorizer(preprocessor=normaliser, stop_words=sorted(MOTS_VIDES),
                                   ngram_range=(1, 2), sublinear_tf=True)
        self.matrice = self.vec.fit_transform([texte_fiche(f) for f in self.fiches])

    def chercher(self, question: str):
        scores = cosine_similarity(self.vec.transform([question]), self.matrice)[0]
        i = int(scores.argmax())
        return (self.fiches[i], float(scores[i])) if scores[i] >= SEUIL else (None, float(scores[i]))


def afficher(f: dict) -> str:
    l = [f"\n=== {f['titre']} ===", f["resume"], "\nÉtapes :"]
    l += [f"  {i}. {e}" for i, e in enumerate(f["etapes"], 1)]
    l += ["\nPièces :"] + [f"  - {p}" for p in f["pieces"]]
    l += [f"\nCoût : {f['cout']}", f"Délai : {f['delai']}", f"À savoir : {f['a_savoir']}",
          f"Lien officiel : {f['lien']}", f"(Information vérifiée le {f['verifie_le']} : les procédures changent, "
          "confirme toujours sur le site officiel.)"]
    return "\n".join(l)


def repondre(a: Assistant, question: str) -> str:
    fiche, score = a.chercher(question)
    if fiche is None:
        return ("Je n'ai pas cette démarche dans ma base pour l'instant. "
                "Consulte le portail officiel : https://service-public.bj")
    return afficher(fiche)


if __name__ == "__main__":
    a = Assistant()
    if len(sys.argv) > 1:
        print(repondre(a, " ".join(sys.argv[1:])))
    else:
        print("Assistant démarches Bénin (tape 'q' pour quitter)")
        while (q := input("\nTa question : ").strip().lower()) not in {"q", "quitter"}:
            print(repondre(a, q))
