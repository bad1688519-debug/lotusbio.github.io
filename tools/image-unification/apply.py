from pathlib import Path
import json,re,subprocess
ROOT=Path(__file__).resolve().parents[2]
manifest=json.loads((ROOT/'tools/image-unification/manifest.json').read_text());products=manifest['products']
cat=ROOT/'wholesale-peptides/index.html';text=cat.read_bytes().decode();updated=[]
for r in products:
 text=text.replace(r['original_image'],r['image'])
 p=ROOT/'products'/r['slug']/'index.html';s=p.read_bytes().decode();assert r['original_image'] in s or r['image'] in s,r['slug'];s=s.replace(r['original_image'],r['image']);s=re.sub(r'(<meta property="og:image" content=")[^"]+',lambda m:m[1]+'https://lbiopeptides.com'+r['image'],s);p.write_bytes(s.encode());updated.append(str(p.relative_to(ROOT)))
cat.write_bytes(text.encode());updated.append(str(cat.relative_to(ROOT)))
# Verify that metadata and visible images agree, and that original option texts are identical.
for r in products:
 p=ROOT/'products'/r['slug']/'index.html';s=p.read_text();orig=subprocess.check_output(['git','show','HEAD:'+str(p.relative_to(ROOT))],cwd=ROOT,text=True)
 assert re.findall(r'<option.*?</option>',s)==re.findall(r'<option.*?</option>',orig)
 assert re.search(r'<link rel="canonical"[^>]+>',s)[0]==re.search(r'<link rel="canonical"[^>]+>',orig)[0]
 assert re.search(r'<section class="product-order".*?<img src="([^"]+)"',s,re.S)[1]==r['image']
 assert re.search(r'<meta property="og:image" content="([^"]+)"',s)[1]=='https://lbiopeptides.com'+r['image']
 assert (ROOT/r['image'].lstrip('/')).is_file()
 assert r['image_specification'] in r['specifications']
for src in re.findall(r'<a class="catalog-card".*?<img src="([^"]+)"',text,re.S):assert src.startswith('/assets/unified/')
print(json.dumps({'pages':len(updated),'products':len(products),'options_and_canonicals_preserved':True}))
(ROOT/'tools/image-unification/changed-pages.json').write_text(json.dumps(updated,indent=2))
