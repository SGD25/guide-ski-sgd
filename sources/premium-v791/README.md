# V07.91 — Perspective du livre et bannière de référence

## Rendu

Une enveloppe `.book-object` regroupe les deux pages, les feuilles et la couverture.
Sa projection réduit la largeur au sommet de 4 % tout en conservant la largeur
et la hauteur à la base. Le contenu des fichiers A4 n’est pas redimensionné ni
rééchantillonné : la projection est appliquée par le navigateur. Cette enveloppe
reste indépendante du cadre de mesure non transformé pour éviter les boucles
de mise en page. Les liens suivent naturellement la projection de leur parent.

La couverture inférieure dépasse de 7 px, avec seulement 1,5 à 3 px de papier
visible. Les traits multiples brillants ont été retirés. Les ombres du pli sont
plus progressives ; l’ombre portée sous le livre est plus diffuse. La largeur
visuelle des flèches reste fixe et leur position suit le côté incliné à leur
hauteur réelle, y compris pendant le défilement.

## Bannière

Police variable Inter intégrée localement : titre graisse 900, 42 px en largeur
standard, sous-titre 20 px, avec adaptations aux conteneurs. Le sous-titre est
plus étendu que le titre. La zone anthracite vise 44 % de la bannière lorsque
l’espace le permet et se décale pour protéger le texte sur petit écran.
Un trait vertical sépare les commandes. Le SVG du logo V07.89 est inchangé.

Police : Google Fonts / Inter, `ofl/inter/Inter[opsz,wght].ttf`, récupérée le
25 octobre 2026 puis sous-ensemble latin encodé en WOFF avec fontTools. Les axes
de graisse et de taille optique sont conservés. Aucune requête vers un fournisseur
de polices à l’ouverture du site. Licence : `assets/fonts-v791/OFL.txt`.
Source : https://github.com/google/fonts/tree/main/ofl/inter

## Vérification

- `tests/guide-smoke.cjs` : 46 pages, ordre, chapitres, liens et habillage conservés.
- `tests/reader-chrome.cjs` : six fenêtres, affichages normal/large/page unique,
  défilement, flèches sur la couverture, navigation, sommaire et impression.
- `tests/reader-responsive.cjs` : quatorze autres dimensions, absence de
  chevauchement, de découpe et de va-et-vient aux seuils de redimensionnement.
- `tests/reader-perspective.cjs` : coins effectivement projetés, axe central
  conservé, police chargée, sous-titre plus large, clic sur une page en perspective,
  sommaire incorporé cliquable, clavier, retour au mode plat et 46 images A4
  d’origine à l’impression.

Servir le dépôt sur le port 8765 ; les tests utilisent Playwright et acceptent
`CHROMIUM_EXECUTABLE_PATH`. Contrôle visuel effectué sur les captures du lecteur réel.

## Retour arrière

Parent publié : `9e8c0b4ff91db2130d8b18132cddc153ea4644c6` (V07.90).
Copies de `premium-book.css`, `book-effects.js` et `reader.js` V07.90 dans ce dossier.
Aucune modification des images, du texte ni des couleurs des pages.
