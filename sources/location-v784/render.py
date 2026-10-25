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
(5,'ISOSKI, régler et contrôler','Compléter les données ISOSKI : âge, type de skieur, taille et poids confirmés. Relever le BSL sur la chaussure retenue.\nRégler et contrôler les deux skis. Expliquer le chaussage et le déchaussage.','BSL = LONGUEUR DE SEMELLE, EN MM',PURPLE),
(6,'Encaisser et rassurer','Enregistrer impérativement dans Gingkoia les mesures relevées, les données ISOSKI et les réglages effectués. Finaliser le paiement et rappeler les modalités du retour.\nAu moindre souci, le client peut appeler ou revenir pour trouver un matériel mieux adapté.','GINGKOIA : TOUT ENREGISTRER EN CAISSE',GREEN)]

for i,(n,t,b,tag,col) in enumerate(steps):step(p,75+(i%2)*1145,1030+(i//2)*580,n,t,b,tag,col)
finish(p,'Un client écouté, un matériel adapté, un départ serein.','Prendre le temps de conseiller et de vérifier le confort. Le client doit savoir qu’il peut compter sur nous si son matériel ne lui convient pas ou s’il a besoin d’un conseil.','« Le matériel doit vous convenir : si quelque chose vous gêne, contactez-nous ou revenez au magasin. »','Parcours magasin SPORT GOOD DEAL • Réglages et contrôles : procédure ISOSKI, notices fabricants et formation pratique.')
