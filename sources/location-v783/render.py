from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
src=ROOT/'sources/final-polish-v781/render.py'
ns={'__file__':str(src)};exec(src.read_text().split('# PAGE 3:')[0],ns)
globals().update({k:v for k,v in ns.items() if k not in ['__file__','HERE','OUT','ROOT','ns']})
OUT=HERE/'pages';OUT.mkdir(exist_ok=True);ns['OUT']=OUT
# Functions share the original rendering namespace.
def hero(p,file,title,body):
 p.photo(str(ROOT/'sources/closing-proposals/media'/file),(75,545,1430,985))
 card(p,(1470,560,2325,955),'#EDF6F4')
 yy=text(p,1505,590,title,52,775,'serif',INK)+28
 text(p,1505,yy,body,41,775,bottom=930)
def step(p,x,y,n,title,body,tag,col):
 w=1105;h=550;soft={BLUE:'#ECF3F9',GREEN:'#EDF6F4',CORAL:'#FCF0E9',PURPLE:SOFT}[col]
 card(p,(x,y,x+w,y+h),soft);num(p,x+50,y+52,n,color=col)
 yy=text(p,x+105,y+26,title,48,960,'serif',INK)+26
 text(p,x+32,yy,body,40,1040,bottom=y+h-105)
 p.rect((x+22,y+h-85,x+w-22,y+h-22),col,None,12);text(p,x+40,y+h-72,tag,29,1020,'bold',WHITE,bottom=y+h-28)
p=head(41,'Bien accueillir, ','bien équiper.','Du premier échange au passage en caisse : avancer dans le bon ordre.','LE PARCOURS LOCATION · AVANT LE DÉPART')
hero(p,'accueil.png','Le séjour commence par un bon accueil.','Accueillir avec le sourire, échanger sur les vacances et prendre le temps d’écouter. Mettre le client à l’aise dès son arrivée.')
steps=[
(1,'Cerner le profil du skieur','Demander son niveau, sa taille, son poids et sa fréquence de pratique. Faire préciser son aisance réelle et son style de ski.\nCes informations orientent le choix du matériel.','GABARIT · NIVEAU · PRATIQUE',BLUE),
(2,'Comprendre le programme','Où va-t-il skier et combien de jours ? Piste, bord de piste, hors-piste : faire préciser la répartition prévue et le terrain.\nQu’attend-il de son matériel pour ce séjour ?','DESTINATION · TERRAIN · DURÉE',GREEN),
(3,'Faire essayer les chaussures','Essayer les deux pieds avec les chaussettes de ski. Ajuster la languette, fermer progressivement et faire fléchir.\nVérifier le maintien du talon et l’absence de douleur localisée.','VALIDER LES CHAUSSURES AVANT LA SUITE',CORAL),
(4,'Choisir les skis et les bâtons','Proposer les skis et les bâtons adaptés au terrain, au gabarit et aux attentes. Expliquer le choix.\nVérifier la compatibilité entre les chaussures retenues et les fixations.','UN ENSEMBLE COHÉRENT POUR CE CLIENT',BLUE),
(5,'ISOSKI, régler et contrôler','Compléter les données ISOSKI : âge, type de skieur, taille et poids confirmés. Relever le BSL sur la chaussure retenue.\nRégler et contrôler les deux skis. Montrer le chaussage et le déchaussage, puis faire essayer.','BSL = LONGUEUR DE SEMELLE, EN MM',PURPLE),
(6,'Encaisser et rassurer','Enregistrer impérativement dans Gingkoia les mesures relevées, les données ISOSKI et les réglages effectués. Finaliser le paiement et rappeler les modalités du retour.\nAu moindre souci, le client peut appeler ou revenir pour trouver un matériel mieux adapté.','GINGKOIA : TOUT ENREGISTRER EN CAISSE',GREEN)]

