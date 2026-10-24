"""Finalisation: keep approved raster pages; update selected native layouts and page order."""
from pathlib import Path
import json,sys,importlib.util
from PIL import Image,ImageDraw,ImageOps
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'sources/guide'))
import render as base
from render import Page,INK,BODY,TEAL,CORAL,BLUE,WHITE,LINE,DARK,PALE,W,H,ft,MEDIA,arrow

def module(key,path):
    spec=importlib.util.spec_from_file_location(key,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
boots=module('boots_final',ROOT/'sources/boots/render.py')
nordic=module('nordic_final',ROOT/'sources/nordic/render.py')
juniors=module('juniors_final',ROOT/'sources/juniors/render.py')
rando=module('rando_final',ROOT/'sources/rando/render.py')
snow=module('snow_final',ROOT/'sources/snowboard/render.py')
base.OUT=ROOT/'assets/guide-v767';base.OUT.mkdir(exist_ok=True)
CATALOG=json.loads((ROOT/'sources/guide/catalog.json').read_text())['pages']

def scene(p,name,box,center=(.5,.5)):
    path=MEDIA/name
    if not path.exists():path=MEDIA/(name+'.jpg')
    im=Image.open(path).convert('RGB');im=ImageOps.fit(im,(box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS,centering=center);p.im.paste(im,box[:2])

def cover():
    p=Page(1);p.photo_cover('couverture-v753.png',(0,0,W,H))
    veil=Image.new('RGBA',(W,H),(255,255,255,0));vd=ImageDraw.Draw(veil)
    for y in range(1670):
        a=245 if y<520 else round(245*max(0,1-(y-520)/1150));vd.line((0,y,W,y),fill=(250,252,253,a))
    for y in range(2700,H):vd.line((0,y,W,y),fill=(250,252,253,round(220*(y-2700)/(H-2700))))
    p.im=Image.alpha_composite(p.im.convert('RGBA'),veil).convert('RGB');p.d=ImageDraw.Draw(p.im)
    p.text(100,95,'SPORT GOOD DEAL',48,'bold',INK);p.photo('sgd-logo.png',(2080,65,2300,210))
    p.text(100,190,'LE GUIDE DE FORMATION SKI',35,'bold',TEAL);p.line((100,282,2300,282),LINE,3)
    p.text(96,405,'Le guide',248,'serif',INK);p.text(96,710,'du ski.',294,'italic',CORAL)
    p.text(105,1095,'Former les vendeurs et les loueurs.\nDu premier conseil à la remise du matériel.',56,'sans',INK,width=2100,leading=78)
    cards=[('Comprendre','Le matériel, les formes\net les dimensions.',3),('Reconnaître','Les familles, les terrains\net les pratiques.',8),('Conseiller','Les modèles, les tailles\net le bon discours.',9),('Sécuriser','Les compatibilités,\nles contrôles et le départ.',25)]
    for i,(title,body,n) in enumerate(cards):
        x=70+i*575;p.set_accent(i);p.rect((x,2785,x+535,3150),WHITE,p.accent,24,3)
        p.text(x+26,2815,f'PAGE {n:02}  →',29,'bold',p.accent)
        p.text(x+26,2885,title,51,'serif',INK,width=485)
        p.text(x+26,2975,body,33,width=485,leading=43,bottom=3135)
        p.link((x,2785,x+535,3150),n,title)
    p.line((70,3240,2330,3240),INK,2)
    p.text(76,3280,'COMPRENDRE  /  RECONNAÎTRE  /  CONSEILLER  /  SÉCURISER',31,'bold',INK)
    p.text(2325,3280,'01',31,'bold',INK,center=True)
    return p

def contents():
    p=Page(2);p.header('Tout le guide.','28 pages pour comprendre, reconnaître, conseiller et sécuriser.','01  /  COMPRENDRE')
    # Custom title retains the typography of the approved opening pages.
    p.d.rectangle((70,120,2330,307),fill=base.P['fond'])
    p.text(76,135,'Tout le guide,',148,'serif',INK)
    p.text(1060,145,'en un coup d’œil.',122,'italic',CORAL)
    desc={3:'Les trois zones et les largeurs du ski.',4:'Relier les dimensions aux sensations.',5:'Petits virages ou grandes courbes.',6:'Lire le profil et les zones de rocker.',7:'Comprendre le noyau et les renforts.',8:'Choisir une famille selon le terrain.',9:'Quatre approches de la piste.',10:'Des modèles et des mots pour conseiller.',11:'Accroche, portance et polyvalence.',12:'Trois skis, trois compromis.',13:'Poudreuse, park et figures.',14:'Six exemples freeride / freestyle.',15:'Niveaux, tailles et fixations enfants.',16:'Des exemples juniors Rossignol.',17:'Comprendre le pack de randonnée.',18:'Montée ou freerando : comparer.',19:'Pointure, volume, flex et essayage.',20:'Monter confortablement, skier maintenu.',21:'Programmes, profils et fixations.',22:'Quatre exemples de snowboards Nitro.',23:'Classique, skating, tailles et équipement.',24:'Des exemples Fischer et Rossignol.',25:'Données client, compatibilités et ISOSKI.',26:'Contrôles, réglage et traçabilité.',27:'DVA, pelle, sonde et contrôles du groupe.',28:'Recherche, sauvetage et sac airbag.'}
    labels={3:'Anatomie & lignes de cotes',4:'Largeur & longueur',5:'Rayon de courbure',6:'Cambres & rockers',7:'Construction & noyaux',8:'Les familles de skis',9:'Skis de piste',10:'Exemples piste',11:'Skis all-mountain',12:'Exemples all-mountain',13:'Freeride & freestyle',14:'Exemples freeride & freestyle',15:'Skis juniors',16:'Exemples juniors',17:'Skis de randonnée',18:'Exemples rando',19:'Chaussures alpines',20:'Chaussures de randonnée',21:'Choisir son snowboard',22:'Exemples Nitro',23:'Ski de fond : classique & skating',24:'Exemples de ski de fond',25:'Fixations : comprendre le réglage',26:'Fixations : contrôler avant de louer',27:'Avalanche : s’équiper & contrôler',28:'Avalanche : rechercher & secourir'}
    groups=[(70,440,1170,1310,0,'01 / Comprendre','Les repères du matériel',list(range(3,8)),125),(70,1340,1170,2845,1,'02 / Reconnaître & conseiller','Les familles de skis',list(range(8,17)),141),(1230,440,2330,1735,1,'02 / Reconnaître & conseiller','Rando, chaussures, snow & fond',list(range(17,25)),135),(1230,1765,2330,2845,3,'03 / Sécuriser','Avant de confier le matériel',list(range(25,29)),215)]
    for x,y,x2,y2,accent,title,subtitle,nums,rh in groups:
        p.set_accent(accent);p.rect((x,y,x2,y2),WHITE,p.accent,25,3);p.rect((x+3,y+3,x2-3,y+174),p.soft,None,23)
        p.text(x+30,y+28,title,43,'serif',INK,width=1040)
        p.text(x+30,y+106,subtitle,31,'bold',p.accent,width=1040)
        for i,n in enumerate(nums):
            yy=y+215+i*rh
            if i:p.line((x+28,yy-24,x2-28,yy-24),LINE,2)
            p.text(x+30,yy,labels[n],39,'bold',INK,width=865,leading=46,bottom=yy+54)
            p.text(x+30,yy+61,desc[n],30,width=855,leading=35,bottom=min(yy+rh-8,y2-20))
            p.rect((x2-173,yy-2,x2-26,yy+76),p.soft,None,22)
            p.text(x2-100,yy+18,f'{n:02} →',34,'bold',p.accent,center=True)
            p.link((x+20,yy-12,x2-20,min(yy+rh-12,y2-12)),n,labels[n])
    scene(p,'piste-station-v752.png',(70,2890,794,3175),(.5,.56))
    p.rect((838,2890,2330,3175),DARK,None,24)
    p.text(875,2918,'Le bon parcours au comptoir.',52,'serif',WHITE,width=1410)
    p.text(875,3000,'Terrain → niveau → gabarit → matériel compatible → contrôles.',38,'sans',WHITE,width=1400,leading=46,bottom=3110)
    p.text(875,3120,'Chaque ligne du sommaire est cliquable.',31,'bold',WHITE)
    p.footer();return p

def anatomy():
    p=base.anatomy();p.d.rectangle((1430,2310,2360,2910),fill=base.P['fond'])
    p.rect((1430,2330,2330,2560),WHITE,BLUE,21,3)
    p.text(1460,2352,'Lire les lignes de cotes',43,'serif',INK,width=840)
    p.text(1460,2423,'118 – 95 – 108 mm',51,'bold',BLUE)
    p.text(1460,2500,'Exemple : largeurs spatule – patin – talon.',33,width=840)
    p.text(1468,2600,'REPÈRES AU PATIN',30,'bold',TEAL)
    p.text(1468,2660,'65–80 mm : piste\n80–95 mm : all-mountain\n95–136 mm : freeride',35,width=810,leading=52)
    p.text(1468,2835,'Repères indicatifs : les familles se chevauchent.',28,width=810)
    return p

def waist(p,i,x):
    names=['patin-head-70-v754.png','patin-elan-88-v754.png','patin-rossignol-102-v754.png'];mm=[70,88,102][i]
    im=Image.open(MEDIA/names[i]).convert('RGBA')
    if i==0:
        alpha=Image.open(HERE/'media/patin-head-alpha-v767.png').convert('L');im.putalpha(alpha)
    w=round(mm*2.55);left=round((350-w)/2)
    im=im.crop((left,50,left+w,390));factor=3/2.55
    im=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.LANCZOS)
    p.rect((x+18,755,x+362,1185),'#DDE9ED',None,14)
    p.im.paste(im,(x+190-im.width//2,770),im)
    arrow(p,x+190-mm*3/2,1230,x+190+mm*3/2,1230,p.accent,4,True)
    p.text(x+190,1270,f'{mm} mm',42,'bold',p.accent,center=True)

def dimensions():
    p=Page(4);p.header('Largeur et longueur.','Deux dimensions qui se combinent : vivacité, facilité, stabilité et portance.')
    p.text(76,440,'01  La largeur au patin',65,'serif',INK)
    cols=[(70,'Fin','65–80 mm','HEAD Easy Joy',['Passage de carre rapide','Moins de portance','Souvent plus facile sur piste']),(838,'Intermédiaire','80–95 mm','Elan Ripstick 88',['Un ski plus polyvalent','Compromis piste / hors-piste','Un comportement équilibré']),(1606,'Large','96 mm et +','Rossignol Sender Soul 102',['Plus de portance en neige souple','Moins vif sur neige dure','Souvent plus physique sur piste'])]
    for i,(x,title,range_,model,points) in enumerate(cols):
        p.set_accent(i);p.rect((x,560,x+724,1410));p.rect((x+2,562,x+722,725),p.soft,None,20)
        p.text(x+32,585,title,61,'serif',INK);p.text(x+32,665,range_,45,'bold',p.accent)
        waist(p,i,x);p.bullets(x+390,790,points,300,35,23)
        p.text(x+362,1352,model,28,'bold',INK,center=True)
    p.accent=TEAL;p.soft=PALE;p.rect((70,1450,2330,1575),PALE,None,28)
    p.text(110,1480,'Plus large ne veut pas dire meilleur : choisir le patin selon le terrain, le niveau et les sensations.',39,width=2150)
    p.text(76,1645,'02  La longueur par rapport au skieur',65,'serif',INK)
    for i,(x,title,delta,sh,name,desc) in enumerate([(70,'Piste facile','−20 à −10 cm',580,'ski-fin-detoure-v754.png','Accessible et rassurant'),(838,'Polyvalent','−10 à −5 cm',622,'ski-intermediaire-detoure-v754.png','Maniabilité et tenue'),(1606,'Freeride','0 à +15 cm',678,'ski-large-detoure-v754.png','Portance et stabilité')]):
        p.set_accent(i);p.rect((x,1760,x+724,2830));p.rect((x+2,1762,x+722,1945),p.soft,None,20)
        p.text(x+362,1790,title,59,'serif',INK,center=True);p.text(x+362,1880,delta,49,'bold',p.accent,center=True)
        ground=2660;top=ground-650
        person=Image.open(MEDIA/'skieur-illustration-v752.png').convert('RGBA');person=person.crop(person.getchannel('A').getbbox());person=ImageOps.contain(person,(435,650),Image.Resampling.LANCZOS)
        p.im.paste(person,(x+65,ground-person.height),person)
        ski=Image.open(MEDIA/name).convert('RGBA');ski=ski.crop(ski.getchannel('A').getbbox());ski=ImageOps.contain(ski,(100,sh),Image.Resampling.LANCZOS)
        axis=x+457;p.im.paste(ski,(axis-ski.width//2,ground-ski.height),ski)
        p.line((x+120,ground,x+600,ground),LINE,3)
        p.line((x+160,top,x+668,top),LINE,3);p.line((axis+45,ground-ski.height,x+672,ground-ski.height),p.accent,3)
        arrow(p,x+650,top,x+650,ground-ski.height,p.accent,4,True)
        p.text(x+362,2730,desc,38,'bold',p.accent,width=660,center=True)
    p.remember('La largeur et la longueur se choisissent ensemble.','Court et fin : plus vif et accessible. Long et large : plus de stabilité et de portance. Ajuster ces repères au modèle, au niveau, au gabarit et au terrain.')
    p.footer('Gros plans de vrais patins à une même échelle. Skis verticaux, proportions conservées et bases alignées. Longueurs indicatives, à adapter au programme.')
    return p

def radius():
    p=base.radius();p.rect((70,2430,794,2865),WHITE,LINE,22,3)
    p.text(100,2460,'Le skieur agit aussi',43,'serif',INK,width=664)
    p.text(100,2545,'Vitesse, prise de carre et pression modifient la trajectoire. Avec un même ski, on peut fermer ou ouvrir davantage le virage.',37,width=664,leading=45,bottom=2808)
    p.text(100,2815,'Le rayon ne fait pas tout.',31,'bold',TEAL,width=664)
    return p

def families():
    p=base.families()
    for x,n,page in [(70,3,13),(838,4,13),(1606,5,17)]:
        color=base.ACCENTS[(n-1)%4];p.rect((x,2240,x+724,2870),None,color,26,4)
        p.rect((x+26,2760,x+698,2840),DARK,None,16)
        p.text(x+52,2782,f'Découvrir / page {page:02} →',33,'bold',WHITE)
    return p

PISTE=[
 dict(title='Piste facile',photo='debutante-piste-v752.png',specs=[('Patin','≈ 70–75 mm'),('Longueur','≈ −20 à −15 cm'),('Rayon','Court, selon le modèle')],behavior='Le ski tourne facilement à vitesse modérée et pardonne les petites erreurs d’appui.',client='Débutant, skieur qui appréhende ou qui cherche surtout une conduite facile.',points='Tolérance, faible effort et maniabilité. Le but : apprendre et prendre confiance.',question='Vous enchaînez déjà les virages, ou vous cherchez surtout à vous rassurer ?',speech='Un ski facile à faire tourner, pour progresser sans vous fatiguer.'),
 dict(title='Piste polyvalent',photo='allmountain-bord-piste-v753.png',specs=[('Patin','≈ 75–85 mm'),('Longueur','≈ −10 cm'),('Rayon','Court à moyen, variable')],behavior='Un équilibre entre facilité, tenue de courbe et stabilité pour varier les virages sur piste.',client='Skieur loisir déjà à l’aise, qui veut une paire pour skier toute la journée.',points='Plus de soutien qu’un ski facile, sans viser la puissance d’un ski performance.',question='Vous voulez varier les virages sur piste, sans trop vous fatiguer ?',speech='Un compromis pour varier les virages sur piste, avec du maintien et de la facilité.'),
 dict(title='Piste performance',photo='piste-performance-v753.png',specs=[('Patin','Souvent ≈ 70–80 mm'),('Longueur','≈ −10 à −5 cm'),('Rayon','Selon les courbes visées')],behavior='Plus d’accroche, de réponse et de soutien quand les appuis et la vitesse augmentent.',client='Bon skieur, sportif, qui maîtrise ses appuis et cherche à carver avec précision.',points='Construction plus tonique : elle demande de l’engagement et peut fatiguer davantage.',question='Vous skiez déjà sur la carre et recherchez plus de tenue dans les virages ?',speech='Plus de précision et de répondant, à condition d’avoir les appuis pour l’exploiter.'),
 dict(title='Spécialités piste',photo='piste-specialiste.jpg',specs=[('Slalom','Court, souvent < 170 cm'),('Patin SL','≈ 65–68 mm'),('Géant','Plus long, souvent à la taille')],behavior='Slalom : virages courts et très vifs. Géant : courbes plus longues, stabilité et vitesse.',client='Skieur technique à expert, avec un objectif précis de virages ou d’entraînement.',points='Choisir SL ou GS selon les courbes. Un ski spécialisé n’est pas forcément un ski de course FIS.',question='Vous cherchez des virages très courts, ou plutôt de grandes courbes engagées ?',speech='On choisit la spécialité selon vos courbes : vif en slalom, plus posé en géant.')]

def piste():
    p=Page(9);p.header('Les skis de piste.','Quatre approches : comportement, profil client et questions pour bien orienter.','02  /  LES FAMILLES')
    for i,c in enumerate(PISTE):
        x=70+(i%2)*1160;y=432+(i//2)*1250;p.set_accent(i)
        p.rect((x,y,x+1100,y+1210),WHITE,p.accent,25,3);p.rect((x+3,y+3,x+1097,y+124),p.soft,None,23)
        p.number(x+25,y+24,i+1);p.text(x+121,y+33,c['title'],55,'serif',INK)
        scene(p,c['photo'],(x+25,y+150,x+445,y+464),(.5,.5))
        for j,(label,value) in enumerate(c['specs']):
            yy=y+157+j*99;p.text(x+475,yy,label,29,'bold',p.accent)
            p.text(x+475,yy+43,value,34,width=590,leading=40,bottom=yy+92)
        for yy,label,body in [(y+500,'Comportement',c['behavior']),(y+655,'Pour quel client ?',c['client']),(y+795,'Les points à expliquer',c['points'])]:
            p.text(x+30,yy,label,31,'bold',p.accent)
            p.text(x+30,yy+47,body,34,width=1040,leading=40,bottom=yy+139)
        p.rect((x+22,y+940,x+1078,y+1060),p.soft,None,15)
        p.text(x+42,y+952,'LA QUESTION À POSER',24,'bold',p.accent)
        p.text(x+42,y+990,c['question'],29,width=1010,leading=33,bottom=y+1058)
        p.rect((x+22,y+1078,x+1078,y+1192),DARK,None,15)
        p.text(x+42,y+1089,'À DIRE AU CLIENT',24,'bold',WHITE)
        p.text(x+42,y+1124,'« '+c['speech']+' »',29,'bold',WHITE,width=1010,leading=32,bottom=y+1190)
    p.remember('Le bon ski dépend du niveau réel et des sensations recherchées.','Facile, polyvalent, performance ou spécialisé : relier le comportement du ski au besoin du client. Une largeur ou un prix ne suffit pas à classer un modèle.')
    p.footer('Repères de longueur par rapport à la taille du skieur, à adapter au modèle et au gabarit. SL = slalom ; GS = géant. Rayon et patin sont indicatifs. Exemples en page 10.')
    return p

def products():
    p=base.products()
    p.d.rectangle((70,3230,2000,3320),fill=base.P['fond'])
    p.text(76,3237,'Forza 40 CA Xpress : Rossignol RAPPX05, intermédiaire. Forza 70 TI Konect : RAOPR02, avancé / expert. Caractéristiques de ces références ; vérifier le millésime et la longueur.',26,width=1890,bottom=3313)
    return p

if __name__=='__main__':
    builders=[cover,contents,anatomy,dimensions,radius,families,piste,products,juniors.advice_page,rando.intro_page,boots.alpine,boots.touring,snow.intro_page,nordic.intro_page,nordic.examples_page]
    base.write_manifest_pages(build() for build in builders)
