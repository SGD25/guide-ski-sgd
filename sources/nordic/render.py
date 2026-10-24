"""Nordic spread: 19 explains classic/skating, 20 shows four real product examples.

Manufacturer photos are cropped only at empty margins and scaled proportionally.
The reader continues to display one complete HD image per guide page.
"""
from pathlib import Path
import json, sys
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
sys.path.insert(0, str(ROOT / 'sources/guide'))
import render as common
from render import Page, INK, BODY, TEAL, CORAL, BLUE, WHITE, LINE, DARK

common.OUT = ROOT / 'assets/guide-v767'
common.OUT.mkdir(exist_ok=True)
MANIFEST = ROOT / 'sources/freeride-freestyle/manifest.json'
PRODUCTS = json.loads((HERE / 'products.json').read_text())


def photo(p, name, box, center=(.5, .5)):
    im = Image.open(HERE / 'media' / name).convert('RGB')
    im = ImageOps.fit(im, (box[2]-box[0], box[3]-box[1]), Image.Resampling.LANCZOS, centering=center)
    p.im.paste(im, box[:2])


def intro_page():
    p = Page(23)
    p.header('Les skis de fond.', 'La première question : « Vous skiez dans les rails ou en pas de patineur ? »', '02  /  LES FAMILLES')
    p.accent, p.soft = BLUE, '#ECF3F9'
    p.rect((70, 440, 2330, 1200), WHITE, BLUE, 24, 3)
    p.number(100, 472, 1)
    p.text(200, 478, 'Le classique', 64, 'serif', INK)
    p.text(950, 483, 'AVANCER DANS LES RAILS', 31, 'bold', BLUE)
    photo(p, 'classique-fischer.jpg', (95, 565, 885, 1170), (.44, .50))
    p.rect((110, 1080, 870, 1155), DARK, None, 15)
    p.text(133, 1100, 'Skis parallèles, poussée vers l’avant.', 31, 'bold', WHITE, width=710)
    p.text(950, 575, 'Dans les rails, on avance avec des skis parallèles et une poussée vers l’avant. Une zone anti-recul sous le pied prend appui sur la neige pendant la poussée.', 37, width=1320, leading=45, bottom=730)
    grips = [
        ('Écailles', 'Reliefs moulés dans la semelle, sous le pied. Un anti-recul simple, robuste et peu exigeant en entretien.', BLUE),
        ('Peaux', 'Courtes bandes intégrées sous le pied, conservées pendant toute la sortie. Elles combinent accroche et glisse.', TEAL),
        ('À fart de retenue', 'Un fart d’accroche à choisir selon la neige. À connaître, mais ce n’est pas l’offre proposée chez SGD.', CORAL)
    ]
    for i, (title, body, color) in enumerate(grips):
        y = 750+i*142
        p.d.ellipse((950, y+10, 961, y+21), fill=color)
        p.text(980, y, title, 38, 'bold', color)
        p.text(980, y+55, body, 35, width=1290, leading=40, bottom=y+136)

    p.accent, p.soft = TEAL, '#EDF5F6'
    p.rect((70, 1240, 2330, 1670), WHITE, TEAL, 24, 3)
    p.number(100, 1265, 2)
    p.text(200, 1272, 'Le skating', 64, 'serif', INK)
    photo(p, 'skating-fischer.jpg', (1510, 1260, 2305, 1650), (.70, .50))
    p.text(102, 1360, 'Le pas de patineur : les skis poussent en V sur une piste damée large. L’impulsion vient des appuis latéraux et des bâtons. Semelle de glisse sur toute la longueur ; talon libre, comme en classique.', 37, width=1350, leading=45, bottom=1547)
    p.rect((95, 1570, 1470, 1640), '#EDF5F6', None, 14)
    p.text(118, 1589, 'Ni écailles ni peaux : la poussée vient de la prise de carre.', 31, 'bold', TEAL, width=1320)

    # Comparative rows keep ski, pole and footwear choices aligned by technique.
    p.rect((70, 1710, 2330, 1780), DARK, None, 14)
    p.text(96, 1730, 'REPÈRES ADULTES', 28, 'bold', WHITE)
    p.text(490, 1726, 'CLASSIQUE', 37, 'bold', WHITE)
    p.text(1430, 1726, 'SKATING', 37, 'bold', WHITE)
    for y, end in [(1795, 1950), (1965, 2140), (2155, 2405)]:
        p.rect((70, y, 2330, end), WHITE, LINE, 16, 2)
        p.line((450, y+15, 450, end-15), LINE, 3)
        p.line((1385, y+15, 1385, end-15), LINE, 3)
    p.text(98, 1825, 'Skis', 43, 'serif', INK)
    p.text(490, 1816, '≈ taille +15 à +20 cm', 42, 'bold', BLUE, width=855)
    p.text(490, 1880, 'Repère pour un modèle traditionnel.', 33, width=850)
    p.text(1430, 1816, '≈ taille +5 à +10 cm', 42, 'bold', TEAL, width=850)
    p.text(1430, 1880, 'Les modèles compacts font exception.', 33, width=850)
    p.text(98, 1993, 'Bâtons', 43, 'serif', INK)
    p.text(490, 1980, 'Taille en cm × 0,83', 40, 'bold', BLUE, width=855)
    p.text(490, 2034, 'Ex. : 1,70 m → environ 140 cm.', 33, width=855)
    p.text(490, 2084, 'Repère habituel : à l’aisselle.', 33, 'bold', BLUE, width=855)
    p.text(1430, 1980, 'Taille en cm × 0,90', 40, 'bold', TEAL, width=850)
    p.text(1430, 2034, 'Ex. : 1,70 m → environ 150–155 cm.', 33, width=855)
    p.text(1430, 2084, 'Repère : entre le menton et le nez.', 33, 'bold', TEAL, width=855)
    p.text(98, 2185, 'Chaussures', 39, 'serif', INK)
    p.text(98, 2250, 'Pied maintenu,', 29, width=320)
    p.text(98, 2290, 'orteils à l’aise.', 29, width=320)
    for x, key, name in [(490, 'classic', 'Rossignol X-9 Classic'), (1430, 'skate', 'Rossignol X-9 Skate')]:
        product_photo(p, {'photo': 'rossignol-x9-'+key+'.jpg', 'key': key}, (x, 2175, x+300, 2350))
        p.text(x+150, 2360, name, 26, 'bold', INK, center=True)
    p.text(815, 2180, 'Avant-pied souple', 35, 'bold', BLUE, width=530)
    p.text(815, 2240, 'Pour dérouler le pied et pousser. Tige plutôt basse.', 34, width=530, leading=41, bottom=2390)
    p.text(1755, 2180, 'Semelle plus rigide', 35, 'bold', TEAL, width=530)
    p.text(1755, 2240, 'Collier haut : maintien de cheville pour les appuis latéraux.', 34, width=530, leading=41, bottom=2390)

    p.rect((70, 2430, 2330, 2675), '#FCF0E9', None, 22)
    p.text(98, 2450, 'Le poids et le niveau règlent le choix du cambre.', 43, 'serif', INK, width=2200)
    p.text(98, 2515, 'En classique : trop souple, l’anti-recul frotte ; trop rigide, il est difficile à mettre en contact pour pousser.', 33, width=1070, leading=38, bottom=2635)
    p.text(1258, 2515, 'Débutant : flex facile à charger et longueur maniable, dans sa plage de poids. Confirmé : ajuster au geste, à la technique et au rythme.', 33, width=1035, leading=38, bottom=2635)
    p.text(98, 2640, 'Le barème poids / rigidité du fabricant prime sur le calcul de longueur. Deux skieurs de même taille peuvent avoir des besoins différents.', 28, width=2200, leading=32, bottom=2673)

    p.rect((70, 2700, 2330, 2915), '#EDF5F6', None, 22)
    p.text(98, 2715, 'Normes : juste ce qu’il faut reconnaître.', 41, 'serif', INK)
    p.text(98, 2772, 'NNN (piste), Prolink, Turnamic : interfaces de chaussures compatibles. Choisir une fixation adaptée au classique ou au skating.', 30, width=1070, leading=35, bottom=2843)
    p.text(1258, 2772, 'SNS : ancien système Salomon, avec les noms Profil et Pilot. Non compatible avec nos fixations NNN.', 30, width=1035, leading=35, bottom=2843)
    p.rect((90, 2850, 2310, 2905), DARK, None, 13)
    p.text(112, 2862, 'À dire au client : « Chez nous, uniquement du NNN. Vérifions la compatibilité de vos chaussures. »', 30, 'bold', WHITE, width=2170, leading=35, bottom=2900)
    p.remember('Classique ou skating d’abord ; poids, niveau et compatibilité ensuite.', 'Le calcul en centimètres donne un départ. Le poids détermine la plage de longueur / rigidité ; les chaussures et les bâtons doivent correspondre à la pratique.')
    p.footer('Repères de loisir, à adapter au modèle, au niveau et au barème de poids. Écailles / peaux : pas de fart de retenue, mais glisse à entretenir. Sources : Fischer, Rossignol, Salomon. Photos : Fischer / Rossignol.')
    return p


