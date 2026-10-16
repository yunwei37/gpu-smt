from pathlib import Path
import subprocess,json,time,datetime
from PIL import Image,ImageOps,ImageDraw
r=Path('/workspaces/repository');o=Path("/workspaces/repository/docs/tmp/bootstrap/step-0010-20261014T133154+0000/experiment-039");d=Path('/tmp/gpu-smt-paid-preparation-paper-qa-20261016');d.mkdir(exist_ok=True)
start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
z=subprocess.run(['pdftoppm','-png','-r','90',str(r/'docs/paper/main.pdf'),str(d/'page')],capture_output=True,text=True)
pages=sorted(d.glob('page-*.png'))
for block in range((len(pages)+3)//4):
 subset=pages[block*4:block*4+4];images=[Image.open(p).convert('RGB') for p in subset]
 w=max(x.width for x in images);h=max(x.height for x in images);sheet=Image.new('RGB',(w*2,h*2),(220,220,220))
 for j,img in enumerate(images):sheet.paste(img,((j%2)*w,(j//2)*h))
 sheet.save(d/('sheet-'+str(block+1)+'.png'))
v={'started_utc':start,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'wall_seconds':time.monotonic()-t,'exit_code':z.returncode,'pages':len(pages),'sheets':(len(pages)+3)//4,'render_dir':str(d),'stderr':z.stderr}
(o/'render.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps(v))
