from pathlib import Path
import sys,io,os
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
util=ROOT/'sources/bindings-v776-revision/render.py'
ns={'__file__':str(util)};exec(util.read_text().split('def pivot_photo')[0],ns)
globals().update({k:v for k,v in ns.items() if k not in ['__file__','BASE','OUT']})
OUT=ROOT.parent/'output/closing-pages';OUT.mkdir(exist_ok=True);ns['OUT']=OUT
M=ROOT/'sources/bindings-v776-revision/media'
def close(p,title,body,quote,source='Proposition de formation magasin • Illustrations de comptoir générées ; photos produit : sources du guide.'):
 finish(p,title,body,quote,source)
def step(p,x,y,w,h,n,title,body,tag=None):
 card(p,(x,y,x+w,y+h));num(p,x+48,y+50,n)
 yy=text(p,x+100,y+23,title,52,w-135,'serif',INK)+26
 yy=text(p,x+32,yy,body,43,w-64,bottom=y+h-95)
 if tag:
  p.rect((x+25,y+h-90,x+w-25,y+h-25),SOFT,None,11);text(p,x+40,y+h-75,tag,31,w-80,'bold',PURPLE,bottom=y+h-30)
def smallstep(p,x,y,w,n,title,body):
 num(p,x+25,y+24,n,r=25);yy=text(p,x+68,y,title,45,w-70,'bold',INK)+16
 return text(p,x+68,yy,body,39,w-78)+33
# 41
p=head(41,'Bien accueillir, ','bien équiper.','Une location réussie commence par les bonnes questions et un véritable essayage.','LE PARCOURS LOCATION · 1 / AVANT LES RÉGLAGES')
p.photo(str(HERE/'media/accueil.png'),(75,540,1585,1250))
card(p,(1620,565,2325,1215),SOFT)
text(p,1660,605,'Écouter avant de choisir.',57,620,'serif',INK)
text(p,1660,780,'Le niveau annoncé est un point de départ. Faire préciser le terrain, la fréquence et l’aisance réelle du client.',46,610,bottom=1150)
step(p,75,1300,1105,680,1,'Comprendre le programme','Où allez-vous skier ? Sur quelles pistes êtes-vous à l’aise ?\nÀ quelle fréquence skiez-vous ?\nQue souhaitez-vous retrouver ou éviter par rapport à votre dernier matériel ?','TERRAIN · EXPÉRIENCE · ATTENTES')
step(p,1220,1300,1105,680,2,'Recueillir les données','Renseigner les données utiles au réglage : poids, taille, âge, type de skieur et BSL.\nLe BSL est la longueur extérieure de la semelle, en mm : ce n’est pas la pointure.','INFORMATIONS CONFIRMÉES AVEC LE CLIENT')
step(p,75,2030,1105,680,3,'Faire essayer les chaussures','Faire essayer les deux pieds avec les chaussettes de ski. Positionner la languette, fermer progressivement et faire fléchir.\nDemander : où sentez-vous une gêne ? Le talon bouge-t-il ?','DU MAINTIEN, SANS DOULEUR LOCALISÉE')
step(p,1220,2030,1105,680,4,'Choisir un ensemble cohérent','Choisir les skis et les bâtons selon la pratique, le gabarit et les attentes.\nConfirmer la compatibilité chaussure / fixation avant les réglages. Expliquer simplement le choix proposé.','CHAUSSURES VALIDÉES → MATÉRIEL ADAPTÉ')
close(p,'Un conseil personnalisé, pas un choix automatique.','Écouter, confirmer les données, faire essayer, puis expliquer le matériel retenu.','« Sur quelles pistes êtes-vous à l’aise, et que souhaitez-vous faire pendant votre séjour ? »','Essayage : guides Rossignol et Salomon. Compatibilité : notices du fabricant. Illustration de comptoir générée.')
#42
p=head(42,'Bien faire partir, ','bien réceptionner.','Le départ et le retour font partie de la même prestation.','LE PARCOURS LOCATION · 2 / DÉPART ET RETOUR')
p.photo(str(HERE/'media/retour.png'),(75,540,1585,1250));card(p,(1620,565,2325,1215),SOFT)
text(p,1660,605,'Faire parler le client.',57,620,'serif',INK)
text(p,1660,780,'Un retour de location est aussi une information utile : confort, comportement du matériel, incident ou difficulté rencontrée.',46,610,bottom=1150)
for x,title in [(75,'AVANT LE DÉPART'),(1220,'AU RETOUR')]:
 card(p,(x,1300,x+1105,2720));p.rect((x+20,1320,x+1085,1420),PURPLE,None,14);text(p,x+45,1345,title,42,1010,'bold',WHITE)
