"""Pages 15–16: junior advice and five genuine Rossignol product examples.

Native typesetting and exact tables; original manufacturer images keep their
proportions. Only empty image margins are cropped. The first fourteen approved
poster records are retained verbatim. Sources and editorial distinctions: README.
"""
from pathlib import Path
import json, sys
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
sys.path.insert(0, str(ROOT / 'sources/guide'))
import render as common
from render import Page, INK, BODY, TEAL, CORAL, BLUE, WHITE, LINE, DARK, ft

common.OUT = ROOT / 'assets/guide-v759'
common.OUT.mkdir(exist_ok=True)
MANIFEST = ROOT / 'sources/freeride-freestyle/manifest.json'
PRODUCTS = json.loads((HERE / 'products.json').read_text())
PURPLE = '#75638F'


def section(p, y, number, title, color=TEAL):
    p.d.ellipse((76, y, 144, y + 68), fill=color)
    p.text(110, y + 13, str(number).zfill(2), 35, 'bold', WHITE, center=True)
    p.text(168, y + 6, title, 52, 'serif', INK, width=2120)


def advice_page():
    p = Page(15)
    p.header('Les skis juniors.', 'Comprendre son niveau, adapter la longueur, choisir une fixation adaptée à son gabarit.', '02  /  LES FAMILLES')
    section(p, 440, 1, 'Comprendre les niveaux ESF', BLUE)
    p.text(79, 531, 'La question à poser : « Quel est le dernier niveau obtenu, et sur quelles pistes est-il à l’aise ? »', 37, width=2240)
    # Reading order: top to bottom within each blue, green, then orange column.
    # These are summaries of acquired
    # skills, never an automatic medal-to-ski-length correspondence.
    levels = [
        ('Piou-Piou', 'Découvrir la neige, le matériel et les premières glissades.'),
        ('Ourson', 'Premiers virages en chasse-neige et premières remontées.'),
        ('Flocon', 'Enchaîner les virages en chasse-neige et contrôler sa vitesse.'),
        ('1ère étoile', 'Virages simples dérapés, équilibre sur pente faible à moyenne.'),
        ('2e étoile', 'Virages skis parallèles sur pente moyenne, bosses et creux.'),
        ('3e étoile', 'Virages parallèles plus précis, freinage dérapé et rythme.'),
        ('Étoile de bronze', 'Godille, changements de rythme et découverte de neiges variées.'),
        ('Étoile d’argent', 'Trajectoires plus précises, appuis affinés et premiers chronos.'),
        ('Étoile d’or', 'Aisance sur terrains et neiges variés ; mini-géant chronométré.')
    ]
    for col, (color, soft) in enumerate(zip([BLUE, TEAL, CORAL], ['#ECF3F9', '#EDF5F6', '#FCF0E9'])):
        x = 70 + col * 768
        p.rect((x, 604, x + 724, 1140), soft, color, 24, 5)
    for i, (title, body) in enumerate(levels):
        col, row = i // 3, i % 3
        x, y = 70 + col * 768, 614 + row * 177
        color = [BLUE, TEAL, CORAL][col]
        if row:
            p.line((x + 24, y - 10, x + 700, y - 10), color, 2)
        p.text(x + 24, y + 13, title, 38, 'bold', color)
        p.text(x + 24, y + 76, body, 32, width=676, leading=37, bottom=y + 153)
    p.rect((70, 1162, 2330, 1305), DARK, None, 20)
    p.text(96, 1184, 'FLÈCHE ≠ ÉTOILE', 32, 'bold', WHITE)
    p.text(540, 1182, 'Flèche : test chronométré en géant. Chamois : test en slalom. « Flèche d’argent » indique un résultat au chrono, différent de l’Étoile d’argent.', 35, 'sans', WHITE, width=1745, leading=42, bottom=1295)

    section(p, 1342, 2, 'Cinq familles : des repères pour choisir la longueur', TEAL)
    p.rect((70, 1434, 2330, 1502), DARK, None, 13)
    p.text(96, 1453, 'LE PROFIL DE L’ENFANT', 29, 'bold', WHITE)
    p.text(640, 1453, 'LONGUEUR DU SKI', 29, 'bold', WHITE)
    p.text(1175, 1453, 'CE QUE L’ON CHERCHE', 29, 'bold', WHITE)
    groups = [
        ('Pitchounes', '≈ 60–70 cm', 'Tout-petits, première fois à skis. Court et léger pour découvrir la glisse et déplacer les pieds facilement.'),
        ('Débutants', 'Taille −25 à −20 cm', 'Enfants déjà plus grands, mais qui apprennent. Faciliter le chasse-neige, les virages et l’arrêt.'),
        ('Débrouillards', 'Taille −15 cm', 'Ils tournent et contrôlent leur vitesse. Garder de la maniabilité avec davantage d’appui pour progresser.'),
        ('Confirmés', 'Taille −10 cm', 'Ils maîtrisent leurs virages. Gagner en soutien et en stabilité, avec un flex qu’ils peuvent encore déformer.'),
        ('Experts', 'Selon le programme', 'Slalom, géant ou freeride : modèles et longueurs spécifiques. Partir de la pratique réelle et du gabarit.')
    ]
    for i, (profile, length, why) in enumerate(groups):
        y = 1514 + i * 143
        color = [BLUE, TEAL, CORAL, PURPLE, INK][i]
        p.rect((70, y, 2330, y + 131), WHITE, LINE, 15, 2)
        p.d.rounded_rectangle((70, y, 82, y + 131), radius=5, fill=color)
        p.text(102, y + 35, profile, 43, 'serif', INK, width=480)
        p.text(640, y + 39, length, 39, 'bold', color, width=510)
        p.text(1175, y + 20, why, 34, width=1110, leading=40, bottom=y + 128)
    p.text(79, 2248, '« Taille » = hauteur de l’enfant. Repères SGD indicatifs : adapter au poids, à l’aisance, au flex et au modèle. Plus court facilite le pivot ; plus long apporte de l’appui.', 35, width=2240, leading=43, bottom=2338)
    p.text(79, 2340, 'À dire aux parents : « On choisit pour sa taille d’aujourd’hui, sans prendre trop grand pour l’an prochain. »', 34, 'bold', TEAL, width=2240, bottom=2383)

    section(p, 2402, 3, 'La fixation : le poids compte, la chaussure aussi', CORAL)
    p.rect((70, 2494, 1170, 2740), '#EDF5F6', None, 20)
    p.text(98, 2513, 'Une plage de déclenchement adaptée', 36, 'bold', INK, width=1030)
    p.text(98, 2573, 'Demander le poids réel. Le réglage nécessaire doit entrer dans la plage de la fixation. Pour un enfant léger, un seuil minimal trop élevé peut être inadapté. Les indices DIN / Z ne sont pas des kilos.', 34, width=1035, leading=40, bottom=2734)
    p.rect((1230, 2494, 2330, 2740), '#FCF0E9', None, 20)
    p.text(1258, 2513, 'Vérifier l’ensemble ski–fixation–chaussure', 35, 'bold', INK, width=1035)
    p.text(1258, 2573, 'Le réglage tient aussi compte de la taille, de l’âge, du niveau et de la longueur de semelle en mm. Vérifier la norme de semelle (alpine / GripWalk, enfant / adulte) et sa compatibilité avec la fixation.', 34, width=1035, leading=40, bottom=2734)
    p.rect((70, 2764, 2330, 2902), DARK, None, 18)
    p.text(96, 2783, 'RÉGLAGE DE SÉCURITÉ', 29, 'bold', WHITE)
    p.text(560, 2782, 'Réglage et contrôle indispensables en atelier, à réévaluer quand l’enfant grandit ou change de chaussures. Cf. page « Sécurité » — à venir.', 35, 'sans', WHITE, width=1725, leading=42, bottom=2892)
    p.remember('Le bon ski, c’est celui que l’enfant maîtrise aujourd’hui.', 'Niveau acquis + taille + poids + pratique réelle. La médaille oriente la discussion ; elle ne choisit ni la longueur ni la fixation à elle seule. Pour un petit, la facilité et la confiance passent avant la marge de croissance.')
    p.footer('Synthèse pédagogique : ESF. Longueurs : repères SGD à adapter, distincts des tableaux fabricants. Fixations : recommandations Rossignol / LOOK.')
    return p


