"""Render the approved guide as complete HD page images.

Pillow typesets exact content; product photographs are only placed proportionally.
The old published pages remain in assets/ and Git history.
"""
from pathlib import Path
import json, math
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[2]
MEDIA = Path(__file__).parent / 'media'
OUT = ROOT / 'assets/guide-v750'
OUT.mkdir(exist_ok=True)
CHECK = Path(__file__).parent / '.cache'
CHECK.mkdir(exist_ok=True)
P = json.loads((ROOT/'design/charte-candidate-sgd.json').read_text())['palette']
W,H = 2400,3394
INK,BODY,TEAL,LINE,PALE,DARK = [P[k] for k in ['titres','texte','accent','filets','encarts_clairs','encarts_forts']]
WHITE='#ffffff'
FONTS=Path('/usr/share/fonts/opentype/urw-base35')
FONT={}
def ft(size,kind='sans'):
    key=(size,kind)
    if key not in FONT:
        name={'sans':'NimbusSans-Regular','bold':'NimbusSans-Bold','serif':'NimbusRoman-Bold','italic':'NimbusRoman-BoldItalic'}[kind]
        FONT[key]=ImageFont.truetype(str(FONTS/(name+'.otf')),size)
    return FONT[key]

class Page:
    def __init__(self,n):
        self.n=n;self.im=Image.new('RGB',(W,H),P['fond']);self.d=ImageDraw.Draw(self.im);self.links=[]
    def rect(self,box,fill=WHITE,outline=LINE,r=22,width=3):
        self.d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)
    def line(self,points,fill=LINE,width=3):self.d.line(points,fill=fill,width=width)
    def text(self,x,y,s,size=36,kind='sans',fill=BODY,width=None,leading=None,center=False,bottom=None):
        f=ft(size,kind);rows=[]
        for paragraph in s.split('\n'):
            row=''
            for word in paragraph.split():
                trial=(row+' '+word).strip()
                if width and self.d.textlength(trial,font=f)>width and row:
                    rows.append(row);row=word
                else:row=trial
            rows.append(row)
        lh=leading or round(size*1.22)
        end=y+len(rows)*lh
        if bottom is not None:assert end<=bottom,(self.n,s[:55],end,bottom)
        for row in rows:
            xx=x-self.d.textlength(row,font=f)/2 if center else x
            assert xx>=0 and xx+self.d.textlength(row,font=f)<=W,(self.n,'horizontal overflow',row)
            self.d.text((round(xx),y),row,font=f,fill=fill,anchor='lt');y+=lh
        return end
    def photo(self,name,box):
        im=Image.open(MEDIA/(name+'.jpg')).convert('RGB')
        im=ImageOps.contain(im,(round(box[2]-box[0]),round(box[3]-box[1])),Image.Resampling.LANCZOS)
        self.im.paste(im,(round((box[0]+box[2]-im.width)/2),round((box[1]+box[3]-im.height)/2)))
    def header(self,title,subtitle,chapter='01  /  COMPRENDRE'):
        self.text(76,48,'CHAPITRE '+chapter,32,'bold',TEAL)
        self.line((700,66,2070,66))
        self.rect((2110,36,2324,102),P['fond'],P['reperes'],12,2)
        self.text(2217,53,f'PAGE {self.n:02}',31,'bold',INK,center=True)
        self.text(76,130,title,113,'serif',INK,bottom=275)
        self.text(78,267,subtitle,40,'sans',TEAL,width=2240,bottom=395)
    def number(self,x,y,n):
        self.d.ellipse((x,y,x+72,y+72),fill=P['reperes'])
        self.text(x+36,y+13,str(n),47,'serif',WHITE,center=True)
    def label(self,x,y,s,width,size=31):
        self.rect((x-10,y-8,x+width+10,y+size+19),PALE,None,10)
        return self.text(x,y+1,s,size,'bold',TEAL)+26
    def bullets(self,x,y,items,width,size=35,gap=16):
        for s in items:
            self.d.ellipse((x,y+12,x+9,y+21),fill=P['reperes'])
            y=self.text(x+25,y,s,size,width=width-25)+gap
        return y
    def remember(self,headline,body):
        y=2945;self.rect((70,y,2330,y+250),PALE,None,25)
        self.rect((70,y,514,y+250),DARK,None,25);self.d.rectangle((480,y,514,y+250),fill=DARK)
        self.text(292,y+91,'À retenir',65,'serif',WHITE,center=True)
        self.text(555,y+24,headline,42,'serif',INK,width=1725,bottom=y+130)
        self.text(555,y+99,body,33,width=1725,leading=43,bottom=y+237)
    def footer(self,note=''):
        if note:self.text(76,3237,note,26,width=2240,bottom=3313)
        self.line((70,3330,2330,3330),P['reperes'],3)
        self.text(76,3351,'SPORT GOOD DEAL  /  GUIDE DU SKI',27,'bold',INK)
        self.text(2325,3350,str(self.n).zfill(2),29,'bold',INK,center=True)
    def link(self,box,page,label):self.links.append({'box':box,'page':page,'label':label})
    def save(self):
        dest=OUT/f'page-{self.n:02}.jpg'
        self.im.save(dest,quality=94,subsampling=0,optimize=True,dpi=(240,240))
        with Image.open(dest) as im:im.verify()
        preview=self.im.copy();preview.thumbnail((1000,1415));preview.save(CHECK/f'page-{self.n:02}.jpg',quality=93)
        return {'page':self.n,'path':str(dest.relative_to(ROOT)),'links':self.links}

