"""Build reviewed reference sections; never infer a batch identity from a catalog name."""
from pathlib import Path
import html, json, re

ROOT = Path(__file__).resolve().parents[1]
SOURCES = json.loads((ROOT / 'scripts/molecular-sources-2026-09-28.json').read_text())
DATE = '2026-09-28'
DATA = {}

def add(slug, title, intro, heading, detail, check, images=(), sources=(), related=()):
    DATA[slug] = dict(title=title, intro=intro, heading=heading, detail=detail,
                      check=check, images=list(images), sources=list(sources), related=list(related))

add('retatrutide', 'Retatrutide: modified peptide identity',
    'Retatrutide is also identified in the research literature as LY3437943. It is a modified peptide with a lipid-bearing side chain; the complete identity includes the peptide sequence, non-standard residues, attachment site and linker.',
    'Sequence notation matters',
    'A one-letter sequence can omit the chemistry of non-standard residues and side-chain modifications. When comparing a proposed material with a published reference, request an explicit residue-by-residue specification and the full modification description. Similar names or an equal nominal mass do not establish identical structures.',
    'Use RT catalog codes for the pack sizes above. Match the structural specification to batch identity data, and review purity and measured vial content as separate results.',
    images=['retatrutide'],
    sources=[('https://pubchem.ncbi.nlm.nih.gov/substance/507750402','IUPHAR/BPS substance record linking retatrutide to CID 171390338'),('https://pmc.ncbi.nlm.nih.gov/articles/PMC11255275/','Li et al., 2024: retatrutide structural study')],
    related=[('tirzepatide','Tirzepatide'),('semaglutide','Semaglutide')])
add('tirzepatide', 'Tirzepatide: peptide and lipid side chain',
    'Tirzepatide is a 39-residue synthetic peptide conjugated to a C20 fatty diacid moiety. Its molecular identity therefore includes more than the amino-acid backbone. PubChem CID 156588324 is the reference compound used below.',
    'Parent peptide versus a salt form',
    'The reference formula describes the depicted parent compound. An acetate or another counterion-containing preparation needs a separate material-form description. A peptide intermediate or a stereoisomer should not be treated as the finished reference simply because it has a similar name.',
    'TR codes identify the listed pack sizes. For a repeat-order comparison, request the modification details, batch-linked identity result and the basis used for any content measurement.',
    images=['tirzepatide'], related=[('retatrutide','Retatrutide'),('semaglutide','Semaglutide')])
add('mots-c', 'MOTS-c: mitochondrial-derived peptide reference',
    'MOTS-c was described as a 16-amino-acid peptide encoded within the mitochondrial 12S rRNA region. The reference image depicts the database peptide, rather than mitochondrial DNA or a protein carrying a MOTS-c tag.',
    'Reference peptide and modified constructs',
    'A tagged construct, a sequence mutant and an unmodified peptide are different research materials. Specify the complete sequence and terminal form when comparing MOTS-c listings; the biological name alone does not describe an experimental construct.',
    'The MS10, MS15, MS20 and MS40 entries distinguish pack quantities. Confirm identity and handling documentation for the actual material; a database illustration is not a stability study for a supplied vial.',
    images=['mots-c'], sources=[('https://pubmed.ncbi.nlm.nih.gov/25738459/','Lee et al., 2015: original MOTS-c study')], related=[('ss-31','SS-31'),('nad-plus','NAD+')])
add('ipamorelin', 'Ipamorelin: a modified pentapeptide',
    'Ipamorelin is a five-residue peptide whose reference sequence is Aib–His–D-2-Nal–D-Phe–Lys–NH2. Aib and D-2-Nal are non-standard residues, and the C-terminal amide is part of the identity.',
    'Keep stereochemistry explicit',
    'The D designations and naphthyl-containing residue must be retained in a structural comparison. A sequence written only as ordinary amino-acid initials can hide these distinctions. The parent reference also does not specify every possible counterion in a supplied preparation.',
    'IP5 and IP10 are single-product pack entries. They should be distinguished from the CJC-1295 or Tesamorelin combinations, where the amount of Ipamorelin must be stated separately.',
    images=['ipamorelin'], related=[('cjc-1295-ipamorelin','CJC-1295 + Ipamorelin'),('tesamorelin-ipamorelin','Tesamorelin + Ipamorelin')])
