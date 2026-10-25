from pathlib import Path
import math
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
src=ROOT/'sources/final-polish-v781/render.py';ns={'__file__':str(src)};exec(src.read_text().split('# PAGE 3:')[0],ns)
globals().update({k:v for k,v in ns.items() if k not in ['__file__','HERE','OUT','ROOT','ns']})
OUT=HERE/'pages';OUT.mkdir(exist_ok=True);ns['OUT']=OUT;MEDIA=ROOT/'sources/snow-lexicon/media'
def box(p,b,title,body,col=BLUE,size=38):
 soft={BLUE:'#ECF3F9',GREEN:'#EDF6F4',CORAL:'#FCF0E9',PURPLE:SOFT}[col];card(p,b,soft)
 x,y,x2,y2=b;yy=text(p,x+25,y+20,title,45,x2-x-50,'serif',INK)+20
 return text(p,x+25,yy,body,size,x2-x-50,bottom=y2-18)
def pic(p,name,b):return p.photo(str(MEDIA/(name+'.png')),b)
def num(p,x,y,n,r=32,color=PURPLE):
 p.d.ellipse((x-r,y-r,x+r,y+r),fill=color,outline=WHITE,width=3);p.d.text((x,y+1),str(n),font=ft(round(r*1.3),'bold'),fill=WHITE,anchor='mm')
def leader(p,pts,col=CORAL):
 p.d.line(pts,fill=col,width=4);x,y=pts[-1];p.d.ellipse((x-7,y-7,x+7,y+7),fill=col)
def tag(p,x,y,t,w,col=BLUE):p.rect((x,y,x+w,y+62),WHITE,col,16,2);text(p,x+15,y+12,t,32,w-30,'bold',col)
p=head(21,'Snowboard : ','les mots de la planche.','Nommer une caractéristique, puis expliquer ce qu’elle change sur la neige.','LEXIQUE PRO · ANATOMIE, SHAPES, FLEX ET SEMELLES · NITRO 2025–2026')
# True manufacturer photo: nose left, tail right.
card(p,(75,550,2325,1150),'white')
im=Image.open(MEDIA/'team-top.png').rotate(90,expand=True);im=im.resize((1720,round(im.height*1720/im.width)),Image.Resampling.LANCZOS);p.im.paste(im,(340,730),im)
text(p,110,575,'NITRO TEAM 2026 · VUE DU DESSUS',30,1000,'bold',PURPLE)
for x,y,t,w,col,pts in [
(105,660,'NOSE = avant',340,BLUE,[(275,722),(350,885)]),
(1950,660,'TAIL = arrière',340,CORAL,[(2120,722),(2045,885)]),
(550,640,'INSERTS = ancrages filetés',570,GREEN,[(835,702),(890,880)]),
(1200,640,'TOPSHEET = face supérieure',605,PURPLE,[(1500,702),(1450,840)]),
(270,1050,'CARRE = bord métallique',520,BLUE,[(530,1050),(620,1036)]),
(1450,1050,'CHANT = flanc de la planche',640,GREEN,[(1750,1050),(1800,1036)])]:
 tag(p,x,y,t,w,col);leader(p,pts,col)
# Emphasised vocabulary and a clear Wide callout.
card(p,(75,1180,805,1600),'#ECF3F9')
strip(p,(95,1200,785,1265),'WIDE = VERSION ÉLARGIE',BLUE)
text(p,105,1290,'Pour les boots de grande pointure.',38,665,'bold',INK)
text(p,105,1390,'WAIST WIDTH : largeur au patin.\nCARRE EFFECTIVE : portion utile à l’accroche, différente de la longueur totale.',36,665,bottom=1580)
box(p,(835,1180,1565,1600),'SIDECUT = ligne de cotes','La courbe des carres donne un rayon, parfois plusieurs. À conditions comparables, petit rayon : virages plus courts ; grand rayon : courbes plus longues.',GREEN,38)
card(p,(1595,1180,2325,1600),'#FCF0E9')
for yy,term,desc in [(1205,'FLEX','Souplesse dans la longueur.'),(1300,'TORSION','Déformation entre les carres.'),(1395,'POP','Rebond pour décoller.')]:
 text(p,1620,yy,term,35,670,'bold',CORAL);text(p,1620,yy+43,desc,34,670)