for i,(n,t,b,tag,col) in enumerate(steps):step(p,75+(i%2)*1145,1030+(i//2)*580,n,t,b,tag,col)
finish(p,'Un client écouté, un matériel adapté, un départ serein.','Prendre le temps d’essayer, expliquer le choix et vérifier le confort. Le client doit se sentir bien équipé et savoir qu’il peut compter sur nous.','« Le matériel doit vous convenir : si quelque chose vous gêne, contactez-nous ou revenez au magasin. »','Parcours magasin SPORT GOOD DEAL • Réglages et contrôles : procédure ISOSKI, notices fabricants et formation pratique.')
# Return page: client conversation and internal material flow, no departure repetition.
p=head(42,'Au retour, ','bien réceptionner.','Écouter le client, valoriser son expérience et préparer le matériel pour la suite.','LE PARCOURS LOCATION · LE RETOUR AU MAGASIN')
hero(p,'retour.png','Deux objectifs au retour.','Recueillir ce que le client a vécu, puis orienter chaque équipement vers le bon traitement en atelier.')
for x,t,col,soft in [(75,'AVEC LE CLIENT',GREEN,'#EDF6F4'),(1220,'EN INTERNE : LE MATÉRIEL',BLUE,'#ECF3F9')]:
 card(p,(x,1030,x+1105,2760),soft);strip(p,(x+20,1050,x+1085,1140),t,col)
def item(p,x,y,n,title,body,col=GREEN):
 num(p,x+28,y+25,n,r=27,color=col);yy=text(p,x+78,y,title,46,940,'serif',INK)+22
 yy=text(p,x+10,yy,body,40,1010)
 return yy+45
y=item(p,110,1190,1,'Écouter son expérience','« Tout s’est bien passé ? » Faire préciser le confort des chaussures et le comportement des skis. Écouter les difficultés, incidents ou anomalies, même si rien ne paraît cassé.')
y=item(p,110,y,2,'Garder une trace utile','Noter le matériel concerné et les circonstances de chaque problème. Consigner aussi les références, tailles et modèles appréciés pour retrouver ses préférences lors d’une prochaine visite.')
card(p,(100,y,1155,2715),'white');strip(p,(120,y+20,1135,y+105),'LE MATÉRIEL LUI A PLU ? IL PEUT L’ACHETER.',CORAL)
yy=text(p,140,y+145,'Proposer de garder ce qu’il a aimé.',49,960,'serif',INK)+26
yy=text(p,140,yy,'Skis, chaussures et bâtons : il peut acheter l’ensemble ou seulement une partie, par exemple ses skis ou ses chaussures.',42,950)+35
p.rect((135,yy,1120,yy+240),'#FCF0E9',None,16)
text(p,160,yy+28,'Déduire du prix d’achat la location déjà payée sur le matériel qu’il achète.',44,905,'bold',CORAL,bottom=yy+220)
assert yy+240<2690,yy
text(p,145,yy+285,'Exemple : le client achète uniquement ses chaussures. Déduire la location déjà payée pour ses chaussures.',36,940,bottom=2690)
# Six concise internal steps, maintaining the same readable body size.
def internal(y,n,title,body,col=BLUE):
 x=1255
 num(p,x+28,y+24,n,r=27,color=col)
 yy=text(p,x+78,y,title,44,940,'serif',INK)+17
 yy=text(p,x+10,yy,body,39,1010)
 return yy+30
y=internal(1180,1,'Examiner les deux skis','Vérifier semelles, carres, structure et fixations : impacts, fissures, déformations, pièces abîmées. Tenir compte des remarques du client.')
y=internal(y,2,'Identifier et signaler','Étiqueter l’anomalie sur le ski, mettre le matériel à part et prévenir le responsable d’atelier en précisant les faits.',CORAL)
y=internal(y,3,'Sécher les skis','Même sans anomalie, sécher soigneusement les skis, notamment les carres, pour éviter la rouille.')
y=internal(y,4,'Transmettre à l’atelier','Ramener les skis dans le circuit de reprise et de refartage. Remise à disposition après traitement et contrôles.',GREEN)
y=internal(y,5,'Vérifier et sécher les chaussures','Vérifier leur état et signaler tout problème. Ramener les chaussures sur les sèche-chaussures prévus à cet effet dans l’atelier.')
y=internal(y,6,'Trier et ranger les bâtons','Pliés ou abîmés : demander au chef d’atelier s’ils sont récupérables ou à jeter. En bon état : les réunir avec des élastiques et les remettre en rayon.',GREEN)
assert y<2740,y
finish(p,'Tout retour de skis passe par le circuit atelier.','Anomalie : identifier, isoler et prévenir. Sinon : sécher, transmettre pour reprise et refartage, puis suivre la remise à disposition.','« Vous avez aimé ce matériel ? Vous pouvez l’acheter : nous déduisons la location déjà payée sur les articles conservés. »','Process et offre d’achat SPORT GOOD DEAL • Illustrations de comptoir générées. Le signalement client accompagne le matériel à l’atelier.')
print('Pages 41–42 ready:',OUT)
