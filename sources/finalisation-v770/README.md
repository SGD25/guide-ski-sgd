# Option choisie : l’onglet — V07.70

La proposition visuelle n° 1 « L’onglet » a été choisie dans la conversation. Son image de référence est conservée dans `onglet-valide.png`. Le bouton corail avec ampoule et libellé est repris de cette image dans `sources/guide/media/a-retenir-onglet-v770.png`, avec ses proportions préservées, et posé à cheval sur le bord supérieur d’un cadre blanc fin bleu ardoise. Titres et conseils sont composés en texte natif, dans les polices du guide, pour garantir leur netteté et leur exactitude.

Le dessin est appliqué aux seuls rappels des pages 3–28. La couverture, le sommaire, les autres contenus, photos, logos et liens restent conservés. Les quatre pages de sécurité gardent une variante compacte du même onglet adaptée à leur espace disponible. Les textes sont ceux de la version précédente.

Base : `4944aede30287ed9b4e5f3f17f313b95a31625d3`. Le manifeste initial est conservé dans `baseline-v769.json`, et les anciens posters restent présents pour un retour arrière.

Reproduire : `python sources/finalisation-v770/render.py`, puis `python sources/guide/build_site.py`. Contrôle : `node tests/guide-smoke.cjs`. Le rendu vérifie les débordements et la conservation des pixels hors des rappels avant encodage. Les pages de sécurité restent en PNG ; leurs liens externes sont copiés à l’identique.
