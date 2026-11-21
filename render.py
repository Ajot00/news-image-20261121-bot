from PIL import Image, ImageDraw, ImageFont
import hashlib

W = H = 1024
PAPER, INK = (244, 232, 204), (31, 39, 37)
PALE, RULE, MUTED = (235, 217, 179), (173, 151, 112), (91, 86, 73)
RED, TEAL, GOLD = (159, 55, 38), (47, 101, 98), (205, 157, 68)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
im = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(im)

def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)

def fit(text, width, size, bold=False):
    f = font(size, bold)
    while d.textbbox((0, 0), text, font=f)[2] > width and size > 12:
        size -= 1
        f = font(size, bold)
    return f

def wrap(text, f, width):
    lines, current = [], ""
    for word in text.split():
        test = (current + " " + word).strip()
        if d.textbbox((0, 0), test, font=f)[2] <= width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def paragraph(text, x, y, width, f, fill=INK, leading=3, max_lines=None):
    lines = wrap(text, f, width)
    if max_lines:
        lines = lines[:max_lines]
    for value in lines:
        d.text((x, y), value, font=f, fill=fill)
        y += f.size + leading

def rule(y, x1=28, x2=996, color=RULE, width=2):
    d.line((x1, y, x2, y), fill=color, width=width)

def card(x, y, w, h, kicker, title, body, accent):
    d.rounded_rectangle((x, y, x+w, y+h), radius=8, fill=PALE, outline=RULE, width=2)
    d.rectangle((x+1, y+1, x+8, y+h-1), fill=accent)
    d.text((x+18, y+9), kicker.upper(), font=font(13, True), fill=accent)
    d.text((x+18, y+27), title, font=fit(title, w-36, 22, True), fill=INK)
    paragraph(body, x+18, y+57, w-36, font(13), leading=2, max_lines=5)

# Masthead
d.text((30, 18), "THE WORLD", font=font(54, True), fill=INK)
d.text((690, 27), "SATURDAY", font=font(18, True), fill=RED)
d.text((690, 50), "21 NOVEMBER 2026", font=font(26, True), fill=INK)
d.text((32, 83), "GLOBAL NEWS • CLIMATE • SECURITY • ECONOMY", font=font(15, True), fill=MUTED)
rule(109, color=INK, width=4)

# Climate lead with an original geometric Antalya coast illustration.
d.rounded_rectangle((28,124,996,322), radius=10, fill=(232,215,176), outline=RULE, width=2)
d.rectangle((29,125,995,132), fill=RED)
d.text((48,143), "WORLD CLIMATE SUMMIT · ANTALYA, TÜRKİYE", font=font(16,True), fill=TEAL)
d.text((45,164), "COP31 OVERTIME", font=font(46,True), fill=INK)
lead = "Antalya climate talks miss Friday’s deadline as the closing plenary is suspended until Saturday; a France- and Panama-led coalition fights a draft dropping all fossil-fuel language and the $120bn adaptation target, with negotiations running into the weekend."
paragraph(lead,48,222,620,font(16),leading=3,max_lines=4)
d.ellipse((802,151,866,215), fill=GOLD)
d.polygon([(690,263),(754,229),(816,249),(866,225),(930,245),(995,233),(995,321),(690,321)], fill=TEAL)
d.polygon([(690,278),(755,253),(824,267),(886,247),(942,264),(995,250),(995,321),(690,321)], fill=(69,132,126))
d.polygon([(690,241),(725,226),(748,236),(768,215),(795,233),(823,228),(844,251),(814,260),(778,250),(749,265),(713,255)], fill=(193,164,116))
for a,b in [(714,785),(852,932),(744,821)]:
    yy = 279 if a == 714 else (291 if a == 852 else 304)
    d.line((a,yy,b,yy), fill=PAPER, width=3)
d.line((953,274,953,248), fill=INK, width=3)
d.arc((938,230,969,262),185,350,fill=INK,width=3)
d.arc((927,233,964,263),185,350,fill=INK,width=3)
d.text((48,300), "DEADLINE MISSED / TALKS RESUME SATURDAY", font=font(15,True), fill=RED)

