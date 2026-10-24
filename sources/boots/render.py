"""Two HD boot-training posters, genuine manufacturer photos and exact native labels."""
from pathlib import Path
import json,sys
from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'sources/guide'))
import render as common
from render import Page,INK,BODY,TEAL,CORAL,BLUE,WHITE,LINE,DARK,arrow
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
    p.rect((70,990,2330,1660),'#EDF5F6',TEAL,25,5)
    p.text(100,1017,'La largeur au métatarse : le premier réflexe.',57,'serif',INK,width=2180)
    p.text(100,1102,'Mesurer les deux pieds debout, à l’endroit le plus large de l’avant-pied (métatarses). Le « last » indique la largeur du chaussant, en mm, à une pointure de référence.',36,width=1610,leading=43,bottom=1235)
    # Native schematic: forefoot width at the metatarsal heads, not foot length.
    fx,fy=1980,1085
    contour=[(45,0),(78,-15),(115,-13),(151,1),(172,28),(179,61),(172,94),(152,126),(139,161),(143,187),(131,211),(108,224),(80,223),(59,209),(52,186),(60,157),(58,128),(38,94),(26,61),(26,32)]
    p.d.polygon([(fx+x*.6,fy+y*.65) for x,y in contour],fill=WHITE,outline=TEAL,width=3)
    arrow(p,fx+15,fy+42,fx+109,fy+42,CORAL,3,True)
    p.text(fx+62,fy+153,'Métatarses',27,'bold',TEAL,center=True)
    cards=[('LV','Low Volume','≈ 98 mm','Pied plutôt fin',BLUE,'#ECF3F9'),('MV','Medium Volume','≈ 100 mm','Pied de largeur moyenne',TEAL,'#EDF5F6'),('HV','High Volume','≈ 102 mm et +','Pied plutôt large',CORAL,'#FCF0E9')]
    for i,(tag,name,last,client,color,soft) in enumerate(cards):
        x=100+i*750;p.accent=color
        p.rect((x,1280,x+710,1500),WHITE,color,19,3)
        p.text(x+23,1301,tag,60,'serif',color)
        p.text(x+145,1310,name,29,'bold',INK)
        p.text(x+23,1373,last,53,'bold',color,width=660)
        p.text(x+23,1450,client,32,width=660)
    p.accent=TEAL
    p.text(100,1521,'Repères usuels, pas des normes : comparer à la même pointure de référence. Selon la gamme, on trouve aussi du 96, 104 mm… Vérifier le tableau fabricant.',30,width=2190,leading=35,bottom=1592)
    p.rect((91,1600,2309,1647),DARK,None,12)
    p.text(115,1610,'Pied large ≠ pied long : changer de volume, pas prendre une pointure de trop. Contrôler aussi cou-de-pied et talon.',30,'bold',WHITE,width=2160,bottom=1647)

    p.rect((70,1690,2330,1955),WHITE,LINE,22,3)
    p.text(100,1710,'Le flex : un soutien que le skieur peut utiliser.',46,'serif',INK,width=2200)
    for i,(number,label,color) in enumerate([('60–90','Souple / découverte',BLUE),('90–110','Intermédiaire / polyvalent',TEAL),('110–130+','Rigide / appuis puissants',CORAL)]):
        x=100+i*750;p.text(x,1780,number,48,'serif',color)
        p.text(x+265,1785,label,29,'bold',INK,width=420,leading=33,bottom=1852)
    p.text(100,1860,'Plus le chiffre monte, plus la chaussure résiste vers l’avant. Trop rigide : fatigue, flexion difficile. Trop souple : manque de soutien.',31,width=2190,leading=36,bottom=1934)
    p.text(100,1910,'Repères adultes : adapter au gabarit, au niveau et à la mobilité. Flex non normé ; sensation plus ferme au froid.',28,width=2200,bottom=1950)
    for x,title,color,soft,items in [
      (70,'Trop petite / trop serrée',CORAL,'#FCF0E9',[
       'Orteils comprimés ou recroquevillés, pression persistante même en flexion.',
       'Douleurs, engourdissements et pieds froids si la compression est excessive.',
       'Changer longueur ou forme selon le problème ; ne pas promettre « ça se fera ».']),
      (1220,'Trop grande',BLUE,'#ECF3F9',[
       'Talon qui se soulève, pied qui glisse : appuis retardés et perte de précision.',
       'Frottements / ampoules ; les orteils peuvent buter à l’avant quand le pied glisse.',
       'Serrer à fond écrase le pied sans rattraper une coque trop longue ou trop volumineuse.'])]:
        p.accent=color;p.rect((x,1985,x+1110,2330),soft,color,22,3)
        p.text(x+29,2004,title,47,'serif',INK,width=1050)
        end=p.bullets(x+30,2073,items,1045,31,4)
        assert end<2322,(title,end)
    p.accent=TEAL;p.rect((70,2360,2330,2640),WHITE,TEAL,24,3)
    p.text(100,2377,'Longueur et essayage : valider le maintien.',44,'serif',INK)
    p.text(100,2442,'Mondopoint = longueur du pied en cm : 26,5 cm → base d’essai 26.5. La pointure de ville ne suffit pas.',31,width=2190,bottom=2485)
    p.text(100,2495,'Chaussette fine ; talon calé. Debout, les orteils peuvent effleurer l’avant ; en flexion, ils reculent. Talon tenu, orteils mobiles : jamais écrasés, jamais de pied qui flotte.',32,width=2190,leading=37,bottom=2575)
    p.text(100,2574,'Essayer plusieurs minutes. Point dur : autre forme / volume ou atelier. Thermoformage et semelle peuvent affiner le confort, sans corriger une coque trop grande.',30,width=2190,leading=35,bottom=2637)
    p.accent=BLUE
    p.rect((70,2670,2330,2915),'#ECF3F9',None,22)
    lower=[('Semelle et fixation','Alpin : ISO 5355. GripWalk : ISO 23223, avec fixation compatible. GripWalk facilite la marche ; ce n’est pas une fonction randonnée.'),('BSL : le chiffre en mm','Longueur extérieure gravée sur la coque, différente du Mondopoint. Même pointure ≠ même BSL : faire vérifier le réglage des fixations.'),('En vente et en location','Contrôler coque, fermetures, chausson et usure des semelles. Sécher sans chaleur forte. Réglages / contrôles : voir pages 25–26.')]
    for i,(title,body) in enumerate(lower):
        x=100+i*750;p.text(x,2690,title,35,'bold',INK,width=690)
        p.text(x,2745,body,30,width=690,leading=35,bottom=2907)
    p.remember('Le bon volume : un pied tenu, sans compression.','Longueur en Mondopoint + largeur au métatarse + cou-de-pied et talon. Essayer le bon LV / MV / HV avant de choisir le flex. Ne jamais surtailler pour loger un pied large.')
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
