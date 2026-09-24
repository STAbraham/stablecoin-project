import os, re, subprocess, glob, math
from PIL import Image

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tracks/c-usdc-vasp-privy/research/diagrams")
PAD = 16

HARNESS = """<!DOCTYPE html><html><head><meta charset="utf-8">
<script src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.9.1/mermaid.min.js"></script>
<style>body{{background:#fff;margin:0;padding:{pad}px;font-family:-apple-system,Helvetica,Arial}}</style>
</head><body><pre class="mermaid">{src}</pre>
<script>mermaid.initialize({{startOnLoad:true, theme:'neutral', flowchart:{{useMaxWidth:false}}, sequence:{{useMaxWidth:false}}, state:{{useMaxWidth:false}}}});</script>
</body></html>"""

for mmd in sorted(glob.glob(f"{DG}/*.mmd")):
    name = os.path.splitext(os.path.basename(mmd))[0]
    html = f"{DG}/{name}.html"
    open(html, "w").write(HARNESS.format(pad=PAD, src=open(mmd).read()))

    # pass 1: measure rendered SVG
    dom = subprocess.run([CHROME, "--headless=new", "--disable-gpu",
        "--virtual-time-budget=8000", "--window-size=2400,2400",
        "--dump-dom", f"file://{html}"], capture_output=True, text=True).stdout
    m = re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', dom)
    if not m:
        print(name, "NO VIEWBOX"); continue
    w, h = float(m.group(1)), float(m.group(2))
    ww, wh = math.ceil(w) + 2*PAD, math.ceil(h) + 2*PAD

    # pass 2: screenshot at 2x
    shot = f"{DG}/{name}.png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu",
        "--virtual-time-budget=8000", "--force-device-scale-factor=2",
        f"--window-size={ww},{wh}", f"--screenshot={shot}",
        f"file://{html}"], capture_output=True, text=True)

    img = Image.open(shot)
    pw, ph = img.size
    # print size: fit 6.2in wide x 8.3in tall, never larger than ~12pt text (dpi>=192 at 2x render)
    dpi = max(192, pw/6.2, ph/8.3)
    q = img.convert("RGB").quantize(colors=64)
    q.save(shot, optimize=True, dpi=(round(dpi), round(dpi)))
    print(f"{name}: {pw}x{ph}px, dpi={round(dpi)}, prints {pw/dpi:.1f}x{ph/dpi:.1f}in, {os.path.getsize(shot)//1024}KB")