def product_photo(p, c, box):
    im = Image.open(HERE / 'media' / c['photo']).convert('RGBA')
    if im.getchannel('A').getextrema()[0] == 0:
        bb = im.getchannel('A').getbbox()
    else:
        bb = im.convert('L').point(lambda value: 255 if value < 155 else 0).getbbox()
    assert bb, c['key']
    margin = max(12, round(im.width*.018))
    bb = (max(0, bb[0]-margin), max(0, bb[1]-margin), min(im.width, bb[2]+margin), min(im.height, bb[3]+margin))
    im = im.crop(bb)
    ratio = im.width/im.height
    im = ImageOps.contain(im, (box[2]-box[0], box[3]-box[1]), Image.Resampling.LANCZOS)
    assert abs(im.width/im.height-ratio) < .008, c['key']
    p.im.paste(im, ((box[0]+box[2]-im.width)//2, (box[1]+box[3]-im.height)//2), im)


def examples_page():
    p = Page(24)
    p.header('Exemples classique & skating.', 'Quatre vrais modèles Fischer et Rossignol pour apprendre à reconnaître le bon programme.', '02  /  LES FAMILLES')
    for family, y0, title, subtitle, color, soft in [
        ('classique', 440, '01 / Classique', 'Écailles ou peaux : deux solutions sans fart de retenue.', BLUE, '#ECF3F9'),
        ('skating', 1710, '02 / Skating', 'Semelle de glisse et appuis latéraux : un matériel spécifique.', TEAL, '#EDF5F6')
    ]:
        p.accent, p.soft = color, soft
        p.rect((70, y0, 2330, y0+1180), WHITE, color, 24, 4)
        p.rect((73, y0+3, 2327, y0+115), soft, None, 21)
        p.text(102, y0+27, title, 58, 'serif', INK)
        p.text(720, y0+39, subtitle, 33, 'bold', color, width=1570)
        p.line((1200, y0+145, 1200, y0+1155), LINE, 3)
        for i, c in enumerate([c for c in PRODUCTS if c['family']==family]):
            x, y = 95+i*1150, y0+145
            p.text(x+22, y+12, c['brand'].upper(), 26, 'bold', color)
            p.text(x+22, y+57, c['name'], 50, 'serif', INK, width=1015)
            product_photo(p, c, (x+12, y+137, x+176, y+473))
            p.rect((x+10, y+484, x+178, y+530), soft, None, 12)
            p.text(x+94, y+496, c['badge'], 24, 'bold', color, center=True)
            tx = x+205
            p.text(tx, y+135, 'Positionnement', 28, 'bold', color)
            p.text(tx, y+180, c['position'], 34, width=830, leading=40, bottom=y+307)
            p.text(tx, y+319, 'Ce que le fabricant met en avant', 27, 'bold', color, width=830)
            p.text(tx, y+365, c['maker'], 33, width=830, leading=39, bottom=y+523)
            p.text(x+22, y+553, 'Vocabulaire utile', 29, 'bold', color)
            p.text(x+22, y+595, c['vocab'], 32, 'bold', INK, width=1010, leading=38, bottom=y+675)
            p.text(x+22, y+685, 'Fiche technique', 29, 'bold', color)
            for j, (label, value) in enumerate(c['specs']):
                yy = y+729+j*34
                if j%2 == 0:
                    p.d.rectangle((x+17, yy-2, x+1040, yy+33), fill=common.P['lignes_tableau'])
                p.text(x+24, yy, label, 27, 'bold', color, width=210)
                p.text(x+245, yy, value, 29, width=790, leading=34, bottom=yy+35)
            p.rect((x+10, y+880, x+1040, y0+1160), DARK, None, 17)
            p.text(x+30, y+894, 'À DIRE AU CLIENT', 27, 'bold', WHITE)
            p.text(x+30, y+933, '« '+c['speech']+' »', 31, 'bold', WHITE, width=990, leading=35, bottom=y0+1152)
    p.remember('Écailles ou peaux en classique ; semelle de glisse en skating.', 'Le bon modèle dépend du programme, du niveau et du poids. Vérifier le barème de chaque référence et la rigidité de la paire ; équiper ensuite avec la bonne fixation et la bonne chaussure.')
    p.footer('Photos et caractéristiques : Fischer / Rossignol. Cotes spatule–patin–talon. IFP = plaque du ski ; TURNAMIC = interface compatible NNN piste. Longueurs disponibles selon référence, à choisir avec le barème de poids.')
    return p


if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--page',type=int,choices=[23,24])
    args=parser.parse_args()
    builds=[(23,intro_page),(24,examples_page)]
    common.write_manifest_pages([build() for n,build in builds if not args.page or args.page==n],MANIFEST)
