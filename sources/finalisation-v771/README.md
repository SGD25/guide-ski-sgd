# Onglet « À dire au client » et fond des rappels — V07.71

Base : `b9d5a40746d04eaa428b854ac86dec4b655c258e`. La maquette n° 1 envoyée puis jointe par l’utilisateur est conservée dans `client-valide.png`. Le bouton bleu avec bulle de dialogue est repris de cette image dans `sources/guide/media/a-dire-client-onglet-v771.png`, en conservant ses proportions. Le rectangle d’extraction est documenté dans `asset.json`.

## Application

- **42 encarts et phrases client** : onglet bleu accroché au bord supérieur d’un cadre bleu ardoise, fond bleu très pâle et phrase en bleu foncé. Les phrases de chaque modèle sont conservées ; l’exemple générique de la maquette n’est pas copié sur les différents skis. Les bandes courtes utilisent une disposition compacte du même dessin.
- La phrase adressée aux parents en page 15 reste explicitement destinée aux parents dans le texte du cadre.
- **26 rappels « À retenir », pages 3–28** : onglet corail approuvé conservé, et fond **`#FCF0E9`**, le même orange très diffus que la troisième catégorie 50/50 de la page 12 (`SOFTS[2]`).
- Couverture, sommaire, autres contenus, images produits, photos de skieurs, logo SGD et navigation sont conservés. Les anciennes images restent disponibles.

`client-panels.json` garde chaque phrase et sa zone d’origine. `collect.py` les relève depuis les générateurs existants, en mémoire, sans remplacer leurs posters ; le script de la page 12 est seulement analysé, car il écrit directement des images. Les contenus du guide ne sont pas reconstruits à partir de ces rendus : seuls les encarts du manifeste V07.70 sont remplacés.

## Reproduire

1. `python sources/finalisation-v771/render.py`
2. `python sources/guide/build_site.py`
3. `node tests/guide-smoke.cjs`

Le composant commun est `Page.client` dans `sources/guide/render.py`. Le rendu vérifie la présence des 42 phrases, leur ajustement dans leur cadre, et l’absence de modification hors des zones des encarts avant encodage. `layout-report.json` garde les tailles de caractères retenues : les 41 phrases client gardent leur taille ; seule la bande destinée aux parents passe de 34 à 31 px. Les pages de sécurité restent en PNG et leurs liens sont conservés. Les rappels gardent exactement leur contenu précédent.
