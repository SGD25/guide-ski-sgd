# Textile et harmonisation — V07.72

Double page approuvée par l’utilisateur, insérée après les exemples de ski de fond et avant Sécuriser.

- Pages 25–26 : l’image approuvée est divisée en deux, sans régénération des illustrations ni du texte. Seuls les anciens repères de haut et bas de page sont remplacés par les éléments communs.
- Pages 2–30 : mêmes coordonnées, polices et couleurs de chapitre pour les en-têtes et pieds de page. Couverture conservée, sauf son renvoi vers Sécuriser.
- Sommaire et destinations internes mis à jour ; liens externes de sécurité conservés.
- Avant encodage des pages de diffusion, une comparaison des pixels contrôle que les modifications des pages existantes restent dans les zones de repères et de numéros de renvoi indiquées dans `content-preservation.json`.
- Les pages de diffusion utilisent le même encodage JPEG qualité 94 que les pages natives précédentes. Le fichier original approuvé est conservé séparément.

Reconstruction : `python sources/textile-v772/render.py`, puis `python sources/guide/build_site.py` et `node tests/guide-smoke.cjs`.
