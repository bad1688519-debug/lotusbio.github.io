"""Maintain product-specific purchasing notes and contextual internal links."""
from pathlib import Path
import html
import re
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
DATA = {
 'retatrutide': ('Retatrutide','RT20',20,'Keep RT codes separate from TR codes when preparing a multi-product request. RT20 identifies the 20 mg Retatrutide vial format; TR20 belongs to Tirzepatide.','Ask for the complete material specification, including sequence and modifications, and documents linked to the proposed batch.','retatrutide-api'),
 'tirzepatide': ('Tirzepatide','TR30',30,'Choose each TR specification separately when ordering more than one vial size. TR30 and TR60 are distinct catalog lines and should have their own box quantities.','Confirm the supplied material form, batch identity and the basis of any reported content result.','tirzepatide-api'),
 'semaglutide': ('Semaglutide','SM10',10,'The vial catalog lists SM10, SM20 and SM30. State whether you need one specification or a mixed request, with a box count for each code.','Match the complete modified peptide and supplied material form to the proposed batch documentation.','semaglutide-api'),
 'bpc-157': ('BPC-157','BC5',5,'BC5 and BC10 are the standalone BPC-157 entries. If you are requesting this single product, use its BC code and do not substitute a combination-product code.','Confirm the stated sequence, terminal form and any counterion designation. Request identity, purity and measured content information as separate items where available.',None),
 'tb-500': ('TB-500','BT10',10,'BT5 and BT10 distinguish the listed vial quantities. Include the required sequence and terminal specification with your inquiry so the catalog name is not the only identity reference.','Resolve whether the proposed material is a fragment or a full-length peptide before comparing quotations. Request the matching identity specification and batch documentation.',None),
 'ghk-cu': ('GHK-Cu','CU50',50,'CU50 and CU100 identify the 50 mg and 100 mg vial formats. Specify GHK-Cu explicitly; a request for the free GHK peptide or AHK-Cu is a different material inquiry.','Ask how the copper-containing material is specified and how content is reported. Match the material description and batch reference across the quote, label and available report.',None),
 'kpv': ('KPV','KP10',10,'KP5 and KP10 are the listed KPV formats. Use the catalog code as well as the product name to keep the 5 mg and 10 mg options separate in repeat orders.','Check the sequence and terminal form against the material specification. If measured vial content is needed, request that result explicitly rather than relying on purity alone.',None),
 'mots-c': ('MOTS-c','MS40',40,'The catalog lists MS10, MS15, MS20 and MS40. Record the required code and number of boxes for each format; a request for 40 mg alone does not specify the number of vials.','Confirm the intended peptide sequence and terminal form. Ask for handling information tied to the actual supplied material and identify the batch needed for any repeat-order comparison.',None),
 'nad-plus': ('NAD+','NJ500',500,'NJ100, NJ500 and NJ1000 correspond to the listed NAD+ vial formats. Include the NJ code in your request rather than quoting only a total mass for the whole order.','Confirm the oxidized material and its stated salt or hydrate form, together with the basis used to report content and the handling information for that material.',None),
 'ss-31': ('SS-31','2S10',10,'The SS-31 entries are 2S10 and 2S50. Use these codes and the vial specification together, especially when discussing a document that names Elamipretide.','Confirm the supplied form and whether a content result is expressed as peptide or as the complete salt. A raw-material document should not be assumed to measure content in finished vials.',None),
 'cagrilintide': ('Cagrilintide','CGL5',5,'CGL5 and CGL10 are the standalone Cagrilintide catalog options. Specify the individual product and box count when it is part of a larger multi-product inquiry.','Match the full material identity and any salt designation to the proposed batch. Request available identity and content documentation for the selected vial format.',None),
 'aod9604': ('AOD9604','5AD',5,'The catalog uses 5AD for 5 mg and 10AD for 10 mg vials. Include the code exactly as listed so that a number in the product name is not mistaken for the vial quantity.','Use the stated material specification and identity documentation to compare suppliers. Confirm terminal and structural details against the reference section below.',None),
}

