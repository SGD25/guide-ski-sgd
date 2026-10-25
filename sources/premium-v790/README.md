# V07.90 — Livre ouvert, bannière plus affirmée

## Périmètre

- Nouveau logo V07.89 conservé, sans modification du SVG ni de ses dégradés.
- Titre 36 px (jusqu’à 44 px sur grande bannière), graisse 900 ; sous-titre 14 px.
  Tailles adaptées aux bannières compactes ; boutons agrandis et pictogrammes.
- La diagonale anthracite suit la position réelle des commandes, sans couvrir le titre.
- Couverture graphite seulement visible aux côtés et en bas. Feuilles en éventail,
  contours légèrement courbes et ombres générés dans un SVG décoratif.
- Faces inclinées de 0,45° en double page ; aucune inclinaison en page unique ni
  à l’impression. Aucune déformation non linéaire du texte. Proportions A4 conservées.
- Images, texte, couleurs, liens, ordre et nombre des 46 pages inchangés.

## Code

`book-effects.js` est chargé avant `reader.js`. Il crée une seule décoration SVG,
non interactive, masquée aux lecteurs d’écran. Le dessin est recalculé uniquement
quand ses dimensions ou le mode de lecture changent. `premium-book.css` surcharge
l’habillage précédent et reste séparé des styles du contenu.

Le calcul de hauteur réserve la plus grande hauteur de bannière mesurée dans une
même disposition. Cela évite un va-et-vient entre les seuils de taille du logo
quand la largeur du livre dépend elle-même de la hauteur disponible. La réserve
est recalculée lors d’un changement de fenêtre ou de mode.

## Vérification

`node tests/guide-smoke.cjs` : 46 pages, liens du sommaire et overlays conservés.
`tests/reader-chrome.cjs` : six fenêtres, modes normal/large/page unique, défilement,
flèches, feuilletage, sommaire, impression, absence de chevauchement et d’erreur JS.
`tests/reader-responsive.cjs` : quatorze tailles supplémentaires et stabilisation
du redimensionnement, y compris les seuils 735/742/915/920 px de hauteur.

Tests navigateur : servir le dépôt sur le port 8765 et définir
`CHROMIUM_EXECUTABLE_PATH` si Chromium n’est pas fourni par Playwright.

## Retour arrière

Les sources V07.89 utiles sont conservées dans ce dossier. Le commit parent
`0e0c1f20eeb3c025e6ad7f242f3059c11716d8d7` contient toute la version précédente.
Aucune image de page n’a été régénérée.
