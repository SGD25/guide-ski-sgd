"""Two HD boot-training posters, genuine manufacturer photos and exact native labels."""
from pathlib import Path
import json,sys
from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'sources/guide'))
import render as common
from render import Page,INK,BODY,TEAL,CORAL,BLUE,WHITE,LINE,DARK
common.OUT=ROOT/'assets/guide-v767';common.OUT.mkdir(exist_ok=True)
MANIFEST=ROOT/'sources/freeride-freestyle/manifest.json'

def photo(p,name,box):
    im=Image.open(HERE/'media'/name).convert('RGBA')
    if im.getchannel('A').getextrema()[0]==0:bb=im.getchannel('A').getbbox()
    else:bb=im.convert('L').point(lambda v:255 if v<210 else 0).getbbox()
    if bb:
        im=im.crop((max(0,bb[0]-12),max(0,bb[1]-12),min(im.width,bb[2]+12),min(im.height,bb[3]+12)))
    ratio=im.width/im.height
    im=ImageOps.contain(im,(box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS)
    assert abs(im.width/im.height-ratio)<.02
    p.im.paste(im,((box[0]+box[2]-im.width)//2,(box[1]+box[3]-im.height)//2),im)

def step(p,x,y,n,title,body,width=1040,bottom=None):
    p.d.ellipse((x,y,x+48,y+48),fill=p.accent)
    p.text(x+24,y+9,str(n),30,'bold',WHITE,center=True)
    p.text(x+69,y+1,title,33,'bold',INK,width=width-69)
    return p.text(x+69,y+47,body,32,width=width-69,leading=37,bottom=bottom)

def alpine():
    p=Page(19);p.header('Les chaussures alpines.','« Quel est votre niveau, et vos chaussures actuelles vous font-elles mal ? »','02  /  LES FAMILLES')
    p.accent,p.soft=BLUE,'#ECF3F9'
    p.rect((70,440,2330,960),WHITE,BLUE,24,3)
    photo(p,'rossignol-hi-speed.jpg',(100,463,720,850))
    p.text(410,868,'Rossignol Hi-Speed 100 HV GW',31,'bold',INK,center=True)
    p.text(410,914,'Exemple réel : flex 100, volume HV.',27,'sans',BODY,center=True)
    p.text(800,466,'Maintenir le pied, transmettre les appuis.',52,'serif',INK,width=1470)
    anatomy=[('Coque + collier','L’enveloppe rigide tient le pied ; le collier entoure la jambe et accompagne la flexion.'),('Chausson','Il apporte confort et isolation. Sa mousse se tasse avec l’usage : du jeu peut apparaître.'),('Fermetures + strap','Crochets ou BOA règlent le maintien. Serrer plus fort ne corrige pas une mauvaise taille.'),('Semelle','C’est l’interface avec la fixation : type de semelle, longueur extérieure et usure comptent.')]
    for i,(title,body) in enumerate(anatomy):
        y=550+i*96;p.text(800,y,title,33,'bold',BLUE);p.text(800,y+43,body,33,width=1460,leading=39,bottom=y+88)
    p.rect((70,990,2330,1390),WHITE,LINE,24,3)
    p.text(100,1011,'Le flex = la résistance à la flexion vers l’avant.',49,'serif',INK,width=2200)
    p.text(100,1080,'Plus le chiffre monte, plus la chaussure résiste. Chercher un appui progressif que le skieur peut réellement fléchir.',34,width=2190,leading=40,bottom=1124)
    for i,(number,label,color,soft) in enumerate([('60–90','Souple / découverte',BLUE,'#ECF3F9'),('90–110','Intermédiaire / polyvalent',TEAL,'#EDF5F6'),('110–130+','Rigide / appuis puissants',CORAL,'#FCF0E9')]):
        x=95+i*750;p.rect((x,1145,x+710,1250),soft,None,17)
        p.text(x+23,1160,number,53,'serif',color)
        p.text(x+308,1165,label,29,'bold',INK,width=375,leading=34,bottom=1248)
    p.text(100,1270,'Repères adultes larges, à adapter au gabarit, au niveau et à la mobilité. Le flex n’est pas normé ; le froid peut durcir la sensation.',30,width=2200,leading=35,bottom=1308)
    p.text(100,1320,'Trop rigide : flexion difficile, fatigue, appuis en arrière.',31,'bold',BLUE,width=1050,leading=36,bottom=1384)
    p.text(1250,1320,'Trop souple : manque de soutien quand les appuis augmentent.',31,'bold',CORAL,width=1040,leading=36,bottom=1384)
    p.rect((70,1420,2330,1730),'#EDF5F6',None,22)
    p.text(100,1442,'La bonne longueur',44,'serif',INK)
    p.text(100,1510,'Mesurer les deux pieds debout : longueur et largeur. Mondopoint = longueur du pied en cm. Exemple : 26,5 cm → base d’essai 26.5. La pointure de ville ne suffit pas.',34,width=1055,leading=40,bottom=1720)
    p.text(1250,1442,'Le bon volume',44,'serif',INK)
    p.text(1250,1510,'Last = largeur de chaussant à l’avant-pied, à une pointure de référence. Repères : LV ≈ 98 mm, MV ≈ 100, HV ≈ 102 et +. Vérifier aussi cou-de-pied et talon. Pied large ≠ pied plus long !',34,width=1040,leading=40,bottom=1720)
    p.text(100,1685,'Thermoformage du chausson ou semelle interne adaptée : des ajustements à valider avec l’atelier, sans surtailler la coque.',28,width=2200,leading=33,bottom=1720)
    for x,title,color,soft,items in [
      (70,'Trop petite / trop serrée',CORAL,'#FCF0E9',[
       'Orteils comprimés ou recroquevillés, pression persistante même en flexion.',
       'Douleurs, engourdissements et pieds froids si la compression est excessive.',
       'Changer longueur ou forme selon le problème ; ne pas promettre « ça se fera ».']),
      (1220,'Trop grande',BLUE,'#ECF3F9',[
       'Talon qui se soulève, pied qui glisse : appuis retardés et perte de précision.',
       'Frottements / ampoules ; les orteils peuvent buter à l’avant quand le pied glisse.',
       'Serrer à fond écrase le pied sans rattraper une coque trop longue ou trop volumineuse.'])]:
        p.accent=color;p.rect((x,1760,x+1110,2180),soft,color,22,3)
        p.text(x+29,1783,title,48,'serif',INK,width=1050)
        end=p.bullets(x+30,1860,items,1045,34,16)
        assert end<2170,(title,end)
    p.accent=TEAL;p.rect((70,2210,2330,2640),WHITE,TEAL,24,3)
    p.text(100,2232,'Un essayage en quatre temps.',49,'serif',INK)
    steps=[(100,2300,'Chausser proprement.','Une chaussette fine, sans pli. Caler le talon ; serrer progressivement, sans écraser.'),(1250,2300,'Tester debout, puis fléchir.','Debout, les orteils peuvent effleurer l’avant ; en flexion, ils reculent. Jamais écrasés.'),(100,2430,'Vérifier le maintien.','Le talon reste tenu en flexion ; orteils mobiles, sans douleur ni engourdissement.'),(1250,2430,'Prendre le temps.','Essayer plusieurs minutes. Si point dur : autre modèle / volume ou avis de l’atelier.')]
    for i,(x,y,title,body) in enumerate(steps):step(p,x,y,i+1,title,body,1040,y+125)
    p.rect((90,2570,2310,2625),DARK,None,13)
    p.text(113,2582,'À dire au client : « Je cherche à bien vous maintenir, sans vous écraser le pied. »',31,'bold',WHITE,width=2170,leading=36,bottom=2620)
    p.accent=BLUE
    p.rect((70,2670,2330,2915),'#ECF3F9',None,22)
    lower=[('Semelle et fixation','Alpin : ISO 5355. GripWalk : ISO 23223, avec fixation compatible. GripWalk facilite la marche ; ce n’est pas une fonction randonnée.'),('BSL : le chiffre en mm','Longueur extérieure gravée sur la coque, différente du Mondopoint. Même pointure ≠ même BSL : faire vérifier le réglage des fixations.'),('En vente et en location','Contrôler coque, fermetures, chausson et usure des semelles. Sécher sans chaleur forte. Réglages / contrôles : voir pages 25–26.')]
    for i,(title,body) in enumerate(lower):
        x=100+i*750;p.text(x,2690,title,35,'bold',INK,width=690)
        p.text(x,2745,body,30,width=690,leading=35,bottom=2907)
    p.remember('Ajustée, jamais douloureuse ; maintenue, jamais flottante.','La bonne chaussure bloque le talon sans écraser les orteils. Vérifier longueur, largeur et volume ; choisir ensuite un flex que le skieur peut réellement utiliser.')
    p.footer('Flex et largeurs : repères, pas prescriptions universelles. Le last varie avec la pointure et le modèle ; LV / MV / HV ne sont pas des niveaux. Sources : Rossignol, Salomon, Atomic, Tyrolia. Photo : Rossignol.')
    p.link((70,3230,2000,3318),25,"Sécurité et réglage des fixations")
    return p

def touring():
    p=Page(20);p.header('Les chaussures de rando.','« Quelle est votre priorité : monter léger ou privilégier la descente ? »','02  /  LES FAMILLES')
    p.accent=TEAL
    p.rect((70,440,2330,1060),WHITE,TEAL,24,3)
    photo(p,'maestrale-0.png',(100,475,630,965))
    photo(p,'maestrale-3.png',(665,490,1050,935))
    p.text(560,980,'SCARPA Maestrale — vrai modèle de randonnée',29,'bold',INK,center=True)
    p.text(560,1025,'Collier articulé ; mécanisme ski / marche visible au dos.',25,'sans',BODY,center=True)
    p.rect((1100,465,2305,730),'#ECF3F9',None,20)
    p.text(1130,486,'MARCHE / montée',54,'serif',INK)
    p.text(1130,562,'Déverrouiller le collier : la jambe avance et recule plus librement pour allonger le pas. Régler les fermetures selon la notice, en gardant le pied tenu.',36,width=1135,leading=43,bottom=725)
    p.rect((1100,755,2305,1040),'#EDF5F6',None,20)
    p.text(1130,778,'SKI / descente',54,'serif',INK)
    p.text(1130,855,'Verrouiller le mécanisme, refermer les crochets et le strap selon la notice. Le collier soutient alors les appuis. Contrôler le verrouillage avant la descente.',36,width=1135,leading=43,bottom=1034)
    p.rect((70,1090,2330,1450),WHITE,LINE,24,3)
    p.text(100,1110,'Légèreté à la montée, soutien à la descente.',50,'serif',INK,width=2200)
    p.text(100,1180,'Priorité montée / dénivelé',36,'bold',BLUE,width=1050)
    p.text(100,1235,'Coque, chausson et fermetures allégés ; grand débattement pour une marche plus naturelle. À construction plus légère, moins d’amorti et parfois moins de soutien en neige difficile.',34,width=1050,leading=40,bottom=1400)
    p.text(1250,1180,'Priorité descente / freerando',36,'bold',CORAL,width=1040)
    p.text(1250,1235,'Plus de renforts et de maintien pour piloter les skis, souvent plus de masse à remonter. Accorder le niveau de soutien de la chaussure au ski, au gabarit et aux appuis du client.',34,width=1040,leading=40,bottom=1400)
    p.text(100,1405,'Comparer le poids par chaussure, dans la pointure indiquée. Semelle crantée / caoutchouc : meilleure adhérence à pied, selon le terrain.',28,width=2200,leading=33,bottom=1442)
    p.rect((70,1480,2330,1815),'#EDF5F6',None,22)
    p.text(100,1500,'Le chaussant doit réussir deux tests.',48,'serif',INK)
    p.text(100,1570,'En marchant',35,'bold',BLUE)
    p.text(100,1620,'Faire plusieurs pas en mode marche. Orteils sans butée répétée, talon calé, pas de point dur ni frottement anormal. Pas de pointure en plus automatique « pour la montée ».',34,width=1050,leading=40,bottom=1785)
    p.text(1250,1570,'En position ski',35,'bold',TEAL)
    p.text(1250,1620,'Verrouiller puis fléchir : talon maintenu, pied stable, orteils non comprimés. Le chausson peut se tasser ; le thermoformage affine le fit, sans corriger une mauvaise taille de coque.',34,width=1040,leading=40,bottom=1785)
    p.text(100,1775,'Le flex reste non normé. Les degrés de débattement ne disent pas tout de la facilité de marche : il faut essayer.',28,width=2200,leading=33,bottom=1810)
    p.rect((70,1845,2330,2400),WHITE,CORAL,24,3)
    p.text(100,1866,'Compatibilité : regarder sous la chaussure.',49,'serif',INK,width=2200)
    p.text(100,1930,'Inserts tech = logements métalliques pour les pins. Mode marche ≠ compatibilité automatique.',33,'bold',CORAL,width=2200)
    norms=[('Alpin / ISO 5355','Semelle alpine. Sans inserts tech : pas de montée sur une fixation à pins. Certaines fixations à cadre acceptent l’alpin : vérifier la notice.',BLUE),('GripWalk / ISO 23223','Semelle favorisant la marche, avec fixation compatible. Le logo GW ne garantit ni inserts tech, ni mécanisme adapté à de longues montées.',TEAL),('Touring / ISO 9523','Semelle de randonnée, souvent crantée et arrondie. Pas de compatibilité automatique avec une fixation alpine ou simplement marquée GW.',CORAL)]
    for i,(title,body,c) in enumerate(norms):
        y=1990+i*102
        p.rect((95,y,550,y+84),'#F3F6F6',None,13)
        p.text(120,y+23,title,31,'bold',c,width=410,leading=35,bottom=y+77)
        p.text(585,y+4,body,33,width=1700,leading=39,bottom=y+88)
    p.rect((92,2300,2308,2390),DARK,None,13)
    p.text(114,2310,'Inserts présents ≠ compatibilité garantie : valider les deux fabricants. Fixations hybrides, anciennes semelles WTR ou hors norme : vérifier les modèles exacts avec l’atelier.',30,'bold',WHITE,width=2170,leading=34,bottom=2382)
    p.rect((70,2430,2330,2915),'#FCF0E9',None,22)
    p.text(100,2452,'Avant de confier la paire au client.',49,'serif',INK)
    checks=[('1 / Identifier le matériel','Demander le modèle exact des fixations, le programme et les skis. Relever semelle, inserts et BSL (longueur extérieure en mm). Valider l’ensemble avec l’atelier.'),('2 / Faire manipuler','Le client passe lui-même de marche à ski. Vérifier que le verrouillage fonctionne ; dégager neige / glace si nécessaire. Refermer et tester avant de descendre.'),('3 / Contrôler et entretenir','Vérifier coque, articulations, mécanisme, inserts, semelles et fermetures. Sécher les chaussons doucement, sans chaleur forte ; faire contrôler les pièces usées.')]
    for i,(title,body) in enumerate(checks):
        x=100+i*750;p.text(x,2530,title,34,'bold',INK,width=690)
        p.text(x,2590,body,32,width=690,leading=38,bottom=2825)
    p.rect((90,2830,2310,2898),DARK,None,14)
    p.text(113,2844,'À dire au client : « On valide le confort en marchant, le maintien en ski et la compatibilité de tout le pack. »',30,'bold',WHITE,width=2170,leading=35,bottom=2895)
    p.remember('Deux modes, un seul impératif : le bon maintien.','La légèreté aide à monter, le collier verrouillé aide à skier. Le bon choix doit convenir au pied et au programme, avec une compatibilité chaussure / fixation vérifiée.')
    p.footer('Semelles et inserts : vérifier les notices des modèles exacts, y compris les exceptions et systèmes propriétaires. Réglages et contrôle de sécurité : voir pages 25–26. Sources : SCARPA, Dynafit, Rossignol, Tyrolia. Photos : SCARPA.')
    p.link((70,3230,2000,3318),25,"Sécurité et réglage des fixations")
    return p

if __name__=='__main__':
    common.write_manifest_pages([alpine(),touring()],MANIFEST)