y=1470
for n,t,b in [(1,'Régler et contrôler','Effectuer les réglages et contrôles prévus avec les chaussures retenues. Vérifier les deux skis.'),(2,'Montrer, puis faire refaire','Expliquer le chaussage et le déchaussage, semelles débarrassées de la neige. Faire manipuler le client.'),(3,'Donner un point de contact','Douleur, maintien insuffisant ou déchaussages répétés : demander au client de revenir ou de contacter le magasin.'),(4,'Finaliser la location','Compléter la fiche, identifier le matériel et rappeler les modalités du retour.')]:y=smallstep(p,110,y,1025,n,t,b)
assert y<2700,y
y=1470
for n,t,b in [(1,'Écouter le retour','« Tout s’est bien passé ? » Faire préciser le matériel concerné et les circonstances d’un problème.'),(2,'Examiner et signaler','Examiner le matériel. Noter une anomalie ou un incident rapporté, même si rien ne paraît cassé.'),(3,'Orienter le matériel','Mettre à part les éléments nécessitant un contrôle ou une intervention. Prévenir le référent ou l’atelier.'),(4,'Préparer la suite','Séchage, nettoyage et remise en état selon l’organisation du magasin. Remettre en location après les contrôles prévus.')]:y=smallstep(p,1255,y,1025,n,t,b)
assert y<2700,y
close(p,'Le client doit savoir utiliser son matériel et signaler un problème.','Une démonstration suivie d’un essai du client vaut mieux qu’une explication donnée trop vite.','« Montrez-moi comment vous chaussez et déchaussez, pour vérifier que tout est clair. »')
#43
p=head(43,'Les bonnes questions, ','au bon moment.','Quatre situations courantes pour transformer une demande en conseil adapté.','AU COMPTOIR · QUESTIONNER → COMPRENDRE → PROPOSER')
cases=[('Je suis bon skieur.','Où skiez-vous ? À quelle fréquence ? Sur quelles pistes êtes-vous vraiment à l’aise ?','Reformuler la pratique réelle avant de sélectionner le matériel.','Déduire le niveau de l’assurance du client ou de son apparence.'),('Mes chaussures me font mal.','Où précisément ? Dès l’essayage ou après un moment ? Sur un pied ou les deux ?','Reprendre l’essayage : chaussette, languette, fermeture, maintien et forme de chaussure.','Passer automatiquement à une pointure supérieure ou dire « c’est normal ». '),('Mes skis déchaussent trop facilement.','Sur quel ski ? Dans quelles circonstances ? Une chute, de la neige sous la semelle, un problème de chaussage ?','Reprendre les vérifications du matériel, du chaussage et des données de réglage. Passer la main si nécessaire.','Augmenter le DIN sans rechercher la cause du problème.'),('Je veux les mêmes skis que mon ami.','Que vous plaît-il dans ce modèle ? Avez-vous le même gabarit, la même pratique et les mêmes attentes ?','Expliquer ce qui convient au client et proposer une alternative si elle est plus adaptée.','Choisir un ski uniquement parce qu’un proche le recommande.')]
for i,(q,ask,do,avoid) in enumerate(cases):
 y=560+i*550;card(p,(75,y,2325,y+510));p.rect((95,y+18,2305,y+122),SOFT,None,15);num(p,145,y+67,i+1,r=29);text(p,205,y+40,'« '+q+' »',53,2030,'serif',INK)
 text(p,112,y+155,'JE DEMANDE',31,990,'bold',PURPLE);text(p,112,y+210,ask,40,1005,bottom=y+460)
 p.line((1175,y+160,1175,y+470),LINE,3)
 text(p,1220,y+155,'LE BON RÉFLEXE',31,1040,'bold',PURPLE);yy=text(p,1220,y+202,do,39,1050)+18
 text(p,1220,yy,'À éviter : '+avoid,36,1050,fill=CORAL,bottom=y+490)
