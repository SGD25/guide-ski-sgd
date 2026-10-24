from pathlib import Path
import sys,io,os,json,copy,math
from PIL import Image,ImageDraw,ImageChops
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent;OUT=HERE/'pages';OUT.mkdir(exist_ok=True)
u=ROOT/'sources/bindings-v776-revision/render.py';ns={'__file__':str(u)};exec(u.read_text().split('def pivot_photo')[0],ns)
globals().update({k:v for k,v in ns.items() if k not in ['__file__','BASE','OUT']});ns['OUT']=OUT
from render import P
BG=P['fond'];M=ROOT/'sources/bindings-v776-revision/media';GM=ROOT/'sources/guide/media';GREEN='#297A78';MOUNTAIN=GM/'montagnes-aquarelle-v753.png'
def chapter(n):
 if n<8:return 'CHAPITRE 01 / COMPRENDRE',BLUE
 if n<25:return 'CHAPITRE 02 / RECONNAÎTRE ET CONSEILLER LE MATÉRIEL',CORAL
 if n<31:return 'CHAPITRE 03 / RECONNAÎTRE ET CONSEILLER TEXTILES ET ACCESSOIRES',GREEN
 if n<41:return 'CHAPITRE 04 / SÉCURISER',PURPLE
 return 'CHAPITRE 05 / ACCUEILLIR, LOUER ET ACCOMPAGNER',GREEN

def strip(p,box,title,fill=PURPLE):
 p.rect(box,fill,None,14);text(p,box[0]+25,box[1]+16,title,34,box[2]-box[0]-50,'bold',WHITE)
def head(n,a,b,sub,tag):
 p=Page(n);ch,col=chapter(n);p.accent=col;p.soft=SOFT
 p.d.rectangle((0,0,2400,13),fill=col)
 fs=35
 while p.d.textlength(ch,font=ft(fs,'bold'))>1985:fs-=1
 text(p,76,48,ch,fs,1990,'bold',col);p.rect((2110,36,2324,102),BG,'#8BA3AF',28,2);p.text(2217,53,f'PAGE {n:02}',31,'bold',INK,center=True)
 size=150
 while p.d.textlength(a,font=ft(size,'serif'))+p.d.textlength(b,font=ft(size,'italic'))>2250:size-=1
 p.text(76,135,a,size,'serif',INK);p.text(76+p.d.textlength(a,font=ft(size,'serif')),145,b,size,'italic',CORAL)
 text(p,78,325,sub,43,2230,bottom=433)
 p.rect((75,445,2325,520),INK,None,15);text(p,103,464,tag,33,2180,'bold',WHITE)
 return p

def finish(p,title,body,quote,source):
 p.remember(title,body,(75,2830,2325,3100));p.client((75,3125,2325,3235),quote,38)
 text(p,76,3260,source,22,1880,bottom=3318);p.line((70,3330,2010,3330),'#8BA3AF',3);text(p,76,3351,'SPORT GOOD DEAL  /  GUIDE DU SKI',27,1650,'bold',INK)
 p.photo('sgd-logo.png',(2070,3273,2240,3374));p.text(2325,3350,f'{p.n:02}',29,'bold',INK,center=True)
 p.im.save(OUT/f'page-{p.n:02}.png');im=p.im.copy();im.thumbnail((1000,1415));im.save(OUT/f'apercu-{p.n:02}.jpg',quality=95)
def enriched_card(p,box,heading,body,color=BLUE):
 soft={BLUE:'#ECF3F9',CORAL:'#FCF0E9',GREEN:'#EDF6F4',PURPLE:SOFT}.get(color,SOFT)
 card(p,box,soft);x,y,x2,y2=box
 p.d.rounded_rectangle((x,y,x+9,y2),4,fill=color)
 yy=text(p,x+32,y+25,heading,49,x2-x-60,'serif',INK)+22
 text(p,x+32,yy,body,40,x2-x-64,bottom=y2-20)
