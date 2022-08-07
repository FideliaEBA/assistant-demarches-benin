# Assistant démarches administratives — Bénin

Chatbot qui répond aux questions sur des démarches administratives au Bénin (casier judiciaire, NPI, IFU, documents d'état civil) et renvoie vers les sites officiels.

## Principe : une IA qui ne devine pas

La version 1 est un **moteur de recherche sémantique** (TF-IDF + similarité cosinus) : l'assistant retrouve la fiche la plus proche de la question dans une base de fiches vérifiées, puis l'affiche (étapes, pièces, coût, délai, lien officiel, date de vérification). Si aucune fiche n'est assez proche, il le dit au lieu d'inventer une réponse. C'est un choix volontaire : pour des démarches officielles, une fausse réponse est pire que pas de réponse.

> Les procédures changent vite (par exemple, le casier judiciaire est devenu instantané le 1er novembre 2026). Chaque fiche porte donc sa **date de vérification**, ses **sources** et le lien officiel à consulter.

## Utilisation

Interface web : ouvrir `index.html` dans un navigateur.

Version Python :

```
pip install -r requirements.txt
python assistant.py "comment avoir mon casier judiciaire ?"
python tester.py          # lance les tests de pertinence
```

## Structure

```
data/fiches.json       base de connaissances (à enrichir)
assistant.py           moteur de recherche TF-IDF (scikit-learn)
tester.py              tests : bonne fiche, ou aucune fiche pour une question hors sujet
build_web_data.py      convertit fiches.json en fiches.js pour la page web
index.html, style.css, script.js   interface de chat (moteur équivalent en JavaScript)
```

## Ajouter une démarche

1. Ajouter une fiche dans `data/fiches.json` (mêmes champs que les autres, avec sources et date de vérification).
2. Lancer `python build_web_data.py`.
3. Ajouter une question de test dans `tester.py` puis lancer `python tester.py`.

## Pistes d'amélioration

- Ajouter beaucoup plus de démarches (passeport, permis, mariage, inscription scolaire…)
- Version 2 (RAG) : brancher un modèle de langage pour formuler des réponses en langage naturel, uniquement à partir des fiches retrouvées
- Embeddings multilingues pour mieux comprendre les questions mal orthographiées
- Mode vocal pour les personnes peu à l'aise avec l'écrit

## Auteure

Fidélia EBA-DOVI, INSTI Lokossa. GitHub : [FideliaEBA](https://github.com/FideliaEBA)
