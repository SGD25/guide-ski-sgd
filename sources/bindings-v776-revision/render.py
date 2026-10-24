"""Revised illustrated review pages. Not published. All technical photos are manufacturer originals."""
from pathlib import Path
import sys,math
from PIL import Image,ImageDraw,ImageOps,ImageFilter
BASE=Path(__file__).resolve().parent;M=BASE/'media';OUT=BASE/'pages';OUT.mkdir(exist_ok=True)
(BASE.parents[1]/'assets').mkdir(exist_ok=True)
import io,os
_original_save=Image.Image.save
def complete_save(self,fp,format=None,**kwargs):
 if isinstance(fp,(str,Path)) and str(fp).endswith('.png'):
  data=io.BytesIO();_original_save(self,data,format='PNG',**kwargs);payload=data.getvalue();tmp=Path(str(fp)+'.tmp')
  with open(tmp,'wb',buffering=0) as f:
   view=memoryview(payload)
   while view:
    written=f.write(view);view=view[written:]
   os.fsync(f.fileno())
  os.replace(tmp,fp)
 else:_original_save(self,fp,format=format,**kwargs)
Image.Image.save=complete_save
sys.path.insert(0,str(BASE.parent/'guide'))
from render import Page,ft,INK,BODY,TEAL,CORAL,BLUE,LINE,WHITE,W,H
PURPLE='#75638F';PALE='#F1F5F7';SOFT='#F2EFF7'
def text(p,x,y,s,size=43,w=1000,kind='sans',fill=BODY,bottom=None):
 return p.text(x,y,s,size,kind,fill,width=w,leading=round(size*1.20),bottom=bottom)
def card(p,box,fill=WHITE,outline=LINE):p.rect(box,fill,outline,26,2)
def photo(p,name,box):return p.photo(str(M/name),box)
def anchor(box,x,y):return (box[0]+box[2]*x,box[1]+box[3]*y)
def arrow(p,pts,color=CORAL,width=12,head=30):
 p.d.line(pts,fill=color,width=width,joint='curve');a,b=pts[-2],pts[-1];dx=b[0]-a[0];dy=b[1]-a[1];l=math.hypot(dx,dy);ux,uy=dx/l,dy/l
 p.d.polygon([b,(b[0]-head*ux+head*.52*uy,b[1]-head*uy-head*.52*ux),(b[0]-head*ux-head*.52*uy,b[1]-head*uy+head*.52*ux)],fill=color)
def num(p,x,y,n,r=32,color=PURPLE):
 p.d.ellipse((x-r,y-r,x+r,y+r),fill=color,outline=WHITE,width=3);p.text(x,y-22,str(n),40,'bold',WHITE,center=True)
def label(p,x,y,n,title,desc,w=620,point=None,side='left'):
 if point:
  dest=(x+w+10,y+26) if side=='left' else (x-20,y+26)
  elbow=((point[0]+dest[0])/2,dest[1]);p.d.line([point,elbow,dest],fill='#879CA8',width=4)
  p.d.ellipse((point[0]-7,point[1]-7,point[0]+7,point[1]+7),fill=CORAL)
 num(p,x+30,y+25,n);yy=text(p,x+78,y,title,45,w-78,'bold',INK)+15
 if desc:yy=text(p,x+78,yy,desc,38,w-78)
 return yy
def head(n,a,b,sub,tag):
 p=Page(n);p.accent=PURPLE;p.soft=SOFT
 p.d.rectangle((0,0,2400,13),fill=PURPLE)
 text(p,76,48,'CHAPITRE 03 / SÉCURISER',35,1350,'bold',PURPLE);p.line((1460,66,2070,66),LINE,3)
 p.rect((2110,36,2324,102),'#F9FBFC','#8BA3AF',28,2);p.text(2217,53,f'PAGE {n:02}',31,'bold',INK,center=True)
 size=153
 while p.d.textlength(a,font=ft(size,'serif'))+p.d.textlength(b,font=ft(size,'italic'))>2250:size-=1
 p.text(76,135,a,size,'serif',INK);x=76+p.d.textlength(a,font=ft(size,'serif'));p.text(x,145,b,size,'italic',CORAL)
 text(p,78,325,sub,44,2230,bottom=435)
 p.rect((75,445,2325,515),SOFT,None,14);text(p,103,462,tag,33,2180,'bold',PURPLE)
 return p