def ribbon(p,y,title):strip(p,(75,y,2325,y+70),title,INK)
def label(p,x,y,n,title,desc,w=620,point=None,side='left'):
 # Colored definition labels retain original leader-line coordinates.
 color=BLUE if n%2 else GREEN
 yy=y-12;h=80+math.ceil(max(1,len(desc))/max(20,int((w-95)/21)))*46
 h=max(145,min(h,280));card(p,(x-5,yy,x+w+5,yy+h),'#ECF3F9' if n%2 else '#EDF6F4')
 if point:
  dest=(x+w+10,y+26) if side=='left' else (x-20,y+26);elbow=((point[0]+dest[0])/2,dest[1]);p.d.line([point,elbow,dest],fill='#879CA8',width=4);p.d.ellipse((point[0]-7,point[1]-7,point[0]+7,point[1]+7),fill=CORAL)
 num(p,x+30,y+25,n,color=color);end=text(p,x+78,y,title,43,w-88,'bold',INK)+14
 text(p,x+78,end,desc,37,w-90)
# PAGE 3: keep all existing illustration and copy, change only requested panels.
p=Page(3);p.im=Image.open(ROOT/'assets/guide-v772/page-03.jpg').convert('RGB');p.d=ImageDraw.Draw(p.im);before=p.im.copy()
regions=[(1450,1880,2310,2285),(1425,2320,2340,2875)]
p.d.rectangle(regions[0],fill='white');p.rect((1465,1900,2295,2265),'#ECF3F9',None,16)
text(p,1490,1925,'REPÈRES AU PATIN',32,780,'bold',BLUE)
text(p,1490,1990,'65–80 mm : piste\n80–95 mm : all-mountain\n95–136 mm : freeride',38,775,leading if False else 'sans') if False else None
p.text(1490,1990,'65–80 mm : piste\n80–95 mm : all-mountain\n95–136 mm : freeride',38,width=775,leading=52)
text(p,1490,2170,'Repères indicatifs : les familles se chevauchent.',30,775,bottom=2260)
p.d.rectangle(regions[1],fill=BG);p.rect((1430,2340,2330,2825),'white',BLUE,24,3)
text(p,1460,2370,'Lire les lignes de cotes',49,845,'serif',INK);text(p,1460,2440,'Trois largeurs, en millimètres.',32,840)
for x,value,name,col in [(1585,'118','SPATULE','#B88427'),(1880,'88','PATIN',BLUE),(2170,'108','TALON',CORAL)]:
 p.text(x,2520,value,76,'serif',col,center=True);p.text(x,2625,name,35,'bold',col,center=True)
