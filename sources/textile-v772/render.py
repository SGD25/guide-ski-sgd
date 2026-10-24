"""Integrate the approved textile spread and harmonise page furniture only.

The approved spread is cropped into its two pages, never regenerated. Existing
content pixels are checked outside the page furniture and numbered cross-references.
"""
from pathlib import Path
from copy import deepcopy
import json, sys, importlib.util
from PIL import Image, ImageDraw, ImageOps, ImageChops
ROOT=Path(__file__).resolve().parents[2]; HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'sources/guide'))
import render as base
from render import Page, INK, BODY, TEAL, BLUE, CORAL, WHITE, LINE, DARK, ft
OUT=ROOT/'assets/guide-v772'; OUT.mkdir(exist_ok=True)
OLD=json.loads((HERE/'baseline-v771.json').read_text())
BG=base.P['fond']; W,H=2400,3394

def furniture(p,n,old=None):
    """Identical positions, fonts and colours for every interior page."""
    areas=[(0,0,W,112),(0,3327,W,H)]
    # Keep all source notes; clear only the old logo area on the right.
    logo=(2045,3270 if old==28 else 3222,2290,3339)
    areas.append(logo)
    p.d.rectangle((0,0,W,112),fill=BG)
    color=BLUE if n<8 else CORAL if n<27 else '#75638F'
    label='OUVERTURE / LE SOMMAIRE' if n==2 else ('CHAPITRE 01 / COMPRENDRE' if n<8 else 'CHAPITRE 02 / RECONNAÎTRE & CONSEILLER' if n<27 else 'CHAPITRE 03 / SÉCURISER')
    p.d.rectangle((0,0,W,13),fill=color)
    p.text(76,48,label,35,'bold',color)
    p.line((1460,66,2070,66),LINE,3)
    p.rect((2110,36,2324,102),BG,base.P['reperes'],28,2)
    p.text(2217,53,f'PAGE {n:02}',31,'bold',INK,center=True)
    p.d.rectangle(logo,fill=BG)
    p.d.rectangle((0,3327,W,H),fill=BG)
    # Remove the previous thin footer rule, which varied slightly by renderer.
    # Only turquoise line pixels are touched; nearby black source notes survive.
    pix=p.im.load()
    for y in range(3308,3340):
        hits=sum(1 for x in range(70,2005) if (lambda c:c[1]>c[0]+5 and c[2]>c[0]+5 and c[0]<249)(pix[x,y]))
        if hits>1800:
            p.d.rectangle((60,y,2012,y),fill=BG);areas.append((60,y,2012,y))
    p.line((70,3330,2010,3330),base.P['reperes'],3);areas.append((70,3329,2010,3332))
    p.photo('sgd-logo.png',(2070,3273,2240,3374));areas.append((2070,3273,2240,3374))
    p.text(76,3351,'SPORT GOOD DEAL  /  GUIDE DU SKI',27,'bold',INK)
    p.text(2325,3350,f'{n:02}',29,'bold',INK,center=True)
    return areas