text(p,1620,1490,'Souple : facile à déformer.\nRigide : davantage de soutien.',34,670,bottom=1585)
text(p,90,1620,'SHAPE = FORME VUE DU DESSUS · LE CAMBRE SE LIT DE PROFIL',31,2220,'bold',PURPLE)
def dimension(p,x,y1,y2,col):
 arrow(p,[(x,y1),(x,y2)],col,4,12);arrow(p,[(x,y2),(x,y1)],col,4,12)
# A schematic explicitly exaggerates setback; photographs stay untouched.
shapes=[
 ('t1-top','TWIN / TRUE TWIN','T1 · recul 0 mm',0,BLUE,'AVANT = ARRIÈRE','Montage centré, nose et tail symétriques. Même équilibre dans les deux sens : utile en switch et en freestyle.'),
 ('team-top','DIRECTIONAL TWIN','Team · recul 15 mm',28,GREEN,'MONTAGE UN PEU RECULÉ','Une forme proche du twin, avec les fixations légèrement vers le tail sur la Team. Polyvalence, switch encore accessible.'),
 ('squash-top','DIRECTIONNEL','Squash · recul 25 mm',48,CORAL,'AVANT PLUS PRÉSENT','Sur la Squash : montage reculé, nose plus large et tail en queue d’hirondelle. Portance et conduite privilégiée vers l’avant.')]
for i,(f,t,sub,shift,col,caption,body) in enumerate(shapes):
 x=75+i*760
 card(p,(x,1680,x+730,2390),{BLUE:'#ECF3F9',GREEN:'#EDF6F4',CORAL:'#FCF0E9'}[col])
 text(p,x+23,1700,t,39,690,'bold',col);text(p,x+23,1760,sub,32,690,'bold',INK)
 pic(p,f,(x+25,1835,x+115,2150))
 # Nose at the top and tail at the bottom, each diagram shares the same centre.
 bx=x+260;top=1840;bottom=2160;mid=(top+bottom)/2
 if i<2:p.rect((bx-65,top,bx+65,bottom),'#BDCFD8',INK,60,3)
 else:
  pts=[(bx+66*math.cos(math.pi+j*math.pi/30),top+66+66*math.sin(math.pi+j*math.pi/30)) for j in range(31)]
  pts += [(bx+48,bottom-5),(bx,bottom-35),(bx-48,bottom-5)]
  p.d.polygon(pts,fill='#BDCFD8',outline=INK,width=3)
 for xx in range(int(bx-100),int(x+660),16):p.line((xx,mid,xx+8,mid),'#7D8F99',2)
 for cy in [mid-60+shift,mid+60+shift]:
  p.rect((bx-82,cy-17,bx+82,cy+17),WHITE,col,6,4)
  p.line((bx-12,cy-11,bx+12,cy+11),col,3);p.line((bx+12,cy-11,bx-12,cy+11),col,3)
 dimension(p,bx+110,top,mid-60+shift,col)
 dimension(p,bx+110,mid+60+shift,bottom,col)
 text(p,x+425,1835,'NOSE / AVANT',28,280,'bold',col)
 text(p,x+425,1935,'Fixations :\nblocs blancs',29,280)
 text(p,x+425,2070,'TAIL / ARRIÈRE',28,280,'bold',col)
 text(p,x+25,2190,caption,29,680,'bold',col)
 text(p,x+25,2245,body,34,680,bottom=2375)
