"""Add pages 13–14 as complete HD images; retain the twelve approved pages.

Scenery is illustrative. All six product photos and technical facts come from
manufacturer pages listed in products.json / photos.json. Product pixels are
never generated, stretched, recolored or retouched; only empty margins are cropped.
"""
from pathlib import Path
import json,sys
from PIL import Image,ImageDraw,ImageOps,ImageChops
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'sources/guide'))
import render as common
from render import Page,INK,BODY,TEAL,CORAL,BLUE,WHITE,PALE,LINE,DARK,ft
common.OUT=ROOT/'assets/guide-v755';common.OUT.mkdir(exist_ok=True)
MEDIA=HERE/'media'
PURPLE='#75638F'
PRODUCTS=json.loads((HERE/'products.json').read_text())

def scene(p,name,box):
    im=Image.open(MEDIA/name).convert('RGB')
    im=ImageOps.fit(im,(box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS,centering=(.5,.06 if 'freestyle' in name else .43))
    p.im.paste(im,box[:2])

def family_page():
    p=Page(13);p.header('Freeride & freestyle.','Deux familles, deux intentions : flotter en neige profonde ou jouer avec les figures.','02  /  LES FAMILLES')
    cards=[dict(x=70,n=3,color=TEAL,soft='#EDF5F6',title='Les skis freeride',sub='Priorité à la neige non damée et à la poudreuse.',photo='freeride-scene.jpg',waist='> 105 mm',waistnote='Repère poudreuse',length='Longueur : souvent autour de la taille à +10 / +15 cm ; à ajuster au modèle et au gabarit.',behavior='Le ski s’enfonce moins et pivote plus facilement en neige profonde. Sur piste dure, il est moins vif d’une carre à l’autre et souvent plus physique.',client='Un skieur déjà à l’aise, qui sort réellement des pistes et cherche davantage de portance.',points=['La largeur aide à rester en surface : elle ne remplace pas la technique du skieur.','Le rocker relève l’avant plus tôt et facilite la mise en surface ; le talon relevé aide au pivot.','Le flex et la longueur règlent le soutien : plus joueur pour pivoter, plus ferme pour engager.'],question='Vous cherchez surtout la poudreuse, ou un ski pour sortir des pistes dans des neiges variées ?',speech='Ce ski porte davantage en neige profonde et pivote facilement. En échange, il est moins vif sur piste dure.'),
    dict(x=1230,n=4,color=PURPLE,soft='#F2EFF7',title='Les skis freestyle',sub='Priorité au park, aux sauts et à la créativité.',photo='freestyle-scene.jpg',waist='≈ 85–100 mm',waistnote='Repère park / jeu',length='Longueur : souvent proche de la taille (±5 cm), selon le niveau, le gabarit et les figures.',behavior='Le ski facilite le jeu avec le terrain, le ski en arrière et les réceptions. Le caractère dépend surtout du flex, du profil et du montage.',client='Un skieur qui veut apprendre ou pratiquer des figures ; demander s’il préfère les rails ou les sauts.',points=['Twin-tip : spatule et talon relevés pour skier aussi en arrière, appelé switch.','Souple pour les butters (appuis sur les spatules) ; plus de soutien pour les sauts et les réceptions.','Plat : pivot facile. Cambre + double rocker : accroche et rebond (pop). Le cambre plat n’est pas obligatoire.'],question='Vous faites surtout des rails et des butters, ou des sauts avec des réceptions appuyées ?',speech='Le twin-tip facilite le ski en arrière. On choisit ensuite la souplesse et le profil selon les figures et les sauts.')]
    for c in cards:
        x=c['x'];p.accent=c['color'];p.soft=c['soft']
        p.rect((x,432,x+1100,2900),WHITE,c['color'],28,3)
        p.rect((x+2,434,x+1098,660),c['soft'],None,24)
        p.d.ellipse((x+30,470,x+102,542),fill=c['color']);p.text(x+66,483,str(c['n']).zfill(2),39,'serif',WHITE,center=True)
        p.text(x+130,477,c['title'],64,'serif',INK,width=935)
        p.text(x+34,580,c['sub'],36,width=1032)
        scene(p,c['photo'],(x+25,700,x+1075,1190))
        p.rect((x+30,1220,x+1070,1354),c['soft'],None,20)
        p.text(x+58,1250,c['waist'],59,'serif',INK)
        p.text(x+550,1244,'LARGEUR AU PATIN',27,'bold',c['color'])
        p.text(x+550,1290,c['waistnote'],34,'bold',INK)
        p.text(x+34,1380,c['length'],32,width=1032,leading=39,bottom=1470)
        y=1490
        for label,body in [('Comportement',c['behavior']),('Pour quel client ?',c['client'])]:
            y=p.label(x+34,y,label,1032,32)
            y=p.text(x+34,y,body,39,width=1032,leading=47)+26
        y=p.label(x+34,y,'Les points à expliquer',1032,32)
        y=p.bullets(x+34,y,c['points'],1032,37,14)
        assert y<2430,('family content',c['title'],y)
        p.rect((x+25,2440,x+1075,2620),c['soft'],None,18)
        p.text(x+48,2460,'LA QUESTION À POSER',28,'bold',c['color'])
        p.text(x+48,2510,c['question'],35,width=1000,leading=42,bottom=2610)
        p.rect((x+25,2650,x+1075,2875),DARK,None,18)
        p.text(x+48,2670,'À DIRE AU CLIENT',29,'bold',WHITE)
        p.text(x+48,2722,'« '+c['speech']+' »',36,'bold',WHITE,width=1000,leading=43,bottom=2863)
    p.remember('Freeride : de la portance. Freestyle : un programme de figures.','Un ski large n’est pas forcément un freeride ; un twin-tip n’est pas forcément souple. Pour le freestyle, le cambre plat est une option : on choisit surtout selon les rails, les sauts et le niveau.')
    p.footer('Repères indicatifs : les familles se chevauchent. Hors-piste : autonomie, connaissance du terrain et équipement adaptés.');return p

def packshot(p,c,box):
    im=Image.open(MEDIA/c['photo']).convert('RGBA')
    if im.getchannel('A').getextrema()[0]==0:bb=im.getchannel('A').getbbox()
    elif c['key']=='rossignol':
        mask=im.convert('L').point(lambda a:255 if a<180 else 0)
        bb=mask.getbbox()
        if bb:bb=(max(0,bb[0]-8),max(0,bb[1]-8),min(im.width,bb[2]+8),min(im.height,bb[3]+8))
    else:
        mask=ImageChops.difference(im.convert('RGB'),Image.new('RGB',im.size,'white')).convert('L').point(lambda a:255 if a>25 else 0)
        bb=mask.getbbox()
    if bb:im=im.crop(bb)
    ow,oh=im.size
    im=ImageOps.contain(im,(box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS)
    assert abs(im.width/im.height-ow/oh)<.008,c['name']
    p.im.paste(im,((box[0]+box[2]-im.width)//2,(box[1]+box[3]-im.height)//2),im)

def examples_page():
    p=Page(14);p.header('Exemples freeride & freestyle.','Six vrais modèles pour relier une construction, une sensation et un besoin client.','02  /  LES FAMILLES')
    for row,(family,label,color) in enumerate([('freeride','01  /  FREERIDE  —  TROIS CARACTÈRES EN NEIGE SOUPLE',TEAL),('freestyle','02  /  FREESTYLE  —  PRÉCISION, REBOND OU SOUPLESSE',PURPLE)]):
        y0=500+1250*row
        p.text(78,y0-64,label,34,'bold',color)
        for i,c in enumerate([v for v in PRODUCTS if v['family']==family]):
            x=70+i*768;cw=724;end=y0+1150;p.set_accent(i)
            p.rect((x,y0,x+cw,end),WHITE,p.accent,23,3)
            p.rect((x+2,y0+2,x+cw-2,y0+124),p.soft,None,21)
            p.text(x+26,y0+17,c['brand'],25,'bold',p.accent)
            p.text(x+26,y0+57,c['name'],47,'serif',INK,width=670)
            packshot(p,c,(x+22,y0+150,x+175,y0+552))
            tx=x+202;tw=494
            for yy,title,body,limit in [(144,'Positionnement',c['position'],324),(332,'Ce que le fabricant met en avant',c['maker'],564)]:
                p.text(tx,y0+yy,title,24,'bold',p.accent,width=tw,leading=29)
                p.text(tx,y0+yy+41,body,29,width=tw,leading=34,bottom=y0+limit)
            p.rect((x+24,y0+582,x+700,y0+670),p.soft,None,15)
            p.text(x+45,y0+601,c['waist'],49,'serif',INK)
            p.text(x+320,y0+596,'AU PATIN  /  '+c['ref'],26,'bold',p.accent)
            p.text(x+320,y0+634,c['tag'],25,'bold',INK,width=357)
            p.text(x+28,y0+687,'Vocabulaire utile',27,'bold',p.accent)
            p.text(x+28,y0+728,c['vocab'],29,'bold',INK,width=668,leading=34,bottom=y0+810)
            p.text(x+28,y0+790,'Fiche technique',27,'bold',p.accent)
            yy=y0+832
            for j,(label,value) in enumerate(c['specs']):
                h=35
                if j%2==0:p.d.rectangle((x+25,yy-4,x+700,yy+h-4),fill=common.P['lignes_tableau'])
                p.text(x+33,yy,label,26,'bold',p.accent,width=165)
                actual=p.text(x+210,yy,value,27,width=482,leading=31,bottom=yy+34)
                yy+=h
            sy=y0+984
            p.rect((x+20,sy,x+704,end-17),DARK,None,15)
            p.text(x+37,sy+11,'À DIRE AU CLIENT',24,'bold',WHITE)
            p.text(x+37,sy+44,'« '+c['speech']+' »',28,'bold',WHITE,width=650,leading=32,bottom=end-25)
    p.remember('Même largeur, caractères différents : faire parler le programme.','Identifier d’abord le terrain et le style. Relier ensuite les technologies à un bénéfice concret : portance, pivot, amorti, rebond ou souplesse. Les six modèles sont des exemples, pas un classement.')
    p.footer('Photos et données : fabricants cités. * Cotes et rayon à la longueur indiquée. Positionnement et vocabulaire : repères de conseil.');return p

if __name__=='__main__':
    records=json.loads((HERE/'approved-pages-v754.json').read_text())
    # Link the existing chapter opener to the new family page, without renumbering.
    p=common.families();records[7]=p.save()
    for build in [family_page,examples_page]:
        p=build();records.append(p.save());print('Page',p.n,'OK',flush=True)
    (ROOT/'sources/guide/.cache/manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
    (HERE/'manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
