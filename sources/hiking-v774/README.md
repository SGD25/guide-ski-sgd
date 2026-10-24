# Randonnée pédestre — V07.74

Pages 27 et 28 validées dans le chat puis autorisées à la publication le 24 octobre 2026. Images copiées octet pour octet, sans recomposition. La dernière correction de la page 27 porte sur les phrases de membrane et de conseil client.

Contenu : construction, matériaux de tige (pleine fleur, nubuck, croûte, mesh), semelles, EVA/PU, cambrion, crampons, Vibram/Megagrip et membranes. Choix selon terrain, charge, durée et chaussant ; hauteur de tige distincte de la rigidité ; flexion/torsion, essayage en cinq étapes et entretien. Les classes de rigidité proposées sont des repères de conseil, sans certification universelle.

Références techniques consultées :
- https://perwangerleather.com/en/typical-types-of-leather-for-outdoor-and-mountain-boots/
- https://www.vibram.com/fr/TECH_megagrip.html
- https://www.gore-tex.com/technologies/footwear
- https://www.hanwag.com/us/en-us/our-story/materials/soles/sole-overview/
- https://us.lowa.com/blogs/news/how-to-choose-the-right-hiking-shoes-boots
- https://support.hanwag.com/hc/en-gb/articles/360016299439-Size-chart
- https://www.salewa.com/expertise/how-to-choose-hiking-shoes
- https://www.meindl.ch/wsshop/Sportco/img/Meindl-B2C/Dateien/Anwendungsgebiete.pdf

Exécution : `python sources/hiking-v774/apply.py`, `python sources/guide/build_site.py`, `node tests/guide-smoke.cjs`. Les écritures image sont atomiques. Le script contrôle les pixels des pages existantes hors régions de pagination, conserve les liens externes et vérifie le décodage des 32 images avant publication.
