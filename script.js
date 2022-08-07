// Moteur de recherche TF-IDF en JavaScript : même principe que assistant.py
const SEUIL = 0.10;
const MOTS_VIDES = new Set("le la les un une des de du d l et ou a au aux en pour par sur je j mon ma mes me moi ce cette ces est sont c quoi comment quel quelle quels quelles que qu qui dans avoir obtenir faire veux voudrais besoin peut puis il faut se sa son ses y".split(" "));

function normaliser(t) {
  return t.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^a-z0-9]+/g, " ").trim();
}
function tokens(t) {
  return normaliser(t).split(" ").filter(w => w && !MOTS_VIDES.has(w)).map(w => w.length > 3 ? w.replace(/[sx]$/, "") : w);
}
function texteFiche(f) {
  return [f.titre, f.mots_cles, f.mots_cles, f.resume, f.etapes.join(" ")].join(" ");
}

// Index : TF (sous-linéaire) x IDF, vecteurs normalisés
const docs = FICHES.map(f => tokens(texteFiche(f)));
const df = {};
docs.forEach(d => new Set(d).forEach(w => df[w] = (df[w] || 0) + 1));
const idf = w => Math.log((1 + docs.length) / (1 + (df[w] || 0))) + 1;
function vecteur(toks) {
  const tf = {};
  toks.forEach(w => tf[w] = (tf[w] || 0) + 1);
  const v = {};
  let n = 0;
  for (const w in tf) { v[w] = (1 + Math.log(tf[w])) * idf(w); n += v[w] ** 2; }
  n = Math.sqrt(n) || 1;
  for (const w in v) v[w] /= n;
  return v;
}
const index = docs.map(vecteur);

function chercher(question) {
  const q = vecteur(tokens(question));
  let best = -1, bestScore = 0;
  index.forEach((d, i) => {
    let s = 0;
    for (const w in q) if (d[w]) s += q[w] * d[w];
    if (s > bestScore) { bestScore = s; best = i; }
  });
  return bestScore >= SEUIL ? FICHES[best] : null;
}

// Affichage
const $ = id => document.getElementById(id);
function ajouter(classe, noeud) {
  const d = document.createElement("div");
  d.className = "msg " + classe;
  d.appendChild(noeud);
  $("chat").appendChild(d);
  d.scrollIntoView({ behavior: "smooth", block: "end" });
}
function texte(t) { const p = document.createElement("p"); p.textContent = t; return p; }

function carte(f) {
  const el = document.createElement("div");
  const liste = (tag, arr) => `<${tag}>${arr.map(x => `<li>${x}</li>`).join("")}</${tag}>`;
  el.innerHTML = `<h2></h2><p></p>
    <h3>Étapes</h3>${liste("ol", f.etapes)}
    <h3>Pièces</h3>${liste("ul", f.pieces)}
    <h3>Coût</h3><p>${f.cout}</p>
    <h3>Délai</h3><p>${f.delai}</p>
    <h3>À savoir</h3><p>${f.a_savoir}</p>
    <p><a href="${f.lien}" target="_blank" rel="noopener">Ouvrir le site officiel</a></p>
    <p class="meta">Information vérifiée le ${f.verifie_le.split("-").reverse().join("/")}. Les procédures changent : confirme toujours sur le site officiel.</p>`;
  el.querySelector("h2").textContent = f.titre;
  el.querySelector("p").textContent = f.resume;
  return el;
}

function poser(question) {
  ajouter("user", texte(question));
  const f = chercher(question);
  if (f) ajouter("bot", carte(f));
  else {
    const el = document.createElement("div");
    el.innerHTML = `<p>Je n’ai pas cette démarche dans ma base pour l’instant. Consulte le portail officiel : <a href="https://service-public.bj" target="_blank" rel="noopener">service-public.bj</a>.</p><p class="meta">Démarches que je connais : ${FICHES.map(f => f.titre).join(" · ")}</p>`;
    ajouter("bot", el);
  }
}

$("form").addEventListener("submit", e => {
  e.preventDefault();
  const q = $("q").value.trim();
  if (q) { poser(q); $("q").value = ""; }
});
["Casier judiciaire", "Retrouver mon NPI", "Obtenir mon IFU", "Acte de naissance en ligne"].forEach(t => {
  const b = document.createElement("button");
  b.type = "button"; b.textContent = t; b.onclick = () => poser(t);
  $("chips").appendChild(b);
});
ajouter("bot", texte("Bonjour ! Je peux t’expliquer : " + FICHES.map(f => f.titre.toLowerCase()).join(" ; ") + "."));
