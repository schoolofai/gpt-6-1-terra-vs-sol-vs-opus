import glob,json,os
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops, ImageStat
OUT='captures/tough'; rep={}
with sync_playwright() as p:
  b=p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
  for d in sorted(glob.glob('runs_tough/R9/*')):
    m=d.split('/')[-1]; f=d+'/work/index.html'; key=f'{m}_R9'; errs=[]; r={}
    ctx=b.new_context(viewport={'width':1280,'height':800},record_video_dir=f'{OUT}/vid_{key}',record_video_size={'width':1280,'height':800})
    pg=ctx.new_page(); pg.on('pageerror',lambda e:errs.append('pageerror: '+str(e))); pg.on('console',lambda c: errs.append(c.text) if c.type=='error' else None)
    pg.goto('file://'+os.path.abspath(f)); pg.wait_for_timeout(4000)
    r['webgl_canvas']=pg.evaluate("(()=>{const c=[...document.querySelectorAll('canvas')];return c.some(x=>{try{return !!(x.getContext('webgl2')||x.getContext('webgl'))}catch(e){return false}})})()")
    shots=[]
    for i,t in enumerate([0,700,700,3000]):
      pg.wait_for_timeout(t); fn=f'{OUT}/{key}_{i}.png'; pg.screenshot(path=fn); shots.append(fn)
    a,bb=Image.open(shots[1]).convert('L'),Image.open(shots[2]).convert('L')
    r['frame_diff_700ms']=round(ImageStat.Stat(ImageChops.difference(a,bb)).mean[0],2)
    r['animated']=r['frame_diff_700ms']>0.3
    # mouse orbit drag
    pg.mouse.move(640,400); pg.mouse.down(); pg.mouse.move(900,380,steps=10); pg.mouse.up(); pg.wait_for_timeout(500); pg.screenshot(path=f'{OUT}/{key}_drag.png')
    r['console_errors']=errs[:5]; r['no_errors']=not errs
    rep[m]=r; ctx.close(); print(m,r)
json.dump(rep,open(f'{OUT}/r9_report.json','w'),indent=1)
