# V07.95 — Orange vermillon validé

Le corail terre cuite devient `#F04D2E`, suivant l’aperçu approuvé. Les titres,
repères et onglets « À retenir » reprennent cet accent ; les autres familles
de couleurs restent en place. Les pages 27–32 et 41–42, déjà illustrées avec
un orange vif, conservent leurs couleurs.

## Conservation du contenu

Les 46 images HD `assets/guide-v785/` ne sont pas modifiées. `build.cjs` crée
des surimpressions WebP transparentes sans perte, limitées aux composants de
l’ancienne palette. Les rectangles des photos sont exclus et contrôlés après
décodage. Les petits groupes de pixels isolés sont ignorés. Les proportions,
les textes et les liens du guide restent identiques.

`pages/palette.js` pose les surimpressions derrière les en-têtes et pieds de
page, sans intercepter les clics. Le même habillage est présent en lecture,
pendant le feuilletage et à l’impression. `audit.json` donne le détail par page.

## Reconstruction et vérification

Exécuter `node sources/palette-v795/build.cjs` avec Sharp disponible.
Contrôles : masques transparents dans toutes les zones photographiques
protégées, inspection des doubles pages 3–4, 21–22, 35–36, 43–44 et 45–46 ;
tests du guide, de la perspective, du zoom et de la remontée au changement de page.

Le pied « ÉDITION 2026–2027 » et le filet de chapitre abaissé de la V07.94
sont conservés. Le chapitre 02 adopte le nouvel orange dans son en-tête.
