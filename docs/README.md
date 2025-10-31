# Documentation Site

This directory contains the GitHub Pages site for the marketplace.

The site is automatically generated from plugin metadata by running:

```bash
make update
```

This will:
1. Generate plugin documentation
2. Build the website data (data.json)
3. Update the site with your branding from `.template-config.json`

## Deployment

The site is automatically deployed to GitHub Pages when you push to the main branch (configured in `.github/workflows/deploy-docs.yml`).