close(p,'Une phrase du client n’est pas un diagnostic.','Faire préciser les faits, reprendre les vérifications utiles et expliquer la solution proposée.','« Je vais vous poser quelques questions pour comprendre ce qui se passe et vous proposer une solution adaptée. »','Cas pédagogiques proposés pour la formation magasin. Essayage : guides fabricants. Réglages : notices et formation pratique.')
#44
p=head(44,'Un doute ? ','Le bon réflexe.','Repérer une anomalie, transmettre les faits et faire vérifier avant de remettre en location.','AU COMPTOIR · OBSERVER NE SUFFIT PAS À VALIDER LE MATÉRIEL')
for x,n,t,b,col in [(75,1,'Je vérifie','Je reprends les informations, le chaussage et les contrôles que je maîtrise.',PURPLE),(840,2,'Je mets de côté','Si une anomalie reste à contrôler, j’identifie le matériel et je le sépare du parc disponible.',CORAL),(1605,3,'Je passe la main','Je transmets le matériel et les faits au référent ou à l’atelier avant toute remise en location.',INK)]:
 card(p,(x,560,x+720,980),SOFT);num(p,x+51,612,n,color=col);text(p,x+105,582,t,51,590,'serif',INK);text(p,x+35,700,b,40,650,bottom=945)
text(p,78,1030,'Trois zones à regarder de près.',65,2250,'serif',INK)
text(p,78,1125,'Photos de repérage : elles montrent les pièces, pas des exemples de matériel déclaré défectueux.',35,2250)
photoitems=[('boot-sole.png','SEMELLES DES CHAUSSURES','Usure marquée, déformation ou dommage aux zones en contact avec la fixation : faire vérifier.'),('nx-toe.png','BUTÉE ET TALONNIÈRE','Pièce abîmée ou manquante, fissure, jeu inhabituel ou fermeture anormale : mettre à part.'),('nx-perspective.png','FREINS / SKI-STOPS','Frein tordu, bloqué ou qui ne revient pas librement : signaler et faire contrôler.')]
for i,(img,t,b) in enumerate(photoitems):
 x=75+i*765;card(p,(x,1230,x+720,2180));p.photo(str(M/img),(x+25,1270,x+695,1735));text(p,x+32,1780,t,35,660,'bold',PURPLE);text(p,x+32,1890,b,40,655,bottom=2155)
card(p,(75,2240,2325,2730),SOFT)
text(p,112,2275,'Une transmission utile à l’atelier.',58,2160,'serif',INK)
text(p,112,2385,'Identifier le matériel • Décrire le symptôme • Noter les circonstances • Préciser ce qui a été vérifié.',42,2150)
p.rect((112,2505,2288,2680),WHITE,None,14)
text(p,145,2535,'Exemple : « Ski n° 124 : le client signale deux déchaussages du ski droit. Matériel mis à part ; contrôle demandé au référent. »',41,2070,bottom=2655)
close(p,'En cas de doute, faire vérifier avant de remettre au client.','Un contrôle visuel seul ne garantit pas le bon fonctionnement. Le signalement du client compte aussi.','« Je préfère faire vérifier ce point par notre référent avant de vous remettre le matériel. »','Repères visuels : documentation LOOK et photos du guide. Exemples non exhaustifs ; compléter par la formation pratique.')
# Export reviewed pages as one printable proposal.
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
c=canvas.Canvas(str(OUT/'propositions-location-comptoir.pdf'),pagesize=(595.28,841.89))
for n in range(41,45):
 c.drawImage(ImageReader(str(OUT/f'page-{n}.png')),0,0,width=595.28,height=841.89);c.showPage()
c.save()
print('Four proposals and PDF ready:',OUT)