text(p,1460,2720,'Dans l’ordre : de l’avant vers l’arrière du ski.',34,835,bottom=2810)
diff=ImageChops.difference(before,p.im)
for b in regions:ImageDraw.Draw(diff).rectangle(b,fill=0)
assert diff.getbbox() is None
p.im.save(OUT/'page-03.png');im=p.im.copy();im.thumbnail((1000,1415));im.save(OUT/'apercu-03.jpg',quality=95)
# 33–34: exact approved release illustrations, recomposed into a richer page.
for n,mode,title,subtitle in [(33,'latéral','Le déclenchement ','La butée libère l’avant de la chaussure sur le côté.'),(34,'frontal','Le déclenchement ','La talonnière libère le talon vers le haut lors d’un basculement vers l’avant.')]:
 p=head(n,title,mode+'.',subtitle,'COMPRENDRE LE MOUVEMENT • REPÉRER LA PIÈCE QUI LIBÈRE LA CHAUSSURE')
 card(p,(75,550,2325,1550),'#ECF3F9' if n==33 else '#EDF6F4')
 strip(p,(100,570,2300,650),'TORSION → SORTIE LATÉRALE' if n==33 else 'BASCULEMENT VERS L’AVANT → TALON VERS LE HAUT',BLUE if n==33 else GREEN)
 old=Image.open(ROOT/f'assets/guide-v779/page-{n}.png');fig=old.crop((125,720,2280,1715));fig.thumbnail((2150,780),Image.Resampling.LANCZOS);p.im.paste(fig,(round(120+(2150-fig.width)/2),675))
 # Caption is part of the approved teaching content.
 text(p,115,1480,'Fixation alpine générique : illustration de principe, non spécifique à la LOOK NX12.',31,2130)
 if n==33:
  data=[('1 · Maintenir','La chaussure est tenue entre la butée à l’avant et la talonnière à l’arrière.'),('2 · Solliciter','Une torsion tend à faire pivoter la chaussure par rapport au ski.'),('3 · Libérer','Lorsque le seuil est atteint, la butée laisse sortir l’avant sur le côté.')]
 else:
  data=[('1 · Maintenir','La mâchoire de la talonnière retient le débord arrière de la chaussure.'),('2 · Solliciter','Le basculement du skieur vers l’avant tend à soulever le talon.'),('3 · Libérer','Lorsque le seuil est atteint, la talonnière s’ouvre et le talon peut monter.')]
 for i,(h,b) in enumerate(data):enriched_card(p,(75+i*765,1600,795+i*765,2020),h,b,[BLUE,GREEN,CORAL][i])
 if n==33:
  card(p,(75,2070,1110,2780),'white');strip(p,(95,2090,1090,2160),'LA PIÈCE À RECONNAÎTRE',BLUE)
  photo(p,'nx-toe.png',(105,2210,535,2730));text(p,565,2225,'La butée avant',48,500,'serif',INK);text(p,565,2310,'Les mâchoires retiennent l’avant. La plaque antifriction facilite le glissement de la semelle.',39,495)
  enriched_card(p,(1150,2070,2325,2450),'Gauche ou droite ?','Les deux sorties dessinées sont des possibilités alternatives : ce ne sont pas deux étapes successives.',BLUE)
  enriched_card(p,(1150,2490,2325,2780),'Élasticité ≠ déclenchement','Un petit déplacement peut être absorbé et recentré sans libérer la chaussure.',CORAL)
  finish(p,'Latéral : l’avant de la chaussure sort sur le côté.','Torsion = sollicitation ; butée = pièce concernée ; déclenchement = libération. Aucun système ne déclenche dans toutes les chutes.','« En cas de torsion suffisante, la fixation peut libérer l’avant de la chaussure sur le côté. »','Illustration : Mechanics of Sport / Simon Weller, légendes françaises. Photo : LOOK. Repères techniques : documentation LOOK.')
 else:
  enriched_card(p,(75,2070,1180,2430),'Le corps va vers l’avant.','« Frontal » désigne ici le sens du basculement. Ce n’est pas une chaussure qui coulisse simplement vers la spatule.',GREEN)
  enriched_card(p,(1220,2070,2325,2430),'Le talon monte.','Le mouvement de libération est vertical. La talonnière s’ouvre et la chaussure peut ensuite se dégager.',BLUE)
  card(p,(75,2470,2325,2780),'#FCF0E9');text(p,115,2500,'Ne pas confondre avec le déchaussage volontaire.',49,2100,'serif',INK)
  text(p,115,2590,'À l’arrêt, on actionne le levier prévu pour ouvrir la talonnière. Lors d’un déclenchement, l’ouverture répond à une sollicitation suffisante de la chaussure.',40,2110,bottom=2760)
  finish(p,'Frontal : basculement vers l’avant, talon libéré vers le haut.','La butée et la talonnière ont des rôles complémentaires. Les mécanismes et leurs réglages dépendent du modèle.','« Lors d’un basculement vers l’avant, la talonnière peut s’ouvrir pour laisser monter le talon. »','Illustration : Mechanics of Sport / Simon Weller, légendes françaises. Sens de libération : documentation technique alpine.')