# Five additional lead cards; together with the climate lead these are six cards.
stories = [
 ("POLAND · NATO","RUTTE DUE IN WARSAW","After Russian Kh-101 missiles and a drone came down in Poland Friday, PM Tusk called it a deliberate provocation; Poland seeks stronger NATO air cover.",RED),
 ("BRAZIL · POLITICS","BOLSONARO HOSPITALISED","Jailed ex-president Jair Bolsonaro was taken to hospital with severe abdominal pain.",GOLD),
 ("UNITED STATES · FIRE","RINDERKNECHT CONVICTED","A federal jury convicted Jonathan Rinderknecht of starting the deadly 2025 Palisades Fire in Los Angeles, which killed 12; the verdict was reported Saturday.",RED),
 ("MARKETS · WALL STREET","DOW, S&P IN CORRECTION","The S&P 500 and Dow entered correction after Friday’s roughly 3.7% AI-led sell-off.",TEAL),
 ("INDIA · CYCLONE","AKVAN WEAKENS","Cyclone Akvan weakened after crossing the coasts of Odisha and Andhra Pradesh.",GOLD),
]
card(28,338,310,148,*stories[0])
card(356,338,310,148,*stories[1])
card(684,338,310,148,*stories[2])
card(192,496,310,148,*stories[3])
card(522,496,310,148,*stories[4])

# Locator strip: six dots and readable place labels over simplified continents.
d.rounded_rectangle((28,657,996,740), radius=8, fill=(237,222,188), outline=RULE, width=2)
d.text((43,666), "THE WORLD TODAY", font=font(15,True), fill=INK)
d.polygon([(205,691),(225,681),(242,685),(251,697),(240,709),(232,725),(219,717),(214,704)],fill=(190,174,137))
d.polygon([(265,708),(278,704),(287,714),(284,731),(274,735),(267,723)],fill=(190,174,137))
d.polygon([(399,689),(421,684),(437,691),(432,701),(418,704),(412,717),(400,710)],fill=(190,174,137))
d.polygon([(425,706),(439,707),(445,720),(438,733),(428,726)],fill=(190,174,137))
d.polygon([(495,690),(520,681),(541,685),(554,695),(546,705),(523,702),(515,714),(500,705)],fill=(190,174,137))
d.polygon([(526,709),(540,707),(548,718),(544,733),(533,729)],fill=(190,174,137))
d.polygon([(698,694),(716,687),(730,691),(735,701),(723,707),(712,702)],fill=(190,174,137))
for mx,my,label,lx,ly in [(237,695,"LOS ANGELES",245,686),(430,699,"ANTALYA",390,682),(456,704,"POLAND",469,695),(552,710,"ODISHA",559,701),(287,722,"BRAZIL",294,713),(727,699,"WELLINGTON",735,686)]:
    d.ellipse((mx-4,my-4,mx+4,my+4),fill=RED,outline=PAPER,width=1)
    d.text((lx,ly),label,font=font(11,True),fill=INK)

# Nine concise briefs in three balanced columns.
rule(753,color=INK,width=3)
d.text((31,758),"THE DAY · NINE MORE STORIES",font=font(15,True),fill=RED)
briefs = [
 ("INDIA 159/1 IN WELLINGTON","India closed day two of the Wellington Test at 159/1, trailing New Zealand by 209."),
 ("PAYMENT VENDOR HACKS","JPMorgan, Visa and Mastercard reported third-party vendor cyberattacks; core payment networks were unaffected."),
 ("WFP WARNS OF 2027 AID CUTS","The UN World Food Programme warned funding shortages could cut food aid in 2027."),
 ("10,000 ROHINGYA TO TÜRKIYE","Malaysia will resettle 10,000 Rohingya refugees in Türkiye after the ICJ ruling."),
 ("HYUNDAI REVEALS NEW ELANTRA","Hyundai unveiled the eighth-generation Elantra at the Los Angeles Auto Show."),
 ("CARLSEN FORFEITS RAPID GAMES","Magnus Carlsen forfeited rapid games at a chess tournament."),
 ("NSE RISES TO WORLD NO. 5","India’s NSE became the world’s fifth-largest listed exchange, overtaking Nasdaq and Hong Kong."),
 ("PAKISTAN BOMBING: 5 DEAD","A suicide car bombing at a security checkpoint killed five people and injured 13."),
 ("UEFA BACKS DIALLO","UEFA backed Diallo to stand against Infantino in the FIFA election."),
]
colx,rowy = [31,359,687],[783,856,929]
for i,(label,story) in enumerate(briefs):
    x,y=colx[i%3],rowy[i//3]
    d.text((x,y),label,font=fit(label,300,16,True),fill=TEAL)
    paragraph(story,x,y+20,300,font(12),leading=1,max_lines=4)
for y in (849,922):
    rule(y,31,993,RULE,1)
d.line((344,780,344,1001),fill=RULE,width=1)
d.line((672,780,672,1001),fill=RULE,width=1)
d.rectangle((17,12,1006,1007),outline=INK,width=2)

out="entry.png"
im.save(out,format="JPEG",quality=95,optimize=True,progressive=False,subsampling=0)
data=open(out,"rb").read()
assert data[:2]==b"\xff\xd8" and len(data)<1048576
print(f"{out}: {im.width}x{im.height}, {len(data)} bytes, sha256={hashlib.sha256(data).hexdigest()}")