def arrow(p,x1,y1,x2,y2,color=TEAL,width=5,both=False):
    p.line((x1,y1,x2,y2),color,width)
    a=math.atan2(y2-y1,x2-x1)
    for x,y,direction in [(x2,y2,a)]+([(x1,y1,a+math.pi)] if both else []):
        p.d.polygon([(x,y),(x-22*math.cos(direction-.48),y-22*math.sin(direction-.48)),(x-22*math.cos(direction+.48),y-22*math.sin(direction+.48))],fill=color)

def ski(p,x,y,w,h,color=INK):
    # Explicit schematic: wider tip/tail and narrower waist.
    pts=[]
    for i in range(101):
        t=i/100;half=w*(.29+.21*abs(2*t-1))
        if t<.04:half*=math.sqrt(max(0,1-((t-.04)/.04)**2))
        if t>.98:half*=.85
        pts.append((x-half,y+t*h))
    pts+= [(2*x-a,b) for a,b in reversed(pts)]
    p.d.polygon(pts,fill=color);p.d.line(pts+[pts[0]],fill=INK,width=3)
    p.line((x,y+40,x,y+h-25),'#ffffff',2)
    p.rect((x-w*.34,y+h*.45,x+w*.34,y+h*.55),'#5E7B87',None,6)

def person(p,x,y,h,color):
    # Flat comparison figure, with constant skier height across the three cases.
    p.d.ellipse((x-49,y,x+49,y+96),fill=INK)
    p.rect((x-42,y+40,x+42,y+69),'#A9CCD3',None,9)
    p.d.polygon([(x-67,y+112),(x+67,y+112),(x+87,y+h*.57),(x-87,y+h*.57)],fill=color)
    p.line((x-60,y+139,x-112,y+h*.52),color,44);p.line((x+60,y+139,x+116,y+h*.51),color,44)
    p.line((x-42,y+h*.56,x-55,y+h-28),INK,65);p.line((x+42,y+h*.56,x+55,y+h-28),INK,65)
    p.rect((x-100,y+h-49,x-16,y+h),DARK,None,12);p.rect((x+16,y+h-49,x+100,y+h),DARK,None,12)
    p.line((x,y+116,x,y+h*.55),'#D6E8EB',3)

def cover():
    p=Page(1);p.im.paste(INK,(0,0,W,H));p.d=ImageDraw.Draw(p.im)
    p.text(110,105,'SPORT GOOD DEAL',46,'bold',WHITE)
    p.text(110,218,'FORMATION VENDEURS & LOUEURS',32,'bold','#ACD6DC')
    p.line((110,312,2290,312),'#628D9B',3)
    p.text(108,460,'Le guide',252,'serif',WHITE)
    p.text(108,750,'du ski.',290,'italic','#A3D4D9')
    p.text(115,1150,'Comprendre le matériel.\nTrouver les mots pour bien conseiller.',54,width=2090,fill=WHITE,leading=73)
    p.photo('montagne',(110,1430,2290,2710))
    for x,n,title,desc in [(110,'01','Comprendre','Les bases du matériel'),(870,'02','Reconnaître','Les familles de skis'),(1630,'03','Conseiller','Des arguments concrets')]:
        p.text(x,2840,n,34,'bold','#A3D4D9');p.text(x,2910,title,59,'serif',WHITE)
        p.text(x,3000,desc,34,fill='#D9EAEE')
    p.line((110,3200,2290,3200),'#628D9B',3)
    p.text(110,3250,'LE MANUEL POUR PRENDRE CONFIANCE EN MAGASIN',30,'bold',WHITE)
    p.text(2290,3250,'01',30,'bold',WHITE,center=True)
    return p

TOPICS=[('Anatomie du ski',3),('Largeur et longueur',4),('Lignes de cotes et rayon',5),('Cambres et rockers',6),('Au cœur du ski',7),('Les familles de skis',8),('Les skis de piste',9),('Exemples de skis de piste',10),('Les skis all-mountain',11),('Exemples all-mountain',12)]
def contents():
    p=Page(2);p.header('Au fil des pages.','Un parcours simple : comprendre le matériel, puis reconnaître les familles.','00  /  LE SOMMAIRE')
    for x,chapter,title,sub,topics in [(70,'01','Comprendre le ski','LES BASES POUR EXPLIQUER',TOPICS[:5]),(1230,'02','Les familles','LES REPÈRES POUR CONSEILLER',TOPICS[5:])]:
        p.rect((x,495,x+1100,2480));p.number(x+38,540,chapter)
        p.text(x+38,670,title,74,'serif',INK)
        p.text(x+40,780,sub,29,'bold',TEAL)
        y=940
        for label,n in topics:
            p.line((x+40,y-35,x+1060,y-35))
            p.text(x+40,y,label,45,'serif',INK,width=800)
            p.rect((x+895,y-10,x+1045,y+70),PALE,None,12)
            p.text(x+970,y+7,f'{n:02}  →',34,'bold',TEAL,center=True)
            p.link((x+25,y-35,x+1075,y+130),n,label);y+=270
    p.rect((70,2570,2330,2865),DARK,None)
    p.text(120,2610,'Un guide à utiliser pendant la vente.',63,'serif',WHITE)
    p.text(120,2713,'Les pages de repères expliquent le matériel. Les exemples donnent des mots et des arguments pour parler au client.',38,fill=WHITE,width=2130)
    p.text(76,3040,'Cliquez sur un sujet pour accéder directement à sa page.',35,fill=TEAL)
    p.footer();return p