add('selank', 'Selank: seven-residue peptide identity',
    'The Selank reference is Thr–Lys–Pro–Arg–Pro–Gly–Pro, a seven-residue peptide. Its sequence differs from Semax even though the names are sometimes grouped together in catalogs.',
    'Distinguish the parent from derivatives',
    'Acetylation, amidation or replacement of a residue changes the chemical identity. A material described as a Selank derivative requires its own specification rather than automatic assignment to the parent structure shown here.',
    'SK5 and SK10 list Selank pack options. For the Semax + Selank entry, check each component quantity and the analytical coverage for both peptides.',
    images=['selank'], related=[('semax','Semax'),('semax-selank','Semax + Selank')])
add('semax', 'Semax: ACTH-fragment-related peptide reference',
    'The Semax reference sequence is Met–Glu–His–Phe–Pro–Gly–Pro. PubChem lists this seven-residue molecule under ACTH (4–7), Pro–Gly–Pro-. It is a defined peptide, not full-length ACTH.',
    'Sequence and modification checks',
    'Retain the methionine-containing sequence and terminal chemistry when comparing reference records. A preparation bearing an additional acetyl group, an amide or another modification needs to be identified separately.',
    'XA5 and XA10 refer to the single-product packs above. XSL20 is a separate combination entry; its total amount should not be interpreted as the amount of Semax alone.',
    images=['semax'], related=[('selank','Selank'),('semax-selank','Semax + Selank')])
add('epithalon', 'Epithalon / Epitalon: tetrapeptide reference',
    'Epithalon and Epitalon are spellings used for the Ala–Glu–Asp–Gly tetrapeptide reference. PubChem CID 219042 records the parent compound as Epitalon.',
    'A name match is only the first check',
    'Compare the sequence, terminal groups and material form in the specification. The diagram depicts a defined four-residue molecule and should not be used to identify a mixture or extract with a similar name.',
    'ET10 and ET50 distinguish the listed pack sizes. Ask for the identity assignment behind the batch report; a marketing description or a reference molecular weight alone is not batch verification.',
    images=['epithalon'], related=[('dsip','DSIP'),('thymosin-alpha-1','Thymosin alpha 1')])
add('dsip', 'DSIP: delta sleep-inducing peptide reference',
    'DSIP is the abbreviation used for delta sleep-inducing peptide, a nine-residue peptide recorded in PubChem CID 68816. The chemical reference identifies the molecule; the descriptive name is not a performance claim for a catalog vial.',
    'Linear peptide versus related forms',
    'The displayed parent structure should be distinguished from a phosphate-containing preparation, a cyclic derivative or an extended sequence. Those names can appear in related database records but are not interchangeable specifications.',
    'The DS5 and DS10 pack choices do not encode salt form. Include the required chemical form and documentation in the inquiry so the quoted material can be matched to the intended reference.',
    images=['dsip'], related=[('epithalon','Epithalon'),('semax','Semax')])
add('ss-31', 'SS-31 / Elamipretide: tetrapeptide identity',
    'SS-31 is associated with the Elamipretide reference in PubChem CID 11764719. The depicted peptide contains four residues, including a dimethyl-substituted tyrosine unit and a terminal amide.',
    'Stereochemistry and counterions',
    'The stereochemical assignments are part of the reference. Hydrochloride, acetate and other counterion-containing records may carry different formulas from the parent compound; compare the exact named form rather than a rounded molecular weight alone.',
    '2S10 and 2S50 are the catalog pack codes. Ask whether reported content is expressed as peptide or as the complete supplied salt, and use the batch specification to interpret the result.',
    images=['ss-31'], related=[('mots-c','MOTS-c'),('nad-plus','NAD+')])
add('tesamorelin', 'Tesamorelin: modified GHRH analogue',
    'Tesamorelin is a synthetic analogue of growth hormone-releasing hormone. The reference molecule includes a long peptide chain and an N-terminal modification; it should not be replaced with a diagram of an unmodified GHRH fragment.',
    'Distinguish related GHRH materials',
    'Tesamorelin, Sermorelin and CJC-1295 are separate chemical identities. Shared research terminology does not make their sequences or modifications interchangeable. Use the complete reference structure and supplied material form in a comparison.',
    'TSM5, TSM10 and TSM20 identify the standalone packs. The Tesamorelin + Ipamorelin listing is a different, two-component entry with separately stated amounts.',
    images=['tesamorelin'], related=[('sermorelin','Sermorelin'),('tesamorelin-ipamorelin','Tesamorelin + Ipamorelin')])