text(p,90,2410,'Pointillés : milieu du croquis. Recul amplifié pour le voir ; le shape directionnel ne se résume pas au recul.',28,2210)
text(p,90,2460,'TWIN TIP : extrémités relevées. TAPER : nose plus large que le tail. SWALLOWTAIL : queue d’hirondelle.',28,2220,'bold',PURPLE)
box(p,(75,2520,1180,2790),'BASE EXTRUDÉE','Semelle économique, facile à réparer et peu exigeante. Elle bénéficie aussi du fartage. Ex. Prime 2026 : Premium Extruded FH.',BLUE,36)
box(p,(1220,2520,2325,2790),'BASE FRITTÉE / SINTERED','Retient davantage le fart ; bonne glisse si entretenue. Ex. Team / T1 2026 : Sintered EcoSpeed HD. Pas de classement universel entre marques.',GREEN,36)
finish(p,'Shape, cambre et flex : trois caractéristiques différentes.','La forme ne suffit pas à choisir. Relier chaque terme au poids, au niveau, aux boots et au programme. Les notes de flex ne sont pas standardisées entre marques.','« Vous cherchez surtout de la facilité, du soutien à vitesse élevée ou une planche à l’aise dans les deux sens ? »','Visuels et exemples : Nitro, Dealer Manual 2025–2026, p. 33, 36, 45, 49. Lexique : Jones, Burton. Photos fabricants ; repères à adapter au modèle.')
# Page 22: clear native diagrams, not generated mechanical illustrations.
def boot(p,cx,cy,angle,fill,letter,scale=1):
 # Sole silhouette points upward at 0°, with heel narrower than toes.
 im=Image.new('RGBA',(180,280));d=ImageDraw.Draw(im);d.rounded_rectangle((25,8,155,210),55,fill=fill,outline=INK,width=4);d.rounded_rectangle((40,160,140,270),35,fill=fill,outline=INK,width=4)
 d.line((48,90,132,90),fill='white',width=5);d.line((48,125,132,125),fill='white',width=5)
 
 im=im.resize((round(180*scale),round(280*scale))).rotate(angle,expand=True,resample=Image.Resampling.BICUBIC)
 p.im.paste(im,(round(cx-im.width/2),round(cy-im.height/2)),im)
 p.d.ellipse((cx-26,cy-26,cx+26,cy+26),fill=INK)
 p.d.text((cx,cy+1),letter,font=ft(36,'bold'),fill='white',anchor='mm')
def board(p,b):p.rect(b,'#DFE8ED','#8298A4',int((b[3]-b[1])/2),3)
p=head(22,'Snowboard : ','placer le rider.','Comprendre la position des pieds, puis ajuster l’ensemble boots–fixations–planche.','LEXIQUE PRO · REGULAR / GOOFY, STANCE, ANGLES ET FIXATIONS')
for x,word,front,back,rot,col in [(75,'REGULAR','G','D',0,BLUE),(1220,'GOOFY','D','G',180,GREEN)]:
 card(p,(x,550,x+1105,970),'#ECF3F9' if col==BLUE else '#EDF6F4');text(p,x+30,575,word,49,1000,'serif',col)
 text(p,x+30,645,'PIED DROIT DERRIÈRE' if back=='D' else 'PIED GAUCHE DERRIÈRE',39,1000,'bold',INK)
 board(p,(x+100,760,x+1025,940));boot(p,x+390,850,rot,col,front,.6);boot(p,x+750,850,rot,CORAL,back,.6)
 arrow(p,[(x+230,725),(x+100,725)],col,7,20);text(p,x+255,704,'NOSE / SENS HABITUEL',27,740,'bold',col)