def anatomy():
    p=Page(3);p.header('Spatule, patin, talon.','Trois zones pour comprendre la conduite, l’agilité et la portance du ski.')
    p.photo('ski-anatomie',(1090,470,1330,2850))
    blocks=[(70,485,950,1260,'1','Spatule',[('Déjaugeage','Sa forme relevée aide le ski à rester en surface en neige souple.'),('Obstacles','Elle facilite le passage des bosses et des irrégularités.'),('Virages','Sa largeur et sa souplesse participent à l’entrée en courbe.')]),(1430,1130,2330,2300,'2','Patin',[('Sous le pied','C’est la largeur du ski au niveau de la chaussure.'),('Étroit','Le passage d’une carre à l’autre est plus rapide et précis.'),('Large','Il apporte de la portance en neige souple, mais demande plus d’effort pour basculer.')]),(70,1890,950,2865,'3','Talon',[('Sortie de virage','Il guide la fin de courbe et participe à la relance.'),('Stabilité','Il contribue à l’équilibre, notamment quand la vitesse augmente.'),('Selon la pratique','Plutôt plat pour la précision sur piste ; plus relevé pour faciliter le pivot et le ski en marche arrière.')])]
    for x,y,x2,y2,n,title,items in blocks:
        p.rect((x,y,x2,y2));p.number(x+32,y+28,n);p.text(x+130,y+28,title,66,'serif',INK)
        yy=y+152
        for label,body in items:
            yy=p.text(x+38,yy,label,36,'bold',TEAL)+13
            yy=p.text(x+38,yy,body,35,width=x2-x-76)+30
        assert yy<y2-15,(p.n,title,yy,y2)
    for x,y,x2 in [(950,680,1155),(1265,1670,1430),(950,2590,1160)]:
        p.line((x,y,x2,y),TEAL,5);p.d.ellipse((x2-12,y-12,x2+12,y+12),fill=TEAL,outline=WHITE,width=3)
    p.text(1468,2335,'REPÈRES AU PATIN',31,'bold',TEAL)
    p.text(1468,2405,'65–80 mm : piste\n80–95 mm : all-mountain\n95–136 mm : freeride',37,width=810,leading=58)
    p.text(1468,2620,'Des repères indicatifs : les familles se chevauchent.',32,width=780)
    p.remember('Une caractéristique ne raconte pas tout.','Largeur, profil, rigidité et longueur travaillent ensemble.\nOn choisit un ensemble adapté au terrain et au skieur.')
    p.footer('Photo produit : Rossignol. Les repères de largeur sont indicatifs.');return p

def dimensions():
    p=Page(4);p.header('Largeur et longueur.','Deux dimensions qui se combinent : vivacité, facilité, stabilité et portance.')
    p.text(76,435,'01  La largeur au patin',57,'serif',INK)
    cols=[(70,'Fin','65–80 mm',48,INK,['Passage de carre à carre rapide','Moins de portance','Souvent plus facile sur piste']),(838,'Intermédiaire','80–95 mm',70,TEAL,['Un ski plus polyvalent','Compromis piste / hors-piste','Un comportement équilibré']),(1606,'Large','96 mm et +',94,'#648C9C',['Plus de portance en neige souple','Moins vif d’une carre à l’autre','Souvent plus physique sur piste'])]
    for x,name,mm,sw,color,items in cols:
        p.rect((x,550,x+724,1410));p.text(x+34,580,name,55,'serif',INK);p.text(x+34,658,mm,42,'bold',TEAL)
        ski(p,x+100,760,sw,540,color);arrow(p,x+40,1000,x+160,1000,TEAL,both=True)
        p.bullets(x+208,780,items,480,36,30)
    p.rect((70,1450,2330,1565),PALE,None,14)
    p.text(110,1480,'Plus large ≠ meilleur : le bon patin dépend du terrain, du niveau et de la sensation recherchée.',34,width=2150)
    p.text(76,1640,'02  La longueur par rapport au skieur',57,'serif',INK)
    for x,name,delta,sh,col,desc in [(70,'Piste facile','−20 à −10 cm',470,INK,'Accessible, rassurant, petits virages'),(838,'Polyvalent','−10 à −5 cm',520,TEAL,'Le compromis : maniabilité et tenue'),(1606,'Freeride','0 à +15 cm',650,'#648C9C','Portance et stabilité en neige souple')]:
        p.rect((x,1750,x+724,2800));p.text(x+362,1790,name,52,'serif',INK,center=True)
        p.text(x+362,1875,delta,44,'bold',TEAL,center=True)
        base=2625;person(p,x+280,base-600,600,col);ski(p,x+505,base-sh,64,sh,col)
        p.line((x+160,base-600,x+610,base-600),LINE,3)
        if sh!=600:arrow(p,x+610,base-600,x+610,base-sh,TEAL,4,True)
        p.text(x+362,2685,desc,32,width=650,center=True)
    p.remember('La largeur et la longueur se choisissent ensemble.','Court et fin : plus vif et accessible. Long et large : plus de stabilité et de portance.\nCes repères s’ajustent au modèle, au niveau et au gabarit.')
    p.footer('Schémas de comparaison. Longueurs indicatives : à adapter au modèle et à l’usage.');return p

