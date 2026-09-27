from pathlib import Path
import re,json,html,hashlib,io
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy import ndimage,sparse
from scipy.sparse.linalg import spsolve
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'assets/unified';OUT.mkdir(exist_ok=True)
MASTER=ROOT/'assets/semaglutide-lotusbio-research-product.webp'
base=Image.open(MASTER).convert('RGB'); a=np.asarray(base).copy()
font='/usr/share/fonts/opentype/urw-base35/NimbusSans-Bold.otf'
fontreg='/usr/share/fonts/opentype/urw-base35/NimbusSans-Regular.otf'
regions=[(56,240,280,281),(407,299,490,321),(426,373,468,390)]
def mask_rect(rect,white=False):
 x0,y0,x1,y1=rect; ar=a[y0:y1,x0:x1];m=(ar[:,:,1]<145)&(ar[:,:,0]<135) if not white else ar.min(axis=2)>100
 m=ndimage.binary_dilation(m,iterations=2)
 out=np.zeros(a.shape[:2],bool);out[y0:y1,x0:x1]=m;return out
name_mask=mask_rect(regions[0])|mask_rect(regions[1]);dose_mask=mask_rect(regions[2],True)
def heal(mask):
 out=a.copy(); ys,xs=np.where(mask);n=len(ys);ids=np.full(mask.shape,-1,int);ids[ys,xs]=np.arange(n)
 mat=sparse.lil_matrix((n,n));rhs=np.zeros((n,3))
 for i,(y,x) in enumerate(zip(ys,xs)):
  mat[i,i]=4
  for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
   j=ids[y+dy,x+dx]
   if j>=0:mat[i,j]=-1
   else:rhs[i]+=a[y+dy,x+dx]
 out[ys,xs]=np.clip(spsolve(mat.tocsr(),rhs),0,255).round().astype('uint8');return Image.fromarray(out)
# Reconstruct only the two name backgrounds from adjacent unprinted label areas.
# Quadratic surface preserves the master label's lighting; leaf pixels remain untouched.
def clear_names():
 out=a.copy()
 for idx,(x0,y0,x1,y1) in enumerate(regions[:2]):
  Y,X=np.mgrid[y0-5:y1+3,x0:x1];patch=a[y0-5:y1+3,x0:x1].astype(float)
  good=(patch.min(2)>195)&(np.abs(patch[:,:,0]-patch[:,:,1])<7)&((Y<y0)|(Y>=y1))
  if idx==0:good &= X<255
  xx=(X-x0)/(x1-x0);yy=(Y-y0)/(y1-y0)
  F=np.stack([np.ones_like(xx),xx,yy,xx*xx,xx*yy,yy*yy],-1)
  coeff=np.linalg.lstsq(F[good],patch[good],rcond=None)[0]
  pred=np.clip(F@coeff,0,255).round().astype('uint8')
  inside=(Y>=y0)&(Y<y1)
  if idx==0:inside &= ~((X>=254)&(Y>=273)&((patch[:,:,1]-patch[:,:,0])>10)&(patch[:,:,1]>100))
  patchout=out[y0-5:y1+3,x0:x1];patchout[inside]=pred[inside]
 return Image.fromarray(out)
clean=clear_names();clean_dose=clean.copy()
dose_healed=np.asarray(heal(dose_mask));cd=np.asarray(clean_dose).copy();cd[dose_mask]=dose_healed[dose_mask];clean_dose=Image.fromarray(cd)
def text(im,lines,rect,max_size,min_size=5,color=(0,53,45),regular=False):
 x0,y0,x1,y1=rect;w=x1-x0;h=y1-y0;S=4
 for size in np.arange(max_size,min_size-0.1,-0.25):
  f=ImageFont.truetype(fontreg if regular else font,round(size*S));boxes=[f.getbbox(l) for l in lines]; heights=[b[3]-b[1] for b in boxes];gap=1*S
  if max(b[2]-b[0] for b in boxes)<=w*S and sum(heights)+gap*(len(lines)-1)<=h*S:break
 layer=Image.new('RGBA',(w*S,h*S));d=ImageDraw.Draw(layer);y=0
 for line,b in zip(lines,boxes):
  d.text((-b[0],y-b[1]),line,font=f,fill=(*color,255));y+=b[3]-b[1]+gap
 layer=layer.resize((w,h),Image.Resampling.LANCZOS);im.paste(layer,(x0,y0),layer)
 return float(size)
