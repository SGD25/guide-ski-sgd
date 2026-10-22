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
common.OUT=ROOT/'assets/guide-v756';common.OUT.mkdir(exist_ok=True)
MEDIA=HERE/'media'
PURPLE='#75638F'
PRODUCTS=json.loads((HERE/'products.json').read_text())

def scene(p,name,box):
    im=Image.open(MEDIA/name).convert('RGB')
    im=ImageOps.fit(im,(box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS,centering=(.5,.06 if 'freestyle' in name else .43))
    p.im.paste(im,box[:2])

def family_page():
    p=Page(13);p.header('Freeride & freestyle.','Deux familles, deux intentions : flotter en neige profonde ou jouer avec les figures.','02  /  LES FAMILLES')
    cards=[dict(x=70,n=3,color=TEAL,soft='#EDF5F6',title='Les skis freeride',sub='Priorité à la neige non damée et à la poudreuse.',photo='freeride-deep-v756.jpg',waist='> 105 mm',waistnote='Repère poudreuse',length='Longueur : souvent autour de la taille à +10 / +15 cm ; à ajuster au modèle et au gabarit.',behavior='Le ski s’enfonce moins et pivote plus facilement en neige profonde. Sur piste dure, il est moins vif d’une carre à l’autre et souvent plus physique.',client='Un skieur déjà à l’aise, qui sort réellement des pistes et cherche davantage de portance.',points=['La largeur aide à rester en surface : elle ne remplace pas la technique du skieur.','Le rocker relève l’avant plus tôt et facilite la mise en surface ; le talon relevé aide au pivot.','Le flex et la longueur règlent le soutien : plus joueur pour pivoter, plus ferme pour engager.'],question='Vous cherchez surtout la poudreuse, ou un ski pour sortir des pistes dans des neiges variées ?',speech='Ce ski porte davantage en neige profonde et pivote facilement. En échange, il est moins vif sur piste dure.'),
    dict(x=1230,n=4,color=PURPLE,soft='#F2EFF7',title='Les skis freestyle',sub='Priorité au park, aux sauts et à la créativité.',photo='freestyle-scene.jpg',waist='≈ 80–100 mm',waistnote='Repère park / jeu',length='Longueur : de −10 cm à la taille du skieur, selon le programme.',behavior='Twin-tip pour skier en arrière (switch). Plat : pivot facile ; cambre + double rocker : accroche et rebond (pop).',client='Pour les amateurs de figures. Un flex souple aide au jib ; plus de soutien convient aux gros sauts.',points=['Twin-tip : spatule et talon relevés pour skier aussi en arrière, appelé switch.','Souple pour les butters (appuis sur les spatules) ; plus de soutien pour les sauts et les réceptions.','Plat : pivot facile. Cambre + double rocker : accroche et rebond (pop). Le cambre plat n’est pas obligatoire.'],question='Vous faites surtout du jib, du freestyle polyvalent, ou du big air / half-pipe ?',speech='On adapte la longueur à vos figures : plus court pour pivoter, plus long pour garder de la stabilité à vitesse élevée et à la réception.')]
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
        y=1440 if c['n']==4 else 1490
        for label,body in [('Comportement',c['behavior']),('Pour quel client ?',c['client'])]:
            y=p.label(x+34,y,label,1032,32)
            y=p.text(x+34,y,body,39,width=1032,leading=47)+26
        if c['n']==3:
            y=p.label(x+34,y,'Les points à expliquer',1032,32)
            y=p.bullets(x+34,y,c['points'],1032,37,14)
        else:
            y=p.label(x+34,y,'Longueur : trois usages, trois repères',1032,32)
            lengths=[('−10 cm','Park / rails / jib','Plus court et léger aux pieds : moins d’inertie, donc pivot et rotations plus faciles.'),('−5 cm','Freestyle polyvalent','Maniabilité pour les figures, avec assez de longueur pour rester stable sur piste et en neige un peu plus profonde.'),('À la taille','Big air / half-pipe','Plus d’appui à haute vitesse et sur les gros sauts : réceptions stables et meilleur équilibre avant / arrière.')]
            for delta,title,body in lengths:
                # Measure the row before drawing its integrated background.
                words=body.split();lines=1;line=''
                for word in words:
                    trial=(line+' '+word).strip()
                    if p.d.textlength(trial,font=ft(32))>790 and line:lines+=1;line=word
                    else:line=trial
                height=51+lines*37+18
                p.rect((x+25,y-6,x+1075,y+height-16),c['soft'],None,16)
                p.text(x+45,y+18,delta,46,'serif',c['color'],width=220)
                p.text(x+275,y+4,title,36,'bold',INK,width=790)
                end=p.text(x+275,y+51,body,32,width=790,leading=37,bottom=y+height-12)
                y=end+18
        question_y=2470 if c['n']==4 else 2440
        assert y<question_y-12,('family content',c['title'],y)
        question_end=2635 if c['n']==4 else 2620
        p.rect((x+25,question_y,x+1075,question_end),c['soft'],None,18)
        p.text(x+48,question_y+20,'LA QUESTION À POSER',28,'bold',c['color'])
        p.text(x+48,question_y+70,c['question'],35,width=1000,leading=42,bottom=question_end-8)
        speech_y=2660 if c['n']==4 else 2650
        speech_end=2885 if c['n']==4 else 2875
        p.rect((x+25,speech_y,x+1075,speech_end),DARK,None,18)
        p.text(x+48,speech_y+20,'À DIRE AU CLIENT',29,'bold',WHITE)
        p.text(x+48,speech_y+72,'« '+c['speech']+' »',36,'bold',WHITE,width=1000,leading=43,bottom=speech_end-12)
    p.remember('Freeride : portance. Freestyle : longueur adaptée au programme.','En freestyle : jib ≈ −10 cm ; polyvalent ≈ −5 cm ; big air / half-pipe ≈ taille du skieur. Ajuster au gabarit, au niveau, au flex et au modèle. Le cambre plat reste une option.')
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
    records=json.loads((HERE/'manifest.json').read_text())
    assert len(records)==14
    for build in [family_page,examples_page]:
        p=build();records[p.n-1]=p.save();print('Page',p.n,'OK',flush=True)
    (ROOT/'sources/guide/.cache/manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
    (HERE/'manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
