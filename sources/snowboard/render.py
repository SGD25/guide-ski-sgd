"""Snowboard training spread, native exact diagrams and genuine manufacturer photos."""
from pathlib import Path
import json,sys,math
from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'sources/guide'))
import render as common
from render import Page,INK,BODY,TEAL,CORAL,BLUE,WHITE,LINE,DARK
common.OUT=ROOT/'assets/guide-v763';common.OUT.mkdir(exist_ok=True)
MANIFEST=ROOT/'sources/freeride-freestyle/manifest.json'
PRODUCTS=json.loads((HERE/'products.json').read_text())
PURPLE='#75638F'

def product_photo(p,name,box):
    im=Image.open(HERE/'media'/name).convert('RGBA')
    if im.getchannel('A').getextrema()[0]==0:
        bb=im.getchannel('A').getbbox()
    else:
        bb=im.convert('L').point(lambda v:255 if v<220 else 0).getbbox()
    if bb:
        pad=12
        im=im.crop((max(0,bb[0]-pad),max(0,bb[1]-pad),min(im.width,bb[2]+pad),min(im.height,bb[3]+pad)))
    ratio=im.width/im.height
    im=ImageOps.contain(im,(box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS)
    assert abs(im.width/im.height-ratio)<.025
    p.im.paste(im,((box[0]+box[2]-im.width)//2,(box[1]+box[3]-im.height)//2),im)

def scene(p,box):
    im=Image.open(HERE/'media/scene.jpg').convert('RGB')
    im=ImageOps.fit(im,(box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS,centering=(.5,.18))
    p.im.paste(im,box[:2])

def curve(p,x,y,w,kind,color):
    # Schematics show unloaded board profiles from the side, never product silhouettes.
    shapes={
      'camber':[(0,-35),(.13,0),(.5,-30),(.87,0),(1,-35)],
      'flat':[(0,-35),(.13,0),(.5,0),(.87,0),(1,-35)],
      'rocker':[(0,-45),(.25,-13),(.5,0),(.75,-13),(1,-45)],
      'hybrid':[(0,-37),(.12,-2),(.3,-22),(.5,0),(.7,-22),(.88,-2),(1,-37)]}
    points=shapes[kind];smooth=[]
    for k in range(len(points)-1):
        p0=points[max(0,k-1)];p1=points[k];p2=points[k+1];p3=points[min(len(points)-1,k+2)]
        for j in range(25):
            t=j/25
            vals=[.5*((2*p1[d])+(-p0[d]+p2[d])*t+(2*p0[d]-5*p1[d]+4*p2[d]-p3[d])*t*t+(-p0[d]+3*p1[d]-3*p2[d]+p3[d])*t*t*t) for d in [0,1]]
            smooth.append((x+vals[0]*w,y+vals[1]))
    smooth.append((x+w,y+points[-1][1]))
    p.line((x-5,y+11,x+w+5,y+11),LINE,3)
    p.d.line(smooth,fill=color,width=8,joint='curve')
    for xx in [.3,.7]:
        p.d.rounded_rectangle((x+xx*w-16,y-64,x+xx*w+16,y-48),radius=4,fill=INK)

def intro_page():
    p=Page(21);p.header('Choisir son snowboard.','Du premier virage au park : choisir la planche, les boots et les fixations ensemble.','02  /  LES FAMILLES')
    p.rect((70,440,2330,730),DARK,None,24)
    scene(p,(995,440,2330,730))
    p.text(105,470,'La question à poser',34,'bold',WHITE)
    p.text(105,529,'« Vous ridez où, et que savez-vous déjà faire ? »',47,'serif',WHITE,width=840,leading=56,bottom=710)
    families=[
      ('Débutant','Piste, premiers virages.','Flex souple à moyen et profil tolérant : tourner sans forcer, gagner confiance.',BLUE,'#ECF3F9'),
      ('All-mountain','Piste + bords de piste.','Compromis maniabilité / stabilité. Un flex moyen, ou plus tonique selon le niveau.',TEAL,'#EDF5F6'),
      ('Freeride','Poudreuse et terrain varié.','Shape directionnel, portance et soutien. Du nose pour flotter ; plus exigeant selon le modèle.',CORAL,'#FCF0E9'),
      ('Freestyle','Park, sauts et switch.','Twin symétrique pour le switch (autre pied devant). Jib / rails : souple ; sauts : plus de soutien.',PURPLE,'#F2EFF7')]
    for i,(name,terrain,body,c,soft) in enumerate(families):
        x=70+i*575;p.accent,p.soft=c,soft
        p.rect((x,755,x+535,1135),WHITE,c,22,3)
        p.rect((x+3,758,x+532,835),soft,None,20)
        p.text(x+24,777,name,43,'serif',INK)
        p.text(x+24,862,terrain,31,'bold',c,width=487,leading=37,bottom=945)
        p.text(x+24,954,body,33,width=487,leading=39,bottom=1120)
    p.accent=TEAL
    p.text(76,1165,'Lire le cambre, sans confondre profil et souplesse.',49,'serif',INK)
    profiles=[('Classique','camber','Accroche, précision et pop. Demande des appuis plus propres.',BLUE),('Plat','flat','Appui stable, compromis entre facilité et tenue.',TEAL),('Inversé / rocker','rocker','Pivot et portance facilités ; moins de tenue qu’un cambre à construction comparable.',CORAL),('Hybride','hybrid','Mélange cambre / rocker. Ex. Gullwing : rocker central, cambre sous les pieds.',PURPLE)]
    for i,(name,kind,body,c) in enumerate(profiles):
        x=70+i*575;p.rect((x,1240,x+535,1540),WHITE,LINE,18,2)
        p.text(x+23,1260,name,37,'bold',c,width=490)
        curve(p,x+35,1390,465,kind,c)
        p.text(x+23,1420,body,30,width=490,leading=35,bottom=1530)
    p.text(80,1548,'Schémas à vide ; marqueurs = pieds. Cam-Out Nitro : cambre, extrémités relevées plus tôt.',27,width=2230)
    p.rect((70,1600,2330,2095),WHITE,TEAL,24,3)
    p.text(100,1622,'La taille : poids d’abord, hauteur ensuite.',51,'serif',INK)
    p.text(100,1698,'1 / Poids + niveau',34,'bold',BLUE)
    p.text(100,1750,'Lire la plage de poids du modèle. Trop grand / rigide : difficile à déformer ; trop court / souple : moins de soutien.',33,width=670,leading=39,bottom=1910)
    p.text(855,1698,'2 / Longueur + pratique',34,'bold',TEAL)
    p.text(855,1750,'Debout, menton–nez : repère adulte. Parmi les tailles adaptées : plus court pour débuter / jib, plus long pour vitesse / poudreuse.',33,width=680,leading=39,bottom=1910)
    p.text(1610,1698,'3 / Pointure + largeur',34,'bold',CORAL)
    p.text(1610,1750,'Centrer la vraie boot dans la fixation. Un dépassement excessif fait toucher la neige en virage. Wide si nécessaire, pas automatiquement.',33,width=680,leading=39,bottom=1910)
    p.rect((92,1920,2308,2075),'#EDF5F6',None,16)
    p.text(115,1941,'À pratique comparable : park ≈ 2–4 cm plus court ; freeride ≈ 2–4 cm plus long que son choix polyvalent.',33,'bold',TEAL,width=2155,leading=39,bottom=2020)
    p.text(115,2024,'Toujours dans le barème fabricant. Sauts rapides : garder du soutien. Shapes courts et larges : suivre leur taille dédiée.',30,width=2155,leading=35,bottom=2065)
    p.text(76,2125,'Trois façons de chausser.',51,'serif',INK)
    fixes=[
      ('Coque à sangles','rambler.jpg','Embase + spoiler + sangles cheville / avant-pied. Boots classiques ; taille de coque adaptée à la boot. Vérifier aussi disque / inserts.','Nitro Rambler',BLUE),
      ('Entrée arrière','flow.jpg','Le spoiler bascule pour glisser le pied par l’arrière. Boots classiques compatibles ; fermer et vérifier le verrouillage.','Nidecker Flow Fenix',TEAL),
      ('Step-in / Step On®','step-on.jpg','Ex. Step On : la boot se clipse, sans sangles. Boots Step On dédiées et tailles compatibles. Non proposé chez SGD.','Nitro Step On',CORAL)]
    for i,(name,img,body,label,c) in enumerate(fixes):
        x=70+i*770;p.rect((x,2200,x+720,2565),WHITE,c,21,3)
        p.text(x+20,2222,name,39,'serif',INK,width=680)
        product_photo(p,img,(x+18,2295,x+236,2485))
        p.text(x+262,2296,body,31,width=430,leading=36,bottom=2551)
        p.text(x+130,2515,label,23,'bold',INK,center=True)
    p.rect((70,2595,2330,2910),'#FCF0E9',None,22)
    p.text(100,2618,'En vente comme en location : préparer un ensemble cohérent.',45,'serif',INK)
    p.text(100,2687,'Regular = pied gauche devant ; goofy = pied droit. Demander le pied habituel, régler écartement et angles selon le pratiquant, en partant des repères fabricant.',32,width=1070,leading=38,bottom=2807)
    p.text(1250,2687,'Boots : talon maintenu, orteils sans douleur en flexion. Contrôler semelle, carres, inserts / vis, sangles et cliquets ; montrer le chaussage et le déchaussage.',32,width=1040,leading=38,bottom=2807)
    p.text(100,2832,'Fixations de snow : pas de déclenchement automatique comme au ski. Vérifier le montage, le leash selon notice et les consignes de prise en main.',30,'bold',CORAL,width=2180,leading=36,bottom=2905)
    p.remember('Poids + pointure + pratique : le bon trio pour choisir.', 'Une planche, une paire de boots et des fixations qui fonctionnent ensemble. Le repère menton–nez aide à visualiser ; le barème de poids du modèle décide.')
    p.footer('Repères adultes indicatifs, hors planches de carving alpin et splitboards. Hors-piste : équipement et formation adaptés ; cf. future page Sécurité. Sources : Nitro, RIDE, Burton, Nidecker. Photos fabricants.')
    return p

def examples_page():
    p=Page(22);p.header('Quatre planches Nitro.','Des modèles réels pour relier le programme, les caractéristiques et les mots à dire au client.','02  /  LES FAMILLES')
    for i,c in enumerate(PRODUCTS):
        x=70+(i%2)*1150;y=440+(i//2)*1250;color=common.ACCENTS[i];soft=common.SOFTS[i]
        p.accent,p.soft=color,soft
        p.rect((x,y,x+1110,y+1215),WHITE,color,24,4)
        p.rect((x+3,y+3,x+1107,y+145),soft,None,22)
        p.text(x+27,y+23,c['family'].upper(),31,'bold',color,width=1050)
        p.text(x+27,y+77,c['name'],61,'serif',INK)
        p.rect((x+845,y+83,x+1083,y+128),WHITE,None,12)
        p.text(x+964,y+94,'NITRO / '+c['year'],25,'bold',color,center=True)
        product_photo(p,c['photo'],(x+25,y+178,x+250,y+799))
        p.text(x+137,y+807,'VRAI VISUEL NITRO',20,'bold',color,center=True)
        tx=x+285
        p.text(tx,y+177,'Positionnement',31,'bold',color)
        p.text(tx,y+224,c['position'],34,width=785,leading=40,bottom=y+390)
        p.text(tx,y+405,'Ce que le fabricant met en avant',28,'bold',color,width=785)
        p.text(tx,y+452,c['maker'],33,width=785,leading=39,bottom=y+615)
        p.text(tx,y+632,'Vocabulaire utile',30,'bold',color)
        p.text(tx,y+677,c['vocab'],31,width=785,leading=37,bottom=y+830)
        p.text(x+27,y+849,'Fiche technique',30,'bold',color)
        for j,(label,value) in enumerate(c['specs']):
            yy=y+894+j*34
            if j%2==0:p.d.rectangle((x+22,yy-3,x+1085,yy+31),fill=soft)
            p.text(x+30,yy,label,26,'bold',color,width=230)
            p.text(x+270,yy,value,28,width=800,leading=33,bottom=yy+34)
        p.rect((x+22,y+1045,x+1088,y+1194),DARK,None,17)
        p.text(x+43,y+1060,'À DIRE AU CLIENT',27,'bold',WHITE)
        p.text(x+43,y+1104,'« '+c['speech']+' »',31,'bold',WHITE,width=1020,leading=36,bottom=y+1187)
    p.remember('La même longueur n’a pas le même sens sur toutes les planches.', 'Les poids indiqués ici sont des exemples pour une longueur précise. Vérifier le modèle et son millésime, puis la pointure et les fixations ; adapter au niveau et au terrain.')
    p.footer('Photos et données : Nitro, millésimes indiqués. Poids = plage fabricant du snowboarder, jamais poids de la planche. Patin = largeur au centre. W = wide ; MW = mid-wide. Flex Nitro : échelle propre à la marque. Exemples, sans annonce de stock.')
    return p

if __name__=='__main__':
    records=json.loads(MANIFEST.read_text());assert len(records)>=20
    approved=records[:20];following=records[22:]
    for build in [intro_page,examples_page]:
        p=build();record=p.save()
        if len(records)>=p.n:records[p.n-1]=record
        else:records.append(record)
        print('Page',p.n,'OK',flush=True)
    assert records[:20]==approved and records[22:]==following
    MANIFEST.write_text(json.dumps(records,ensure_ascii=False,indent=2))
