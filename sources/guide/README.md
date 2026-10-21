# Pages harmonisées du guide

`python sources/guide/render.py` reconstruit les pages 1 à 11 en images complètes de 2400 × 3394 pixels. La page 12 conserve son image validée et sa source `sources/page12/render.py`.

La palette et les deux familles typographiques sont communes : `design/charte-candidate-sgd.json`, Nimbus Roman pour les titres et Nimbus Sans pour les textes. Les photos et illustrations de `media/` sont reprises des pages publiées ; elles sont placées à leurs proportions d’origine. Les schémas simples sont tracés directement et les textes restent modifiables dans le script.

Les sorties sont dans `assets/guide-v750/`. Les anciens visuels sont conservés. Les liens de sommaire se superposent aux images complètes dans le lecteur ; le texte des liens est accessible au clavier et aux lecteurs d’écran.

Après génération des images, `python sources/guide/build_site.py` reconstruit `pages/NN.js` et `index.html`. Le lecteur utilise `reader.js` et `styles.css`. Le bouton Agrandir passe de la double page à une page unique ; sur mobile, la page unique est automatique.
