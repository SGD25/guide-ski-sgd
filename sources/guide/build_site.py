"""Build the existing reader with HD posters and accessible navigation links."""
from pathlib import Path
import json, html
ROOT=Path(__file__).resolve().parents[2]
records=json.loads((ROOT/'sources/freeride-freestyle/manifest.json').read_text())
titles=['Couverture','Sommaire','Anatomie du ski','Largeur et longueur du ski','Lignes de cotes et rayon','Cambres et rockers','Au cœur du ski','Les familles de skis','Les skis de piste','Exemples de skis de piste','Les skis all-mountain','Exemples de skis all-mountain','Freeride et freestyle','Exemples freeride et freestyle']
descriptions=[
 'Le guide du ski : comprendre le matériel, reconnaître les familles et conseiller en magasin.',
 'Sommaire : anatomie page 3, dimensions page 4, rayon page 5, profils page 6, construction page 7, familles page 8, piste page 9, exemples piste page 10, all-mountain page 11, exemples all-mountain page 12.',
 'Spatule, patin, talon : rôle de chaque zone, effet de la largeur et repères de familles.',
 'Gros plans de vrais skis au patin à une même échelle : 70, 88 et 102 mm. Largeur et longueur par rapport au skieur.',
 'Rayons R11 vert, R15 bleu et R20+ rouge : petits virages, virages variés et grandes courbes ; lecture des cotes et du rayon.',
 'Cinq profils : cambre classique, rocker en spatule, double rocker, plat et inversé.',
 'Construction du ski : noyau mousse ou bois, fibres, titanal, semelle et carres.',
 'Piste page 9, all-mountain page 11, freeride et freestyle page 13 ; leurs exemples page 14. Randonnée à venir.',
 'Piste facile, polyvalent, performance, slalom et géant : patin, longueur, rayon et public.',
 'Head Easy Joy, Rossignol Forza 70° TI Konect, Hero Elite MT TI C.A.M. et Hero ST : positionnement, arguments, vocabulaire, fiches techniques et discours client.',
 'All-mountain 80/20, 70/30 et 50/50 : patins 80–85, 85–95 et 95–105 mm, comportement et questions client.',
 'Rossignol Experience 82 Basalt, Elan Ripstick 88 et Rossignol Sender Soul 102 : vrais visuels, arguments, vocabulaire et fiches techniques.',
 'Freeride : au-delà de 105 mm pour la poudreuse. Freestyle : environ 85 à 100 mm, twin-tip, flex et profil selon rails ou sauts. Comportement, questions, discours client.',
 'Trois exemples freeride : Elan Ripstick 108, Atomic Bent 110, Rossignol Sender 110. Trois freestyle : Faction Prodigy 1, Armada ARV 88 et LINE Blend. Photos fabricants, positionnement, arguments, vocabulaire et fiches techniques.'
]
total=len(records)
assert total==len(titles)==len(descriptions)
for n in range(1,total+1):
    src=records[n-1]['path']
    markup='<figure class="sgd-poster" data-page="'+str(n)+'"><img src="./'+src+'?v=20261022-55" alt="'+html.escape(descriptions[n-1],quote=True)+'" width="2400" height="3394" loading="eager" decoding="async">'
    for link in records[n-1].get('links',[]):
        x,y,x2,y2=link['box'];style=f'left:{x/24:.5f}%;top:{y/33.94:.5f}%;width:{(x2-x)/24:.5f}%;height:{(y2-y)/33.94:.5f}%'
        markup+='<button type="button" class="poster-link page-jump" data-jump="'+str(link['page']-1)+'" style="'+style+'" aria-label="'+html.escape(link['label']+' — page '+str(link['page']),quote=True)+'"></button>'
    markup+='</figure>'
    record={'title':titles[n-1],'chapter':('Ouverture' if n<3 else '01 · Comprendre' if n<8 else '02 · Les familles'),'html':markup}
    (ROOT/f'pages/{n:02}.js').write_text('window.SGD_PAGES.push('+json.dumps(record,ensure_ascii=False,separators=(',',':'))+');\n')
scripts='<script src="./pages/00-init.js?v=20261022-55"></script>\n'+'\n'.join(f'<script src="./pages/{n:02}.js?v=20261022-55"></script>' for n in range(1,total+1))
template='''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#193B4B"><meta name="description" content="Le guide de formation ski SPORT GOOD DEAL : comprendre le matériel et conseiller les clients."><title>Le guide du ski — SPORT GOOD DEAL</title><link rel="stylesheet" href="./styles.css?v=20261022-55"></head>
<body><header class="appbar"><a class="brand" href="#page=1"><img class="brand-logo" src="./sources/guide/media/sgd-logo.png" alt="Sport Good Deal" width="96" height="57"><span class="brand-name">SPORT GOOD DEAL<small>LE GUIDE DU SKI</small></span></a><div class="appbar-actions"><span class="label-version">CATALOGUE / V07.55</span><button id="reading-button" class="bar-button" type="button" aria-pressed="false">Agrandir</button><button id="toc-button" class="bar-button" type="button" aria-expanded="false" aria-controls="toc-overlay">Sommaire</button><button id="print-button" class="bar-button" type="button">Imprimer</button></div></header>
<div class="page-edge-controls" aria-label="Feuilleter le guide"><button id="previous" type="button" aria-label="Page précédente" class="edge-arrow edge-previous">‹</button><button id="next" type="button" aria-label="Page suivante" class="edge-arrow edge-next">›</button></div>
<main class="workstage"><div class="reader-meta"><span>FORMATION VENDEURS & LOUEURS</span><span>COMPRENDRE · RECONNAÎTRE · CONSEILLER</span></div><div id="chapter-band" class="chapter-band" aria-live="polite"></div><div class="book-frame"><div id="book" class="book"><section id="left-page" class="sheet sheet-left" aria-label="Page de gauche"></section><section id="right-page" class="sheet sheet-right" aria-label="Page de droite"></section><div id="flip-sheet" class="flip-sheet" aria-hidden="true"></div></div></div><nav class="controls" aria-label="Position dans le guide"><span id="page-count" class="page-count" aria-live="polite">01–02 / 14</span><span class="shortcut-note">Flèches ← → pour feuilleter · Cliquez sur une page pour l’agrandir</span></nav><div class="progress-track"><div id="progress"></div></div><footer class="reader-footer"><span>SPORT GOOD DEAL · GUIDE DU SKI</span><span>Formation en magasin</span></footer></main>
<div class="overlay" id="toc-overlay" role="dialog" aria-modal="true" aria-label="Sommaire du guide"><div class="overlay-dialog"><div class="overlay-head"><div><span class="eyebrow">ACCÈS DIRECT AUX PAGES</span><h2>Sommaire</h2></div><button id="toc-close" class="close-modal" type="button" aria-label="Fermer le sommaire">×</button></div><div id="toc-grid" class="toc-grid"></div></div></div><div id="print-pages" class="print-pages"></div>
SCRIPTS
<script src="./reader.js?v=20261022-55"></script></body></html>
'''
(ROOT/'index.html').write_text(template.replace('SCRIPTS',scripts))
palette=ROOT/'design/charte-candidate-sgd.json';style=json.loads(palette.read_text());style['statut']='validée le 21 octobre 2026';style['reference']='Bleu ardoise, turquoise et accents corail, bleu glacier et prune ; titres Palatino et textes agrandis.'
palette.write_text(json.dumps(style,ensure_ascii=False,indent=2)+'\n')
print('Lecteur V07.55, 14 pages et sommaires reliés.')
