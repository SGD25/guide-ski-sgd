# Guide — sources modifiables

`python sources/guide/render.py` conserve les pages 1 et 2 approuvées, génère les pages 3 à 9 et actualise uniquement le pied de page et le repère de chapitre des pages 10 à 12 en 2400 × 3394 pixels. La source de la page 12 reste dans `sources/page12/render.py` ; elle est utilisée seulement si cette page doit être modifiée.

`python sources/guide/build_site.py` relie les images au lecteur. `node tests/guide-smoke.cjs` vérifie l’ordre réel des scripts, les 12 pages, les images, les styles et les cibles des sommaires avant publication.

Les images sont versionnées dans `assets/guide-v754/` (pages 3–12) et `assets/guide-v753/` (pages 1–2). Les anciens visuels restent conservés. La palette est définie dans `design/charte-candidate-sgd.json` : bleu ardoise et turquoise, accents bleu glacier, corail et prune. Titres P052 Bold/Bold Italic et textes Nimbus Sans. Les deux familles de polices proviennent de `fonts-urw-base35`.

Les vrais visuels de produits sont placés sans déformation. Le personnage de la page 4 et les scènes de station des pages 8 et 9 sont des illustrations créées pour le guide ; voir `media/illustrations-v752.md` pour leurs consignes. Les mesures, les profils et les zones de rocker sont tracés séparément.

Le bouton Agrandir ou un clic sur une page passe à la lecture d’une seule page. Un second clic, avec le curseur loupe moins, revient à la vue double. Ce choix est conservé localement. Sur mobile, la page unique est automatique.

V07.53 : couverture et sommaire revus, aquarelles de montagne, ski nu Elan et zones anatomiques, largeur légèrement amplifiée dans le seul comparatif de la page 4, skis remis dans la main du personnage, cinq zones de contact avec la neige, définitions regroupées sous chaque construction, nouveaux visuels de bord de piste et de performance. Les illustrations de construction et leurs légendes ont été conservées. Les consignes des nouveaux visuels sont dans `media/illustrations-v753.json`.

V07.54 : retrait des vignettes de montagne répétées ; couleurs anatomiques distinctes ; gros plans de vrais patins à échelle commune sans déformation ; skis détourés placés devant le bras ; page rayon entièrement repensée avec les tracés R11 vert, R15 bleu et R20+ rouge ; sensations à l’intérieur des cadres de construction ; ouverture photographique du chapitre 2 ; vrai logo et repères de chapitre. Pages 1–2 conservées à l’identique. Le manifeste `approved-pages-v753.json` garantit la reconstruction depuis les pages approuvées ; les sources des nouveaux gros plans sont dans `media/produits-v754.json`.

V07.55 : les nouvelles pages 13–14 sont générées par `python sources/freeride-freestyle/render.py`, puis reliées par `python sources/guide/build_site.py`. Ce générateur conserve les douze images approuvées, sauf les accès ajoutés sur la page 8. Le lecteur et le test d’intégration exposent désormais 14 pages. Les sources techniques, photos originales et consignes des deux scènes illustratives sont conservées dans `sources/freeride-freestyle/`.
