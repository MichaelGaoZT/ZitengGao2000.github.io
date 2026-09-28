# Ziteng Gao · 高紫腾

Personal academic homepage, with a layout inspired by [Zhengyi Luo’s website](https://www.zhengyiluo.com/) and [al-folio](https://github.com/alshedivat/al-folio). This is a small, independently implemented static site, not an installation of the full Jekyll theme. Pages work without JavaScript; a small script enhances the mobile navigation.

## Preview locally

No npm, Ruby, or third-party Python packages are required. Use Python 3.9 or newer:

```sh
python3 scripts/build.py
python3 scripts/check_site.py
python3 -m http.server 8000 --bind 127.0.0.1
```

Open http://localhost:8000. When connecting to this server through VS Code, forward port 8000 first.

## Edit the site

- `src/pages/index.html`: English biography, news, selected research, affiliations, and experience.
- `src/pages/cn.html`: Chinese biography and contact information.
- `src/pages/hobbies.html`: badminton page.
- `src/layout.html`: shared page shell, metadata, navigation, and footer.
- `assets/css/main.css`: responsive styles.
- `assets/images/`: photographs, research image, and institution logos from the old site.
- `assets/files/ZitengGao_CV.pdf`: the original CV download.

After editing the source fragments or layout, run `python3 scripts/build.py` and commit the generated `index.html`, `cn/index.html`, and `hobbies/index.html` together with the source changes. Validate with:

```sh
python3 scripts/build.py --check
python3 scripts/check_site.py
```

## Publish with GitHub Pages

The repository is ready for GitHub Pages branch publishing; `.nojekyll` serves the generated HTML directly.

1. Open [Settings → Pages](https://github.com/MichaelGaoZT/ZitengGao2000.github.io/settings/pages).
2. Select **Deploy from a branch**, then **main** and **/ (root)**, and save.
3. Wait for the GitHub Pages deployment to finish.

The default URL is **https://michaelgaozt.github.io/ZitengGao2000.github.io/**. The repository belongs to `MichaelGaoZT`, so naming it `ZitengGao2000.github.io` does not assign it the domain `zitenggao2000.github.io`. All internal links use relative paths and support this project-site prefix. If the hosting URL changes, update `SITE_URL` in `scripts/build.py` and rebuild.

No custom domain is configured, and the old site's `CNAME` was not copied.

## Migration notes

Content was migrated from `MichaelGaoZT/michaelgaozt.github.io` at commit `05b3213`, using the authentic English homepage, Chinese page, and hobbies page. News and experience dates are preserved from that source, whose biography was last updated in March 2026. The inherited hidden pages containing another person's publications, services, awards, social accounts, and meeting links were excluded. No publication venue or acceptance status has been inferred for TouchAnything.

The original CV PDF is preserved as supplied. It predates the Ph.D. update, still lists XPENG as “Present,” and has some dates that differ from the current homepage. Replace it with an updated CV when available; the new website uses the current homepage dates.

## License and credits

Original website code is distributed under the [MIT License](LICENSE). Personal text, CV, photographs, research figures, and third-party logos are outside the code license; their rights remain with their respective owners. This scope statement does not revoke any rights already granted for material in the old repository.

The visual reference is Zhengyi Luo’s al-folio-based homepage. The implementation here uses original HTML/CSS/JavaScript and does not redistribute his biography, research, photos, or site source. Original personal material comes from Ziteng Gao’s previous homepage.