def radius():
    p=Page(5);p.header('Rayon de courbure.','Rayon court : virages serrés. Rayon long : grandes courbes.')
    p.rect((70,440,2330,2180))
    p.photo('ski-anatomie',(255,540,400,2050))
    ox,cy=420,1330
    for r,c in [(440,TEAL),(600,'#487B97'),(800,INK)]:
        cx=ox+r
        for a in range(0,360,8):p.d.arc((cx-r,cy-r,cx+r,cy+r),a,a+4.5,fill=c,width=5)
        p.d.ellipse((cx-12,cy-12,cx+12,cy+12),fill=c,outline=WHITE,width=3)
    arrow(p,ox,cy,2225,cy,INK,4)
    p.d.ellipse((ox-17,cy-17,ox+17,cy+17),fill=TEAL,outline=WHITE,width=5)
    for x,y,r,desc,c in [(695,1060,'R11','Virage serré',TEAL),(1210,890,'R15','Multivirage','#487B97'),(1755,720,'R20+','Grande courbe',INK)]:
        p.rect((x-18,y-12,x+410,y+178),WHITE,None,15)
        p.text(x,y,r,87,'serif',c);p.text(x,y+110,desc,36,'bold',c)
    p.text(580,470,'Le rayon décrit la courbe théorique du ski.',40,'serif',INK)
    boxes=[(70,'Lire les cotes','118 – 95 – 108 mm','Dans l’ordre : spatule, patin, talon. Ici, le patin mesure 95 mm.'),(838,'Lire le rayon','R = 17 m','La mention R ou Radius indique le rayon. Il est donné séparément des cotes.'),(1606,'Trouver l’information','Sur le ski','Cotes et rayon sont souvent imprimés près du talon ou des fixations.')]
    for x,h,b,body in boxes:
        p.rect((x,2240,x+724,2865));p.text(x+34,2275,h,43,'serif',INK)
        p.text(x+34,2380,b,49,'bold',TEAL,width=656)
        p.text(x+34,2520,body,37,width=656,bottom=2825)
    p.remember('Le rayon indique une tendance à tourner.','Court : entrée en courbe vive et virages serrés. Long : grandes courbes.\nLa longueur, le flex et la largeur influencent aussi le comportement réel.')
    p.footer('Schéma pédagogique : les trajectoires réelles dépendent des appuis, de la vitesse et de la neige.');return p

def profiles():
    p=Page(6);p.header('Du classique à l’inversé.','Le profil change le contact avec la neige, l’accroche et la facilité de pivot.')
    data=[('Cambre classique','Le centre du ski est relevé sans charge. Sous l’appui du skieur, le ski se déforme et répartit la pression.',.14,.88,58,76,55),('Rocker en spatule','L’avant se relève plus tôt. Cela facilite la conduite en neige meuble et réduit la longueur de contact.',.29,.88,40,100,55),('Double rocker','La spatule et le talon se relèvent plus tôt. Le ski pivote plus facilement ; les deux rockers peuvent être différents.',.28,.73,35,95,95),('Cambre plat','Peu ou pas de cambre au centre. Une sensation plus directe et un comportement généralement plus permissif.',.12,.88,0,60,60),('Cambre inversé','Le centre touche la neige, les extrémités sont relevées. Un profil très orienté pivot et jeu en neige souple.',.5,.5,0,100,100)]
    for i,(name,desc,cl,cr,cam,front,back) in enumerate(data):
        y=432+i*405;p.rect((70,y,2330,y+380));p.number(100,y+28,i+1)
        p.text(199,y+28,name,49,'serif',INK,width=650)
        p.text(110,y+123,desc,34,width=650,bottom=y+364)
        x0,x1,base=875,2230,y+230
        p.line((x0-30,base+18,x1+30,base+18),LINE,5)
        pts=[]
        for k in range(301):
            t=k/300
            if cl==cr:z=100*(2*t-1)**2
            elif t<cl:z=front*(1-t/cl)**2
            elif t>cr:z=back*((t-cr)/(1-cr))**2
            else:z=cam*math.sin(math.pi*(t-cl)/(cr-cl))**2
            pts.append((x0+(x1-x0)*t,base-z))
        p.d.polygon(pts+[(x,yy+18) for x,yy in reversed(pts)],fill='#8FBAC6')
        p.d.line(pts,fill=INK,width=5);p.d.line([(x,yy+18) for x,yy in pts],fill=INK,width=4)
        xa=x0+(x1-x0)*cl;xb=x0+(x1-x0)*cr
        if cl!=cr:
            for xx in [xa,xb]:p.line((xx,base+15,xx,base+103),TEAL,3)
            arrow(p,xa,base+68,xb,base+68,TEAL,4,True)
            p.text((xa+xb)/2,base+105,'zone de contact',28,'bold',TEAL,center=True)
        else:p.text((x0+x1)/2,base+78,'contact plus centré • pivot facilité',31,'bold',TEAL,center=True)
        if i in [1,2]:p.text(x0+15,y+30,'ROCKER AVANT',27,'bold',TEAL)
        if i==2:p.text(x1-280,y+30,'ROCKER ARRIÈRE',27,'bold',TEAL)
    p.rect((70,2520,2330,2870),PALE,None)
    short=[('Classique','Dynamisme, accroche et puissance ; plus exigeant.'),('Rocker avant','Garde du soutien, facilite l’entrée de virage.'),('Double rocker','Plus de pivot, plus joueur et maniable.'),('Plat','Plus permissif ; moins d’accroche à fort appui.'),('Inversé','Très facile à pivoter ; moins à l’aise sur neige dure.')]
    for i,(a,b) in enumerate(short):
        x=102+i*447;p.text(x,2558,a,38,'serif',INK,width=405)
        p.text(x,2650,b,30,width=405,bottom=2845)
    p.remember('Du soutien vers davantage de pivot.','Vers l’inversé, on gagne généralement en tolérance et en jouabilité.\nSur neige dure, le cambre classique apporte davantage d’accroche et de puissance.')
    p.footer('Profils schématiques, sans charge. Le comportement dépend aussi de la construction et des dimensions.');return p

