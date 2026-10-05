from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
import json,re,math,textwrap
from pathlib import Path
root=Path(__file__).parent
source=(root/'public/app.js').read_text()
# Extract the two original stories from the same source used by the reader.
stories={}
for m in re.finditer(r"id:'(seed|moon)'.*?title:'([^']+)'.*?story:\[(.*?)\]",source):
    stories[m[1]]=(m[2],re.findall(r"'([^']*)'",m[3]))
titles={'garden':'My Happy Garden','butterfly':'Butterfly Color Party','hunt':'Little Nature Detective','kindness':'My Kindness Adventure','numbers':'Count, Draw & Grow','writer':'Once Upon My Story'}
W,H=A4
ink=HexColor('#263b43');teal=HexColor('#087d79')
def frame(c,title,page=1):
    c.setFillColor(teal);c.setFont('Helvetica-Bold',13);c.drawString(45,H-45,'LITTLE BLOOM / FREE ORIGINAL RESOURCE')
    c.setFillColor(ink);c.setFont('Helvetica-Bold',25);c.drawString(45,H-93,title)
    c.setFont('Helvetica',10);c.drawString(45,30,'Little Bloom | For home and classroom use');c.drawRightString(W-45,30,str(page))
def paragraph(c,text,x,y,width=63,size=17):
    c.setFont('Helvetica',size)
    for line in textwrap.wrap(text,width):c.drawString(x,y,line);y-=size*1.6
    return y
for id,(title,pages) in stories.items():
    c=canvas.Canvas(str(root/f'private/downloads/{id}.pdf'),pagesize=A4);c.setTitle(title)
    for i,text in enumerate(pages):
        frame(c,title,i+1);c.setFont('Helvetica',12);c.drawString(45,H-124,f'A story to read together / Page {i+1}')
        c.drawImage(str(root/'private/story-art.jpg'),45,H-450,width=W-90,height=280,preserveAspectRatio=True,anchor='c')
        paragraph(c,text,45,340,width=51,size=17);c.showPage()
    c.save()
for id,title in titles.items():
    c=canvas.Canvas(str(root/f'private/downloads/{id}.pdf'),pagesize=A4);c.setTitle(title);frame(c,title)
    c.setFont('Helvetica',12);c.drawString(45,H-124,'Name: _________________________    Date: __________________')
    c.setStrokeColor(ink);c.setFillColor(ink);c.setLineWidth(2)
    if id=='garden':
        paragraph(c,'Color the flower. Add your own garden around it.',45,H-165,size=13)
        cx,cy=297,440
        for a in range(0,360,60):
            x=cx+75*math.cos(math.radians(a));y=cy+75*math.sin(math.radians(a));c.circle(x,y,49,stroke=1,fill=0)
        c.setFillColorRGB(1,1,1);c.circle(cx,cy,48,stroke=1,fill=1);c.line(cx,315,cx,180)
        p=c.beginPath();p.moveTo(cx,240);p.curveTo(200,300,200,210,cx,240);c.drawPath(p)
        p=c.beginPath();p.moveTo(cx,205);p.curveTo(390,270,400,180,cx,205);c.drawPath(p)
    elif id=='butterfly':
        paragraph(c,'Color both wings. Try making matching patterns.',45,H-165,size=13)
        c.ellipse(135,380,295,630);c.ellipse(300,380,460,630);c.ellipse(155,250,295,405);c.ellipse(300,250,440,405)
        c.ellipse(280,305,315,560);c.circle(298,570,23);c.line(289,590,265,620);c.line(307,590,330,620)
        for x in [212,380]:
            for y in [460,535]:c.circle(x,y,23)
    elif id=='hunt':
        paragraph(c,'Explore with a grown-up. Tick what you discover.',45,H-165,size=13)
        for i,item in enumerate(['A smooth leaf','Something yellow','A bird sound','A tiny shadow','Something with a lovely smell']):
            y=H-230-i*63;c.rect(47,y-6,20,20);c.setFont('Helvetica',17);c.drawString(82,y,item)
        paragraph(c,'Draw your favorite discovery below. Leave nature where you found it.',45,270,width=68,size=12);c.rect(45,75,W-90,155)
    elif id=='kindness':
        paragraph(c,'Try a kind action. Tick it off when you finish.',45,H-165,size=13)
        for i,item in enumerate(['Thank someone who helps you.','Share a toy or a turn.','Help tidy a small space.','Say something kind to a friend.','Make a card for someone you love.']):
            y=H-230-i*63;c.rect(47,y-6,20,20);c.setFont('Helvetica',16);c.drawString(82,y,item)
        c.setFont('Helvetica',13);c.drawString(45,265,'How did being kind make you feel? Draw it here.');c.rect(45,75,W-90,165)
    elif id=='numbers':
        paragraph(c,'Draw the number of dots. Then write the number.',45,H-165,size=13)
        for i in range(1,6):
            y=H-220-(i-1)*110;c.setFont('Helvetica-Bold',35);c.drawString(48,y,str(i));c.rect(105,y-20,270,70);c.line(430,y-5,535,y-5)
    elif id=='writer':
        for i,text in enumerate(['My hero is:','My adventure takes place in:','The problem my hero must solve is:']):
            y=H-190-i*65;c.setFont('Helvetica-Bold',13);c.drawString(45,y,text);c.line(45,y-30,W-45,y-30)
        c.setFont('Helvetica-Bold',15);c.drawString(45,415,'Tell your story:')
        for y in range(380,65,-32):c.line(45,y,W-45,y)
    c.showPage();c.save()
print('Generated 8 PDFs')