text(p,90,990,'Le pied arrière aide à doser la conduite ; les deux pieds participent aux virages. G = gauche · D = droit.',31,2230)
card(p,(75,1070,1180,1850),'#ECF3F9')
strip(p,(95,1090,1160,1160),'STANCE = POSITION DES PIEDS',BLUE)
text(p,110,1190,'STANCE WIDTH = écartement entre les centres des fixations. Partir des repères de la planche et adapter au gabarit et au confort.',38,1030)
strip(p,(95,1380,1160,1450),'SETBACK = RECUL VERS LE TAIL',CORAL)
text(p,110,1480,'Le montage est décalé vers l’arrière : le nose porte plus facilement en poudreuse. Centré : équilibre dans les deux sens. Suivre les repères du modèle.',38,1030)
strip(p,(95,1670,1160,1740),'SWITCH = L’AUTRE PIED DEVANT',GREEN)
text(p,110,1770,'On glisse à l’inverse de sa position habituelle.',36,1030)
card(p,(1220,1070,2325,1850),'#EDF6F4')
text(p,1245,1090,'ANGLES : voir l’orientation des pieds',42,1030,'serif',INK)
text(p,1245,1165,'0° = en travers ; + vers le nose ; − vers le tail.\nVue du dessus : exemples en regular, nose à gauche.',32,1030)
for i,(aa,ab,lab,desc) in enumerate([(15,0,'+15° / 0°','Arrière en travers'),(15,-15,'+15° / −15°','DUCK : pieds ouverts'),(21,6,'+21° / +6°','Deux pieds vers l’avant')]):
 cy=1360+i*145
 board(p,(1260,cy-50,1780,cy+50))
 for cx in [1430,1640]:
  for yy in range(cy-85,cy+85,16):p.line((cx,yy,cx,yy+8),'#94A7AE',2)
 boot(p,1430,cy,aa,BLUE,'G',.39);boot(p,1640,cy,ab,CORAL,'D',.39)
 text(p,1820,cy-45,lab,38,470,'bold',GREEN);text(p,1820,cy+12,desc,30,470)
text(p,1245,1795,'Repères à adapter : confort, pratique et genoux à l’aise.',28,1030,'bold',CORAL)
# A genuine binding photo with separate, precise numbered callouts.
card(p,(75,1890,2325,2440),'white');text(p,100,1910,'UNE FIXATION À SANGLES · NITRO RAMBLER 2026',32,2190,'bold',PURPLE)
b=pic(p,'rambler',(110,1970,760,2405))
items=[(1,'SPOILER','Appui derrière le mollet ; son inclinaison règle la position d’appui.',(.25,.2)),(2,'STRAP DE CHEVILLE','Sangle de cheville : maintien de la boot.',(.52,.43)),(3,'STRAP D’ORTEILS','Sangle d’orteils : cale l’avant de la boot.',(.82,.63)),(4,'BOUCLE','Serre sur la crémaillère ; vérifier dents et fermeture.',(.67,.57)),(5,'EMBASE','Support sous la boot. Le disque règle l’angle et relie aux inserts.',(.58,.89)),(6,'ARCEAU','Entoure le talon et relie les côtés de l’embase ; soutient le spoiler.',(.17,.72))]
for i,(n,t,desc,pt) in enumerate(items):
 cx=b[0]+pt[0]*b[2];cy=b[1]+pt[1]*b[3];num(p,cx,cy,n,r=24,color=CORAL)
 y=1970+i*75;num(p,850,y+20,n,r=23,color=CORAL);text(p,890,y,t,34,1380,'bold',INK);text(p,890,y+38,desc,29,1380,bottom=y+73)
# Practical controls and edge vocabulary.
box(p,(75,2460,1180,2790),'Centrer les boots : éviter le drag','Toe side = carre orteils ; heel side = carre talons. Toe / heel drag : boot qui touche la neige en virage. Vérifier le dépassement des deux côtés avec les vraies boots ; choisir Wide si nécessaire.',BLUE,36)
box(p,(1220,2460,2325,2790),'Le réflexe vendeur / loueur','Taille de fixation, disque, inserts et vis compatibles ; straps centrés, boucles et serrages contrôlés selon notice. Noter regular/goofy, stance et angles dans la fiche client. Leash selon notice.',GREEN,36)
finish(p,'Un montage confortable et compatible, pas une recette unique.','Les fixations de snowboard ne déclenchent pas comme celles du ski. Expliquer les manipulations ; vérifier les boots, la planche et les fixations ensemble.','« Quel pied mettez-vous devant ? Quels écartement et angles vous conviennent habituellement ? »','Sources : Nitro Dealer Manual 2025–2026 p. 109 ; guides Burton (stance, pièces et réglages), Jones. Schémas pédagogiques : vue du dessus, positions simplifiées.')
print('Two snowboard lexicon pages ready:',OUT)
