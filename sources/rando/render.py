"""Touring spread, pages 17–18. Exact typesetting; original manufacturer photos.

User-provided prices and time split are explicitly indicative SGD benchmarks.
Technical statements and product data: primary sources documented in README.
"""
from pathlib import Path
import json, sys
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
sys.path.insert(0, str(ROOT / 'sources/guide'))
import render as common
from render import Page, INK, BODY, TEAL, CORAL, BLUE, WHITE, LINE, DARK

common.OUT = ROOT / 'assets/guide-v760'
common.OUT.mkdir(exist_ok=True)
MANIFEST = ROOT / 'sources/freeride-freestyle/manifest.json'
PRODUCTS = json.loads((HERE / 'products.json').read_text())


def heading(p, y, title, color=TEAL, size=49):
    p.d.rounded_rectangle((72, y+4, 84, y+56), radius=5, fill=color)
    p.text(106, y, title, size, 'serif', INK, width=2200)


def intro_page():
    p = Page(17)
    p.header('Les skis de randonnée.', 'Monter par ses propres moyens, puis redescendre à skis : raisonner sur le pack complet.', '02  /  LES FAMILLES')
    im = Image.open(HERE / 'media/montee-elan.jpg').convert('RGB')
    im = ImageOps.fit(im, (1420, 450), Image.Resampling.LANCZOS, centering=(.5, .58))
    p.im.paste(im, (70, 440))
    p.rect((1530, 440, 2330, 890), DARK, None, 24)
    p.text(1560, 463, 'LE PRINCIPE', 31, 'bold', WHITE)
    p.text(1560, 520, 'Des peaux pour monter sans remontées mécaniques, des fixations qui libèrent le talon, puis une vraie descente à skis.', 37, 'sans', WHITE, width=735, leading=44, bottom=701)
    p.text(1560, 710, '95 % / 5 %', 62, 'serif', WHITE)
    p.text(1560, 784, 'MONTÉE / DESCENTE', 28, 'bold', WHITE)
    p.text(1560, 831, 'Temps : repère SGD schématique, variable selon la sortie.', 28, 'sans', WHITE, width=735, leading=32, bottom=885)

    steps = [
        ('01 / Monter avec les peaux', 'Les peaux sous les semelles glissent vers l’avant et limitent le recul. Talons libres et chaussures en mode marche.'),
        ('02 / Les fixations à inserts', 'Les pointes de la butée avant entrent dans les logements métalliques des chaussures. Les cales soutiennent le talon selon la pente.'),
        ('03 / Passer en descente', 'Retirer les peaux, passer fixations et chaussures en mode ski : le talon est retenu. Toujours suivre la notice du modèle.')
    ]
    for i, (title, body) in enumerate(steps):
        x = 70+i*768
        p.set_accent(i)
        p.rect((x, 925, x+724, 1238), WHITE, p.accent, 20, 3)
        p.text(x+24, 948, title, 35, 'bold', p.accent, width=676, leading=41)
        p.text(x+24, 1015, body, 35, width=676, leading=42, bottom=1228)

    p.rect((70, 1270, 2330, 1500), '#FCF0E9', None, 22)
    p.text(98, 1290, 'Le gain de poids se paie parfois en amorti.', 47, 'serif', INK, width=2200)
    p.text(98, 1362, 'Noyaux légers, profils affinés et renforts ciblés réduisent la masse : moins d’effort à la montée. Mais un ski très léger peut davantage vibrer sur neige glacée ou trafolée (déjà tracée et irrégulière), et demander plus de précision à la descente.', 36, width=2200, leading=43, bottom=1495)

    p.rect((70, 1530, 2330, 1940), '#EDF5F6', None, 22)
    heading(p, 1550, 'Les peaux, en trente secondes')
    skins = [
        ('SYNTHÉTIQUE', 'Souvent économique et très résistant. Bonne accroche à la montée, mais une glisse moins efficace.', BLUE),
        ('100 % MOHAIR', 'Excellente glisse. Accroche selon la neige et la technique ; s’use plus vite que le synthétique.', CORAL),
        ('LE MIX 70 / 30 CHEZ SGD', '70 % mohair + 30 % synthétique : bonne glisse, bonne accroche et plus de résistance qu’un pur mohair.', TEAL)
    ]
    for i, (title, body, color) in enumerate(skins):
        x = 98+i*758
        if i:
            p.line((x-20, 1631, x-20, 1825), LINE, 3)
        p.text(x, 1633, title, 30, 'bold', color, width=700)
        p.text(x, 1683, body, 34, width=697, leading=40, bottom=1844)
    p.text(98, 1867, 'Une peau doit être ajustée au ski en laissant les carres dégagées. Séchage et entretien comptent aussi.', 32, width=2200, leading=37, bottom=1932)

    heading(p, 1970, 'Au magasin : les questions dans le bon ordre', CORAL)
    rows = [
        (2050, 2200, '1. Location ou vente ?', 'LOCATION → Parc de location : niveau, gabarit et sortie envisagée. Choisir dans le matériel disponible.\nVENTE → Poursuivre le conseil ci-dessous.'),
        (2215, 2355, '2. Occasion ou neuf ?', 'Ski seul ou pack ? Occasion, fin de série ou neuf ? Quel budget et quel équipement possède-t-il déjà ?'),
        (2370, 2535, '3. Montée ou descente ?', 'Durée, dénivelé, niveau en descente et neige recherchée. Puis proposer skis + fixations + peaux ; ajouter des chaussures compatibles si nécessaire.')
    ]
    for i, (y, end, title, body) in enumerate(rows):
        p.set_accent(i)
        p.rect((70, y, 2330, end), WHITE, p.accent, 17, 3)
        p.text(98, y+22, title, 35, 'bold', p.accent, width=510, leading=42)
        p.line((620, y+19, 620, end-19), LINE, 3)
        p.text(650, y+17, body, 35, width=1640, leading=42, bottom=end-7)

    heading(p, 2562, 'Annoncer le budget du pack avant de choisir les modèles.', TEAL, 43)
    budgets = [
        ('NEUF / PRIX COURANT', '≈ 2 000 €', INK, '#EDF2F4'),
        ('FIN DE SÉRIE / SGD', '≈ 1 000 €', BLUE, '#ECF3F9'),
        ('OCCASION / SGD', '≈ 600–700 €', TEAL, '#EDF5F6')
    ]
    for i, (label, price, color, soft) in enumerate(budgets):
        x = 70+i*768
        p.rect((x, 2635, x+724, 2810), soft, color, 20, 3)
        p.text(x+25, 2657, label, 29, 'bold', color)
        p.text(x+25, 2716, price, 66, 'serif', INK, width=674)
    p.text(79, 2833, 'Pack complet = skis + fixations + peaux + chaussures. Ordres de grandeur SGD, selon les modèles et le stock ; hors bâtons et équipement de sécurité.', 33, width=2240, leading=40, bottom=2920)
    p.remember('On conseille un ensemble cohérent, adapté à la sortie et au budget.', 'Location → parc. Vente → occasion ou neuf, budget, puis priorité montée ou descente. Vérifier chaussures à inserts compatibles, fixations adaptées et peaux ajustées ; faire contrôler le montage et les réglages en atelier.')
    p.footer('En terrain avalancheux : DVA, pelle, sonde et formation. Cf. page « Sécurité » — à venir. Photo : Elan. Peaux : Colltex / Rossignol. Budgets : repères SGD, hors accessoires et matériel de secours.')
    return p