def esc(s): return html.escape(str(s), quote=True)
def link(slug, suffix='specifications'):
 return f'<a href="/products/{slug}/">{esc(DATA[slug][0])} {suffix}</a>'
def section_marker(key, body):
 return f'\n<!-- {key}:start -->\n{body}\n<!-- {key}:end -->\n'
changed=[]
def save(path,s):
 p=ROOT/path
 if p.read_text()!=s: p.write_text(s);changed.append(path)
def upsert(s,key,body):
 block=section_marker(key,body)
 if f'<!-- {key}:start -->' in s:
  return re.sub(r'\s*<!-- '+key+r':start -->.*?<!-- '+key+r':end -->\s*',lambda _:block,s,flags=re.S)
 return s.replace('</main>',block+'</main>',1)

def main():
 for slug,(name,code,mg,selection,docs,raw) in DATA.items():
  path=f'products/{slug}/index.html';s=(ROOT/path).read_text()
  assert f'{mg} mg × 10 vials · {code}' in s,(slug,code)
  actions=re.search(r'<section><h2>Prepare your wholesale request</h2>.*?(<div class="actions">.*?</div>)</section>',s,re.S)
  # Retain the existing inquiry controls and their exact destinations.
  if actions:
   action_html=actions.group(1)
  else:
   existing=re.search(r'<!-- core-procurement:start -->.*?(<div class="actions">.*?</div>)',s,re.S)
   action_html=existing.group(1) if existing else f'<div class="actions"><a class="button dark" href="/wholesale/?product={quote(name)}#inquiry">Request {esc(name)} pricing</a></div>'
  raw_link=f'<a href="/raw-materials/{raw}/">{esc(name)} raw-material requirements</a>' if raw else '<a href="/raw-materials/">bulk raw-material requirements</a>'
  body=f'''<section class="procurement-notes" id="purchasing-details"><h2>{esc(name)} purchasing details</h2>
<h3>Select the catalog format</h3><p>{esc(selection)}</p>
<p><strong>Quantity example:</strong> {esc(code)} lists {mg} mg per vial and 10 vials per box. An inquiry for 2 boxes means 20 vials at {mg} mg each. These are catalog label quantities, not batch assay results.</p>
<h3>Vials or bulk raw material?</h3><p>The quote selector on this page uses boxes of finished vials. For {raw_link}, specify the required total mass, material specification and container requirements separately; the vial pack does not establish a raw-material minimum order quantity.</p>
<h3>Documents and quotation scope</h3><p>{esc(docs)} Use the <a href="/guides/coa-verification-guide/">COA review checklist</a> to record the product, batch and test scope.</p>
<p>Send the selected code, box count, destination country and requested delivery date. Ask the quote to confirm availability, minimum quantity, preparation time, shipping service and cost. If custom labels or boxes are needed, include them in the <a href="/private-label-peptides/">packaging inquiry</a>. Delivery timing and batch documents are confirmed for the proposed order. The <a href="/guides/wholesale-peptide-supplier-checklist/">supplier checklist</a> covers the wider purchasing review.</p>
{action_html}</section>'''
  if actions:s=s.replace(actions.group(),section_marker('core-procurement',body))
  elif '<!-- core-procurement:start -->' in s:s=upsert(s,'core-procurement',body)
  else:
   s,n=re.subn(r'<section><h2>Packaging and repeat orders</h2>.*?</section>',lambda _:section_marker('core-procurement',body),s,count=1,flags=re.S);assert n==1,slug
  if slug in ['bpc-157','ghk-cu'] and 'href="/products/kpv/"' not in s:
   s=s.replace('<h2>Related catalog products</h2><ul>','<h2>Related catalog products</h2><ul><li>'+link('kpv')+'</li>',1)
  if slug in ['kpv','aod9604']:
   related=['bpc-157','ghk-cu'] if slug=='kpv' else ['cagrilintide','semaglutide']
   s=upsert(s,'core-related-routes','<section><h2>Other catalog specifications</h2><p>For a multi-product inquiry, select each product and pack code separately: '+' · '.join(link(x) for x in related)+'.</p></section>')
  # Remove the older generic duplicate; molecular-reference sections remain intact.
  s=re.sub(r'<section class="procurement-notes"><h2>What to confirm before a wholesale inquiry</h2>.*?</section>','',s,flags=re.S)
  save(path,s)

 groups=[('Vial specifications and raw-material routes',['retatrutide','tirzepatide','semaglutide']),('Single-product vial inquiries',['bpc-157','tb-500','ghk-cu','kpv']),('Additional catalog formats',['mots-c','nad-plus','ss-31','cagrilintide','aod9604'])]
 navigation=''.join('<h3>'+title+'</h3><p>'+' · '.join(link(slug) for slug in slugs)+'</p>' for title,slugs in groups)
 for path,title,intro in [
  ('guides/wholesale-peptide-supplier-checklist/index.html','Apply the checklist to your product','Open the product page to select its catalog code and box quantity before preparing your supplier request. These links group purchasing routes; they do not imply interchangeable materials.'),
  ('wholesale/index.html','Choose a product before requesting a quote','Use the product-specific purchasing notes to distinguish vial quantities from bulk-material requirements. Each product page provides its current catalog formats and an inquiry link.'),
 ]:
  s=(ROOT/path).read_text();body=f'<section class="procurement-notes"><h2>{title}</h2><p>{intro}</p>{navigation}</section>'
  save(path,upsert(s,'core-product-routes',body))
 path='guides/coa-verification-guide/index.html';s=(ROOT/path).read_text()
 body='<section class="procurement-notes"><h2>Connect a report to the requested format</h2><p>Start from the selected product and catalog code, then identify the proposed batch. A report for bulk raw material does not by itself confirm the measured content of finished vials, and a report for one batch should not be assigned to another.</p><ul><li>For '+link('retatrutide')+', '+link('tirzepatide')+' and '+link('semaglutide')+', distinguish the vial order from a bulk-material inquiry.</li><li>For '+link('bpc-157')+', '+link('kpv')+' and '+link('tb-500')+', record the exact identity specification alongside the pack code.</li><li>For '+link('ghk-cu')+', '+link('nad-plus')+' and '+link('ss-31')+', check the stated material form and content basis.</li><li>For '+link('mots-c')+', '+link('cagrilintide')+' and '+link('aod9604')+', match the selected vial format to the quoted batch.</li></ul></section>'
 save(path,upsert(s,'core-document-routes',body))
 path='raw-materials/index.html';s=(ROOT/path).read_text()
 body='<section class="procurement-notes"><h2>Looking for finished vials instead?</h2><p>The raw-material list above is for bulk-material sourcing discussions. For catalog vial formats, use '+', '.join(link(x) for x in DATA)+'. Vial packaging and raw-material quantities are quoted separately.</p></section>'
 save(path,upsert(s,'core-format-routes',body))
 # Give underlinked KPV a visible, descriptive homepage entry alongside the existing highlights.
 path='index.html';s=(ROOT/path).read_text()
 if 'href="/products/kpv/"' not in s:
  match=re.search(r'<a\b[^>]*href="/products/bpc-157/"[^>]*>.*?</a>',s,re.S)
  assert match
  s=s[:match.end()]+match.group().replace('/products/bpc-157/','/products/kpv/').replace('BPC-157','KPV')+s[match.end():]
 save(path,s)
 sitemap=(ROOT/'sitemap.xml').read_text()
 for path in changed:
  url='https://lbiopeptides.com/'+path.removesuffix('index.html')
  pat=r'(<loc>'+re.escape(url)+r'</loc><lastmod>)[^<]+'
  sitemap,n=re.subn(pat,lambda m:m.group(1)+'2026-09-28',sitemap);assert n==1,path
 save('sitemap.xml',sitemap)
 print('Updated:',len(changed),'files');print('\n'.join(changed))

if __name__=='__main__': main()
