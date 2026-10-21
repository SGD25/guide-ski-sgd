# Guide — sources modifiables

`python sources/guide/render.py` génère les 12 pages complètes en 2400 × 3394 pixels. Les contenus de la page 12 restent dans `sources/page12/render.py`, appelé automatiquement.

`python sources/guide/build_site.py` relie les images au lecteur. `node tests/guide-smoke.cjs` vérifie l’ordre réel des scripts, les 12 pages, les images, les styles et les cibles des sommaires avant publication.

Les images sont versionnées dans `assets/guide-v752/`. Les anciens visuels restent conservés. La palette est définie dans `design/charte-candidate-sgd.json` : bleu ardoise et turquoise, accents bleu glacier, corail et prune. Titres P052 Bold/Bold Italic et textes Nimbus Sans. Les deux familles de polices proviennent de `fonts-urw-base35`.

Les vrais visuels de produits sont placés sans déformation. Le personnage de la page 4 et les scènes de station des pages 8 et 9 sont des illustrations créées pour le guide ; voir `media/illustrations-v752.md` pour leurs consignes. Les mesures, les profils et les zones de rocker sont tracés séparément.

Le bouton Agrandir ou un clic sur une page passe à la lecture d’une seule page. Ce choix est conservé localement. Sur mobile, la page unique est automatique.
