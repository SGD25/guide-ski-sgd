# Freeride et freestyle — pages 13 et 14

`python sources/freeride-freestyle/render.py` produit les images HD de 2400 × 3394 pixels et actualise les accès à ces familles sur la page 8. `approved-pages-v754.json` archive les références aux douze pages validées. Le générateur conserve maintenant les pages 1–12 du manifeste publié et reconstruit seulement les pages 13–14. `manifest.json` est le manifeste durable lu par `sources/guide/build_site.py`.

La page 13 reprend la logique de la page all-mountain : terrain, largeur au patin, longueur indicative, comportement, public, points à expliquer, question à poser, discours client et mémorisation. Les largeurs sont des repères de programme et les longueurs dépendent aussi du niveau, du gabarit, du modèle et du rocker. Un cambre plat n’est pas une obligation du freestyle ; le profil se choisit avec le flex et la pratique (rails, butters ou sauts).

La page 14 présente trois freeride (Elan Ripstick 108, Atomic Bent 110, Rossignol Sender 110) et trois freestyle (Rossignol Sprayer Pro, Armada ARV 88, LINE Blend). Les positionnements, le vocabulaire et les phrases client sont des synthèses pédagogiques, et non des citations ou des classements. Les références techniques se rapportent aux longueurs indiquées, pas à toute la gamme.

## Sources vérifiées le 22 octobre 2026

Les URLs des six fiches officielles, références et caractéristiques se trouvent dans `products.json`. Les photos fabricants originales sont dans `media/` et leurs URLs dans `photos.json`. Seules les marges vides sont recadrées lors de la mise en page ; chaque photo est contenue dans sa zone en conservant son rapport largeur/hauteur. Les pixels et graphismes des produits ne sont ni générés ni retouchés.

- Elan Ripstick 108, réf. ADAMMX26 : 143–108–124 mm et 19,8 m en 182 cm ; Tubelite / Carbon Deck / lin / Amphibio.
- Atomic Bent 110, réf. AA0030958 : 133–110–124 mm et 18 m en 180 cm ; HRZN Tech, Light Woodcore et Powder Rocker.
- Rossignol Sender 110, réf. RAPMB01, FW26/27 : 140–110–133 mm et 20 m en 184 cm ; Titanal, VAS, Air Tip et Twin Rocker.
- Rossignol Sprayer Pro, version 2027 : 88 mm et 16 m en 171 cm ; flex fabricant 7/10, peuplier/frêne, renfort carbone/caoutchouc.
- Armada ARV 88, réf. RA0000764 : 120–88–114 mm et 16,5 m en 176 cm ; AR Freestyle Rocker, peuplier et insert frêne.
- LINE Blend, réf. LN261774, version 2027 : 129–98–120 mm et 18,5 m en 175 cm ; flex souple/symétrique, cambre sous le pied et extrémités relevées. Cette génération est à 98 mm, contrairement aux anciens Blend à 100 mm.

## Scènes illustratives de la page 13

Créées avec l’outil ImageGen intégré, puis enregistrées dans `media/freeride-scene.jpg` et `media/freestyle-scene.jpg`. Ces images illustrent les pratiques et ne représentent aucun modèle produit cité. Les consignes sont conservées dans `illustrations.json`. Les six photos produits de la page 14 proviennent uniquement des fabricants.

## V07.56 — compléments demandés

En freestyle, les trois valeurs sont des repères de conseil exprimés par rapport à la taille du skieur : environ −10 cm pour le jib / rails, −5 cm pour le freestyle polyvalent et à la taille pour le big air / half-pipe. La page explique l’inertie, le pivot, la stabilité sur piste / neige plus profonde et l’appui à la réception avec l’équilibre avant / arrière. Ajuster ensuite au gabarit, au niveau, au flex et au modèle.

La nouvelle scène `media/freeride-deep-v756.jpg` montre une tenue ample de freeride et une neige plus profonde. Elle a été créée avec ImageGen intégré ; la consigne exacte est dans `illustrations.json`. La photographie du Sprayer Pro reste une vraie photo fabricant, recadrée uniquement pour enlever les marges et placée sans déformation. Les sources remplacées restent dans l’historique.