def packshot(p, key, box):
    im = Image.open(HERE / 'media' / (key + '.jpg')).convert('RGB')
    # Bound the product using its dark pixels; keep every original pixel inside
    # the rectangle, including light topsheet areas and manufacturer shadows.
    mask = im.convert('L').point(lambda value: 255 if value < 150 else 0)
    bb = mask.getbbox()
    assert bb, key
    margin = max(12, round(im.width * .018))
    bb = (max(0, bb[0]-margin), max(0, bb[1]-margin), min(im.width, bb[2]+margin), min(im.height, bb[3]+margin))
    im = im.crop(bb)
    ratio = im.width / im.height
    im = ImageOps.contain(im, (box[2]-box[0], box[3]-box[1]), Image.Resampling.LANCZOS)
    assert abs(im.width / im.height - ratio) < .008, key
    p.im.paste(im, ((box[0]+box[2]-im.width)//2, (box[1]+box[3]-im.height)//2))


def examples_page():
    p = Page(16)
    p.header('Exemples de skis juniors.', 'Cinq modèles Rossignol pour transformer les caractéristiques en arguments utiles aux parents.', '02  /  LES FAMILLES')
    for i, c in enumerate(PRODUCTS):
        y = 440 + i * 493
        end = y + 471
        p.set_accent(i)
        if i == 4:
            p.accent, p.soft = INK, '#EDF2F4'
        p.rect((70, y, 2330, end), WHITE, p.accent, 22, 3)
        p.rect((72, y+2, 2328, y+89), p.soft, None, 20)
        p.text(96, y+19, str(i+1).zfill(2)+' / '+c['family'], 29, 'bold', p.accent, width=480, leading=34)
        p.text(590, y+16, c['name'], 52, 'serif', INK, width=1700)
        packshot(p, c['key'], (90, y+105, 286, end-20))
        p.text(320, y+110, 'Positionnement', 28, 'bold', p.accent)
        p.text(320, y+152, c['position'], 35, width=1030, leading=41, bottom=y+240)
        p.text(320, y+247, 'Ce que le fabricant met en avant', 28, 'bold', p.accent)
        p.text(320, y+289, c['maker'], 33, width=1030, leading=38, bottom=y+377)
        p.text(1430, y+110, 'Vocabulaire utile', 28, 'bold', p.accent)
        p.text(1430, y+152, c['vocab'], 33, 'bold', INK, width=850, leading=39, bottom=y+237)
        p.text(1430, y+247, 'Fiche technique', 28, 'bold', p.accent)
        for j, (label, value) in enumerate(c['specs']):
            yy = y+283+j*33
            if j % 2 == 0:
                p.d.rectangle((1423, yy-2, 2300, yy+32), fill=common.P['lignes_tableau'])
            p.text(1430, yy, label, 27, 'bold', p.accent, width=150)
            p.text(1590, yy, value, 30, width=710, leading=33, bottom=yy+34)
        p.rect((310, y+386, 2306, end-8), DARK, None, 15)
        p.text(332, y+409, 'À DIRE AU CLIENT', 26, 'bold', WHITE)
        p.text(647, y+392, '« '+c['speech']+' »', 31, 'bold', WHITE, width=1630, leading=34, bottom=end-9)
    p.remember('Un même décor Hero peut cacher des skis très différents.', 'Distinguer le ski d’apprentissage, l’initiation aux portes et le vrai ski de compétition. Pour un expert, préciser le programme : slalom, géant ou freeride. Choisir ensuite la longueur et la fixation adaptées.')
    p.footer('Visuels originaux et données : Rossignol. Cotes spatule–patin–talon et rayons à la longueur indiquée. Positionnement et discours : conseil SGD. Photos à des échelles différentes ; montage de fixation selon le pack.')
    return p


if __name__ == '__main__':
    records = json.loads(MANIFEST.read_text())
    assert len(records) >= 16
    approved = records.copy()
    for build in [advice_page, examples_page]:
        page = build()
        records[page.n-1] = page.save()
        print('Page', page.n, 'OK', flush=True)
    assert records[:14] == approved[:14] and records[16:] == approved[16:]
    MANIFEST.write_text(json.dumps(records, ensure_ascii=False, indent=2))