add('sermorelin', 'Sermorelin: GHRH fragment reference',
    'Sermorelin corresponds to the amidated 1–29 fragment of growth hormone-releasing hormone. PubChem CID 16132413 provides the reference depicted below.',
    'Fragment length and terminal amide',
    'The 29-residue sequence and terminal amide distinguish this reference from full-length GHRH and differently modified analogues. An acetate preparation also requires an explicit counterion description alongside the peptide identity.',
    'SMO5 and SMO10 are the catalog options for Sermorelin. They are different from the SM codes used for Semaglutide, so include both the complete product name and code in a procurement request.',
    images=['sermorelin'], related=[('tesamorelin','Tesamorelin'),('cjc-1295-without-dac','CJC-1295 without DAC')])
add('thymosin-alpha-1', 'Thymosin alpha 1 / Thymalfasin reference',
    'Thymalfasin is the synthetic 28-amino-acid peptide reference associated with thymosin alpha 1. The N-terminal acetyl group is included in the PubChem structure shown here.',
    'Alpha and beta thymosins are distinct',
    'Thymosin alpha 1 should not be identified using a thymosin beta-4 or TB-500 structure. The shared thymosin terminology does not imply the same peptide sequence, chain length or molecular formula.',
    'TA5 and TA10 specify pack options, not biological activity. Confirm the full peptide identity and any counterion designation with the proposed batch documents.',
    images=['thymosin-alpha-1'], related=[('tb-500','TB-500'),('epithalon','Epithalon')])
add('kisspeptin-10', 'Kisspeptin-10: human sequence reference',
    'The reference depicted is the amidated ten-residue peptide Tyr–Asn–Trp–Asn–Ser–Phe–Gly–Leu–Arg–Phe–NH2, recorded in PubChem CID 25240297.',
    'Check the species and fragment',
    'Kisspeptin records include different species sequences and longer fragments. Specify the ten-residue reference and its terminal amide; the Kisspeptin name alone is not enough to select a sequence. The diagram is a human-sequence reference, not proof of the supplied material.',
    'For KS5 or KS10, ask the supply team to confirm sequence identity and material form before matching a batch report to this reference.',
    images=['kisspeptin-10'], related=[('ipamorelin','Ipamorelin'),('sermorelin','Sermorelin')])
add('glutathione', 'Glutathione: reduced tripeptide reference',
    'The reference shown is reduced glutathione, composed of glutamate, cysteine and glycine. Its glutamyl linkage and free sulfur-containing group are visible features of the depicted molecule.',
    'Reduced GSH versus oxidized GSSG',
    'Reduced glutathione and its oxidized disulfide form are different chemical species. Their formulas and molecular weights differ, so a report identifying only glutathione should be read together with the stated form and analytical method.',
    'GTT600 and GTT1500 identify the listed quantities. Confirm whether the assay addresses reduced glutathione, total glutathione or another defined basis, and follow the supplied handling documentation.',
    images=['glutathione'], related=[('nad-plus','NAD+'),('l-carnitine','L-carnitine')])
add('l-carnitine', 'L-carnitine: stereochemical reference',
    'L-carnitine, also called levocarnitine, is a small molecule rather than a peptide. The reference depicts its zwitterionic form, with a positively charged quaternary nitrogen and a negatively charged carboxylate.',
    'Specify L-carnitine rather than a derivative',
    'The L stereochemical designation matters. Acetyl-L-carnitine and counterion-containing forms such as tartrates are different material specifications and should not be assigned the formula of the parent L-carnitine reference.',
    'LC1200 is the L-carnitine entry. It is distinct from LC120, the Lipo-c formulation code, so include the full product name when requesting documentation or a quote.',
    images=['l-carnitine'], related=[('lipo-c','Lipo-c'),('glutathione','Glutathione')])
