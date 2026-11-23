"""Generate the current DFADS system design diagrams as high-resolution JPEGs."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math
import textwrap

OUT = Path(__file__).resolve().parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)
W, H = 3000, 1900
BG = "#F5F8FC"
INK = "#14243A"
MUTED = "#52647A"
BLUE = "#DCEBFF"
TEAL = "#D9F4F0"
PURPLE = "#ECE4FF"
ORANGE = "#FFF0D8"
PINK = "#FFE4E8"
GREEN = "#E2F2E3"
WHITE = "#FFFFFF"
LINE = "#48627E"

FONT_PATH = "C:/Windows/Fonts/arial.ttf"
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"

def font(size=36, bold=False):
    path = FONT_BOLD if bold else FONT_PATH
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()

def canvas(title, subtitle):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.text((110, 70), title, fill=INK, font=font(64, True))
    d.text((112, 158), subtitle, fill=MUTED, font=font(30))
    d.line((110, 220, W-110, 220), fill="#CBD7E5", width=4)
    return im, d

def wrap_lines(d, text, fnt, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if d.textbbox((0, 0), candidate, font=fnt)[2] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def rounded_box(d, xy, text, fill=WHITE, outline="#9AAFC5", title=None,
                body_size=29, title_size=32, radius=28, pad=28, width=3):
    x1, y1, x2, y2 = xy
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)
    if title:
        tf = font(title_size, True)
        d.text((x1+pad, y1+pad), title, fill=INK, font=tf)
        body_y = y1+pad+title_size+14
        maxw = x2-x1-2*pad
        for i, line in enumerate(text.split("\n")):
            for wrapped in wrap_lines(d, line, font(body_size), maxw):
                d.text((x1+pad, body_y), wrapped, fill=MUTED, font=font(body_size))
                body_y += body_size+12
    else:
        f = font(body_size)
        lines = []
        for line in text.split("\n"):
            lines.extend(wrap_lines(d, line, f, x2-x1-2*pad))
        line_h = body_size+12
        y = y1 + max(pad, (y2-y1-len(lines)*line_h)//2)
        for line in lines:
            bb = d.textbbox((0,0), line, font=f)
            d.text((x1+(x2-x1-(bb[2]-bb[0]))/2, y), line, fill=INK, font=f)
            y += line_h

def arrow(d, start, end, label=None, color=LINE, width=5, label_offset=(0,-30)):
    d.line((start, end), fill=color, width=width)
    angle = math.atan2(end[1]-start[1], end[0]-start[0])
    size = 22
    pts = [end,
           (end[0]-size*math.cos(angle-0.48), end[1]-size*math.sin(angle-0.48)),
           (end[0]-size*math.cos(angle+0.48), end[1]-size*math.sin(angle+0.48))]
    d.polygon(pts, fill=color)
    if label:
        mx, my = (start[0]+end[0])//2 + label_offset[0], (start[1]+end[1])//2 + label_offset[1]
        f = font(23, True)
        bb = d.textbbox((mx,my), label, font=f)
        d.rounded_rectangle((bb[0]-9,bb[1]-5,bb[2]+9,bb[3]+5), radius=8, fill=BG)
        d.text((mx,my), label, fill=MUTED, font=f)

def dashed_arrow(d, start, end, label=None):
    x1,y1=start; x2,y2=end
    steps=24
    for i in range(0,steps,2):
        a=i/steps; b=min(i+1,steps)/steps
        p=(x1+(x2-x1)*a,y1+(y2-y1)*a); q=(x1+(x2-x1)*b,y1+(y2-y1)*b)
        d.line((p,q), fill="#7F6AA8", width=4)
    arrow(d,(x1+(x2-x1)*.88,y1+(y2-y1)*.88),end,color="#7F6AA8",width=4)
    if label:
        mx=(x1+x2)//2; my=(y1+y2)//2-24
        d.text((mx,my),label,fill="#6D598E",font=font(22,True))

def store(d, xy, title, subtitle, fill=GREEN):
    x1,y1,x2,y2=xy
    d.rounded_rectangle(xy,radius=26,fill=fill,outline="#7EAA83",width=3)
    d.ellipse((x1,y1,x2,y1+44),fill="#F3FFF3",outline="#7EAA83",width=3)
    d.ellipse((x1,y2-44,x2,y2),fill=fill,outline="#7EAA83",width=3)
    for yy in (y1+22,y2-22): d.line((x1,yy,x2,yy),fill="#7EAA83",width=3)
    d.text((x1+20,y1+58),title,font=font(30,True),fill=INK)
    for i,line in enumerate(wrap_lines(d,subtitle,font(23),x2-x1-40)):
        d.text((x1+20,y1+102+i*32),line,font=font(23),fill=MUTED)

def save(im, name):
    path=OUT/name
    im.save(path,"JPEG",quality=95,subsampling=0,optimize=True,dpi=(220,220))
    print(path)

def use_case():
    im,d=canvas("DFADS Use-Case Diagram","Current system boundary: browser-based Flask app, Streamlit dashboard, and offline research workflow")
    bx=(620,300,2390,1690)
    d.rounded_rectangle(bx,radius=36,fill="#FFFFFF",outline="#52799F",width=5)
    d.rounded_rectangle((bx[0],bx[1],bx[2],bx[1]+90),radius=32,fill="#E8F1FA",outline="#52799F",width=4)
    d.rectangle((bx[0],bx[1]+48,bx[2],bx[1]+90),fill="#E8F1FA")
    title="Audio Deepfake Detection System (DFADS)"
    bb=d.textbbox((0,0),title,font=font(36,True)); d.text(((bx[0]+bx[2]-(bb[2]-bb[0]))/2,325),title,font=font(36,True),fill=INK)
    # Actors
    def actor(cx,cy,label):
        d.ellipse((cx-24,cy-105,cx+24,cy-57),fill=BG,outline=INK,width=5)
        d.line((cx,cy-57,cx,cy+20),fill=INK,width=5)
        d.line((cx-48,cy-28,cx+48,cy-28),fill=INK,width=5)
        d.line((cx,cy+20,cx-42,cy+80),fill=INK,width=5)
        d.line((cx,cy+20,cx+42,cy+80),fill=INK,width=5)
        for i,line in enumerate(wrap_lines(d,label,font(28,True),300)):
            bb=d.textbbox((0,0),line,font=font(28,True)); d.text((cx-(bb[2]-bb[0])/2,cy+95+i*35),line,font=font(28,True),fill=INK)
    actor(270,760,"Analyst / End User")
    actor(270,1370,"Researcher / Maintainer")
    actor(2730,800,"Recording Contributor")
    # use-case ellipse locations
    cases=[
        ((770,470,1370,610),"Upload audio or select\na demo sample",BLUE),
        ((1530,470,2180,610),"Analyze authenticity\n(Real / Fake + confidence)",TEAL),
        ((770,700,1370,840),"Inspect waveform, FFT,\nspectrogram and features",PURPLE),
        ((1530,700,2180,840),"Record microphone audio\nand convert target voice",ORANGE),
        ((770,930,1370,1070),"Review original and\nconverted audio results",PINK),
        ((1530,930,2180,1070),"Save consented recording\nwith speaker ID",GREEN),
        ((770,1190,1370,1330),"Prepare data and extract\nMFCC / LFCC / CQCC",BLUE),
        ((1530,1190,2180,1330),"Train baseline / ResNeXt\nand evaluate robustness",PURPLE),
        ((1100,1450,1850,1590),"Review saved metrics, RVC status\nand voice model availability",TEAL),
    ]
    centers=[]
    for rect,label,color in cases:
        d.ellipse(rect,fill=color,outline="#8296AA",width=3)
        lines=label.split("\n"); lh=34; y=(rect[1]+rect[3]-len(lines)*lh)//2
        for line in lines:
            f=font(28,True); bb=d.textbbox((0,0),line,font=f)
            d.text(((rect[0]+rect[2]-(bb[2]-bb[0]))/2,y),line,font=f,fill=INK); y+=lh
        centers.append(((rect[0],(rect[1]+rect[3])//2),(rect[2],(rect[1]+rect[3])//2)))
    # Actor links use separate whitespace corridors and avoid crossing ovals.
    d.line((318,760,520,760),fill=LINE,width=3)
    d.line((520,535,520,1000),fill=LINE,width=3)
    for idx in (0,2,4):
        cy=(cases[idx][0][1]+cases[idx][0][3])//2
        d.line((520,cy,cases[idx][0][0],cy),fill=LINE,width=3)
    d.line((318,760,460,760),fill=LINE,width=3)
    d.line((460,430,460,760),fill=LINE,width=3)
    d.line((460,430,1460,430),fill=LINE,width=3)
    d.line((1460,430,1460,770),fill=LINE,width=3)
    for idx in (1,3):
        cy=(cases[idx][0][1]+cases[idx][0][3])//2
        d.line((1460,cy,cases[idx][0][0],cy),fill=LINE,width=3)
    d.line((318,1370,560,1370),fill=LINE,width=3)
    d.line((560,1260,560,1520),fill=LINE,width=3)
    d.line((560,1260,770,1260),fill=LINE,width=3)
    cy=(cases[8][0][1]+cases[8][0][3])//2
    d.line((560,cy,1100,cy),fill=LINE,width=3)
    # Researcher links to model training and evaluation through a top corridor.
    d.line((318,1370,480,1370),fill=LINE,width=3)
    d.line((480,1150,480,1370),fill=LINE,width=3)
    d.line((480,1150,1460,1150),fill=LINE,width=3)
    d.line((1460,1150,1460,1260),fill=LINE,width=3)
    d.line((1460,1260,1530,1260),fill=LINE,width=3)
    # Recording contributor associates only with consented recording.
    d.line((2680,800,2480,800),fill=LINE,width=3)
    d.line((2480,800,2480,1000),fill=LINE,width=3)
    d.line((2480,1000,2180,1000),fill=LINE,width=3)
    # Included behavior within the clone use-case, shown in a small note.
    d.rounded_rectangle((1980,1460,2320,1630),radius=18,fill="#F7F2FF",outline="#B8A9D0",width=2)
    d.text((2000,1480),"Optional services",font=font(25,True),fill=INK)
    d.text((2000,1520),"Edge-TTS fallback;",font=font(22),fill=MUTED)
    d.text((2000,1552),"optional speech-to-text",font=font(22),fill=MUTED)
    d.text((2000,1584),"for conversion fallback",font=font(22),fill=MUTED)
    save(im,"dfads_use_case_diagram.jpg")

def architecture():
    im,d=canvas("DFADS Overall System Architecture","Two interactive interfaces share the audio feature and detector services; training and evaluation remain offline workflows")
    # interface band
    d.rounded_rectangle((110,280,2890,620),radius=30,fill="#EEF4FB",outline="#A8BACD",width=3)
    d.text((145,300),"INTERACTION LAYER",font=font(25,True),fill=MUTED)
    rounded_box(d,(170,365,760,555),"Browser UI\napp/templates/index.html\nUpload, mic, plots and clone comparison",BLUE,body_size=27)
    rounded_box(d,(1200,365,1790,555),"Flask web service\napp/app.py · port 5000\nHTML + JSON API routes",TEAL,body_size=27)
    rounded_box(d,(2240,365,2830,555),"Streamlit dashboard\nstreamlit_app.py\nIndependent interface and workflows",PURPLE,body_size=27)
    arrow(d,(760,460),(1190,460),"HTTP",label_offset=(0,-36))
    # service and pipeline band
    d.rounded_rectangle((110,700,2890,1300),radius=30,fill="#FFFFFF",outline="#A8BACD",width=3)
    d.text((145,720),"APPLICATION AND AUDIO PROCESSING",font=font(25,True),fill=MUTED)
    rounded_box(d,(160,800,700,1015),"Audio ingress\nUpload, demo sample or mic\nFormat checks and temporary files",ORANGE,body_size=26)
    rounded_box(d,(820,800,1380,1015),"Preprocess + features\nMono 16 kHz, trim/normalize\nMFCC + LFCC + CQCC-like → 78 values",BLUE,body_size=25)
    rounded_box(d,(1500,800,2020,1015),"Detector service\nScale feature vector\nResNeXt CNN; SVM fallback",TEAL,body_size=26)
    rounded_box(d,(2180,780,2740,1015),"Voice conversion\nLocal rvc-python + PyTorch\n5 teammate .pth / FAISS indexes",PURPLE,body_size=25)
    arrow(d,(700,900),(810,900))
    arrow(d,(1380,900),(1490,900))
    arrow(d,(2020,900),(2170,900),"clone request",label_offset=(0,-35))
    # clone result loop and fallback
    rounded_box(d,(2180,1070,2740,1225),"Edge-TTS synthesis fallback\nText request or RVC failure",PINK,body_size=24)
    arrow(d,(2460,1015),(2460,1060),"if needed",label_offset=(110,-15))
    arrow(d,(2180,1170),(1990,1170),"analyze clone",label_offset=(0,-34))
    # storage band
    d.rounded_rectangle((110,1380,2890,1770),radius=30,fill="#F0F7F0",outline="#A8C2A8",width=3)
    d.text((145,1400),"LOCAL ARTIFACTS AND OFFLINE RESEARCH",font=font(25,True),fill="#58735A")
    store(d,(170,1490,720,1695),"data/","Feature tables, test split,\nrecordings and metadata")
    store(d,(870,1490,1420,1695),"models/","ResNeXt, scaler, SVM,\nlocal RVC weights and indexes",fill="#E7F0FF")
    store(d,(1570,1490,2120,1695),"results/","Evaluation metrics, plots,\nrobustness and clone reports",fill="#FFF2DC")
    store(d,(2270,1490,2820,1695),"app/static/","Original uploads and generated\nclone WAVs served by Flask",fill="#FCE9ED")
    # vertical data links
    arrow(d,(1760,1015),(1845,1480),"save / read metrics",label_offset=(125,0))
    arrow(d,(2460,1225),(2545,1480),"audio artifacts",label_offset=(100,0))
    # offline scripts callout
    d.rounded_rectangle((800,1080,1470,1240),radius=22,fill="#F6F2FF",outline="#B8A9D0",width=3)
    d.text((830,1098),"Offline research scripts",font=font(28,True),fill=INK)
    d.text((830,1140),"src/: preprocessing, training, evaluation",font=font(22),fill=MUTED)
    d.text((830,1172),"and robustness experiments",font=font(22),fill=MUTED)
    arrow(d,(1135,1240),(1140,1480),"train / evaluate",label_offset=(110,0))
    # Flask sends browser requests into audio ingress. Streamlit runs its own
    # inference path and reaches the detector service independently.
    d.line((1290,555,1290,660),fill=LINE,width=4)
    d.line((1290,660,430,660),fill=LINE,width=4)
    arrow(d,(430,660),(430,790),"request → audio pipeline",label_offset=(145,-105))
    d.line((2530,555,2530,650),fill=LINE,width=4)
    d.line((2530,650,1950,650),fill=LINE,width=4)
    arrow(d,(1950,650),(1950,790),"separate inference flow",label_offset=(150,-100))
    save(im,"dfads_overall_architecture.jpg")

def dfd_legacy():
    im,d=canvas("DFADS Data-Flow Diagram (Level 1)","Runtime audio analysis and voice conversion, with optional research and recording-data flows")
    # Runtime actors and processes
    rounded_box(d,(100,510,470,730),"Analyst / User\nBrowser or Streamlit",BLUE,body_size=28)
    rounded_box(d,(2520,1080,2900,1290),"Recording\nContributor",ORANGE,body_size=28)
    rounded_box(d,(650,450,1120,700),"P1 · Receive audio\nUpload / demo / microphone\nValidate and stage input",ORANGE,body_size=26)
    rounded_box(d,(1370,450,1850,700),"P2 · Analyze audio\nPreprocess and extract\n78-D acoustic feature vector",BLUE,body_size=26)
    rounded_box(d,(2090,450,2540,700),"P3 · Classify\nResNeXt or SVM\nReal/Fake + confidence",TEAL,body_size=26)
    rounded_box(d,(1370,900,1850,1130),"P4 · Convert voice\nRVC v2 target conversion\nEdge-TTS fallback",PURPLE,body_size=26)
    rounded_box(d,(2090,900,2540,1130),"P5 · Analyze clone\nSame feature + classifier\npath for synthesized audio",PINK,body_size=25)
    store(d,(650,800,1120,1050),"D1 · Audio files","Temporary source plus original\nand clone WAVs in app/static")
    # Runtime data flows: one clean top row and one clean conversion row.
    arrow(d,(470,620),(640,575),"audio / sample ID",label_offset=(0,-38))
    arrow(d,(1120,575),(1360,575),"audio signal",label_offset=(0,-38))
    arrow(d,(1850,575),(2080,575),"78-D vector",label_offset=(0,-38))
    d.line((2315,450,2315,300),fill=LINE,width=4)
    d.line((2315,300,290,300),fill=LINE,width=4)
    arrow(d,(290,300),(290,500),"verdict + confidence + graph data",label_offset=(165,-28))
    # Separate route for conversion; source audio goes to RVC, then the same
    # analysis process extracts features and classifies the generated result.
    arrow(d,(1120,675),(1360,955),"mic source audio",label_offset=(0,-34))
    arrow(d,(1850,1010),(2080,1010),"converted clone WAV",label_offset=(0,-38))
    d.line((2315,900,2315,780),fill=LINE,width=4)
    d.line((2315,780,1610,780),fill=LINE,width=4)
    arrow(d,(1610,780),(1610,710),"same analysis path",label_offset=(140,-28))
    # Persist the uploaded source file as an audio artifact.
    arrow(d,(885,700),(885,790),"stage source",color="#56855B",width=4,label_offset=(110,-10))
    # Offline research lane, deliberately separated from the live runtime flow.
    d.rounded_rectangle((100,1210,2900,1760),radius=28,fill="#F0F6F0",outline="#A8C2A8",width=3)
    d.text((140,1230),"OFFLINE RESEARCH AND DATASET WORKFLOW",font=font(27,True),fill="#58735A")
    rounded_box(d,(160,1340,500,1580),"Researcher\nRun research\nscripts",PURPLE,body_size=25)
    rounded_box(d,(590,1340,1000,1580),"P6 · Prepare / Train / Evaluate\nBuild features; train baseline /\nResNeXt; run evaluation",BLUE,body_size=23)
    store(d,(1100,1330,1580,1610),"D2 · Research data","Feature table, test split,\nrecordings + CSV metadata")
    rounded_box(d,(1690,1340,2080,1580),"P7 · Save recording\nCheck consent, ID, duration\nand signal level",ORANGE,body_size=23)
    store(d,(2190,1330,2780,1610),"D3 · Models + Results","Scaler, SVM, ResNeXt and RVC files;\nmetrics, plots and evaluation CSVs",fill="#FFF2DC")
    arrow(d,(500,1460),(580,1460),"run",label_offset=(0,-38))
    arrow(d,(1000,1460),(1090,1460),"features / labels",label_offset=(0,-38))
    arrow(d,(1580,1460),(2180,1460),"models + saved metrics",label_offset=(0,-38))
    arrow(d,(2070,1460),(2250,1460),"models + metrics",label_offset=(0,-38))
    # Local model files are also consumed by the runtime inference and RVC services.
    arrow(d,(2440,1330),(2440,720),"load detector / RVC models",color="#56855B",width=4,label_offset=(150,0))
    # Contributor data enters only through explicit consent capture, then is
    # written to the real-recording dataset; the live endpoint does not do this.
    d.line((2710,1290,2710,1720),fill="#56855B",width=4)
    d.line((2710,1720,795,1720),fill="#56855B",width=4)
    arrow(d,(795,1720),(795,1590),"consent + speaker ID + audio",color="#56855B",width=4,label_offset=(160,-8))
    d.rounded_rectangle((1700,1225,2840,1315),radius=16,fill="#FFFFFF",outline="#CBD7E5",width=2)
    d.text((1730,1237),"/api/metrics serves saved results/metrics.json.",font=font(21),fill=MUTED)
    d.text((1730,1268),"No SQL database or cloud sync is implemented.",font=font(21),fill=MUTED)
    save(im,"dfads_data_flow_diagram.jpg")

def dfd():
    im,d=canvas("DFADS Data-Flow Diagram (Level 1)","Runtime audio analysis and voice conversion, with offline model development and evaluation")
    # Online audio path
    rounded_box(d,(100,500,450,720),"Analyst / User\nBrowser or Streamlit",BLUE,body_size=27)
    rounded_box(d,(650,480,1120,720),"P1 · Receive audio\nUpload / demo / microphone\nOptional consented recording",ORANGE,body_size=25)
    rounded_box(d,(1370,480,1850,720),"P2 · Analyze audio\nMono 16 kHz + features\n78-D acoustic vector",BLUE,body_size=26)
    rounded_box(d,(2090,480,2540,720),"P3 · Classify\nResNeXt or SVM\nReal/Fake + confidence",TEAL,body_size=26)
    store(d,(650,850,1120,1080),"D1 · Audio files","Temporary upload; original and\nclone WAVs under app/static")
    rounded_box(d,(1370,870,1850,1090),"P4 · Convert voice\nLocal RVC v2; Edge-TTS\nfallback for text or failure",PURPLE,body_size=25)
    rounded_box(d,(2090,870,2540,1090),"P5 · Analyze clone\nSame feature extraction and\nclassification path",PINK,body_size=25)
    arrow(d,(450,600),(640,600),"audio / sample ID",label_offset=(0,-38))
    arrow(d,(1120,600),(1360,600),"audio signal",label_offset=(0,-38))
    arrow(d,(1850,600),(2080,600),"78-D vector",label_offset=(0,-38))
    d.line((2315,480,2315,340),fill=LINE,width=4)
    d.line((2315,340,275,340),fill=LINE,width=4)
    arrow(d,(275,340),(275,490),"verdict + confidence + graph data",label_offset=(155,-28))
    arrow(d,(885,720),(885,840),"stage source",color="#56855B",width=4,label_offset=(110,-10))
    arrow(d,(1120,670),(1360,940),"mic source audio",label_offset=(0,-34))
    arrow(d,(1850,980),(2080,980),"converted clone WAV",label_offset=(0,-38))
    d.line((2315,870,2315,800),fill=LINE,width=4)
    d.line((2315,800,1610,800),fill=LINE,width=4)
    arrow(d,(1610,800),(1610,730),"same analysis path",label_offset=(140,-27))

    # Offline research/data lane
    d.rounded_rectangle((100,1190,2900,1760),radius=28,fill="#F0F6F0",outline="#A8C2A8",width=3)
    d.text((140,1210),"OFFLINE RESEARCH AND DATASET WORKFLOW",font=font(27,True),fill="#58735A")
    rounded_box(d,(160,1350,500,1580),"Researcher\nRun preparation,\ntraining and evaluation",PURPLE,body_size=24)
    store(d,(700,1330,1250,1600),"D2 · Research data","Features, test split, recordings\nand CSV metadata")
    rounded_box(d,(1450,1350,2020,1580),"P6 · Prepare / Train / Evaluate\nBuild features; train baseline /\nResNeXt; evaluate and test robustness",BLUE,body_size=23)
    store(d,(2220,1330,2810,1600),"D3 · Models + Results","Scaler, SVM, ResNeXt, RVC files;\nmetrics, plots and evaluation CSVs",fill="#FFF2DC")
    arrow(d,(500,1465),(690,1465),"dataset",label_offset=(0,-38))
    arrow(d,(1250,1465),(1440,1465),"features",label_offset=(0,-38))
    arrow(d,(2020,1465),(2210,1465),"results",label_offset=(0,-38))
    d.rounded_rectangle((840,1635,2180,1725),radius=16,fill="#FFFFFF",outline="#CBD7E5",width=2)
    d.text((875,1647),"/api/metrics reads saved metrics.json. No SQL database or cloud sync is implemented.",font=font(22),fill=MUTED)
    save(im,"dfads_data_flow_diagram.jpg")

if __name__ == "__main__":
    use_case()
    architecture()
    dfd()
