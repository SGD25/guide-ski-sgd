# Juniors — pages 15 et 16

Proposition V07.57, 22 octobre 2026. Les quatorze pages approuvées restent inchangées. Les deux nouvelles pages sont des images complètes HD de 2400 × 3394 pixels, avec les titres Palatino, les repères colorés, le logo SGD et les encarts « À retenir » du guide.

## Reconstruire

`python sources/juniors/render.py` actualise uniquement les pages 15 et 16 dans le manifeste commun `sources/freeride-freestyle/manifest.json`. Relier ensuite les 16 pages par `python sources/guide/build_site.py`. Vérification d’intégration : `node tests/guide-smoke.cjs`.

Les fichiers JPG de `media/` sont les originaux téléchargés depuis Rossignol. Les URL exactes sont conservées dans `photos.json`. Le recadrage retire uniquement les marges extérieures ; aucune déformation, recoloration ou reconstruction des skis. Les fixations photographiées illustrent les visuels fabricant : l’équipement réel dépend du pack choisi. Les produits ne sont pas représentés à une échelle de longueur commune.

## Sources et choix pédagogiques

Sources consultées le 22 octobre 2026 :

- ESF, [tests enfants](https://www.esf.net/tests-et-etoiles/ski-alpin-enfants/) : synthèse des acquis du club Piou-Piou, de l’Ourson, du Flocon et des six étoiles. Le dernier niveau obtenu est distingué du cours auquel l’enfant est inscrit.
- ESF, [tests de performance](https://www.esf.net/tests-et-etoiles/ski-alpin-performance/) : Flèche = géant chronométré ; Chamois = slalom chronométré. La Flèche d’argent n’est pas l’Étoile d’argent. Les seuils chronométriques ne sont pas reproduits.
- Rossignol, cinq pages officielles associées aux références exactes dans `products.json`. Les faits techniques sont séparés du positionnement, du vocabulaire et des formulations commerciales rédigés pour SGD. Les cotes et les rayons portent toujours une longueur de référence. Pour Experience Pro RAKJC02, la fiche actuelle étant incomplète sur les cotes, seules les caractéristiques explicitement documentées sont utilisées. Pour les noyaux Hero, le champ technique Microcell prime sur les textes marketing génériques HD Core.
- LOOK, [Kid 4 GW B76](https://www.look-bindings.com/product/kid-4-gw-b76-black) : compatibilité de semelles enfant/adulte alpine et GripWalk, plage de longueur de semelle ; ces compatibilités sont spécifiques à cette référence, pas généralisées aux autres fixations juniors.
- Les formulaires officiels de montage Rossignol demandent poids, âge, taille, longueur de semelle et niveau. Aucun réglage DIN ni barème de poids n’est prescrit dans le guide. La plage de déclenchement et la compatibilité ski–fixation–chaussure doivent être vérifiées, avec réglage et contrôle en atelier.

Les cinq repères de longueur — pitchounes 60–70 cm, débutants taille −25 à −20 cm, débrouillards −15 cm, confirmés −10 cm, experts selon le programme — sont les repères pédagogiques SGD demandés par l’auteur. Ils sont présentés comme indicatifs, distincts des tableaux fabricants, à adapter au poids, à l’aisance, au modèle et au flex. Ce ne sont pas des correspondances automatiques entre médailles ESF et tailles de skis. Le Hero Kid existe en 70, 80 et 92 cm ; sa version 70 cm illustre le premier groupe sans lui inventer une taille 60 cm.

Le Hero Pro Multi-Event sert d’exemple d’initiation aux portes, pas de ski de course pur. Le Hero Athlete GS Pro illustre seulement le programme géant des experts ; un programme slalom ou freeride appelle un autre choix. La page « Sécurité » reste à créer : son renvoi est textuel et sans numéro inventé.

V07.58 : réorganisation de la grille ESF en trois colonnes de haut en bas : Piou-Piou / Ourson / Flocon en bleu ; 1ère / 2e / 3e étoile en vert ; bronze / argent / or en orange. Seule l’image de la page 15 change.

V07.59 : chaque série ESF est réunie dans un seul grand cadre de sa couleur, avec des séparateurs internes. Le reste de la page 15 et les quinze autres pages sont conservés.
