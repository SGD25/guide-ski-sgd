from PIL import Image, ImageDraw, ImageFont, ImageOps
from pathlib import Path
import json
import urllib.request

PROJECT = Path(__file__).resolve().parents[2]
ROOT = PROJECT / 'sources/page12/.cache'
ROOT.mkdir(parents=True, exist_ok=True)
PALETTE = json.loads((PROJECT / 'design/charte-candidate-sgd.json').read_text())['palette']
PHOTO_URLS = {
    'experience82.jpg': 'https://www.rossignol.com/dw/image/v2/BJJZ_PRD/on/demandware.static/-/Sites-rossignol-catalog/default/dwfa94b770/images/large/RAMFS03_EXPERIENCE_82_BASALT_KONECT__RGB72DPI_01.jpg?sw=1600',
    'ripstick88.png': 'https://elansports.com/cdn/shop/files/ripstick_88_2d_addkyp24.png?v=1769778255&width=1600',
    'sender102.jpg': 'https://www.rossignol.com/dw/image/v2/BJJZ_PRD/on/demandware.static/-/Sites-rossignol-catalog/default/dwf0091cd0/images/large/RANMR01000_72DPI_02_v00.jpg?sw=1600',
}
for name, url in PHOTO_URLS.items():
    path = ROOT / name
    if not path.exists():
        with urllib.request.urlopen(url, timeout=40) as response:
            path.write_bytes(response.read())

W, H = 2400, 3394
im = Image.new('RGB', (W, H), PALETTE['fond'])
d = ImageDraw.Draw(im)
NAVY = PALETTE['titres']
BODY = PALETTE['texte']
BROWN = PALETTE['accent']
GOLD = PALETTE['reperes']
LINE = PALETTE['filets']
CREAM = PALETTE['encarts_clairs']
WHITE = '#ffffff'
PANEL = PALETTE['encarts_forts']
FONTS = Path('/usr/share/fonts/opentype/urw-base35')

def font(size, kind='sans'):
    f = {'sans':'NimbusSans-Regular.otf','bold':'NimbusSans-Bold.otf',
         'serif':'NimbusRoman-Bold.otf','italic':'NimbusRoman-BoldItalic.otf'}[kind]
    return ImageFont.truetype(str(FONTS/f), size)

def wrap(s, f, width):
    lines=[]
    for para in s.split('\n'):
        line=''
        for word in para.split():
            test = (line+' '+word).strip()
            if d.textlength(test,font=f)>width and line:
                lines.append(line);line=word
            else:line=test
        lines.append(line)
    return lines

def text(x,y,s,size=35,kind='sans',color=BODY,width=None,leading=None,center=False):
    f=font(size,kind)
    lines=wrap(s,f,width) if width else s.split('\n')
    lh=leading or int(size*1.22)
    for line in lines:
        xx = x - d.textlength(line,font=f)/2 if center else x
        d.text((round(xx),y),line,font=f,fill=color,anchor='lt')
        y+=lh
    return y

def line(x,y,x2,color=LINE,w=2):d.line((x,y,x2,y),fill=color,width=w)

# A finished raster page, built from original manufacturer photos and typeset text.
text(76,48,'CHAPITRE 02  /  LES FAMILLES',32,'bold',BROWN)
line(700,66,2070)
d.rounded_rectangle((2110,36,2324,102),radius=12,outline=GOLD,width=2)
text(2217,53,'PAGE 12',31,'bold',NAVY,center=True)
text(76,130,'Exemples de skis all-mountain',113,'serif',NAVY)
text(78,267,'1 modèle par catégorie pour apprendre à conseiller avec des mots simples.',43,'sans',BROWN)
text(78,333,'Même question de départ : « Vous skiez surtout sur piste, ou aussi en neige non damée ? »',34,'sans',BODY)