def finish(p,title,body,quote,source):
 p.remember(title,body,(75,2830,2325,3100))
 p.client((75,3125,2325,3235),quote,38)
 text(p,76,3260,source,22,1880,bottom=3318)
 p.line((70,3330,2010,3330),'#8BA3AF',3)
 text(p,76,3351,'SPORT GOOD DEAL  /  GUIDE DU SKI',27,1650,'bold',INK)
 p.photo('sgd-logo.png',(2070,3273,2240,3374));p.text(2325,3350,f'{p.n:02}',29,'bold',INK,center=True)
 p.im.save(OUT/f'page-{p.n}.png');small=p.im.copy();small.thumbnail((1000,1415));small.save(OUT/f'apercu-{p.n}.jpg',quality=94)
def pivot_photo(p,im,angle,pivot,at):
 rot=im.rotate(angle,expand=True,resample=Image.Resampling.BICUBIC)
 a=math.radians(angle);dx=pivot[0]-im.width/2;dy=pivot[1]-im.height/2
 rx=rot.width/2+dx*math.cos(a)+dy*math.sin(a);ry=rot.height/2-dx*math.sin(a)+dy*math.cos(a)
 p.im.paste(rot,(round(at[0]-rx),round(at[1]-ry)),rot)
def ribbon(p,y,title):
 p.rect((75,y,2325,y+70),INK,None,14);text(p,110,y+16,title,37,2170,'bold',WHITE)

#31 — two large, individually annotated views, real DIN scales.
p=head(31,'Les fixations ','alpines.','LOOK NX12 Konect GW : reconnaître les pièces et lire les graduations.','L’ANATOMIE • UNE PIÈCE, UN NOM, UNE FONCTION')
p.d.ellipse((720,610,1560,1480),fill='#EDF2F5');p.d.ellipse((720,1640,1560,2630),fill='#EDF2F5')
toe=photo(p,'nx-toe.png',(835,575,1490,1530));heel=photo(p,'nx-heel.png',(800,1640,1500,2620))
label(p,95,610,1,'Fenêtre DIN avant','L’index se lit face à la graduation.',620,anchor(toe,.5,.17))
photo(p,'nx-din-toe.png',(180,840,655,1080));text(p,180,1090,'Gros plan réel',28,500,'bold',PURPLE)
label(p,1620,685,2,'Mâchoires de butée','Elles maintiennent l’avant de la chaussure.',670,anchor(toe,.72,.49),'right')
label(p,95,1210,3,'Plaque antifriction','L’AFD aide la semelle à glisser lors du déclenchement.',620,anchor(toe,.4,.68))
label(p,1620,1220,4,'Levier du rail avant','Il déverrouille la butée pour adapter sa position au BSL.',670,anchor(toe,.56,.94),'right')
ribbon(p,1555,'BUTÉE À L’AVANT  /  TALONNIÈRE À L’ARRIÈRE')
label(p,95,1710,5,'Mâchoire de talon','Elle retient le débord arrière de la chaussure.',620,anchor(heel,.5,.40))
label(p,1620,1730,6,'Frein / ski-stop','Ses deux bras se déploient quand la pédale est libérée.',670,anchor(heel,.94,.20),'right')
label(p,95,2115,7,'Fenêtre DIN arrière','Une seconde valeur à régler et à relire.',620,anchor(heel,.54,.72))
photo(p,'nx-din-heel.png',(235,2335,585,2610));text(p,155,2635,'Vue réelle sur ski',28,600,'bold',PURPLE)
label(p,1620,2220,8,'Pédale du frein','La chaussure l’abaisse au chaussage.',670,anchor(heel,.5,.16),'right')
text(p,95,2700,'DIN / valeur Z : un indice de réglage du déclenchement, pas un poids en kilos.',44,2190,'bold',PURPLE)
finish(p,'Deux fenêtres à lire, deux réglages à vérifier.','Sur cette NX12, la plage annoncée va de 3,5 à 12. La valeur se détermine avec les données du skieur et sa chaussure.','« Le chiffre ne correspond pas à votre poids : plusieurs informations entrent dans le réglage. »','Photos : LOOK (butée) et Utah Ski Gear (NX12 Konect sur ski). Graduations originales, sans reconstruction.')

