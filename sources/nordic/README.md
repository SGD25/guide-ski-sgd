# Ski de fond — pages 19 et 20

V07.61, 22 octobre 2026. Deux images complètes en 2400 × 3394 pixels, dans la charte approuvée du guide. Les dix-huit pages précédentes sont conservées.

## Reconstruire

`python sources/nordic/render.py` actualise les pages 19–20 et leur manifeste commun `sources/freeride-freestyle/manifest.json`. Puis `python sources/guide/build_site.py` relie les vingt pages. `node tests/guide-smoke.cjs` vérifie l’ordre des scripts, l’unique image de chaque page, les ressources et la navigation. Les générateurs randonnée et juniors conservent les pages suivantes.

## Contenu et limites des repères

Page 19 : classique en premier (écailles, peaux, courte mention du fart de retenue non proposé par SGD), puis skating. Le tableau compare les longueurs de skis, les bâtons et les chaussures. Le poids et le niveau servent à choisir la longueur et le flex de la paire selon le barème fabricant, plutôt qu’à appliquer aveuglément une addition à la taille.

Les repères adultes de loisir retenus sont classique +15 à +20 cm, skating +5 à +10 cm ; ce ne sont pas des règles universelles ni des tableaux de poids propres aux quatre références. Les gammes compactes peuvent être plus courtes, dont l’Aeroguide. Pour les bâtons : environ taille en cm ×0,83 en classique et ×0,90 en skating, avec exemples arrondis aux longueurs usuelles pour 1,70 m. Les conventions de mesure, le modèle et la technique peuvent conduire à ajuster la longueur. Ce document ne prescrit pas de limites réglementaires de compétition.

L’encart normes reste volontairement bref : NNN piste / Prolink / TURNAMIC partagent une interface chaussure compatible ; SNS, Profil et Pilot sont des noms d’anciens systèmes à reconnaître, incompatibles avec le NNN vendu chez SGD. Aucune généralisation sur toutes les compatibilités croisées entre anciens produits SNS n’est faite. NNN BC et les variantes hors pistes ne sont pas assimilées au NNN piste. Compatibilité de chaussure et compatibilité de plaque de montage sont distinctes : les exemples IFP requièrent une fixation appropriée à la plaque et à la pratique.

Page 20 : deux grands encarts, classique (Fischer Fibre Crown EF à écailles, Rossignol Delta Sport R-Skin à peaux) puis skating (Fischer Aeroguide Skate 65, Rossignol Delta Sport Skating). Chaque fiche présente positionnement, arguments fabricant, vocabulaire utile, données techniques et phrase de conseil. Le positionnement et les formulations commerciales sont une synthèse SGD, pas des citations. Aucun stock ni prix magasin n’est inventé.

## Sources primaires

Consultées le 22 octobre 2026 :

- [Fischer — longueur des skis](https://www.fischersports.com/blog/what-ski-length-do-i-need-for-cross-country-skis-touring-skis-etc.) : classique traditionnel autour de +20 cm, skating +5 à +10 cm, cruising plus court et prise en compte du poids. Les autres conseils du billet portant sur le ski alpin ne sont pas repris.
- [Salomon — choisir ses skis classiques](https://www.salomon.com/en-nl/sg/a/how-to-choose-classic-cross-country-skis) : trois systèmes d’accroche, +15 à +20 cm à titre de départ, priorité aux recommandations fabricant et au poids, rôle du cambre/flex et adaptation au niveau. Le fart de retenue est distingué de l’entretien de glisse.
- [Fischer — gamme Active](https://www.fischersports.com/fr_fr/active) : Crown / Twin Skin sans fart de retenue, variantes courtes Cruising, Easy/Efficient Forward et Aeroguide pour l’apprentissage. Les photographies officielles de cette page illustrent les deux pratiques.
- [Rossignol — bâtons nordiques](https://www.rossignol.com/pt-en/sports/nordic/poles) : repères ×0,83 pour le classique et ×0,90 pour le skating, présentés comme des recommandations de choix et non comme des règles de compétition.
- [Salomon — chaussures nordiques](https://www.salomon.com/en-us/sg/a/nordic-ski-boots-how-to-choose-the-right-cross-country-pair) : flex d’avant-pied en classique, semelle plus rigide et soutien du collier en skating, maintien et compatibilité. Les chaussures combi restent un compromis, non développé ici conformément au périmètre demandé.
- [Salomon — compatibilité fixations](https://www.salomon.com/en-nl/sg/a/do-all-cross-country-ski-boots-fit-all-cross-country-bindings) : NNN / Prolink / TURNAMIC compatibles en nordique sur pistes, anciens SNS non compatibles avec cette famille. Les fixations restent adaptées au classique ou au skating.
- [Fischer Fibre Crown EF NV43024](https://www.fischersports.com/fibre-crown-ef-mtd/NV43024) : longueurs 179/184/189/194/199/204, cotes 51–46–49 mm, Vario Crown, Efficient Forward, Air Channel Basalite, IFP et set Nordic Tour Step-In TURNAMIC.
- [Rossignol Delta Sport R-Skin RHOCW02](https://www.rossignol.com/fr-fr/delta-sport-r-skin-RHOCW02000189.html) : longueurs 184/189/196/201/206, peau remplaçable, noyau nid d’abeille / peuplier, Activ Cap et plaque IFP. La composition précise de la peau n’est pas reproduite : le texte marketing et un champ technique générique divergent. Aucune cote absente de la page actuelle n’est inventée.
- [Fischer Aeroguide Skate 65 NP27425](https://www.fischersports.com/fr_fr/aeroguide-skate-65-set/NP27425) : 165/175/185, cotes 45–40–45 mm, longueurs compactes, deux rainures, Air Core Basalite, World Cup Pro, set Control Skate Step-In TURNAMIC et plaque IFP.
- [Rossignol Delta Sport Skating RHOCQ03](https://www.rossignol.com/fr-fr/delta-sport-skating-RHOCQ03000180.html) : 163/173/180/186/192, cotes 44–43–43 mm, noyau nid d’abeille / peuplier, Activ Cap, double rainure et plaque IFP.

## Images

`photos.json` conserve les URL exactes des six images originales Fischer / Rossignol. Les photos de produits sont les vrais modèles, sans génération ni recoloration. Seules les marges vides sont recadrées et les images redimensionnées en conservant leurs proportions. Les images ne constituent pas une comparaison à échelle de longueur commune. Les photographies de pratique sont recadrées pour leur emplacement de page.