cards=[
 dict(n='1',ratio='80/20',heading='Priorité piste',brand='ROSSIGNOL',name='Experience 82 Basalt',
      photo='experience82.jpg',waist='82 mm',ref='en 176 cm',
      client='Pour un skieur intermédiaire qui skie surtout sur piste. Il recherche de l’accroche et des virages fluides, avec un peu d’aisance quand la neige devient souple.',
      maker='Drive Tip atténue les vibrations en spatule. Le bois paulownia allège le ski ; le basalte améliore l’amorti. Les chants droits transmettent les appuis pour bien tenir le virage. La ligne de cotes All Trail favorise une entrée en courbe fluide.',
      vocab=['Accrocheur','Fluide','Maniable','Confortable','Stable','Précis'],
      specs=[('Programme','All-mountain orienté piste'),('Niveau','Intermédiaire à confirmé'),('Construction','Bois paulownia + basalte'),('Profil','Rocker All Trail'),('Cotes*','127–82–115 mm'),('Rayon*','16 m en 176 cm')],
      limit='Moins à l’aise en neige profonde qu’un ski plus large.',
      speech='« De l’accroche et du confort pour enchaîner les virages sur piste, avec de l’aisance en neige plus souple. »',
      source='[1] Rossignol · réf. RAMFS03'),
 dict(n='2',ratio='70/30',heading='Plus de polyvalence',brand='ELAN',name='Ripstick 88 (2025)',
      photo='ripstick88.png',waist='88 mm',ref='en 175 cm',
      client='Pour un skieur déjà à l’aise qui alterne piste et neige non damée. Il veut un ski léger sous les pieds, réactif et facile à faire pivoter.',
      maker='Amphibio associe accroche sur piste et facilité de pivot. Les renforts carbone soutiennent le ski et donnent de la relance en sortie de virage. Les fibres de lin atténuent les vibrations pour une glisse plus douce.',
      vocab=['Léger','Agile','Polyvalent','Réactif','Accrocheur','Bonne relance'],
      specs=[('Programme','Piste + neige variée'),('Niveau','Intermédiaire à expert'),('Construction','Bois + carbone + lin'),('Profil','Amphibio : accroche / pivot'),('Cotes*','127–88–106 mm'),('Rayon*','15,8 m en 175 cm')],
      limit='Moins de portance en neige profonde qu’un ski autour de 100 mm.',
      speech='« Léger et réactif : il accroche sur piste et reste agile pour varier les terrains et les types de neige. »',
      source='[2] Elan · réf. ADDKYP24'),
 dict(n='3',ratio='50/50',heading='Piste & hors-piste',brand='ROSSIGNOL',name='Sender Soul 102',
      photo='sender102.jpg',waist='102 mm',ref='en 180 cm',
      client='Pour un skieur confirmé à expert qui sort souvent des pistes. Il cherche un ski qui s’enfonce moins en neige souple, tout en restant utilisable sur piste.',
      maker='Le double rocker facilite le pivot. Air Tip allège les extrémités pour rendre le ski plus maniable. Un renfort métallique sous le pied améliore l’accroche et le soutien ; le système VAS absorbe les vibrations.',
      vocab=['Portance','Pivot facile','Joueur','Stable','Polyvalent','Du soutien'],
      specs=[('Programme','Mixte piste / hors-piste'),('Niveau','Confirmé à expert'),('Construction','Bois peuplier + métal'),('Profil','Double rocker'),('Cotes*','135–102–125 mm'),('Rayon*','17 m en 180 cm')],
      limit='Moins vif sur neige dure ; destiné à un skieur déjà technique.',
      speech='« Il porte mieux en neige souple, pivote facilement et garde du soutien quand vous revenez sur la piste. »',
      source='[3] Rossignol · réf. RANMR01')]