add('aod9604', 'AOD9604: peptide reference and disulfide form',
    'AOD9604 is represented by PubChem CID 71300630. The depicted peptide contains two sulfur atoms joined in a disulfide bond; the bond connectivity is part of the reference identity.',
    'Connectivity is more than a formula',
    'A molecular formula does not by itself describe the disulfide arrangement or prove that a supplied sample matches the depicted form. Request the sequence, terminal chemistry and identity method rather than relying on the AOD abbreviation alone.',
    '5AD and 10AD select the listed pack sizes. If an acetate or another salt is quoted, use that named material form when interpreting mass and content documentation.',
    images=['aod9604'], related=[('tesamorelin','Tesamorelin'),('sermorelin','Sermorelin')])
add('cagrilintide', 'Cagrilintide: modified peptide reference',
    'The Cagrilintide reference includes a peptide chain, a lipid-bearing modification and a disulfide linkage. These features distinguish the complete molecule from an unmodified peptide backbone or a synthetic intermediate.',
    'Confirm the complete modified structure',
    'Match the sequence, lipid attachment and disulfide connectivity in the material specification. A structure from a combination-product record should not be substituted for the single-component reference.',
    'CGL5 and CGL10 are standalone Cagrilintide listings. No Semaglutide content or combination ratio is implied by those catalog codes; any combination must be specified separately.',
    images=['cagrilintide'], related=[('semaglutide','Semaglutide'),('retatrutide','Retatrutide')])
add('vip', 'VIP / Aviptadil: peptide reference',
    'VIP stands for vasoactive intestinal peptide. The Aviptadil reference in PubChem CID 16132300 is the synthetic peptide identity used for the diagram below.',
    'Full reference versus fragments',
    'Database entries also exist for shortened VIP fragments and modified constructs. Check the complete sequence and terminal groups against the intended full peptide reference rather than matching only the VIP abbreviation.',
    'VP5 and VP10 distinguish the catalog quantities. The reference image does not establish batch content or activity; request the specification and the analytical identity assignment for the proposed supply.',
    images=['vip'], related=[('thymosin-alpha-1','Thymosin alpha 1'),('kisspeptin-10','Kisspeptin-10')])
add('5-amino-1mq', '5-amino-1MQ: charged small-molecule reference',
    '5-amino-1MQ refers here to 5-amino-1-methylquinolinium. It is a small aromatic cation rather than a peptide. PubChem CID 950107 depicts the positively charged molecular ion without a counterion.',
    'Counterion changes the complete formula',
    'An iodide or chloride salt includes an additional chemical component and has a different formula weight from the isolated cation. The reference mass below must not be used as the full salt mass without confirming the actual material form.',
    'For 5AM, 10AM or 50AM, request the counterion name and the basis used for stated content. Record whether a result is expressed as cation equivalent or complete salt.',
    images=['5-amino-1mq'], related=[('nad-plus','NAD+'),('l-carnitine','L-carnitine')])
add('melanotan-i-ii', 'Melanotan I and II: separate molecular references',
    'This catalog page groups two distinct peptides. Melanotan I is associated with the Afamelanotide reference; Melanotan II has a different, cyclic peptide structure. They do not share one molecular formula.',
    'Choose the named component',
    'The MT-1 / MT-2 listing is not evidence that both compounds are present in one vial. Specify Melanotan I or Melanotan II explicitly in the inquiry and match the batch document to that selection.',
    'The two reference panels are provided for comparison. Do not assign the formula, identity result or pack label for one peptide to the other.',
    images=['melanotan-i','melanotan-ii'], related=[('kisspeptin-10','Kisspeptin-10')])

# Forms requiring further specification: do not select a convenient but unverified image.
add('ghk-cu', 'GHK-Cu: peptide ligand and copper complex',
    'GHK denotes glycyl-L-histidyl-L-lysine. GHK-Cu describes its copper complex, which must be distinguished from the uncomplexed GHK peptide.',
    'Metal content and chemical form',
    'A copper-complex specification should describe the peptide-to-copper relationship, counterions and the basis of the reported content. A drawing of the free peptide omits the metal, while a particular database coordination model may not describe every supplied form.',
    'For CU50 and CU100, request both the peptide identity and copper-related specification. A blue appearance alone is not a quantitative identity or purity result. A single coordination diagram is not assigned here without the material-form details.',
    sources=[('https://pubmed.ncbi.nlm.nih.gov/3169264/','Maquart et al., 1988: GHK-Cu reference')], related=[('ahk-cu','AHK-Cu'),('glow','GLOW')])