def lines_for(name):
 if name=='CJC-1295 without DAC':return ['CJC-1295','without DAC']
 if name=='CJC-1295 with DAC':return ['CJC-1295','with DAC']
 if ' + ' in name:
  p=name.split(' + ');return [p[0]+' +',p[1]]
 if name=='FOXO4-DRI / FOXO4':return ['FOXO4-DRI / FOXO4']
 if name=='Bacteriostatic Water':return ['Bacteriostatic','Water']
 return [name]
catalog=(ROOT/'wholesale-peptides/index.html').read_text()
cards=re.findall(r'<a class="catalog-card".*?</a>',catalog,re.S)
assert len(cards)==43
records=[]
allowed=np.zeros(a.shape[:2],bool)
for x0,y0,x1,y1 in regions:allowed[y0:y1,x0:x1]=1
for card in cards:
 slug=re.search(r'href="/products/([^/]+)/',card)[1];name=html.unescape(re.search(r'<h2>(.*?)</h2>',card)[1]);src=re.search(r'<img src="([^"]+)"',card)[1]
 specs=html.unescape(re.search(r'class="catalog-formats">(.*?)</p>',card)[1]).split(' · ')
 dose='10 mg' if '10 mg' in specs else specs[0]
 im=(clean if dose=='10 mg' else clean_dose).copy()
 lines=lines_for(name)
 bs=text(im,lines,(58,243,258 if len(lines)>1 else 280,278),39)
 vs=text(im,lines,(409,303 if len(lines)==1 else 300,488,320),16)
 if dose!='10 mg':text(im,[dose],(429,376,468,387),12,color=(248,250,248),regular=True)
 if slug=='semaglutide':im=base.copy()
 dest=OUT/(slug+'.webp');buffer=io.BytesIO();im.save(buffer,format='WEBP',lossless=True,method=4);tmp=dest.with_suffix('.tmp');tmp.write_bytes(buffer.getvalue());tmp.replace(dest)
 decoded=np.asarray(Image.open(dest).convert('RGB'));diff=np.any(decoded!=a,axis=2);outside=int((diff&~allowed).sum());assert outside==0,(slug,outside)
 records.append(dict(slug=slug,name=name,specifications=specs,image_specification=dose,original_image=src,image='/assets/unified/'+slug+'.webp',box_font_size=bs,vial_font_size=vs,changed_pixels=int(diff.sum()),outside_text_regions_changed_pixels=outside))
(ROOT/'tools/image-unification/manifest.json').write_text(json.dumps({'master':'/assets/semaglutide-lotusbio-research-product.webp','master_sha256':hashlib.sha256(MASTER.read_bytes()).hexdigest(),'text_regions':regions,'products':records},indent=2,ensure_ascii=False))
clean.save(ROOT/'tools/image-unification/blank-name-master.png')
# Contact sheet is a QA preview, not a website asset.
sheet=Image.new('RGB',(5*256,9*290),'#f3f5f5');d=ImageDraw.Draw(sheet);f=ImageFont.truetype(fontreg,13)
for i,r in enumerate(records):
 x=(i%5)*256;y=(i//5)*290;sheet.paste(Image.open(OUT/(r['slug']+'.webp')).resize((256,256)),(x,y));d.text((x+8,y+259),r['name'],font=f,fill='black');d.text((x+8,y+275),r['image_specification'],font=f,fill='#24544a')
sheet.save(ROOT/'tools/image-unification/contact-sheet.jpg',quality=92)
print(json.dumps({'count':len(records),'outside_regions_changes':sum(r['outside_text_regions_changed_pixels'] for r in records),'total_bytes':sum(p.stat().st_size for p in OUT.glob('*.webp'))}))