#32 — genuine boot photos with clear movement, large before/after panels.
p=head(32,'Comprendre le ','déclenchement.','La chaussure reste tenue en ski ; elle peut se libérer sous certaines sollicitations.','LES MOUVEMENTS • LATÉRAL, FRONTAL ET LIBÉRATION DE LA BUTÉE')
# A real sole photographed from below gives an unambiguous footprint.
card(p,(75,550,2325,1465),PALE)
num(p,130,610,1);text(p,190,580,'LATÉRAL : la chaussure pivote sur le côté',52,2050,'serif',INK)
text(p,115,665,'Vue de dessous — on suit la semelle de la chaussure.',33,2100,'bold',PURPLE)
# Original aligned sole left, rotated sole right; common ski axis and bindings shown below.
for x in [180,1290]:
 p.d.rounded_rectangle((x,970,x+890,1100),58,fill='#C6D7DF',outline='#94ADB9',width=3)
 p.d.rounded_rectangle((x+60,955,x+135,1115),15,fill=PURPLE);p.d.rounded_rectangle((x+730,955,x+800,1115),15,fill=PURPLE)
sole=Image.open(M/'boot-sole.png').convert('RGBA');sole=ImageOps.contain(sole,(720,310))
p.im.paste(sole,(260,865),sole)
pivot_photo(p,sole,-25,(sole.width*.92,sole.height*.5),(2075,1030))
arrow(p,[(1035,980),(1190,980)],CORAL,15,35)
arrow(p,[(1550,1060),(1500,940),(1435,850)],CORAL,14,32)
text(p,280,1200,'1. Chaussure alignée',40,850,'bold',INK)
text(p,1350,1200,'2. L’avant sort latéralement',40,870,'bold',INK)
text(p,115,1290,'La butée s’ouvre sur le côté lorsque la sollicitation dépasse le seuil de déclenchement. La chaussure peut alors quitter la fixation.',43,2170,bottom=1440)
# Front fall — actual boot profile, toe points LEFT; it rotates about toe.
card(p,(75,1505,2325,2410),WHITE)
num(p,130,1565,2);text(p,190,1535,'FRONTAL : chute vers l’avant, talon vers le haut',52,2050,'serif',INK)
text(p,115,1620,'Vue de profil — la flèche montre le mouvement du talon.',33,2100,'bold',PURPLE)
boot=Image.open(M/'boot-side.png').convert('RGBA').transpose(Image.Transpose.FLIP_LEFT_RIGHT);boot=ImageOps.contain(boot,(690,520))
p.d.rounded_rectangle((180,2200,1110,2240),18,fill='#C6D7DF');p.im.paste(boot,(300,1685),boot)
p.d.rounded_rectangle((1300,2200,2210,2240),18,fill='#C6D7DF')
pivot_photo(p,boot,22,(boot.width*.07,boot.height*.97),(1450,2195))
arrow(p,[(1040,1950),(1220,1950)],CORAL,15,35)
arrow(p,[(2015,2165),(2030,2080),(2040,1980)],CORAL,15,35)
text(p,220,2270,'Le talon est maintenu.',39,900,'bold',INK);text(p,1320,2270,'Il se soulève et se libère.',39,900,'bold',INK)
card(p,(75,2450,1455,2780),SOFT);card(p,(1490,2450,2325,2780),'#FCF0E9')
text(p,110,2485,'Et l’avant de la chaussure ?',46,1300,'serif',INK)
text(p,110,2560,'La butée Full Action de cette LOOK permet aussi une libération vers le haut, indépendante de la talonnière, notamment lors de sollicitations arrière ou combinées.',39,1300)
text(p,1525,2485,'L’élasticité',46,760,'serif',CORAL)
text(p,1525,2560,'Un petit mouvement peut être absorbé, puis recentré, sans déclencher.',40,760)
finish(p,'« Frontal » décrit la chute vers l’avant.','Dans ce cas, la talonnière libère le talon vers le haut ; la chaussure se dégage ensuite. Aucun système ne déclenche dans toutes les chutes.','« La fixation doit vous maintenir en ski et pouvoir vous libérer dans certaines situations de chute. »','Photos chaussure : Rossignol Hi-Speed. Montages pédagogiques de mouvement, non procédures de test. Technologie : LOOK Full Action.')