add('ahk-cu', 'AHK-Cu: alanine-containing copper peptide',
    'AHK-Cu is the copper complex of L-alanyl-L-histidyl-L-lysine. Its first residue is alanine; GHK-Cu contains glycine in that position and is a different peptide complex.',
    'Keep ligand and metal specifications together',
    'The ligand sequence, copper content and stated counterion or complex form should be supplied together. Using a GHK-Cu diagram would obscure the alanine/glycine distinction, so no substitute structure is assigned to this entry.',
    'AU50 and AU100 identify AHK-Cu packs; CU50 and CU100 refer to GHK-Cu. Include the complete code and product name when requesting a batch report.',
    sources=[('https://pubmed.ncbi.nlm.nih.gov/17703734/','Pyo et al., 2007: AHK-Cu study')], related=[('ghk-cu','GHK-Cu')])
add('cjc-1295-with-dac', 'CJC-1295 with DAC: modification-specific identity',
    'The original CJC-1295 research describes a modified GHRH analogue bearing a maleimide-containing lysine derivative. That additional chemistry is relevant to the DAC designation and cannot be represented by an unmodified peptide sequence alone.',
    'Confirm the added group',
    'The supplied structural specification should identify the peptide sequence and the conjugation-related modification. A diagram for a no-DAC analogue would omit a defining feature of this listing.',
    'CD5 and CD10 are the with-DAC pack codes. Request the expected identity assignment for that modified form; do not compare its mass directly with a no-DAC specification.',
    sources=[('https://pubmed.ncbi.nlm.nih.gov/15817669/','Jetté et al., 2005: CJC-1295 molecular design')], related=[('cjc-1295-without-dac','CJC-1295 without DAC')])
add('cjc-1295-without-dac', 'CJC-1295 without DAC: sequence-specific reference',
    'This entry is explicitly labeled without DAC. Published analytical work distinguishes CJC-1295 forms, making the complete sequence and terminal modifications more informative than the abbreviated catalog name alone.',
    'Do not reuse the with-DAC drawing',
    'A maleimide-bearing DAC structure is not an appropriate illustration for this listing. The no-DAC sequence and terminal form should be confirmed before a molecular drawing or calculated mass is assigned.',
    'CND5 and CND10 refer to the standalone no-DAC product. CP10 and CP20 are combination entries with Ipamorelin and need separate component quantities and form confirmation.',
    sources=[('https://pubmed.ncbi.nlm.nih.gov/34665524/','Memdouh et al., 2021: analysis of GHRH analogues')], related=[('cjc-1295-with-dac','CJC-1295 with DAC'),('cjc-1295-ipamorelin','CJC-1295 + Ipamorelin')])
add('foxo4-dri', 'FOXO4-DRI: a designed peptide, not the full FOXO4 protein',
    'FOXO4-DRI refers to a designed D-retro-inverso peptide used in published cellular-senescence research. It should not be identified using a structure of the full FOXO4 protein or an ordinary L-amino-acid peptide with the same written letters.',
    'Direction and stereochemistry',
    'For a retro-inverso material, residue order and D/L configuration are essential identity information. Request the complete sequence, terminal modifications and expected mass before comparing analytical records.',
    'F410 is a catalog quantity code, not a sequence identifier. A molecular diagram remains unassigned until the proposed material can be matched to a defined structural reference.',
    sources=[('https://pubmed.ncbi.nlm.nih.gov/28340339/','Baar et al., 2017: FOXO4-DRI research')])
add('igf-1-lr3', 'IGF-1 LR3: extended protein analogue',
    'Long R3 IGF-I differs from native IGF-I by an Arg substitution at position 3 and a 13-amino-acid N-terminal extension. These changes distinguish the LR3 reference from ordinary IGF-I.',
    'Sequence and folded state',
    'A native IGF-I drawing is not a complete representation of LR3. For this protein analogue, sequence identity and disulfide/folding-related characterization are separate questions from a simple formula or an overall purity percentage.',
    'The IG1 listing specifies 1 mg per vial in the catalog pack. Request the exact LR3 sequence and available identity documentation; biological activity should only be reported when supported by the relevant assay.',
    sources=[('https://pubmed.ncbi.nlm.nih.gov/10608814/','Yang et al., 1999: LR3 IGF-I folding study')])
