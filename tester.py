"""Petits tests : chaque question doit renvoyer la bonne fiche (ou aucune)."""
from assistant import Assistant

CAS = [
    ("comment avoir mon casier judiciaire ?", "casier-judiciaire"),
    ("je veux un extrait B3", "casier-judiciaire"),
    ("c'est quoi le NPI et comment le retrouver", "npi"),
    ("obtenir le certificat FID gratuitement", "npi"),
    ("comment obtenir mon IFU pour mes impôts", "ifu"),
    ("télécharger mon acte de naissance en ligne", "documents-anip"),
    ("certificat de résidence", "documents-anip"),
    ("où trouver mon numéro personnel d'identification", "npi"),
    ("combien coûte le casier", "casier-judiciaire"),
    ("quelle est la recette du gâteau au chocolat ?", None),
    ("quel temps fait-il demain à Cotonou", None),
]

if __name__ == "__main__":
    a, ok = Assistant(), 0
    for question, attendu in CAS:
        fiche, score = a.chercher(question)
        obtenu = fiche["id"] if fiche else None
        ok += obtenu == attendu
        print(f"{'OK ' if obtenu == attendu else 'ECHEC'} {score:.2f}  {question!r} -> {obtenu}")
    print(f"\n{ok}/{len(CAS)} tests réussis")
