# À retenir — V07.69

Refonte graphique des seuls encarts de mémorisation, sur les 26 pages qui en comportent (3–28).

Un seul bandeau bleu ardoise, arrondi et sans ombre, intègre un ruban de marque-page corail, le libellé « À RETENIR », puis le titre et le texte du conseil. L’ancien bouton ampoule et le cadre séparé sont retirés. Couleurs, contenus, logo SPORT GOOD DEAL, autres illustrations et navigation sont conservés.

Base : commit `9a4fcf17a86eb309621678f9defb2ee0dbeb5e22`. Le manifeste d’origine est dans `baseline-v768.json`. Les anciens posters restent présents.

Reproduction : `python sources/finalisation-v769/render.py`, puis `python sources/guide/build_site.py`. Le motif est défini dans `Page.remember`, fichier `sources/guide/render.py`, pour les futures pages également.

Les textes proviennent du rappel approuvé de chaque page. Le rendu contrôle les débordements et l’absence de modification hors du rectangle des encarts. Les liens internes et externes sont copiés à l’identique. Les pages de sécurité restent en PNG pour conserver exactement leurs pixels hors encart. Contrôle d’intégration : `node tests/guide-smoke.cjs`.