add('snap-8', 'Snap-8: match the peptide to the specification',
    'This catalog lists Snap8 / Snap-8 under NP810. Before assigning a molecular structure, match the supplied peptide to its explicit chemical name, sequence and terminal groups rather than relying on the short label alone.',
    'Peptide versus formulated solution',
    'A commercially named peptide solution can include a carrier and other ingredients. Its concentration and complete composition are different information from the mass of an isolated peptide. The reference supplier page below describes a solution product and does not verify the identity or origin of the NP810 material.',
    'Request the peptide specification, material form and available analytical identity data. A molecular formula or structure will be appropriate only after those details identify a specific compound.',
    sources=[('https://www.lubrizol.com/solutions/products/beauty/detail-pages/snap-8-peptide-solution-c','Lubrizol: SNAP-8 peptide solution C, formulation reference')])
add('adamax', 'Adamax: define the supplied molecule',
    'AX5 and AX10 are the Adamax catalog entries at 5 mg and 10 mg per vial. The existing listing does not state an amino-acid sequence, terminal modifications or a database identifier.',
    'Avoid identity assumptions from the name',
    'A Semax diagram or another related peptide image would imply a specific chemical identity that is not established by this catalog entry. The quotation should provide the complete chemical or sequence specification for the proposed material.',
    'Ask for the sequence, D/L assignments where applicable, terminal groups, counterion and identity method. Those details allow a buyer to decide whether two products labeled Adamax are actually comparable.',
    related=[('semax','Semax reference')])
add('bacteriostatic-water', 'Bacteriostatic water: formulation information',
    'The BAC3 and BAC10 entries are liquid pack formats of 3 ml and 10 ml per vial. They are formulation listings, not peptide identities, so a peptide molecular diagram would be inappropriate.',
    'Composition and quality are separate details',
    'Confirm the water specification and any preservative identity and concentration in the actual formulation. The catalog name alone does not document the composition or establish a sterility or endotoxin test result.',
    'Request the relevant batch documentation and labeled storage conditions. Volume is a pack measurement; it is not evidence of compatibility with a particular research material or a substitute for formulation-specific information.')

# Mixtures: retain the component quantities already stated by the catalog.
add('bpc-157-tb-500', 'BPC-157 + TB-500: component amounts',
    'The catalog specifies equal labeled amounts of BPC and TB: BB10 lists 5 mg + 5 mg, BB20 lists 10 mg + 10 mg, BB30 lists 15 mg + 15 mg, and BB40 lists 20 mg + 20 mg per vial.',
    'Two peptides, two identity checks',
    'This combination does not have one molecular formula. BPC-157 has its own reference, while the TB component needs an explicit sequence and terminal specification before a structure is assigned.',
    'Request analytical coverage for both components and confirmation of the labeled quantities. A combined purity figure does not by itself quantify each peptide.',
    related=[('bpc-157','BPC-157 structure'),('tb-500','TB-500 identity notes')])
add('semax-selank', 'Semax + Selank: 10 mg + 10 mg catalog composition',
    'XSL20 is listed as Semax 10 mg plus Selank 10 mg per vial, for a combined labeled amount of 20 mg. These are two distinct peptide sequences, not a single hybrid molecule.',
    'Read each reference separately',
    'The Semax and Selank reference pages show their individual structures. The two names should remain separate on the specification and analytical documentation; a blend has no single component molecular weight.',
    'Confirm both component identities and the quantity of each in the proposed batch. The stated catalog composition is a specification, not a measured result for every lot.',
    related=[('semax','Semax structure'),('selank','Selank structure')])