# Reuse precise original photo positions and leader lines for anatomy and PLUM.
s=u.read_text()
block=s[s.index('#31 —'):s.index('#32 —')].replace('head(31,','head(35,')
block=block.replace('L’index se lit face à la graduation.','Lire la graduation face à l’index, sans se placer en biais.').replace('Elles maintiennent l’avant de la chaussure.','Elles retiennent l’avant et permettent sa libération latérale.').replace('L’AFD aide la semelle à glisser lors du déclenchement.','AFD : surface de contact qui facilite le glissement de la semelle.').replace('Il déverrouille la butée pour adapter sa position au BSL.','Il adapte la position au BSL. Ce levier ne règle pas la valeur DIN.').replace('Elle retient le débord arrière de la chaussure.','Elle retient le débord arrière et libère le talon vers le haut.').replace('Une seconde valeur à régler et à relire.','Seconde graduation : régler, puis relire la valeur réellement affichée.')
block=block.replace("finish(p,'Deux fenêtres", "enriched_card(p,(1620,2480,2310,2670),'Frein = ski-stop','Deux noms pour la même fonction.',GREEN)\nfinish(p,'Deux fenêtres")
exec(block)
#36 controls: fill useful blank space with distinct reminders, retaining real DIN scales.
block=s[s.index('#34 —'):s.index('#35 —')].replace('head(34,','head(36,')
block=block.replace("# two enlarged photos", "text(p,120,920,'BSL : longueur extérieure de semelle en mm, distincte de la pointure.',33,2140,'bold',PURPLE)\n# two enlarged photos")
block=block.replace("card(p,(x,1130,x+1110,1800),WHITE)","card(p,(x,1130,x+1110,1800),'#ECF3F9' if x==75 else '#EDF6F4')")
block=block.replace("card(p,(x,2110,x+730,2545),SOFT)","card(p,(x,2110,x+730,2545),'#ECF3F9' if x==75 else ('#EDF6F4' if x==835 else '#FCF0E9'))")
block=block.replace("card(p,(75,2580", "for xx,lab in [(75,'GAUCHE + DROIT'),(835,'AVEC LA CHAUSSURE RETENUE'),(1595,'DOUTE → RÉFÉRENT')]:\n text(p,xx+35,2475,lab,27,660,'bold',PURPLE)\ncard(p,(75,2580")
exec(block)
#37 original precise numbered anatomy, enriched definitions.
block=s[s.index('#35 —'):s.index('#36 —')].replace('head(35,','head(37,')
block=block.replace('Ils entrent dans les inserts de la chaussure.','Les pointes entrent dans les inserts métalliques avant de la chaussure.').replace('Il sélectionne le mode marche ou ski.','Il sélectionne marche ou ski : ce n’est pas une vis de réglage DIN.').replace('Un appui pour le talon à la montée.','Elle soutient le talon en montée ; elle ne le verrouille pas.').replace('Elles s’engagent dans les inserts du talon.','Les deux pointes s’engagent dans les inserts arrière en descente.').replace('Il adapte la position arrière à la chaussure.','Il adapte la position à la longueur de la chaussure.').replace('Elle immobilise la talonnière sur le rail.','Elle fixe la position arrière sur son rail.')
exec(block)
#38 technical originals, stronger visual separation and compact departure check.
block=s[s.index('#36 —'):s.index('for n in (31,33,35):')].replace('head(36,','head(38,')
block=block.replace('SOFT if x==75 else WHITE',"'#ECF3F9' if x==75 else '#EDF6F4'")
block=block.replace('card(p,(75,1785,1470,2460),WHITE)',"card(p,(75,1785,1470,2460),'#ECF3F9')").replace('card(p,(1510,1785,2325,2460),WHITE)',"card(p,(1510,1785,2325,2460),'#EDF6F4')")
exec(block)
# 41–44 retain scenes, add concrete examples and pictured counter situations.
def close(p,title,body,quote,source='Formation magasin • Illustrations de comptoir générées ; photos produit : sources du guide.'):
 finish(p,title,body,quote,source)
def step(p,x,y,w,h,n,title,body,tag=None):
 color=[BLUE,GREEN,CORAL,PURPLE][n-1];soft=['#ECF3F9','#EDF6F4','#FCF0E9',SOFT][n-1]
 card(p,(x,y,x+w,y+h),soft);num(p,x+48,y+50,n,color=color)
 yy=text(p,x+100,y+23,title,52,w-135,'serif',INK)+26;yy=text(p,x+32,yy,body,43,w-64,bottom=y+h-245)
 examples={1:'À faire préciser : pistes faciles, pistes plus raides, neige damée ou neige souple ?',2:'À lire sur la chaussure : relever le BSL réel, même si le client connaît sa pointure.',3:'À écouter : un point douloureux, une compression ou un talon qui se soulève.',4:'À expliquer : « Je vous propose ce modèle parce qu’il correspond à votre pratique. »'}
 p.rect((x+25,y+h-235,x+w-25,y+h-105),'white',None,13);text(p,x+45,y+h-216,examples[n],34,w-90,bottom=y+h-115)
 p.rect((x+25,y+h-90,x+w-25,y+h-25),color,None,11);text(p,x+40,y+h-75,tag,30,w-80,'bold',WHITE,bottom=y+h-30)
def smallstep(p,x,y,w,n,title,body):
 num(p,x+25,y+24,n,r=25,color=GREEN);yy=text(p,x+68,y,title,45,w-70,'bold',INK)+16
 return text(p,x+68,yy,body,39,w-78)+33