def contents():
    p=Page(2)
    p.text(76,135,'Tout le guide,',148,'serif',INK)
    p.text(1060,145,'en un coup d’œil.',122,'italic',CORAL)
    p.text(78,323,'30 pages pour comprendre, reconnaître, conseiller et sécuriser.',42,width=2240)
    desc={3:'Les trois zones et les largeurs du ski.',4:'Relier les dimensions aux sensations.',5:'Petits virages ou grandes courbes.',6:'Lire le profil et les zones de rocker.',7:'Comprendre le noyau et les renforts.',8:'Choisir une famille selon le terrain.',9:'Quatre approches de la piste.',10:'Des modèles et des mots pour conseiller.',11:'Accroche, portance et polyvalence.',12:'Trois skis, trois compromis.',13:'Poudreuse, park et figures.',14:'Six exemples freeride / freestyle.',15:'Niveaux, tailles et fixations enfants.',16:'Des exemples juniors Rossignol.',17:'Comprendre le pack de randonnée.',18:'Montée ou freerando : comparer.',19:'Pointure, volume, flex et essayage.',20:'Monter confortablement, skier maintenu.',21:'Programmes, profils et fixations.',22:'Quatre exemples de snowboards Nitro.',23:'Classique, skating, tailles et équipement.',24:'Des exemples Fischer et Rossignol.',25:'Évacuer, isoler et protéger.',26:'Déperlance, membranes et indices.',27:'Données client, compatibilités et ISOSKI.',28:'Contrôles, réglage et traçabilité.',29:'DVA, pelle, sonde et contrôles du groupe.',30:'Recherche, sauvetage et sac airbag.'}
    labels={3:'Anatomie & lignes de cotes',4:'Largeur & longueur',5:'Rayon de courbure',6:'Cambres & rockers',7:'Construction & noyaux',8:'Les familles de skis',9:'Skis de piste',10:'Exemples piste',11:'Skis all-mountain',12:'Exemples all-mountain',13:'Freeride & freestyle',14:'Exemples freeride & freestyle',15:'Skis juniors',16:'Exemples juniors',17:'Skis de randonnée',18:'Exemples rando',19:'Chaussures alpines',20:'Chaussures de randonnée',21:'Choisir son snowboard',22:'Exemples Nitro',23:'Ski de fond : classique & skating',24:'Exemples de ski de fond',25:'Textile : le système 3 couches',26:'Textile : membranes & respirabilité',27:'Fixations : comprendre le réglage',28:'Fixations : contrôler avant de louer',29:'Avalanche : s’équiper & contrôler',30:'Avalanche : rechercher & secourir'}
    groups=[(70,440,1170,1310,0,'01 / Comprendre','Les repères du matériel',range(3,8),125),(70,1340,1170,2845,1,'02 / Reconnaître & conseiller','Les familles de skis',range(8,17),141),(1230,440,2330,1875,1,'02 / Reconnaître & conseiller','Rando, chaussures, snow, fond & textile',range(17,27),119),(1230,1905,2330,2845,3,'03 / Sécuriser','Avant de confier le matériel',range(27,31),180)]
    for x,y,x2,y2,accent,title,subtitle,nums,rh in groups:
        p.set_accent(accent);p.rect((x,y,x2,y2),WHITE,p.accent,25,3);p.rect((x+3,y+3,x2-3,y+174),p.soft,None,23)
        p.text(x+30,y+28,title,43,'serif',INK,width=1040)
        p.text(x+30,y+106,subtitle,29,'bold',p.accent,width=1040)
        for i,n in enumerate(nums):
            yy=y+215+i*rh
            if i:p.line((x+28,yy-24,x2-28,yy-24),LINE,2)
            size=35 if x>1000 else 39
            p.text(x+30,yy,labels[n],size,'bold',INK,width=865,leading=42,bottom=yy+54)
            p.text(x+30,yy+53,desc[n],28 if x>1000 else 30,width=855,leading=34,bottom=min(yy+rh-8,y2-20))
            p.rect((x2-173,yy-2,x2-26,yy+76),p.soft,None,22)
            p.text(x2-100,yy+18,f'{n:02} →',34,'bold',p.accent,center=True)
            p.link((x+20,yy-12,x2-20,min(yy+rh-12,y2-12)),n,labels[n])
    p.photo_cover('piste-station-v752.png',(70,2890,794,3175),(.5,.56))
    p.rect((838,2890,2330,3175),DARK,None,24)
    p.text(875,2918,'Le bon parcours au comptoir.',52,'serif',WHITE,width=1410)
    p.text(875,3000,'Terrain → niveau → gabarit → matériel compatible → contrôles.',38,'sans',WHITE,width=1400,leading=46,bottom=3110)
    p.text(875,3120,'Chaque ligne du sommaire est cliquable.',31,'bold',WHITE)
    furniture(p,2);return p

def references(p,old):
    areas=[]
    if old==15:
        b=(550,2775,2305,2896);areas.append(b);p.d.rectangle(b,fill=DARK)
        p.text(560,2782,'Réglage et contrôle indispensables en atelier, à réévaluer quand l’enfant grandit ou change de chaussures. Voir les pages 27–28 pour la sécurité des fixations.',35,'sans',WHITE,width=1725,leading=42,bottom=2892)
    if old==19:
        b=(1595,2740,2300,2910);areas.append(b);p.d.rectangle(b,fill='#ECF3F9')
        p.text(1600,2745,'Contrôler coque, fermetures, chausson et usure des semelles. Sécher sans chaleur forte. Réglages / contrôles : voir pages 27–28.',30,width=690,leading=35,bottom=2907)
    notes={17:'En terrain avalancheux : DVA, pelle, sonde et formation. Voir pages 29–30. Photos : Elan, POMOCA (peau illustrative 65/35), Dynafit, SCARPA. Le mix 70/30 reste le repère SGD. Budgets : hors accessoires et matériel de secours.',20:'Semelles et inserts : vérifier les notices des modèles exacts, y compris les exceptions et systèmes propriétaires. Réglages et contrôle de sécurité : voir pages 27–28. Sources : SCARPA, Dynafit, Rossignol, Tyrolia. Photos : SCARPA.',21:'Repères adultes indicatifs, hors planches de carving alpin et splitboards. Hors-piste : équipement et formation adaptés ; voir sécurité avalanche pages 29–30. Sources : Nitro, RIDE, Burton, Nidecker. Photos fabricants.'}
    if old in notes:
        b=(70,3230,2000,3318);areas.append(b);p.d.rectangle(b,fill=BG)
        p.text(76,3237,notes[old],26,width=1890,bottom=3313)
    return areas