#33 — real lever details and exact Konect example
p=head(33,'Adapter la fixation ','au BSL.','LOOK NX12 Konect GW : les leviers déplacent les pièces ; les vis règlent le DIN.','LE RAIL • DÉVERROUILLER, COULISSER, REVERROUILLER')
card(p,(75,550,2325,870),SOFT)
text(p,115,590,'BSL = longueur extérieure de semelle, en mm',53,2100,'serif',INK)
text(p,115,685,'Lire le nombre moulé sur la coque. Ce n’est ni la pointure, ni la taille Mondopoint. Une autre chaussure peut exiger une autre position sur le rail.',43,2120)
# explicit manual views of two levers, make each large, no generic lever representation
for x,title,lever,rail,desc in [(75,'À L’AVANT : LA BUTÉE','nx-toe-lever.png','nx-rail-front.png','Lever à l’arrière de la butée : il libère son coulissement sur l’interface Konect.'),(1215,'À L’ARRIÈRE : LA TALONNIÈRE','nx-heel-lever.png','nx-rail-back.png','Lever à l’arrière de la talonnière : il permet d’avancer ou de reculer celle-ci.')]:
 card(p,(x,910,x+1110,1845),WHITE)
 text(p,x+35,950,title,40,1040,'bold',PURPLE)
 photo(p,lever,(x+85,1030,x+1025,1410));photo(p,rail,(x+50,1430,x+1060,1630))
 text(p,x+40,1660,desc,40,1030)
ribbon(p,1880,'SANS CHAUSSURE ENGAGÉE : OUVRIR LE LEVIER → COULISSER → REFERMER ET VÉRIFIER L’ENCLENCHEMENT')
card(p,(75,1990,1190,2780),SOFT)
text(p,115,2030,'Exemple concret : BSL 310 mm',49,1035,'serif',INK)
text(p,115,2120,'Sur le tableau Konect présenté ici :',40,1035)
p.rect((115,2210,1150,2330),WHITE,None,18);text(p,145,2240,'BUTÉE : 308   /   TALONNIÈRE : 304',44,975,'bold',PURPLE)
text(p,115,2390,'Les deux repères ne sont pas forcément identiques : on suit le tableau du système, pas un arrondi au hasard.',42,1030)
text(p,115,2600,'Ces nombres sont des repères de longueur ; ce ne sont pas des valeurs DIN.',40,1030,'bold',INK)
card(p,(1225,1990,2325,2780),WHITE)
text(p,1265,2030,'Puis contrôler la poussée',49,1020,'serif',INK)
photo(p,'nx-pressure-ok.png',(1270,2140,1690,2650))
text(p,1735,2150,'Chausser complètement.',40,545,'bold',PURPLE)
text(p,1735,2240,'Sur ce Konect, la tige témoin ne doit pas dépasser le chariot plastique. Elle peut rester masquée dans le levier.',38,545)
text(p,1265,2690,'Déchausser, rechausser, puis vérifier à nouveau.',36,1010,'bold',INK)
finish(p,'Adapter la longueur, puis vérifier avec la chaussure réelle.','Le repère de longueur sert à positionner les éléments ; le témoin de poussée confirme le réglage une fois la chaussure engagée.','« Je règle les rails pour votre longueur de semelle, puis je vérifie la poussée chaussure en place. »','Figures et exemple BSL : manuel technique LOOK 2026/27, p. 17–18. Procédure propre au système Konect GW.')

#34 — screwdriver and four-window reading, no instrument references
p=head(34,'Régler et ','contrôler.','Une méthode simple : les bonnes données, les bonnes vis, puis une vérification complète.','AU MAGASIN • LOOK NX12 KONECT GW')
card(p,(75,550,2325,980),SOFT)
num(p,130,615,1);text(p,190,582,'Déterminer la valeur avec ISOSKI',54,2050,'serif',INK)
text(p,120,695,'POIDS  •  TAILLE  •  ÂGE  •  TYPE DE SKIEUR  •  BSL',49,2160,'bold',PURPLE)
text(p,120,790,'Renseigner les données réelles du client. Le type de skieur décrit sa vitesse, son terrain et sa pratique ; pas seulement ses années d’expérience.',42,2140)
# two enlarged photos; a native screwdriver pictogram communicates the action, not a pretend photo.
num(p,130,1050,2);text(p,190,1018,'Régler les vis de déclenchement au tournevis',53,2050,'serif',INK)
for x,title,img in [(75,'BUTÉE : LA FENÊTRE AVANT','nx-din-toe.png'),(1215,'TALONNIÈRE : LA FENÊTRE ARRIÈRE','nx-din-heel.png')]:
 card(p,(x,1130,x+1110,1800),WHITE);text(p,x+35,1170,title,38,1040,'bold',PURPLE)
 photo(p,img,(x+95,1265,x+650,1650))
 # screwdriver silhouette in its own side area, never placed on a fake screw
 p.d.rounded_rectangle((x+800,1300,x+875,1490),22,fill=CORAL);p.d.rectangle((x+825,1480,x+850,1610),fill='#B6C5CD');p.d.polygon([(x+825,1610),(x+850,1610),(x+845,1640),(x+830,1640)],fill=INK)
 text(p,x+45,1700,'Tourner la vis, puis relire l’index en face.',38,1020,'bold',INK)
