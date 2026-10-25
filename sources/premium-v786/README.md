# V07.86 — Habillage premium validé

Bannière blanche/anthracite, S original dans les en-têtes des 46 pages,
logo de pied 575px au lieu de 720px et numéro 48px au lieu de 60px.
Les couleurs et les images HD V07.85 sont conservées sans réencodage.
`pages/branding.js` ajoute les deux bandes SVG au chargement, avant reader.js,
pour la lecture, le feuilletage et l'impression. Elles ne capturent aucun clic.
Les liens du sommaire et les boutons de couverture restent inchangés.

Le livre utilise des gradients CSS, une tranche et des ombres. Le texte reste
plat et net. Le mobile et le mode agrandi affichent une page. Le bureau ajuste
la double page à la hauteur disponible. Respect de prefers-reduced-motion.

Validation : smoke test 46 pages et contrôle Chromium réel : navigation,
zoom, sommaire jusqu'à la page 46, 46 pieds à l'impression, mobile 390px sans
débordement et aucune erreur JavaScript.

Retour V07.85 : rétablir styles-v785.css et supprimer l'inclusion
pages/branding.js dans index.html. Les posters originaux sont inchangés.
