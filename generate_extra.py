from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from pathlib import Path
import random
W,H=A4;root=Path(__file__).parent
teal=HexColor('#087d79');ink=HexColor('#263b43')
def page(c,title,subtitle,n=1):
 c.setFillColor(teal);c.roundRect(35,H-105,W-70,70,15,fill=1,stroke=0);c.setFillColorRGB(1,1,1);c.setFont('Helvetica-Bold',24);c.drawString(55,H-68,title);c.setFont('Helvetica',11);c.drawString(55,H-89,subtitle);c.setFillColor(ink);c.setStrokeColor(ink);c.setFont('Helvetica',11);c.drawString(45,H-137,'Name: __________________________    Date: _________________');c.setFont('Helvetica',10);c.drawString(45,30,'LITTLE BLOOM / For home and classroom use');c.drawRightString(W-45,30,str(n))
# A simple original word search, with an answer page.
rng=random.Random(17);grid=[[rng.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(10)]for _ in range(10)];words=['FLOWER','GARDEN','SUN','LEAF','RAIN'];placements=[(0,1),(2,3),(4,5),(6,2),(8,4)]
for word,(r,col) in zip(words,placements):
 for j,ch in enumerate(word):grid[r][col+j]=ch
c=canvas.Canvas(str(root/'private/downloads/wordsearch.pdf'),pagesize=A4);c.setTitle('Garden Word Search')
for n in [1,2]:
 page(c,'Garden Word Search','Find five garden words. Look from left to right.',n);size=38;x0=107;y0=H-208;c.setFont('Helvetica-Bold',17)
 for r in range(10):
  for col in range(10):
   if n==2 and any(r==rr and cc<=col<cc+len(w) for w,(rr,cc) in zip(words,placements)):c.setFillColor(HexColor('#ffe080'));c.rect(x0+col*size-7,y0-r*size-7,28,28,fill=1,stroke=0)
   c.setFillColor(ink);c.drawString(x0+col*size,y0-r*size,grid[r][col])
 c.setFont('Helvetica-Bold',16);c.drawCentredString(W/2,180,'FLOWER   GARDEN   SUN   LEAF   RAIN');c.setFont('Helvetica',13);c.drawCentredString(W/2,130,'Circle each word, then draw your favorite garden discovery.');c.showPage()
c.save()
# Maze: DFS carving guarantees one traversable path.
N=9;rng=random.Random(4);visited={(0,0)};stack=[(0,0)];edges=set()
while stack:
 x,y=stack[-1];choices=[(xx,yy)for xx,yy in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]if 0<=xx<N and 0<=yy<N and (xx,yy)not in visited]
 if not choices:stack.pop();continue
 nxt=rng.choice(choices);edges.add(frozenset([(x,y),nxt]));visited.add(nxt);stack.append(nxt)
def solve(pos,seen):
 if pos==(N-1,N-1):return[pos]
 for edge in edges:
  if pos in edge:
   nxt=next(iter(edge-{pos}))
   if nxt not in seen:
    out=solve(nxt,seen|{nxt})
    if out:return[pos]+out
 return None
solution=solve((0,0),{(0,0)});c=canvas.Canvas(str(root/'private/downloads/maze.pdf'),pagesize=A4);c.setTitle('The Garden Maze')
for n in [1,2]:
 page(c,'The Garden Maze','Find a path from START to FINISH.',n);s=49;ox=77;oy=210;c.setLineWidth(2)
 for y in range(N):
  for x in range(N):
   left=ox+x*s;bottom=oy+(N-1-y)*s
   if y==0 and x!=0:c.line(left,bottom+s,left+s,bottom+s)
   if x==0:c.line(left,bottom,left,bottom+s)
   if x==N-1 or frozenset([(x,y),(x+1,y)])not in edges:c.line(left+s,bottom,left+s,bottom+s)
   if y==N-1:
    if x!=N-1:c.line(left,bottom,left+s,bottom)
   elif frozenset([(x,y),(x,y+1)])not in edges:c.line(left,bottom,left+s,bottom)
 c.setFont('Helvetica-Bold',12);c.drawString(ox,oy+N*s+15,'START');c.drawRightString(ox+N*s,oy-22,'FINISH')
 if n==2:
  p=c.beginPath();p.moveTo(ox+s/2,oy+(N-.5)*s)
  for x,y in solution:p.lineTo(ox+(x+.5)*s,oy+(N-y-.5)*s)
  c.setStrokeColor(teal);c.setLineWidth(3);c.drawPath(p);c.setStrokeColor(ink)
 c.setFont('Helvetica',13);c.drawString(45,125,'Go slowly and try another path when you meet a wall.');c.showPage()
c.save()
c=canvas.Canvas(str(root/'private/downloads/shapes.pdf'),pagesize=A4);c.setTitle('My Shape Studio');page(c,'My Shape Studio','Trace each shape, then draw one beside it.');c.setFont('Helvetica',13);c.drawString(45,H-173,'Can you find these shapes around your home?')
for i,label in enumerate(['Circle','Square','Triangle','Rectangle']):
 y=H-270-i*125;c.setFont('Helvetica-Bold',15);c.drawString(45,y+53,label);c.setDash(3,4)
 if i==0:c.circle(125,y,35)
 if i==1:c.rect(90,y-35,70,70)
 if i==2:
  p=c.beginPath();p.moveTo(85,y-35);p.lineTo(165,y-35);p.lineTo(125,y+35);p.close();c.drawPath(p)
 if i==3:c.rect(75,y-27,100,54)
 c.setDash();c.setStrokeColor(HexColor('#bccfc8'));c.roundRect(265,y-45,265,90,12);c.setStrokeColor(ink)
c.showPage();c.save()
c=canvas.Canvas(str(root/'private/downloads/gratitude.pdf'),pagesize=A4);c.setTitle('My Little Gratitude Journal');page(c,'My Little Gratitude Journal','Notice three lovely things about today.');
for y,label in [(H-200,'Someone who helped me today:'),(H-370,'Something that made me smile:'),(H-540,'One small thing I am thankful for:')]:
 c.setFillColor(ink);c.setFont('Helvetica-Bold',14);c.drawString(45,y,label);c.setStrokeColor(HexColor('#bdd7c9'));c.roundRect(45,y-133,W-90,115,12);c.setStrokeColor(ink)
c.setFont('Helvetica',12);c.drawString(45,85,'Draw or write in each box. Your grown-up can help you.');c.showPage();c.save();print('Four additional PDFs created')