card_top, card_bottom = 432, 2900
xs=[70,838,1606]
cw=724
log=[]
for c,x in zip(cards,xs):
    d.rounded_rectangle((x,card_top,x+cw,card_bottom),radius=23,fill=WHITE,outline=LINE,width=3)
    d.rounded_rectangle((x+1,card_top+1,x+cw-1,card_top+209),radius=22,fill=CREAM)
    d.rectangle((x+2,card_top+120,x+cw-2,card_top+208),fill=CREAM)
    d.ellipse((x+28,card_top+25,x+100,card_top+97),fill=GOLD)
    text(x+64,card_top+38,c['n'],47,'serif',WHITE,center=True)
    text(x+124,card_top+25,c['ratio'],60,'serif',BROWN)
    text(x+32,card_top+107,c['heading'],46,'serif',NAVY)
    pct=c['ratio'].split('/')
    text(x+32,card_top+162,f'{pct[0]} % piste / {pct[1]} % hors-piste',29,'sans',BODY)
    text(x+cw/2,card_top+247,c['brand'],29,'bold',BROWN,center=True)
    text(x+cw/2,card_top+292,c['name'],43,'serif',NAVY,center=True)

    # Only transparent canvas is removed from Elan's packshot. Product pixels,
    # colours, geometry and aspect ratio are preserved. No generated imagery.
    photo=Image.open(ROOT/c['photo']).convert('RGBA')
    if c['photo'].endswith('.png'):photo=photo.crop(photo.getbbox())
    box=(x+23,card_top+390,x+215,card_top+1270)
    photo=ImageOps.contain(photo,(box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS)
    px=(box[0]+box[2]-photo.width)//2; py=box[1]+(box[3]-box[1]-photo.height)//2
    im.paste(photo,(px,py),photo)
    log.append({'model':c['name'],'photo_source':c['photo'],'placed':(photo.width,photo.height),'photo_y':py})

    tx=x+240;tw=cw-272;y=card_top+380
    def heading(label, size=29):
        global y
        ff=font(size,'bold')
        ls=wrap(label,ff,tw-24)
        hh=len(ls)*34+22
        d.rounded_rectangle((tx-10,y-8,tx+tw+10,y+hh-8),radius=10,fill=CREAM)
        y=text(tx+2,y+2,label,size,'bold',BROWN,width=tw-24,leading=34)+24
    heading('Positionnement')
    y=text(tx,y,c['client'],32,'sans',BODY,width=tw,leading=39)+30
    heading('Ce que le fabricant met en avant',28)
    y=text(tx,y,c['maker'],32,'sans',BODY,width=tw,leading=39)
    log[-1]['upper_text_end']=y
    assert y < card_top+1285, (c['name'],'upper',y)

    by=card_top+1306
    d.rounded_rectangle((x+32,by,x+cw-32,by+112),radius=15,fill=CREAM)
    text(x+57,by+17,c['waist'],57,'serif',NAVY)
    text(x+340,by+16,'AU PATIN',26,'bold',BROWN)
    text(x+340,by+56,c['ref'],30,'sans',BODY)
    tx=x+34;tw=cw-68;y=by+148
    heading('Vocabulaire utile',30)
    for row in range(3):
        for col in range(2):
            xx=tx+col*(tw//2)
            d.ellipse((xx,y+11,xx+8,y+19),fill=GOLD)
            text(xx+22,y,c['vocab'][row*2+col],34,'bold',NAVY)
        y+=43
    y+=23
    heading('Fiche technique',30)
    for j,(label,value) in enumerate(c['specs']):
        fh=font(31,'sans');ls=wrap(value,fh,tw-213)
        rh=max(48,len(ls)*36+12)
        if j%2==0:d.rectangle((tx-3,y-5,tx+tw+3,y+rh-5),fill=PALETTE['lignes_tableau'])
        text(tx+6,y+2,label,29,'bold',BROWN)
        text(tx+205,y+1,value,31,'sans',BODY,width=tw-213,leading=36)
        y+=rh
    y+=19
    y=text(tx,y,'Limite : '+c['limit'],30,'sans',BODY,width=tw,leading=36)
    y+=16

    sy=card_bottom-270
    assert y < sy-14, (c['name'],y,sy)
    d.rounded_rectangle((x+24,sy,x+cw-24,card_bottom-24),radius=15,fill=PANEL)
    text(x+44,sy+19,'À DIRE AU CLIENT',30,'bold',WHITE)
    end=text(x+44,sy+67,c['speech'],35,'bold',WHITE,width=cw-88,leading=41)
    assert end<card_bottom-30,(c['name'],end)
    log[-1]['content_end']=y

# Consistent, prominent reminder panel.
ay=2945
d.rounded_rectangle((70,ay,2330,ay+250),radius=25,fill=CREAM)
d.rounded_rectangle((70,ay,514,ay+250),radius=25,fill=PANEL)
d.rectangle((480,ay,514,ay+250),fill=PANEL)
text(292,ay+91,'À retenir',65,'serif',WHITE,center=True)
text(555,ay+23,'L’all-mountain : une seule paire pour varier les terrains.',42,'serif',NAVY)
text(555,ay+85,'Sur piste : privilégier l’accroche et des virages faciles à enchaîner.',32,'sans',BODY)
text(555,ay+134,'En neige souple : chercher à moins s’enfoncer et à pivoter facilement.',32,'sans',BODY)
text(555,ay+187,'Adapter ensuite le modèle et la longueur au niveau et au poids du client.',32,'bold',NAVY)

text(76,3221,'Ratios : repères pédagogiques du guide. * Cotes et rayon pour la longueur précisée sous le ski ; la largeur peut varier selon la taille.',26,'sans',BODY)
text(76,3267,'Visuels et données techniques : Rossignol et Elan. Positionnement et vocabulaire : repères de conseil. Photos non retouchées.',26,'sans',BODY)
line(70,3330,2330,GOLD,3)
text(76,3351,'SPORT GOOD DEAL  /  GUIDE DU SKI',27,'bold',NAVY)
text(2325,3350,'12',29,'bold',NAVY,center=True)

out=PROJECT/'assets/page12-charte-sgd-v748.jpg'
im.save(out,quality=97,subsampling=0,optimize=True,dpi=(240,240))
with Image.open(out) as check:
    check.verify()
with Image.open(out) as check:
    check.load()
    assert check.size == (W,H)
im.crop((60,2625,2340,2905)).save(ROOT/'charte-sgd-encarts-check.jpg',quality=96,subsampling=0)
preview=im.copy();preview.thumbnail((1440,2037));preview.save(ROOT/'charte-sgd-preview-check.jpg',quality=95,subsampling=0)
(ROOT/'charte-sgd-layout-log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2))
print(out)
print(json.dumps(log,ensure_ascii=False))