def product_photo(p, c, box):
    im = Image.open(HERE / 'media' / c['photo']).convert('RGBA')
    if im.getchannel('A').getextrema()[0] == 0:
        bb = im.getchannel('A').getbbox()
    else:
        bb = im.convert('L').point(lambda value: 255 if value < 160 else 0).getbbox()
    assert bb, c['key']
    margin = max(12, round(im.width*.018))
    bb = (max(0, bb[0]-margin), max(0, bb[1]-margin), min(im.width, bb[2]+margin), min(im.height, bb[3]+margin))
    im = im.crop(bb)
    ratio = im.width/im.height
    im = ImageOps.contain(im, (box[2]-box[0], box[3]-box[1]), Image.Resampling.LANCZOS)
    assert abs(im.width/im.height-ratio) < .008
    p.im.paste(im, ((box[0]+box[2]-im.width)//2, (box[1]+box[3]-im.height)//2), im)


def choice_page():
    p = Page(18)
    p.header('Choisir ses skis de rando.', 'Deux priorités et trois vrais modèles : relier l’effort de montée au plaisir de la descente.', '02  /  LES FAMILLES')
    families = [
        (70, TEAL, '#EDF5F6', 'Priorité à la montée', 'GRAND DÉNIVELÉ / EFFICACITÉ', '≈ 75–90 mm', 'Plus fin et léger : moins d’effort à chaque pas. Longueur maniable pour les conversions (demi-tours en montée). Moins de portance et souvent moins d’amorti en descente.', 'Vous privilégiez le dénivelé ou le plaisir de skier à la descente ?'),
        (1230, CORAL, '#FCF0E9', 'Priorité à la descente', 'FREERANDO / NEIGE SOUPLE', '≈ 95–110 mm', 'Plus de largeur et de matière pour la portance, les appuis et l’amorti. Longueur souvent proche de la taille, selon niveau et modèle. Un ensemble plus lourd à emmener en montée.', 'Quelle neige visez-vous, pour quel effort à la montée ?')
    ]
    for x, color, soft, title, kicker, waist, body, question in families:
        p.accent, p.soft = color, soft
        p.rect((x, 440, x+1100, 1110), WHITE, color, 24, 3)
        p.text(x+30, 466, title, 58, 'serif', INK, width=1040)
        p.text(x+32, 550, kicker, 29, 'bold', color)
        p.rect((x+25, 605, x+1075, 704), soft, None, 17)
        p.text(x+47, 625, waist, 56, 'serif', INK)
        p.text(x+665, 631, 'AU PATIN', 29, 'bold', color)
        p.text(x+665, 673, 'Repère indicatif', 25, 'sans', BODY)
        p.text(x+32, 735, body, 37, width=1036, leading=45, bottom=961)
        p.rect((x+25, 973, x+1075, 1094), DARK, None, 17)
        p.text(x+44, 986, 'LA QUESTION À POSER', 26, 'bold', WHITE)
        p.text(x+44, 1019, question, 32, 'bold', WHITE, width=1010, leading=34, bottom=1090)

    for i, c in enumerate(PRODUCTS):
        y, end = 1150+i*590, 1710+i*590
        p.set_accent(i)
        p.rect((70, y, 2330, end), WHITE, p.accent, 22, 3)
        p.rect((72, y+2, 2328, y+89), p.soft, None, 20)
        p.text(96, y+19, c['tag'], 28, 'bold', p.accent, width=460, leading=34)
        p.text(590, y+16, c['brand']+' · '+c['name'], 53, 'serif', INK, width=1690)
        product_photo(p, c, (90, y+112, 286, y+391))
        p.rect((92, y+407, 286, y+467), p.soft, None, 13)
        p.text(189, y+419, c['waist'], 40, 'serif', INK, center=True)
        p.text(320, y+112, 'Positionnement', 28, 'bold', p.accent)
        p.text(320, y+157, c['position'], 35, width=1030, leading=42, bottom=y+244)
        p.text(320, y+257, 'Ce que le fabricant met en avant', 28, 'bold', p.accent)
        p.text(320, y+300, c['maker'], 34, width=1030, leading=40, bottom=y+426)
        p.text(1430, y+112, 'Vocabulaire utile', 28, 'bold', p.accent)
        p.text(1430, y+157, c['vocab'], 33, 'bold', INK, width=850, leading=39, bottom=y+278)
        p.text(1430, y+282, 'Fiche technique', 28, 'bold', p.accent)
        for j, (label, value) in enumerate(c['specs']):
            yy = y+324+j*34
            if j%2 == 0:
                p.d.rectangle((1423, yy-2, 2300, yy+33), fill=common.P['lignes_tableau'])
            p.text(1430, yy, label, 27, 'bold', p.accent, width=150)
            p.text(1590, yy, value, 29, width=710, leading=34, bottom=yy+35)
        p.rect((310, y+445, 2306, end-12), DARK, None, 15)
        p.text(332, y+481, 'À DIRE AU CLIENT', 26, 'bold', WHITE)
        p.text(647, y+460, '« '+c['speech']+' »', 33, 'bold', WHITE, width=1630, leading=38, bottom=end-15)
    p.remember('Le plus léger n’est pas automatiquement le meilleur choix.', 'Grand dénivelé : économiser l’effort. Freerando : accepter plus de masse pour la portance et le comportement en descente. Comparer le poids de l’ensemble ski + fixation, à longueur comparable, et garder une chaussure cohérente.')
    p.footer('Photos et données : Rossignol / Elan. Cotes spatule–patin–talon et rayon à la longueur indiquée. Programmes : repères SGD. Modèles illustratifs ; choix selon niveau, gabarit, terrain et disponibilité.')
    return p


if __name__ == '__main__':
    records = json.loads(MANIFEST.read_text())
    assert len(records) >= 18
    approved = records.copy()
    for build in [intro_page, choice_page]:
        p = build()
        records[p.n-1] = p.save()
        print('Page', p.n, 'OK', flush=True)
    assert records[:16] == approved[:16] and records[18:] == approved[18:]
    MANIFEST.write_text(json.dumps(records, ensure_ascii=False, indent=2))