def construction():
    p=Page(7);p.header('Ce qui se cache à l’intérieur.','Renforts, noyau, carres et semelle : chaque assemblage crée un compromis.')
    for x,n,h,desc,img in [(70,1,'Une construction simple','Un exemple léger et tolérant, avec un noyau injecté en mousse.','construction-mousse'),(1230,2,'Une structure renforcée','Un exemple plus structuré : bois, fibres et renfort métallique.','construction-bois')]:
        p.rect((x,432,x+1100,2000));p.number(x+28,465,n)
        p.text(x+30,575,h,53,'serif',INK,width=1040)
        p.text(x+30,675,desc,36,width=1030)
        p.photo(img,(x+20,860,x+1080,1950))
    mats=[(70,2070,'Bois','Flex progressif, variable selon l’essence et l’usinage.'),(1230,2070,'Mousse / composite','Des solutions diverses, souvent choisies pour le poids et le coût.'),(70,2325,'Fibre de verre','Un renfort très courant dans les constructions de skis.'),(1230,2325,'Carbone / titanal','Modifient précision, masse et amortissement selon leur intégration.')]
    for x,y,h,body in mats:
        p.rect((x,y,x+1100,y+220),PALE,None);p.text(x+30,y+25,h,49,'serif',INK)
        p.text(x+30,y+99,body,34,width=1030,bottom=y+207)
    for i,(h,b) in enumerate([('Souple / tolérant','Rassurant, facile à déformer.'),('Équilibré','Confort, tenue et facilité.'),('Tonique / précis','Plus de répondant sous l’appui.'),('Rigide / exigeant','Stable et précis, plus physique.')]):
        x=70+i*580;p.rect((x,2630,x+520,2875));p.text(x+24,2660,h,39,'serif',INK,width=475)
        p.text(x+24,2760,b,31,width=475,bottom=2865)
    p.remember('Adapter la construction au skieur.','Un ski trop rigide peut fatiguer et freiner la progression.\nLe noyau seul ne suffit pas : un ski en bois peut aussi être accessible et tolérant.')
    p.footer('Illustrations de construction reprises du guide validé. Deux exemples, sans règle absolue liée au seul noyau.');return p

def families():
    p=Page(8);p.header('Les familles de skis.','Chaque famille répond à un terrain, à un niveau et à une envie de glisse.','02  /  LES FAMILLES')
    for x,n,h,desc,img,page in [(70,1,'Les skis de piste','Précis, rassurants et efficaces sur piste damée.','piste-facile',9),(1230,2,'Les skis all-mountain','Polyvalents : de la priorité piste au mélange piste / neige souple.','allmountain-7030',11)]:
        p.rect((x,432,x+1100,1550));p.number(x+32,470,n)
        p.text(x+32,585,h,66,'serif',INK)
        p.photo(img,(x+25,710,x+1075,1150))
        p.text(x+32,1200,desc,40,width=1025)
        p.rect((x+32,1405,x+1068,1503),DARK,None,14)
        p.text(x+70,1432,f'Découvrir la famille  /  page {page:02}  →',36,'bold',WHITE)
        p.link((x,432,x+1100,1550),page,h)
    cards=[(70,'03','Freeride','Plus larges, avec de la portance en neige profonde.','NEIGE SOUPLE'),(838,'04','Freestyle','Du jeu, des figures, du park et des profils adaptés.','PARK & CRÉATIVITÉ'),(1606,'05','Randonnée','Légèreté à la montée, compromis pour la descente.','MONTÉE & DESCENTE')]
    for x,n,h,body,tag in cards:
        p.rect((x,1640,x+724,2640));p.number(x+30,1680,n)
        # Schematic mountain motif; no fabricated product imagery.
        p.d.polygon([(x+80,2050),(x+270,1820),(x+390,1970),(x+500,1845),(x+650,2050)],fill=PALE)
        p.line((x+80,2050,x+270,1820,x+390,1970,x+500,1845,x+650,2050),TEAL,8)
        p.text(x+35,2120,h,66,'serif',INK)
        p.text(x+35,2220,body,38,width=654)
        p.text(x+35,2460,tag,29,'bold',TEAL,width=654)
        p.text(x+35,2530,'À venir',33,'bold',BODY)
    p.remember('Commencer par le terrain et la pratique réelle.','La famille donne une direction. Le niveau, le gabarit et les sensations recherchées\npermettent ensuite d’affiner le choix du modèle.')
    p.footer('Les exemples de modèles complètent les familles : skis de piste page 10, all-mountain page 12.');return p

