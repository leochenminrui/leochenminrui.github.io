# Minrui Chen · 陳 民瑞

Japanese and English academic homepage: **https://leochenminrui.github.io/**.

This site brings together current research interests, an updated biography, publications, and talks. It uses the owner's supplied avatar, a Japanese-era chronology, responsive layouts, and light/dark themes.

## Edit and preview

Only Python 3 is required; there are no third-party build dependencies.

```sh
python3 scripts/build.py
python3 -m http.server 8000 --directory site
```

Open <http://localhost:8000/ja/> or <http://localhost:8000/en/>.

- `data/biography.json`: bilingual chronology, degree dates and certificate numbers.
- `data/publications.json`: papers and publication metadata.
- `data/presentations.json`: conference and workshop presentations.
- `data/research.json`: current research directions in Japanese and English.
- `data/talks.json`: invited talks and seminars.
- `data/SOURCES.md`: verification notes and source links.
- `scripts/build.py`: page templates and bilingual profile text.
- `site/assets/`: styles, accessible interactions and the owner-supplied avatar.

Rebuild after changing data or templates and commit the generated pages with the source. The website can also be served directly from `site/`.

## Publishing

GitHub Pages is configured to deploy from GitHub Actions. A push to `main` builds and publishes `site/` using `.github/workflows/pages.yml`.

Academic content is based on the owner's previous Google Site and Google Scholar profile, with final bibliographic details checked against publisher records. Degree dates and certificate numbers were checked against owner-provided diplomas; the original documents are not included in this repository.

The design continues the restrained academic style used in the MankeiChan homepage, originally inspired by [Kairi Furui's website](https://www.yumizsui.com/en/). All website code is an original implementation.
