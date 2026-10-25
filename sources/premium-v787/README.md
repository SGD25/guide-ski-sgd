# V07.87 — livre plus grand et couverture complète

Suppression à l'écran des deux lignes répétées (formation et chapitre),
bannière plus compacte, espace disponible réaffecté aux vraies pages.
La double page tient dans l'écran en mode normal. Le bouton « Élargir le livre »
affiche les deux pages à la largeur disponible, avec défilement vertical.
Le zoom sur une seule page existant reste disponible.

Couverture gris graphite sur les quatre côtés, tranche séparée de la couverture,
ombres de gouttière centrales et coins légèrement arrondis. Aucun réencodage
ou changement du contenu des 46 images, des couleurs ou des liens internes.

Tests : node tests/guide-smoke.cjs ; tests/premium-reader.cjs via Playwright
et serveur local port 8765 (CHROMIUM_EXECUTABLE_PATH si nécessaire).
1366×768, 1920×1080, 1024×768 et mobile 390×844 ; navigation, zoom, sommaire,
mode large et impression. Comparaison visuelle des captures bureau et mobile.

Retour arrière possible avec styles-v786.css et reader-v786.js.
