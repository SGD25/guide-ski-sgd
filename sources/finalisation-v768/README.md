# Ajustements — V07.68

24 octobre 2026. Base : `815b91bf38c1e6acff36c6d901e95d51426cb0ae`. Le manifeste avant intervention est conservé dans `baseline-v767.json` et les anciens posters restent présents. Visibilité inchangée.

## Corrections

- Page 3 : portance du patin large en neige souple, effort supplémentaire de bascule sur piste en neige damée ; exemple pédagogique **118–88–108 mm** pour retrouver le repère 88 mm du ski illustré. Il s’agit d’un exemple de lecture, pas d’une fiche constructeur de l’Elan.
- Page 4 : skis toujours verticaux, mêmes proportions et bases alignées. Axe déplacé de 457 à 410 px dans chaque colonne, devant l’avant-bras. Les vrais gros plans de patins et leurs détourages sont conservés.
- Page 5 : **radius**, autre terme pour le rayon ; chercher R / radius près des lignes de cotes, au talon ou au patin. La valeur dépend de la longueur du ski. Tracés verts et rouges conservés.
- Page 9 : nouveau slalomeur avec corps, skis et piquet proche entièrement cadrés.
- Page 11 : trois nouvelles scènes illustratives : bord de piste damée, neige non damée entre deux pistes reconnaissables, puis hors-piste. Rubriques approuvées conservées.
- Page 15 : les neuf véritables insignes ESF à droite de chaque grade, dans les trois colonnes approuvées.
- Page 17 : vraies petites photos d’une peau POMOCA, de la butée et talonnière Dynafit, et du mécanisme SCARPA ; plume vectorielle discrète près du gain de poids. La peau photographiée est un mix 65/35, distinct du repère SGD **70/30**. Budgets et parcours vendeur conservés.
- Page 19 : grand bloc volume avant le flex, localisation des métatarses, trois cartes **LV ≈ 98 / MV ≈ 100 / HV ≈ 102 mm et +**. Valeurs indicatives à pointure de référence ; vérifier modèle et tableau fabricant. Contrôler aussi cou-de-pied et talon. Message principal : **pied large ≠ pied long : changer de volume sans surtailler**. Longueur Mondopoint, essayage, conséquences d’une mauvaise taille et compatibilités restent présents.
- Rappels de toutes les pages 3–28 : fond bleu ardoise, texte blanc, contour corail, bouton ampoule conservé. Couverture et sommaire 1–2 inchangés. Les pages de sécurité gardent exactement leurs pixels originaux hors du panneau de texte, et leurs liens externes.

## Sources primaires

Consultées le 24 octobre 2026 :

- [ESF — Ski alpin enfants](https://www.esf.net/tests-et-etoiles/ski-alpin-enfants) : neuf vrais insignes. URL exactes dans `photos.json`, copies `media/esf-1.png` à `esf-9.png`, proportions conservées.
- [Rossignol — chaussures de piste](https://www.rossignol.com/us-en/sports/alpine-ski/ski-boots/on-piste) : chaussants 98, 100 et 102 mm ; gamme Speed de 104 mm.
- [Rossignol — Hi-Speed LV](https://www.rossignol.com/ro-en/super-hi-speed-lv-skiboot-RBO2590000.html) : Low Volume, 98 mm. Les lettres ne sont pas des normes ou des niveaux ; l’essayage reste déterminant.
- [Dynafit — Speed Turn](https://www.dynafit.com/fr-fr/fixation-speed-turn-08-0000048950) : vraie photo de la fixation à inserts.
- [POMOCA — Tour Explore](https://www.pomoca.com/fr/peaux/330-tour-explore) : vraie peau mixte 65/35. Rectangle `(290,170,790,700)` isolant le rouleau dans la photo d’ensemble ; aucun détail produit retouché.
- SCARPA : photo Maestrale déjà sourcée dans `sources/boots/`.

## Images générées

Outil intégré **image_gen.imagegen**, mode `photorealistic-natural` ; prompts complets dans `image-prompts.json`. Fichiers utilisés : `sources/guide/media/allmountain-8020-v768.jpg`, `allmountain-7030-v768.jpg`, `allmountain-5050-v768.jpg`, `slalom-specialiste-v768.jpg`. Ces scènes illustrent le terrain et le programme. Les photos des produits et insignes ESF restent des visuels véritables, sans génération.

## Reproduire

1. `python sources/finalisation-v768/render.py`
2. `python sources/guide/build_site.py`
3. `node tests/guide-smoke.cjs`

Contrôles : débordements des textes ; pixels hors des rappels préservés sur les pages approuvées avant encodage, et strictement identiques après sauvegarde PNG pour la sécurité ; 28 images, initialisation du lecteur, sommaire complet, ordre des doubles pages, tous les liens internes / externes et classement des Forza. Rendu inspecté sur les pages corrigées. Une image complète par page, loupe et vue double conservées.