text(p,100,1850,'Utiliser l’empreinte adaptée. Respecter la plage du modèle ; ne pas ajouter un cran « pour être tranquille ».',43,2180,'bold',CORAL)
num(p,130,2030,3);text(p,190,1998,'Faire le tour des deux skis, avec les chaussures',51,2050,'serif',INK)
for x,title,body in [(75,'4 fenêtres à relire','Butée et talonnière du ski gauche, puis du ski droit. Vérifier les valeurs effectivement affichées.'),(835,'Rails et chaussage','Leviers fermés, éléments bien enclenchés, chaussure correctement tenue et témoin de poussée conforme.'),(1595,'Compatibilité et freins','NX12 Konect GW : semelles adultes ISO 5355 A ou GripWalk ISO 23223 A. Appuis propres, freins libres.')]:
 card(p,(x,2110,x+730,2545),SOFT);text(p,x+35,2150,title,46,660,'serif',INK);text(p,x+35,2240,body,40,660)
card(p,(75,2580,2325,2780),'#FCF0E9')
text(p,115,2615,'Terminer la fiche magasin',44,2100,'bold',CORAL)
text(p,115,2690,'Matériel, BSL, valeurs réglées, vérifications, date et opérateur. Faire essayer le chaussage au client.',38,2100)
finish(p,'Le rail adapte la longueur ; la vis DIN règle le déclenchement.','Si quelque chose coince, paraît usé ou ne correspond pas au repère attendu, reprendre la vérification avec le responsable.','« Vos chaussures sont réglées pour ces skis. Revenez nous voir si vous changez de chaussures. »','Photos : LOOK et Utah Ski Gear, NX12 Konect GW. ISOSKI : données skieur et BSL. Gestes à pratiquer avec le formateur.')

#35 — one number per precise part, big PLUM cutouts
p=head(35,'Les fixations ','PLUM.','Exemple : Guide 12. Apprendre les noms des pièces avant de manipuler.','LA RANDONNÉE À INSERTS • BUTÉE AVANT ET TALONNIÈRE')
p.d.ellipse((640,680,1640,1550),fill='#EDF2F5');p.d.ellipse((650,1780,1650,2650),fill='#EDF2F5')
toe=photo(p,'plum-toe.png',(680,700,1680,1540));heel=photo(p,'plum-heel.png',(740,1750,1580,2690))
label(p,95,595,1,'Pins avant','Ils entrent dans les inserts de la chaussure.',560,anchor(toe,.48,.15))
label(p,1740,595,2,'Levier WALK / SKI','Il sélectionne le mode marche ou ski.',565,anchor(toe,.83,.69),'right')
label(p,95,1120,3,'Ressorts de butée','Ils participent à la fermeture des mâchoires.',560,anchor(toe,.28,.65))
label(p,1740,1110,4,'Support couteaux','Il reçoit les couteaux PLUM compatibles.',565,anchor(toe,.23,.30),'right')
ribbon(p,1580,'EN MONTÉE, LA CHAUSSURE PIVOTE SUR LES INSERTS AVANT ET LE TALON RESTE LIBRE')
label(p,95,1750,5,'Cale haute','Un appui pour le talon à la montée.',565,anchor(heel,.12,.25))
label(p,1740,1750,6,'Fourchettes arrière','Elles s’engagent dans les inserts du talon.',565,anchor(heel,.80,.40),'right')
label(p,95,2160,7,'Corps de talonnière','Il pivote pour changer de mode et de hauteur d’appui.',565,anchor(heel,.57,.65))
label(p,1740,2160,8,'Rail de réglage','Il adapte la position arrière à la chaussure.',565,anchor(heel,.58,.84),'right')
label(p,95,2555,9,'Vis de longueur','Elle immobilise la talonnière sur le rail.',565,anchor(heel,.46,.76))
label(p,1740,2555,10,'Embase de fixation','Support fixé au ski par les vis de montage.',565,anchor(heel,.84,.83),'right')
finish(p,'Inserts, fourchettes, cale, rail : quatre mots à retenir.','Cette Guide 12 est illustrée sans ski-stop. Le leash (lanière de sécurité) et les accessoires se choisissent selon l’usage et la notice.','« Vérifions que vos chaussures à inserts sont bien compatibles avec cette fixation. »','Photos : PLUM Guide 12. Anatomie vérifiée dans la notice GUIDE. Les flèches désignent une pièce précise, sans regroupement.')