PISTE=[
 ('Piste facile','Accessible et tolérant, pour progresser en confiance.','piste-facile',[('Patin','Environ 70–75 mm'),('Longueur','Environ −20 à −15 cm'),('Rayon','Court, environ 10 à 12 m'),('Public','Débutant, skieur qui appréhende')],['Déclenchement facile','Virages courts à moyens','Rassurant et peu physique']),
 ('Piste polyvalent','Le compromis pour skier toute la journée sur piste.','piste-polyvalent',[('Patin','Environ 75–85 mm'),('Longueur','Environ −10 cm'),('Rayon','Autour de 15 m'),('Construction','Plus tonique qu’un piste facile'),('Public','Skieur loisir à l’aise, cherchant polyvalence et stabilité')],['Bon équilibre facilité / tenue','Un peu de bord de piste','Plus complet, un peu plus exigeant']),
 ('Piste performance','Plus nerveux et accrocheur, pour un skieur sportif.','piste-performance',[('Patin','Généralement 70–80 mm'),('Longueur','Environ −10 à −5 cm'),('Rayon','Variable selon la pratique'),('Public','Bon skieur recherchant la précision')],['Plus de répondant','Plus d’accroche et de précision','Bonne tenue sur neige ferme'])]
def piste():
    p=Page(9);p.header('Les skis de piste.','Quatre approches : de la facilité d’apprentissage à la précision sportive.','02  /  LES FAMILLES')
    for i,(h,sub,img,rows,pros) in enumerate(PISTE):
        x=70+(i%2)*1160;y=432+(i//2)*1250;cw=1100
        p.rect((x,y,x+cw,y+1210));p.number(x+28,y+25,i+1)
        p.text(x+125,y+29,h,57,'serif',INK)
        p.text(x+30,y+128,sub,34,width=1040)
        p.photo(img,(x+25,y+235,x+1075,y+650))
        yy=y+695
        for label,value in rows:
            p.text(x+32,yy,label,32,'bold',TEAL)
            end=p.text(x+255,yy,value,33,width=808)
            yy=max(yy+57,end+12)
        p.line((x+30,yy+7,x+1070,yy+7));p.bullets(x+33,yy+32,pros,1032,33,8)
    x,y=1230,1682;p.rect((x,y,x+1100,y+1210));p.number(x+28,y+25,4)
    p.text(x+125,y+29,'Spécialités piste',57,'serif',INK)
    p.text(x+30,y+128,'Des skis ciblés pour une pratique technique et engagée.',34,width=1040)
    p.photo('piste-specialiste',(x+25,y+235,x+1075,y+505))
    for xx,h,rows,pros in [(x+30,'Slalom',[('Patin','Environ 65–68 mm'),('Longueur','Courte, souvent < 170 cm')],['Très vif, rayons courts','Passage de carre rapide']),(x+580,'Géant / grandes courbes',[('Patin','Fin à intermédiaire'),('Longueur','Souvent à la taille du skieur')],['Rayon environ 18–20 m','Plus stable, usage exigeant'])]:
        p.text(xx,y+555,h,42,'serif',INK,width=485)
        yy=y+675
        for label,value in rows:
            yy=p.text(xx,yy,label,31,'bold',TEAL)+12
            yy=p.text(xx,yy,value,33,width=480)+25
        p.bullets(xx,yy+15,pros,480,32,15)
    p.text(x+32,y+1105,'Pour des skieurs experts : précision et technique.',31,'bold',TEAL,width=1036)
    p.remember('Tous les skis de piste ne recherchent pas la même sensation.','Facilité, accroche, réactivité ou performance : partir du niveau réel du client,\nde son rythme et du type de virages qu’il aime enchaîner.')
    p.footer('Repères de longueur par rapport à la taille du skieur. À ajuster au modèle, au niveau et au gabarit.');return p

PRODUCTS=[
 {'h':'Ski facile','name':'HEAD\nEasy Joy','img':'head-easy-joy','position':'Skieuse débutante, en phase d’apprentissage. Un ski qui met en confiance et facilite la progression.','maker':'Un ski indulgent, facile à contrôler, stable à faible vitesse et qui pardonne les petites erreurs.','words':['Facile','Rassurant','Tolérant','Maniable','Léger','Tourne facilement'],'rows':[('Programme','Piste'),('Niveau','Débutant'),('Patin','70 mm'),('Rayon','13,3 m en 163 cm'),('Profil','Entrée de virage facile')],'speech':'Un ski rassurant, facile à faire tourner, pour progresser sans se faire peur.'},
 {'h':'Ski intermédiaire','name':'ROSSIGNOL\nForza 70° TI Konect','img':'rossignol-forza-70','position':'Skieur intermédiaire qui veut gagner en précision et en contrôle, et profiter de belles sensations sur piste.','maker':'Un ski puissant et précis, pensé pour les virages coupés, avec du contrôle et de la stabilité à bonne vitesse.','words':['Précis','Accrocheur','Stable','Dynamique','Virage coupé','Bonne relance'],'rows':[('Programme','Piste'),('Niveau','Intermédiaire à confirmé'),('Patin','77 mm'),('Rayon','13 à 15 m selon taille'),('Profil','Bonne tenue de courbe')],'speech':'Un ski précis et stable pour enchaîner les virages avec confiance et prendre plaisir à carver.'},
 {'h':'Ski performance','name':'ROSSIGNOL\nHero Elite MT TI C.A.M.','img':'rossignol-hero-mt','position':'Skieur intermédiaire à expert recherchant de la précision, de la performance et du soutien à vitesse élevée sur piste.','maker':'Un ski performant, stable et puissant, avec une excellente tenue de courbe et de la précision quand le rythme augmente.','words':['Précis','Soutenant','Stable','Rapide','Bonne relance','Tenue de courbe'],'rows':[('Programme','Piste performance'),('Niveau','Intermédiaire à expert'),('Patin','73 mm'),('Rayon','12 à 16 m selon taille'),('Construction','Chants droits / ski sportif')],'speech':'Un ski plus sportif, posé sur la carre, qui apporte du soutien et de la relance quand on accélère.'},
 {'h':'Ski spécialiste','name':'ROSSIGNOL\nHero ST','img':'rossignol-hero-st','position':'Skieur technique, à l’aise sur les virages courts, qui recherche un ski très réactif et précis.','maker':'Un ski réactif pour des virages courts et dynamiques, avec une forte accroche et beaucoup de précision.','words':['Nerveux','Réactif','Précis','Virages courts','Forte accroche','Exigeant'],'rows':[('Programme','Spécialité piste'),('Niveau','Expert'),('Patin','68 mm'),('Rayon','11 à 14 m selon taille'),('Style','Virages courts / slalom')],'speech':'Un ski nerveux et précis, taillé pour enchaîner les virages courts avec beaucoup de répondant.'}]
def products():
    p=Page(10);p.header('Exemples de skis de piste.','Un modèle par catégorie pour apprendre à construire son discours produit.','02  /  LES FAMILLES')
    for i,c in enumerate(PRODUCTS):
        x=70+(i%2)*1160;y=432+(i//2)*1250;cw=1100;end=y+1210
        p.rect((x,y,x+cw,end));p.rect((x+2,y+2,x+cw-2,y+125),PALE,None,20)
        p.number(x+25,y+24,i+1);p.text(x+121,y+29,c['h'],58,'serif',INK)
        p.text(x+158,y+166,c['name'],30,'bold',TEAL,width=275,center=True,leading=38)
        p.photo(c['img'],(x+25,y+310,x+294,y+995))
        tx=x+330;tw=735;yy=y+170
        for label,body in [('Positionnement',c['position']),('Ce que le fabricant met en avant',c['maker'])]:
            yy=p.label(tx,yy,label,tw,27)
            yy=p.text(tx,yy,body,30,width=tw,leading=35)+18
        yy=p.label(tx,yy,'Vocabulaire utile',tw,27)
        for j in range(3):
            for k in range(2):p.text(tx+k*370,yy,'• '+c['words'][j*2+k],29,'bold',INK,width=365)
            yy+=38
        yy+=15;yy=p.label(tx,yy,'Fiche technique',tw,27)
        for j,(label,value) in enumerate(c['rows']):
            vals=[];words=value.split();row=''
            for word in words:
                trial=(row+' '+word).strip()
                if p.d.textlength(trial,font=ft(29))>tw-191 and row:vals.append(row);row=word
                else:row=trial
            vals.append(row);rh=max(37,len(vals)*34+5)
            if j%2==0:p.d.rectangle((tx-3,yy-4,tx+tw+3,yy+rh-4),fill=P['lignes_tableau'])
            p.text(tx+3,yy,label,27,'bold',TEAL)
            p.text(tx+191,yy,value,29,width=tw-191,leading=34)
            yy+=rh
        sy=end-157
        assert yy<sy-10,(p.n,c['name'],yy,sy)
        p.rect((x+20,sy,x+1080,end-18),DARK,None,14)
        p.text(x+37,sy+14,'À DIRE AU CLIENT',27,'bold',WHITE)
        p.text(x+37,sy+55,'« '+c['speech']+' »',30,'bold',WHITE,width=1025,leading=35,bottom=end-25)
    p.remember('Un modèle sert à expliquer une catégorie.','Le bon discours relie une sensation au besoin du client : facile à tourner, précis,\nstable ou réactif. Le choix final dépend du niveau, du gabarit et de l’usage.')
    p.footer('Modèles, visuels et données repris de la page validée. Les caractéristiques peuvent varier selon la longueur et le millésime.');return p

def allmountain():
    p=Page(11);p.header('Les skis all-mountain.','De la priorité piste au ski mixte : un compromis entre accroche et portance.','02  /  LES FAMILLES')
    rows=[('80/20','Priorité piste','80–85 mm','allmountain-8020','Surtout sur piste, avec quelques sorties en neige souple.','Sur piste : facile à conduire, rapide d’une carre à l’autre.','Skieur cherchant un peu plus de polyvalence qu’avec un ski de piste.',['Très accessible','Bonne maniabilité sur piste','Un peu plus de portance'],'Bords de piste et neige souple.','Une base très piste, avec davantage d’aisance quand la neige devient souple.'),('70/30','Plus de polyvalence','85–95 mm','allmountain-7030','Principalement sur piste, avec plus d’aisance en neige souple.','Un meilleur équilibre piste / hors-piste, avec un caractère passe-partout.','Skieur qui veut varier les terrains avec une seule paire.',['Très polyvalent','Équilibre accroche / portance','Adapté à un usage loisir sportif'],'Plus confortable hors des pistes damées.','Le compromis pour garder de l’accroche sur piste et varier davantage les terrains.'),('50/50','Piste & hors-piste','95–105 mm','allmountain-5050','Un programme mixte pour alterner piste et neige non damée.','Plus de portance en neige profonde ; moins vif et plus physique sur neige dure.','Skieur qui alterne réellement piste et hors-piste.',['Bonne portance','Reste utilisable sur piste','Plus exigeant sur neige dure'],'Meilleur soutien dans la neige souple.','Plus de portance et de pivot en neige souple, avec un compromis à accepter sur piste dure.')]
    for i,(ratio,h,waist,img,intro,behavior,client,pros,off,speech) in enumerate(rows):
        x=70+768*i;cw=724;p.rect((x,432,x+cw,2900))
        p.rect((x+2,434,x+cw-2,642),PALE,None,22)
        p.number(x+28,457,i+1);p.text(x+124,457,ratio,60,'serif',TEAL)
        p.text(x+32,540,h,46,'serif',INK)
        a,b=ratio.split('/');p.text(x+32,594,f'{a} % piste / {b} % hors-piste',29)
        p.text(x+32,700,intro,37,width=660,bottom=915)
        p.photo(img,(x+20,940,x+704,1240))
        p.rect((x+32,1290,x+692,1410),PALE,None,15)
        p.text(x+55,1312,waist,55,'serif',INK);p.text(x+55,1373,'LARGEUR AU PATIN',27,'bold',TEAL)
        yy=1480;yy=p.label(x+34,yy,'Comportement',656)
        yy=p.text(x+34,yy,behavior,36,width=656)+34
        yy=p.label(x+34,yy,'Pour quel client ?',656)
        yy=p.text(x+34,yy,client,36,width=656)+34
        yy=p.label(x+34,yy,'Les points à expliquer',656)
        yy=p.bullets(x+34,yy,pros,656,35,13)+22
        yy=p.text(x+34,yy,'En neige souple : '+off,33,width=656)+10
        sy=2628;assert yy<sy-10,(p.n,ratio,yy)
        questions=['Vous restez surtout sur piste, avec seulement quelques passages en neige souple ?', 'Vous cherchez une seule paire pour varier les terrains au cours de la journée ?', 'Vous sortez régulièrement des pistes et acceptez un ski moins vif sur neige dure ?']
        p.rect((x+24,2300,x+700,2580),PALE,None,15)
        p.text(x+44,2320,'LA QUESTION À POSER',29,'bold',TEAL)
        p.text(x+44,2380,questions[i],34,width=636,leading=41,bottom=2560)
        p.rect((x+24,sy,x+700,2876),DARK,None,15)
        p.text(x+44,sy+19,'À DIRE AU CLIENT',30,'bold',WHITE)
        p.text(x+44,sy+67,'« '+speech+' »',35,'bold',WHITE,width=636,leading=41,bottom=2858)
    p.remember('Plus de largeur : davantage de portance en neige souple.','En contrepartie, le ski devient souvent moins vif sur neige dure.\nLes ratios 80/20, 70/30 et 50/50 sont des repères pédagogiques indicatifs.')
    p.footer('Les largeurs sont des repères de famille. Les exemples de modèles sont présentés page 12.');return p

if __name__=='__main__':
    records=[]
    for build in [cover,contents,anatomy,dimensions,radius,profiles,construction,families,piste,products,allmountain]:
        p=build();records.append(p.save());print('Page',p.n,'OK',flush=True)
    (CHECK/'manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
    # Fast visual overview; full-resolution pages remain available separately.
    sheet=Image.new('RGB',(2000,1740),'#DCE7EB');d=ImageDraw.Draw(sheet)
    for i,r in enumerate(records):
        im=Image.open(ROOT/r['path']);im.thumbnail((380,540));x=(i%5)*400+(400-im.width)//2;y=(i//5)*580+32
        sheet.paste(im,(x,y));d.text(((i%5)*400+12,(i//5)*580+8),f"PAGE {r['page']:02}",fill=INK,font=ft(18,'bold'))
    sheet.save(CHECK/'overview.jpg',quality=94)
