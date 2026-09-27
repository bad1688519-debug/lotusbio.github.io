# Fixed-master product images

43 product images use the existing 512×512 Semaglutide product photo as the only master. The original file stays unchanged at `assets/semaglutide-lotusbio-research-product.webp`.

Only box name, vial name and vial specification regions change. The master box, bottle, background, leaves, logos and shadows are reused. New files are lossless WebP. Decoded RGB comparison reports zero changed pixels outside the three text regions, for all 43 files. Long names use two lines inside the original name area. Existing small print is retained from the packaging illustration.

`manifest.json` records every product, its page-listed specifications, the representative image specification, source, output, and pixel comparison. 10 mg is selected where listed; otherwise the first listed specification is used. The page selectors retain all 97 specifications.

`build.py` requires Python, Pillow, NumPy and SciPy plus Nimbus Sans fonts. It reconstructs only text-area backgrounds and draws text programmatically. It does not use image generation. `apply.py` updates catalog, main product images and Open Graph images and checks that option text and canonical URLs are preserved.

The catalogue and all 43 detail pages reference `/assets/unified/`. Original assets are retained for rollback. Git history preserves the preceding page versions.
