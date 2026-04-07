# GitHub Pages Deployment

This repository is configured to deploy to GitHub Pages from GitHub Actions.

## Target domain

- Production URL: `https://mm.teddylazebnik.com/`
- GitHub repository: `https://github.com/teddy4445/Markovs-naze`

## Repo-side setup already included

- Vite builds with `base: "/"` in `vite.config.js`
- GitHub Actions workflow: `.github/workflows/deploy-pages.yml`
- Domain hint file: `public/CNAME`

## One-time GitHub setup

1. Push the latest `main` branch to GitHub.
2. Open the repository on GitHub.
3. Go to `Settings` -> `Pages`.
4. Under `Build and deployment`, set `Source` to `GitHub Actions`.
5. In the custom domain field, enter `mm.teddylazebnik.com`.
6. Save, then enable `Enforce HTTPS` after DNS finishes propagating and the certificate is issued.

## DNS setup

Create a DNS `CNAME` record for the subdomain:

- Host / Name: `mm`
- Target / Value: `teddy4445.github.io`

Do not point the subdomain at the repository path. GitHub Pages resolves the repository deployment after the request reaches `teddy4445.github.io`.

## Deploy flow

1. Commit and push to `main`.
2. GitHub Actions runs `.github/workflows/deploy-pages.yml`.
3. The workflow builds the Vite app and uploads `dist/`.
4. GitHub Pages deploys the artifact.

## Local verification

```powershell
cd C:\Users\lazeb\Desktop\Markovs-naze
npm install
npm run build
npm run preview
```

## Notes

- The `public/CNAME` file keeps the intended production domain in the repo, but GitHub Pages custom-domain binding should still be set in repository settings.
- Because the site is deployed on a dedicated subdomain, `base: "/"` is the correct Vite setting.