add('tesamorelin-ipamorelin', 'Tesamorelin + Ipamorelin: 10 mg + 5 mg composition',
    'The TI catalog entry lists Tesamorelin 10 mg plus Ipamorelin 5 mg per vial. This is a 2:1 labeled mass ratio and a combined amount of 15 mg; it is not a statement of molar ratio.',
    'A blend is not a conjugate',
    'Each peptide retains its own molecular identity. A single connected structure would incorrectly suggest that the two molecules are covalently joined.',
    'Request component-specific identification and content information where available. Match the Tesamorelin and Ipamorelin forms to the separate references linked below.',
    related=[('tesamorelin','Tesamorelin structure'),('ipamorelin','Ipamorelin structure')])
add('retatrutide-tirzepatide', 'Retatrutide + Tirzepatide: confirm the split',
    'RET60 lists the two product names with a combined catalog specification of 60 mg per vial. The current listing does not give the amount of each component.',
    'Do not infer a 30 mg + 30 mg ratio',
    'A total mass does not establish an equal split. The quotation must state the Retatrutide quantity, Tirzepatide quantity and the chemical form of each component before the blend can be compared with another specification.',
    'These are separate modified peptides and require separate molecular references. Confirm how the analytical method distinguishes and measures them in the mixture.',
    related=[('retatrutide','Retatrutide reference'),('tirzepatide','Tirzepatide structure')])
add('glow', 'GLOW70: composition-led product review',
    'GLOW70 is listed at 70 mg per vial. The catalog entry does not identify individual ingredients or their quantities, so the name cannot be mapped reliably to a single molecular structure.',
    'Confirm the exact formulation',
    'Do not assume that another supplier\'s GLOW recipe describes this item. Request a component list with the amount of each ingredient, its chemical form and the basis of the 70 mg label.',
    'Only after the formulation is confirmed can the relevant component structures and analytical documents be assigned. Keep the formulation version with repeat-order records.',
    related=[('klow','KLOW specification review')])
add('klow', 'KLOW80: ingredient and quantity confirmation',
    'KLOW80 is listed at 80 mg per vial. The current product table provides a total quantity but no ingredient-by-ingredient composition.',
    'Keep KLOW distinct from GLOW',
    'The different catalog names and total amounts do not establish which ingredients differ. An assumed extra peptide or an online blend recipe should not replace a confirmed formulation specification.',
    'Request the named components, individual quantities and material forms. If the composition changes between orders, review it as a formulation change rather than treating the same short label as proof of equivalence.',
    related=[('glow','GLOW specification review')])
add('lipo-c', 'Lipo-c: liquid formulation specification',
    'LC120 is the catalog code for Lipo-c in 10 ml vials. The code does not state a 120 mg concentration or identify the ingredients in the liquid.',
    'Volume does not determine ingredient content',
    'To compare liquid formulations, request the complete ingredient list and each concentration, with clear units such as mg/ml where applicable. A total vial volume cannot be converted into ingredient mass without those values.',
    'Confirm carriers, any preservatives and formulation-specific documentation. Lipo-c should not be assigned the molecular formula or diagram of L-carnitine merely because their codes share the letters LC.',
    related=[('l-carnitine','L-carnitine reference')])
add('lemon-bottle', 'Lemon Bottle: identify the formulation',
    'The LB entry lists 10 ml per vial. This catalog name and volume do not establish a single chemical identity, complete ingredient list or ingredient concentrations.',
    'Request the label and composition',
    'Confirm the proposed product label, formulation ingredients, concentrations and manufacturer information. A formula taken from a similarly named online product should not be attributed to this listing without a matching specification.',
    'No single-molecule structure is assigned to this formulation entry. For comparison, use the confirmed ingredient identities and the available documentation for the proposed batch rather than an illustrative chemical diagram.',
    related=[('lipo-c','Lipo-c formulation review')])

