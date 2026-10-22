# Randonnée — pages 17 et 18

V07.60, 22 octobre 2026. Deux pages complètes HD en 2400 × 3394 pixels. La charte, les encarts « À retenir » et la vraie signature SGD sont repris. La page 8 reçoit seulement l’accès « Découvrir / page 17 » à la place de « À venir ». Les autres images approuvées sont conservées.

## Reconstruire

`python sources/rando/render.py` produit les pages 17 et 18 dans `assets/guide-v760/` et actualise les deux dernières entrées du manifeste commun `sources/freeride-freestyle/manifest.json`. `python sources/guide/build_site.py` reconstruit le lecteur et son sommaire de 18 pages. `node tests/guide-smoke.cjs` vérifie les scripts, les images et les cibles de navigation.

## Choix de contenu

La page 17 présente la pratique, le talon libre, les inserts et les transitions, puis le compromis légèreté/amorti. L’encart peaux compare les trois matières. Le parcours vendeur commence par location ou vente, redirige la location vers le parc, puis interroge l’état du matériel, le budget, le programme et les éléments déjà possédés. Les montants sont fournis par SGD : environ 2 000 € le pack complet neuf au prix courant, 1 000 € en fin de série et 600–700 € en occasion. Le pack comprend skis, fixations, peaux et chaussures, hors bâtons et matériel de sécurité. Ce sont des ordres de grandeur, pas des offres ni des stocks garantis.

Le ratio de temps 95 % montée / 5 % descente est un repère pédagogique fourni par SGD, explicitement schématique et variable selon la sortie ; il n’est pas présenté comme une moyenne statistique universelle.

Correction technique du brief sur les peaux : le synthétique offre généralement une bonne accroche et une grande résistance, avec moins de glisse ; le mohair privilégie la glisse et s’use plus vite, son accroche dépendant de la neige et de la technique. Le mix 70 % mohair / 30 % synthétique est le choix courant indiqué par SGD. Les mélanges varient selon les fabricants : tous les produits mixtes ne sont pas automatiquement en 70/30.

La page 18 regroupe deux orientations schématiques — montée et freerando — puis trois exemples réels, dont deux Rossignol. La largeur ne suffit pas à déterminer le poids ou l’amorti : la construction, la longueur, la fixation et la chaussure restent déterminantes. Les descriptions de programme et les formulations clients sont une synthèse de conseil SGD ; les caractéristiques proviennent des fabricants.

## Sources primaires

Consultées le 22 octobre 2026 :

- [Colltex — matières des peaux](https://www.colltex.ch/en/materials) : glisse, accroche et résistance du mohair, du synthétique et des mélanges. Confirme notamment l’accroche du synthétique et l’usure plus rapide du mohair.
- [Rossignol — composition des peaux](https://www.rossignol.com/hu-en/skins.html) : référence de mélange 70 % mohair / 30 % nylon. Le texte a été consulté via le HTML fabricant ; certains accès par moteur de recherche rencontrent une boucle de redirection géographique.
- [POMOCA Tour Pro](https://www.pomoca.com/skins/331-tour-pro) : un autre exemple de mélange (65/35), illustrant que le ratio n’est pas universel.
- [ATK — technologies](https://atkbindings.com/en/pages/technology) et [notice DYNAFIT ST Rotation](https://cdn1.dynafit.com/media/pdf/47/05/ea/96-0000800032_8196_Ind-03_How_to_use_ST_Rotation_ANSICHT.pdf) : inserts, talonnières et modes montée/descente. Les consignes propres à chaque fixation ne sont pas généralisées en une procédure universelle ; le guide renvoie à la notice et à l’atelier.
- [FFME — fiches ski-alpinisme](https://www.ffme.fr/ski-alpinisme/fiches-ski-alpinisme/) et [formation randonnée ANENA](https://anena.org/formation/session-ski-de-rando-gestion-du-risque-davalanche-niveau-1-1-jour/) : DVA, pelle, sonde, préparation et formation au risque d’avalanche. Le futur chapitre Sécurité n’a pas encore de numéro : aucun lien ou numéro fictif n’est ajouté.
- [Rossignol Escaper 88 Nano RANQV01](https://www.rossignol.com/us-en/rossignol-escaper-88-nano-skis-RANQV01000.html) : tailles 156/166/176/182, cotes 120–88–110, rayon 18 m en 176, noyau paulownia, Nano Fiberglass et Nano Titanal selon les champs techniques. La description marketing générique mentionne encore du carbone et un noyau cellulaire : les champs techniques spécifiques ont été privilégiés.
- [Rossignol Escaper 97 Nano RANTA01](https://www.rossignol.com/fi-en/mens-touring-skis-escaper-97-nano-open-RANTA01000.html) : tailles 161/169/177/185, cotes 126–97–116, rayon 19 m en 177, paulownia, double rocker, Nano Fiberglass et Nano Titanal. La version Portugal de la page a disparu, le contenu officiel finlandais reste indexé. Le vrai visuel original demeure accessible sur le serveur Rossignol.
- [Elan Ripstick Tour 104 ADGKWB24](https://elansports.com/products/ripstick-tour-104) : tailles 166/173/180/187, cotes 129–104–122, rayon 23 m en 180, Carbon Bridge, noyau bois, carbone, fibre de verre et chants 360°. [Catalogue fabricant](https://salestools.elansports.com/2025-26/en/ripstick-tour-en.html) pour le positionnement et la photo de montée.

Les poids individuels ne sont pas reproduits dans les fiches : les libellés Rossignol « kg/pair » et « 1/2 pair » se contredisent entre versions, et les publications Elan divergent légèrement selon les éditions. Le guide demande de comparer l’ensemble ski + fixation à longueur comparable, plutôt que de publier des valeurs ambiguës.

## Images

`photos.json` conserve les URL exactes des trois visuels produits et de la scène de montée Elan. Ce sont les images originales des fabricants, non générées. Pour les skis : recadrage des marges vides et redimensionnement proportionnel uniquement, aucun allongement, écrasement, recoloriage ou détourage synthétique. Les photos ne constituent pas une comparaison à échelle physique commune. La scène de montée est recadrée pour le bandeau de la page 17.