#36 — actual PLUM drawings, specific adjustments and critical memory
p=head(36,'Monter, puis ','descendre.','PLUM Guide 12 : maîtriser les deux modes et les contrôles essentiels.','WALK / SKI • LE LEVIER N’EST PAS UN RÉGLAGE DE DIN')
for x,title,img,body in [(75,'MONTÉE / WALK','plum-walk.png','Chausser les inserts avant, puis relever le levier en mode marche. Orienter la talonnière pour la montée : le talon reste libre et les cales le soutiennent en pente.'),(1215,'DESCENTE / SKI','plum-ski.png','Replacer la butée en mode SKI, non verrouillée pour la marche. Orienter les fourchettes arrière vers la chaussure, puis engager le talon.')]:
 card(p,(x,550,x+1110,1460),SOFT if x==75 else WHITE);text(p,x+40,595,title,51,1030,'bold',PURPLE)
 photo(p,img,(x+55,700,x+1055,1110));text(p,x+40,1170,body,42,1030)
card(p,(75,1500,2325,1745),'#FCF0E9')
text(p,115,1540,'Descendre avec le levier verrouillé en WALK bloque le fonctionnement prévu.',46,2130,'serif',CORAL)
text(p,115,1665,'On ne verrouille pas la butée pour corriger un déchaussage intempestif.',40,2120,'bold',INK)
# adjustment drawings on large left, spacer on right
card(p,(75,1785,1470,2460),WHITE);card(p,(1510,1785,2325,2460),WHITE)
text(p,110,1825,'Deux réglages à l’arrière',49,1310,'serif',INK)
photo(p,'plum-adjust.png',(100,1905,925,2370))
text(p,960,1940,'Petite vis',39,470,'bold',PURPLE);text(p,960,2005,'Déclenchement frontal.',38,470)
text(p,960,2160,'Grande vis',39,470,'bold',PURPLE);text(p,960,2225,'Déclenchement latéral.',38,470)
text(p,1545,1825,'Le jeu au talon',49,745,'serif',INK)
photo(p,'plum-gap.png',(1540,1910,2295,2260))
text(p,1545,2310,'Guide illustrée : cale de 4 mm prescrite par PLUM.',37,740,'bold',PURPLE)
card(p,(75,2500,2325,2790),SOFT)
text(p,115,2535,'Avant le départ : les quatre vérifications',48,2130,'serif',INK)
text(p,115,2620,'Inserts sans glace • leviers dans le bon mode • talon correctement engagé en descente • cales et talonnière bien orientées.',43,2130)
finish(p,'Faire refaire la transition au client.','Guide 12 : valeurs indicatives de 5,5 à 12, réglages frontal et latéral à l’arrière. Le levier avant choisit le mode WALK ou SKI.','« Montrez-moi comment vous repassez de la montée à la descente, puis ce que vous contrôlez. »','Dessins : notice PLUM GUIDE G034-B. Jeu de 4 mm propre à la Guide illustrée ; ne pas le transposer à tous les modèles PLUM.')

for n in (31,33,35):
 spread=Image.new('RGB',(2400,1697),'white')
 for j,k in enumerate((n,n+1)):
  im=Image.open(OUT/f'page-{k}.png').resize((1200,1697),Image.Resampling.LANCZOS);spread.paste(im,(j*1200,0))
 spread.save(OUT/f'double-page-{n}-{n+1}.jpg',quality=95)
contact=Image.new('RGB',(1800,1698),'white')
for i,n in enumerate(range(31,37)):
 im=Image.open(OUT/f'page-{n}.png');im.thumbnail((600,849));contact.paste(im,((i%3)*600,(i//3)*849))
contact.save(OUT/'controle.jpg',quality=93)
print(OUT)

for file in OUT.glob('page-*.png'):
 Image.open(file).load()
print('All six master pages decoded successfully')
