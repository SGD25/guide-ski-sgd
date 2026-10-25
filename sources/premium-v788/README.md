# V07.88 — Bannière et flèches alignées sur le livre

La bannière reprend la largeur réelle des pages + la couverture (38px bureau,
22px mobile). Un ResizeObserver synchronise cette largeur au redimensionnement,
en mode double-page, en mode large et en zoom simple-page. La typographie utilise
des container queries pour s'adapter à la bannière, et non à la fenêtre entière.

Les flèches restent sur les bords de la couverture. Leur position verticale suit
le centre de la partie visible du livre pendant le défilement. Elles disparaissent
lorsque le livre sort complètement de l'écran. Les contrôles d'impression restent
masqués. Aucun changement des pages ou des couleurs.

Vérifications Playwright : 1366×768, 1920×1080, 1024×768, 820×620,
768×1024, 390×844, modes normal/large/zoom, défilement, navigation,
sommaire et 46 pages à l'impression. Tests dans tests/reader-chrome.cjs.
Backups CSS et lecteur de V07.87 conservés ici.