cs=(ROOT/'sources/closing-proposals/render.py').read_text();block=cs[cs.index('# 41'):cs.index('#43')].replace("HERE/'media/accueil.png'","ROOT/'sources/closing-proposals/media/accueil.png'").replace("HERE/'media/retour.png'","ROOT/'sources/closing-proposals/media/retour.png'")
block=block.replace("close(p,'Le client doit", "enriched_card(p,(110,2455,1145,2685),'Le client est prêt.','Il sait chausser, déchausser et qui contacter si quelque chose ne va pas.',BLUE)\nenriched_card(p,(1255,2455,2290,2685),'Le matériel est suivi.','Identifier les éléments, noter les remarques et transmettre les anomalies.',CORAL)\nclose(p,'Le client doit")
exec(block)
#43 four pictured practical cases.
p=head(43,'Les bonnes questions, ','au bon moment.','Quatre situations courantes pour transformer une demande en conseil adapté.','AU COMPTOIR • QUESTIONNER → COMPRENDRE → PROPOSER')
caseblock=cs[cs.index('cases=['):cs.index('for i,(q,ask,do,avoid)')];exec(caseblock)
photos=[str(GM/'piste-station-v752.png'),str(M/'boot-side.png'),str(M/'nx-din-toe.png'),str(GM/'patin-elan-88-v754.png')]
for i,(q,ask,do,avoid) in enumerate(cases):
 y=560+i*550;col=[BLUE,GREEN,CORAL,PURPLE][i];soft=['#ECF3F9','#EDF6F4','#FCF0E9',SOFT][i]
 card(p,(75,y,2325,y+510),soft);strip(p,(95,y+18,2305,y+110),'« '+q+' »',col)
 p.photo(photos[i],(105,y+145,520,y+465));text(p,560,y+145,'JE DEMANDE',31,760,'bold',col);text(p,560,y+200,ask,38,760,bottom=y+480)
 p.line((1365,y+155,1365,y+470),LINE,3);text(p,1410,y+145,'LE BON RÉFLEXE',31,850,'bold',col);yy=text(p,1410,y+195,do,37,850)+17;text(p,1410,yy,'À éviter : '+avoid,34,850,fill=CORAL,bottom=y+490)
close(p,'Une phrase du client n’est pas un diagnostic.','Faire préciser les faits, reprendre les vérifications utiles et expliquer la solution proposée.','« Je vais vous poser quelques questions pour comprendre ce qui se passe et vous proposer une solution adaptée. »','Cas pédagogiques de formation. Photos : sources du guide. Réglages et contrôles : notices fabricants et formation pratique.')
#44 retain the flow and actual photos; annotate the specific contact areas.
block=cs[cs.index('#44'):cs.index('# Export')]
block=block.replace("card(p,(x,1230,x+720,2180));p.photo(str(M/img),(x+25,1270,x+695,1735));", "card(p,(x,1230,x+720,2180),['#ECF3F9','#EDF6F4','#FCF0E9'][i]);pb=p.photo(str(M/img),(x+25,1270,x+695,1735));\n for ax,ay in ([(.13,.5),(.86,.5)] if i==0 else ([(.45,.68)] if i==1 else [(.15,.49)])):\n  cx=pb[0]+ax*pb[2];cy=pb[1]+ay*pb[3];p.d.ellipse((cx-43,cy-43,cx+43,cy+43),outline=CORAL,width=6)\n text(p,x+32,1730,['APPUIS AVANT ET ARRIÈRE','ZONE DE CONTACT SOUS L’AVANT','BRAS DU FREIN'][i],25,660,'bold',CORAL); ")
block=block.replace("close(p,'En cas de doute", "for xx in [802,1567]:arrow(p,[(xx,800),(xx+30,800)],GREEN,8,18)\nclose(p,'En cas de doute")
exec(block)
# Small contextual decoration in the unused ribbon between body and memory card.
for n in [35,36,37,38,41,42,43,44]:
 f=OUT/f'page-{n}.png';im=Image.open(f);im.load()
# Produce printable review and double-page previews without altering masters.
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
c=canvas.Canvas(str(HERE/'propositions-peaufinements.pdf'),pagesize=(595.28,841.89))
for n in [3,33,34,35,36,37,38,41,42,43,44]:
 c.drawImage(ImageReader(str(OUT/f'page-{n:02}.png')),0,0,width=595.28,height=841.89);c.showPage()
c.save()
for a,b in [(33,34),(35,36),(37,38),(41,42),(43,44)]:
 spread=Image.new('RGB',(2000,1415),'white')
 for i,n in enumerate([a,b]):
  im=Image.open(OUT/f'page-{n}.png');im.thumbnail((1000,1415));spread.paste(im,(i*1000,0))
 spread.save(OUT/f'double-{a}-{b}.jpg',quality=95)
print('Polished pages rendered:',OUT)