def main():
    records=[];checks=[]
    for old,record in enumerate(OLD['records'],1):
        n=old+2 if old>=25 else old
        if old==2:
            p=contents();links=p.links;areas=[];before=None
        else:
            p=Page(n);p.im=Image.open(ROOT/record['path']).convert('RGB')
            if p.im.size!=(W,H):p.im=p.im.resize((W,H),Image.Resampling.LANCZOS)
            p.d=ImageDraw.Draw(p.im);before=p.im.copy();areas=[]
            links=deepcopy(record.get('links',[]))
            for link in links:
                if link['page']>=25:link['page']+=2
            if old==1:
                b=(1818,2805,2310,2862);areas.append(b);p.d.rectangle(b,fill=WHITE)
                p.text(1821,2815,'PAGE 27  →',29,'bold','#75638F')
            else:areas=furniture(p,n,old)+references(p,old)
        if before is not None:
            diff=ImageChops.difference(before,p.im)
            for b in areas:ImageDraw.Draw(diff).rectangle(b,fill=0)
            assert diff.getbbox() is None,('Content changed outside furniture/reference',old)
            checks.append({'old_page':old,'new_page':n,'content_unchanged_outside':areas})
        dest=OUT/f'page-{n:02}.jpg';p.im.save(dest,quality=94,subsampling=0,optimize=True)
        new=deepcopy(record);new.update(page=n,path=str(dest.relative_to(ROOT)),links=links);records.append(new)
        print('Page',n,'OK',flush=True)
    spread=Image.open(HERE/'approved-spread.png').convert('RGB')
    for n,box in [(25,(0,40,742,1010)),(26,(748,40,1491,1010))]:
        p=Page(n);body=ImageOps.contain(spread.crop(box),(2320,3070),Image.Resampling.LANCZOS)
        xy=((W-body.width)//2,125);p.im.paste(body,xy);p.d=ImageDraw.Draw(p.im)
        furniture(p,n)
        assert ImageChops.difference(body,p.im.crop((xy[0],xy[1],xy[0]+body.width,xy[1]+body.height))).getbbox() is None
        dest=OUT/f'page-{n:02}.jpg';p.im.save(dest,quality=94,subsampling=0,optimize=True)
        records.append({'page':n,'path':str(dest.relative_to(ROOT)),'links':[]})
    records.sort(key=lambda r:r['page'])
    (ROOT/'sources/freeride-freestyle/manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
    cat=deepcopy(OLD['catalog']);cat.update(version='V07.72',cache='20261024-72a')
    for meta in cat['pages']:
        if meta['page']>=25:meta['page']+=2
        if meta['chapter'].startswith('02'):meta['chapter']='02 · Reconnaître & conseiller'
    cat['pages'][1]['description']='Sommaire cliquable des 30 pages : matériel 3–7, familles et modèles 8–18, chaussures 19–20, snowboard 21–22, fond 23–24, textile 25–26, fixations 27–28 et avalanche 29–30.'
    cat['pages'] += [{'page':25,'title':'Textile : le système 3 couches','chapter':'02 · Reconnaître & conseiller','description':'Évacuer l’humidité, retenir la chaleur et se protéger : premières couches synthétiques et mérinos, polaire, veste extérieure et gestion des couches.'},{'page':26,'title':'Textile : membranes et respirabilité','chapter':'02 · Reconnaître & conseiller','description':'Déperlance, imperméabilité et respirabilité ; construction d’une veste, membranes GORE-TEX et Sympatex, indices mm, MVTR et RET, et conseil client.'}]
    cat['pages'].sort(key=lambda r:r['page'])
    # Only the printed destination numbers in this existing description change.
    cat['pages'][14]['description']=OLD['catalog']['pages'][14]['description'].replace('25–26','27–28')
    (ROOT/'sources/guide/catalog.json').write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n')
    (HERE/'content-preservation.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
    print('30 pages; approved body pixels preserved; references and contents updated.')

if __name__=='__main__':main()
