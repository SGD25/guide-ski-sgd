# Finalisation — V07.67

24 octobre 2026. Base : commit `b20afc63809f940719b13da54b15f00f4d5c3e2a`, soit les 28 pages réellement publiées, y compris fixations et avalanche. La référence avant intervention est conservée dans `baseline-v766.json`. Les anciens fichiers restent présents : cette révision peut être annulée par un revert du commit, sans recréer les pages.

## Reproduire

1. `python sources/finalisation/render.py` reconstruit les seules pages concernées et préserve les autres entrées du manifeste.
2. `python sources/guide/build_site.py` relie toutes les pages du catalogue, sans perdre les pages de sécurité ajoutées après les anciens générateurs.
3. `node tests/guide-smoke.cjs` contrôle les scripts réellement chargés, les 28 images, tous les liens du sommaire, l’ordre des doubles pages, le classement des Forza et la préservation des pages / liens de sécurité.

Les titres, descriptions, chapitres et version sont désormais dans `sources/guide/catalog.json`. Le manifeste d’images reste `sources/freeride-freestyle/manifest.json`. Les liens externes existants des pages 25–28 sont conservés dans leurs champs `overlays`. Le lecteur garde une image complète par page. Les nouvelles images sont dans `assets/guide-v767/`.

## Corrections

- Couverture : quatre objectifs Comprendre / Reconnaître / Conseiller / Sécuriser, vrai logo, quatre accès directs.
- Sommaire : les pages 3 à 28 ont chacune un lien ; les intitulés et numéros correspondent à l’ordre final.
- Page 3 : lecture de 118–95–108 mm dans l’ordre spatule / patin / talon, avec les repères de largeur au patin.
- Page 4 : skis strictement verticaux, devant la main du personnage, base commune et repères de hauteur. Les trois vrais patins sont agrandis à la même échelle de 3 px/mm ; le fond extérieur au ski blanc est transparent. Les autres produits conservent leurs vrais pixels et proportions.
- Page 5 : la lecture des cotes passe en page 3. Un nouvel encart explique l’action de la vitesse, de la prise de carre et de la pression sur la trajectoire.
- Page 8 : contours de couleur et boutons des trois familles Freeride / Freestyle / Randonnée, comme les deux familles principales.
- Page 9 : quatre catégories alignées sur les pages de familles validées : comportement, public, points à expliquer, question à poser et phrase client ; patin / longueur / rayon restent visibles.
- Page 10 : catégories Piste facile / Piste polyvalent / Piste performance / Spécialités piste. Le Forza 40 CA Xpress illustre le polyvalent ; le Forza 70 TI Konect passe en performance, avancé à expert. Les deux photos complètes proviennent des références officielles citées, sans inventer de ski ni modifier ses proportions.
- Ordre : chaussures alpines 19, chaussures rando 20 ; snowboard 21–22 ; ski de fond 23–24. Les numéros inscrits dans les images, titres du lecteur et liens du sommaire sont cohérents.
- Les anciens renvois « Sécurité — à venir » des pages juniors, randonnée, chaussures et snowboard sont remplacés par les bons numéros et rendus cliquables. Fixations : pages 25–26 ; avalanche : pages 27–28.
- Les images des pages 6, 7, 11–14, 16, 18, 22 et 25–28 sont conservées sans modification. Les pages 15, 17 et 21 ne changent que pour leur renvoi sécurité. Le ruban du chapitre 03 a sa couleur distincte.

## Vérification du Forza

Sources primaires Rossignol, consultées le 24 octobre 2026 :

- [Forza 70 TI Konect, RAOPR02](https://www.rossignol.com/fr-fr/rossignol-ski-homme-forza-70-ti-konect-RAOPR02000.html) : le texte vise explicitement les skieurs avancés et experts. La catégorie précédente « intermédiaire » était incorrecte. Référence présentée : 77 mm au patin, rayon 14 m en 173 cm, noyau peuplier et couche de titanal. Le terme performance décrit ici le programme, pas le seul prix.
- [Forza 40 CA Xpress, RAPPX05](https://www.rossignol.com/fr-fr/skis-piste-homme-forza-40%C2%B0-ca-xpress-RAPPX05000.html) : carving accessible pour le skieur intermédiaire, noyau peuplier et renfort carbone. Référence présentée : 75 mm au patin, rayon 12 m en 164 cm. « Piste polyvalent » est le classement pédagogique SGD, cohérent avec ce positionnement fabricant.

`photos.json` garde les URL exactes et les rectangles de marges vides recadrées pour les deux photos. Les pixels RGB des photos fabricants ne sont ni générés ni recolorés.

## Détourage du ski blanc

Outil intégré imagegen, mode `background-extraction`. Cible : `sources/guide/media/patin-head-70-v754.png`. Sortie de référence conservée dans `sources/finalisation/references/head-detourage-v767.png` ; seul son canal alpha est utilisé dans `sources/finalisation/media/patin-head-alpha-v767.png`. Le rendu compose ce masque avec les pixels RGB de la photo source originale, pour que l’outil ne puisse pas réinventer des détails du produit. Aucune nouvelle photographie de ski n’est générée pour le guide.

Consigne transmise : « Remove ONLY the pale gray/off-white background OUTSIDE the outer left and right ski edges. Keep the entire ski strip from top edge to bottom edge, the real white topsheet, rails, hardware, graphics, details, proportions and exact straight vertical geometry unchanged. Do not invent or redraw a product. Everything outside the actual ski should have a truly transparent alpha channel, not white. Keep original framing and preserve every product detail. No shadow, no decoration, no extra text, no crop of the ski content. »
