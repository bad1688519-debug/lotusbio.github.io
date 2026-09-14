# SEO migration status

Source: 21 URLs fetched from GitHub main on 2026-09-14. Per-file blob SHAs are retained in source-snapshot.json and seo-migration-audit.json.

Completed: all sitemap URLs represented locally; product and guide text restored from the snapshot; titles and descriptions retained; self canonical URLs; WebPage/WebSite and breadcrumb JSON-LD; sitemap; internal page directory; preview noindex preserved. No invented offers, ratings or reviews were added.

Validation: `node check-seo.cjs` checks all 21 routes, one H1 per page, descriptions, canonical URLs, parseable JSON-LD, preview noindex, local link destinations and absence of old-site navigation links.

Rebuild sequence: run `node build.cjs`, then `migrate-seo.py` using Python, then `node check-seo.cjs`. Migration augments the base output: always regenerate base pages before migration. Snapshot HTML is data, not code to execute. Refresh the snapshot and review changes before release.

Not yet approved for launch: full quote-list functionality is not restored; the current form opens a mail client. Product media, non-sitemap legacy URLs, full mobile visual review, live hosting redirects/status codes and actual production rich-result validation still need review. Retaining text does not independently verify supplier claims.

Production export is separate and has NOT been run. `production-export.cjs --approved-release` creates local release output and changes indexing only in that output. It does not deploy. Domain and old production site are unchanged.

