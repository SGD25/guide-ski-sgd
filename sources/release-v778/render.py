from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from pathlib import Path
import fitz
BASE=Path(__file__).resolve().parent; R=BASE.parents[1]; O=R/'assets/guide-v778'; W,H=595.28,841.89
c=canvas.Canvas(str(BASE/'declenchements.pdf'),pagesize=(W,H))
ink='#193B4B'; purple='#75638F'; coral='#BA624F'
def rect(x,y,w,h,color):
 c.setFillColor(HexColor(color));c.roundRect(x,H-y-h,w,h,7,fill=1,stroke=0)
def txt(x,y,s,size=12,font='Helvetica',color=ink):
 c.setFillColor(HexColor(color));c.setFont(font,size);c.drawString(x,H-y-size,s)
def para(x,y,s,w=523,size=12,color=ink):
 p=Paragraph(s,ParagraphStyle('p',fontName='Helvetica',fontSize=size,leading=size*1.35,textColor=HexColor(color)))
 _,h=p.wrap(w,400);p.drawOn(c,x,H-y-h);return h
items=[(34,'Le déclenchement','latéral.','toe','UNE TORSION : L’AVANT DE LA CHAUSSURE SORT SUR LE CÔTÉ',[
('1','La chaussure est maintenue','La butée retient l’avant ; la talonnière retient l’arrière.'),
('2','Une torsion sollicite la butée','La chaussure tend à pivoter par rapport au ski.'),
('3','L’avant se libère sur le côté','Si le seuil de déclenchement est atteint, la butée laisse sortir l’avant de la chaussure.')],
'La pièce à observer : la butée avant','La sortie peut se faire à gauche ou à droite. Sur le dessin, les deux positions de sortie sont des alternatives : ce ne sont pas deux étapes successives.',
'LATÉRAL = SORTIE SUR LE CÔTÉ, AU NIVEAU DE LA BUTÉE.',
'« En cas de torsion suffisante, la fixation peut libérer l’avant de la chaussure sur le côté. »'),
(35,'Le déclenchement','frontal.','heel','UN BASCULEMENT VERS L’AVANT : LE TALON SE LIBÈRE VERS LE HAUT',[
('1','La chaussure est maintenue','Le talon est retenu par la mâchoire de la talonnière.'),
('2','Le skieur bascule vers l’avant','Cette sollicitation tend à soulever le talon de la chaussure.'),
('3','La talonnière libère le talon','Si le seuil de déclenchement est atteint, elle s’ouvre et le talon peut monter.')],
'La pièce à observer : la talonnière','« Frontal » décrit ici le basculement vers l’avant. Le mouvement de libération du talon est vertical : il monte. La chaussure ne coulisse pas simplement vers la spatule.',
'FRONTAL = BASCULEMENT VERS L’AVANT, TALON LIBÉRÉ VERS LE HAUT.',
'« Lors d’un basculement vers l’avant, la talonnière peut s’ouvrir pour laisser monter le talon. »')]
for n,a,b,im,sub,steps,title,body,remember,quote in items:
 rect(0,0,W,H,'#F9FBFC');rect(0,0,W,4,purple)
 txt(24,17,'CHAPITRE 03 / SÉCURISER',8,'Helvetica-Bold',purple);txt(513,17,f'PAGE {n}',8,'Helvetica-Bold')
 txt(24,43,a,29,'Times-Bold');txt(24,77,b,35,'Times-BoldItalic',coral)
 para(24,126,sub,547,9,purple)
 rect(24,156,547,284,'#FFFFFF')
 c.drawImage(ImageReader(str(BASE/f'media/reference-{im}.png')),32,H-428,width=531,height=250,preserveAspectRatio=True,anchor='c',mask='auto')
 # Exact vector annotations replace only the English text, leaving mechanics untouched.
 scale=531/700; height=325 if im=='toe' else 314
 top=428-(250+height*scale)/2
 def labelbox(x,y,w,h,line):
  c.setFillColor(HexColor('#FFFFFF'));c.rect(32+(x-2)*scale,H-top-(y+h+2)*scale,(w+4)*scale,(h+4)*scale,fill=1,stroke=0)
  txt(32+x*scale,top+y*scale,line,8.2,'Helvetica',ink)
 if im=='toe':
  for x,y,w,h,line in [(188,127,92,15,'Une torsion'),(188,149,92,15,'suffisante'),(191,171,87,15,'sollicite'),(192,193,85,12,'la chaussure'),(434,186,92,15,'La butée'),(445,208,80,15,'libère l’avant'),(454,230,81,12,'de la chaussure'),(465,252,85,12,'sur un côté :'),(475,274,80,15,'à gauche'),(475,296,112,12,'ou à droite.')]: labelbox(x,y,w,h,line)
 else:
  for x,y,w,h,line in [(44,48,92,15,'Basculement'),(41,70,98,12,'du skieur'),(47,92,87,15,'vers'),(48,114,85,12,'l’avant'),(356,21,113,12,'La talonnière'),(347,43,137,15,'s’ouvre : le talon'),(338,65,153,15,'monte et les'),(348,87,137,16,'freins peuvent'),(340,109,151,12,'se déployer.')]:labelbox(x,y,w,h,line)
 txt(34,426,'Illustration de principe : fixation alpine générique, non spécifique à la NX12.',7,'Helvetica',purple)
 y=458
 for number,t,d in steps:
  rect(24,y,27,27,purple);txt(33,y+5,number,13,'Helvetica-Bold','#FFFFFF')
  txt(62,y,t,13,'Helvetica-Bold');para(62,y+20,d,500,11);y+=61
 rect(24,650,547,76,'#F2EFF7');txt(36,660,title,13,'Times-Bold');para(36,682,body,521,10.5)
 rect(24,738,547,39,'#FCF0E9');txt(36,743,'À retenir',10,'Helvetica-Bold',coral);para(36,758,remember,520,9)
 para(24,787,quote,547,10)
 txt(24,820,'Illustrations : Mechanics of Sport / Simon Weller • Légendes adaptées en français',6,'Helvetica',purple)
 c.drawImage(ImageReader(str(R/'sources/guide/media/sgd-logo.png')),523,10,width=47,height=28,preserveAspectRatio=True,mask='auto')
 c.showPage()
c.save()
doc=fitz.open(BASE/'declenchements.pdf')
for i,p in enumerate(doc):p.get_pixmap(matrix=fitz.Matrix(2400/W,3394/H),alpha=False).save(str(O/f'page-{34+i}.png'))
print('Created two-page proposal')
