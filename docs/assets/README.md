# Assets

`social-preview.png` is the repository's social preview (Settings › General › Social preview on GitHub). Edit the HTML and render it again with Chrome:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars --window-size=1280,640 \
  --virtual-time-budget=3000 --screenshot=social-preview.png "file://$PWD/social-preview.html"
```