def esc(s): return html.escape(str(s), quote=True)
def image_panel(key):
    r = SOURCES[key]
    assert 'error' not in r, (key,r)
    name = {'melanotan-i':'Melanotan I / Afamelanotide','melanotan-ii':'Melanotan II'}.get(key, r['Title'])
    formula = re.sub(r'(\d+)', r'<sub>\1</sub>', esc(r['MolecularFormula']))
    if formula.endswith('+'): formula=formula[:-1]+'<sup>+</sup>'
    extra = '<p class="reference-note">This CID is currently titled Triple G in PubChem. The linked IUPHAR/BPS substance record associates it with retatrutide. Use the complete sequence and modifications when comparing supplied material.</p>' if key=='retatrutide' else ''
    return f'''<figure class="structure-figure"><a href="/assets/structures/{key}.png" target="_blank" rel="noopener" aria-label="Open {esc(name)} reference structure at full size"><img src="/assets/structures/{key}.png" alt="2D reference structure: {esc(name)}, PubChem CID {r['CID']}" width="1200" height="900" loading="lazy" decoding="async"></a><figcaption>{esc(name)} · PubChem CID {r['CID']} · <a href="/assets/structures/{key}.png" target="_blank" rel="noopener">Open full-size structure ↗</a></figcaption></figure><dl class="molecular-facts"><div><dt>Reference formula</dt><dd>{formula}</dd></div><div><dt>Reference molecular weight</dt><dd>{esc(r['MolecularWeight'])} g/mol</dd></div><div><dt>Reference record</dt><dd><a href="{r['source']}" target="_blank" rel="noopener noreferrer">PubChem CID {r['CID']} ↗</a></dd></div></dl>{extra}'''

def build(slug,d):
    figures=''.join(image_panel(key) for key in d['images'])
    note='<p class="reference-note">Images and numerical properties describe the cited database forms, not batch test results. Confirm the actual supplied form against the specification. Molecular weights retain the precision reported by PubChem.</p>' if figures else ''
    sources=''.join(f'<li><a href="{esc(u)}" target="_blank" rel="noopener noreferrer">{esc(t)} ↗</a></li>' for u,t in d['sources'])
    sources=f'<div class="reference-source"><p>Reference sources</p><ul>{sources}</ul></div>' if sources else ''
    links=' · '.join(f'<a href="/products/{s}/">{esc(label)}</a>' for s,label in d['related'])
    links=f'<p class="reference-source">Related product details: {links}</p>' if links else ''
    return f'''\n<!-- molecular-reference:start -->
<section class="molecular-reference" aria-labelledby="molecular-heading"><p class="eyebrow">PRODUCT IDENTITY &amp; REFERENCE</p><h2 id="molecular-heading">{esc(d['title'])}</h2><p>{esc(d['intro'])}</p>{figures}<h3>{esc(d['heading'])}</h3><p>{esc(d['detail'])}</p><h3>What to confirm for this catalog item</h3><p>{esc(d['check'])}</p>{note}{sources}{links}<p class="reference-source">Reference review: 28 September 2026. Pack details follow the catalog above; batch information is confirmed separately.</p></section>
<!-- molecular-reference:end -->\n'''

def main():
    existing={p.parent.name for p in (ROOT/'products').glob('*/index.html') if 'molecular-reference' in p.read_text() and '<!-- molecular-reference:start -->' not in p.read_text()}
    targets={p.parent.name for p in (ROOT/'products').glob('*/index.html')}-existing
    assert targets==set(DATA), (targets-set(DATA),set(DATA)-targets)
    for slug,d in DATA.items():
        p=ROOT/f'products/{slug}/index.html';s=p.read_text();section=build(slug,d)
        if '<!-- molecular-reference:start -->' in s:
            s=re.sub(r'\s*<!-- molecular-reference:start -->.*?<!-- molecular-reference:end -->\s*',lambda _:section,s,flags=re.S)
        elif '<section class="procurement-notes">' in s:
            s,n=re.subn(r'<section class="procurement-notes">.*?</section>',lambda _:section,s,count=1,flags=re.S);assert n==1
        else:
            s=s.replace('</main>',section+'</main>',1)
        if 'href="/molecular-reference.css"' not in s:s=s.replace('</head>','<link rel="stylesheet" href="/molecular-reference.css"></head>',1)
        assert s.count('id="molecular-heading"')==1,slug
        p.write_text(s)
    p=ROOT/'sitemap.xml';s=p.read_text()
    for slug in DATA:
        pat=r'(<loc>https://lbiopeptides.com/products/'+re.escape(slug)+r'/</loc><lastmod>)[^<]+'
        s,n=re.subn(pat,lambda m:m.group(1)+DATE,s);assert n==1,slug
    p.write_text(s)
    print(f'Updated {len(DATA)} product pages; {sum(len(d["images"]) for d in DATA.values())} reference images.')

if __name__=='__main__':main()
