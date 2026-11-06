"""Generate LinkOps Data Lab's cover art and five-slide PDF from Pillow."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
W, H = 1600, 900
BG = (10, 17, 24)
PANEL = (18, 30, 41)
PANEL2 = (14, 24, 33)
LINE = (43, 62, 74)
WHITE = (239, 246, 246)
MUTED = (157, 176, 184)
TEAL = (114, 224, 193)
BLUE = (143, 184, 245)
AMBER = (244, 199, 119)
FONT_DIR = Path('/System/Library/Fonts/Supplemental')


def font(size, bold=False, mono=False):
    names = ['Menlo.ttc'] if mono else (['Arial Bold.ttf', 'Arial.ttf'] if bold else ['Arial.ttf'])
    for name in names:
        try:
            return ImageFont.truetype(str(FONT_DIR / name), size)
        except OSError:
            pass
    return ImageFont.load_default()


def canvas():
    im = Image.new('RGB', (W, H), BG)
    pix = im.load()
    for y in range(H):
        t = y / H
        color = (int(12 + 7 * (1-t)), int(20 + 13 * (1-t)), int(28 + 18 * (1-t)))
        for x in range(W):
            glow = max(0, 1 - (((x - 1320) / 700) ** 2 + ((y - 40) / 500) ** 2)) * .14
            pix[x, y] = tuple(min(255, int(c + g * glow * 255)) for c, g in zip(color, (0.1, 0.45, 0.58)))
    return im


def rounded(draw, xy, radius=18, fill=PANEL, outline=LINE, width=2):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def label(draw, xy, text, color=TEAL, size=20):
    draw.text(xy, text.upper(), font=font(size, True, True), fill=color)


def brand_mark(draw, x, y, size):
    draw.rounded_rectangle((x, y, x+size, y+size), radius=max(8, size//4), fill=TEAL)
    draw.line((x+size*.24, y+size*.69, x+size*.69, y+size*.24), fill=(7, 26, 28), width=max(3, size//12))
    draw.line((x+size*.45, y+size*.24, x+size*.69, y+size*.24, x+size*.69, y+size*.48), fill=(7, 26, 28), width=max(3, size//12))


def paragraph(draw, xy, text, width, size=24, color=MUTED, gap=9, bold=False):
    f = font(size, bold)
    x, y = xy
    words = text.split()
    lines, line = [], ''
    for word in words:
        test = (line + ' ' + word).strip()
        if draw.textbbox((0, 0), test, font=f)[2] <= width or not line:
            line = test
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    for line in lines:
        draw.text((x, y), line, font=f, fill=color)
        y += size + gap
    return y


def base(kicker, title, subtitle):
    im = canvas()
    d = ImageDraw.Draw(im)
    brand_mark(d, 62, 48, 40)
    d.text((119, 51), 'LinkOps Data Lab', font=font(24, True), fill=WHITE)
    d.text((W-64, 57), 'VULTR AGENT RUSH  ·  BLAST RADIUS ZERO', font=font(15, True, True), fill=(130, 155, 164), anchor='ra')
    d.line((62, 110, W-62, 110), fill=LINE, width=2)
    label(d, (70, 143), kicker)
    d.text((70, 185), title, font=font(49, True), fill=WHITE)
    paragraph(d, (72, 252), subtitle, 1420, 23, MUTED, 6)
    return im, d


def slide_cover():
    im = canvas()
    d = ImageDraw.Draw(im)
    brand_mark(d, 82, 74, 42)
    label(d, (84, 169), 'VULTR AGENT RUSH  ·  BLAST RADIUS ZERO', TEAL, 18)
    d.text((78, 225), 'LinkOps', font=font(102, True), fill=WHITE)
    d.text((82, 338), 'Data Lab', font=font(74, True), fill=(154, 187, 195))
    paragraph(d, (86, 452), 'Ask a question about a CSV. Inspect the plan and Python. Get an answer produced inside a fresh, network-isolated sandbox.', 680, 30, MUTED, 11)
    rounded(d, (86, 672, 654, 753), 18, fill=(16, 34, 34), outline=(53, 95, 83))
    d.text((112, 693), 'MODEL-PLANNED  ·  CODE-EXECUTED  ·  RESULT-VERIFIED', font=font(17, True, True), fill=TEAL)
    # Product pipeline card.
    rounded(d, (840, 194, 1500, 744), 28, fill=(15, 26, 36), outline=(46, 70, 83), width=2)
    label(d, (886, 228), 'ONE TASK  ·  FOUR AUDITABLE STEPS', BLUE, 16)
    items = [
        ('01', 'PLAN', 'Vultr Serverless Inference', TEAL),
        ('02', 'WRITE', 'Generated Python shown', BLUE),
        ('03', 'EXECUTE', 'Disposable Docker sandbox', AMBER),
        ('04', 'VERIFY', 'Real output + chart', TEAL),
    ]
    y = 294
    for no, title, desc, col in items:
        rounded(d, (880, y, 1460, y+88), 15, fill=PANEL, outline=LINE)
        d.ellipse((903, y+25, 943, y+65), fill=(21, 42, 46), outline=col, width=2)
        d.text((913, y+35), no, font=font(14, True, True), fill=col)
        d.text((964, y+16), title, font=font(15, True, True), fill=col)
        d.text((964, y+43), desc, font=font(21, True), fill=WHITE)
        y += 105
    d.text((86, 830), 'Hackathon prototype  ·  synthetic sample data  ·  no personal data', font=font(16), fill=(117, 140, 149))
    return im


def slide_workflow():
    im, d = base('01  /  PRODUCT FLOW', 'From question to executed result', 'A small, visible agent loop makes the work verifiable instead of asking a judge to trust a chat transcript.')
    cards = [
        ('01', 'Ask', '“Which product generated the most revenue? Show a chart.”', TEAL),
        ('02', 'Plan + write', 'Inference sees the question, column names, and up to five preview rows.', BLUE),
        ('03', 'Execute', 'Generated Python reads the full CSV inside a disposable container.', AMBER),
        ('04', 'Explain', 'The UI shows actual stdout, code, a chart, and the model’s summary.', TEAL),
    ]
    x0, y0, gap, cw = 72, 377, 22, 350
    for i, (n, title, desc, col) in enumerate(cards):
        x = x0 + i * (cw + gap)
        rounded(d, (x, y0, x+cw, y0+287), 20)
        d.text((x+24, y0+23), n, font=font(17, True, True), fill=col)
        d.text((x+24, y0+67), title, font=font(30, True), fill=WHITE)
        paragraph(d, (x+24, y0+125), desc, cw-48, 21, MUTED, 8)
        if i < len(cards)-1:
            d.line((x+cw+4, y0+144, x+cw+gap-5, y0+144), fill=col, width=3)
            d.polygon([(x+cw+gap-5,y0+144),(x+cw+gap-17,y0+137),(x+cw+gap-17,y0+151)],fill=col)
    rounded(d, (72, 711, 1528, 798), 16, fill=(16, 32, 34), outline=(49, 84, 75))
    d.text((100, 735), 'DATA HANDLING', font=font(15, True, True), fill=TEAL)
    d.text((302, 729), 'Sample preview to model  ·  Full file only to the sandbox  ·  No file or prompt in app logs', font=font(20), fill=WHITE)
    return im


def slide_containment():
    im, d = base('02  /  CONTAINMENT', 'The execution boundary is the product', 'Generated code is treated as untrusted. It does not run in the web server or receive the inference key.')
    # left path
    rounded(d, (76, 367, 608, 739), 22)
    label(d, (108, 395), 'VULTR VM  ·  CONTROL PLANE', TEAL, 16)
    d.text((109, 446), 'LinkOps orchestrator', font=font(29, True), fill=WHITE)
    paragraph(d, (110, 498), 'Calls Vultr Inference, creates a one-run container, collects output, explains results, removes the workspace.', 435, 21, MUTED, 7)
    rounded(d, (109, 649, 548, 708), 12, fill=(17, 39, 37), outline=(52, 94, 82))
    d.text((129, 668), 'API KEY STAYS HERE', font=font(18, True, True), fill=TEAL)
    # arrow
    d.line((629, 548, 736, 548), fill=BLUE, width=4)
    d.polygon([(736,548),(718,537),(718,559)],fill=BLUE)
    # sandbox
    rounded(d, (764, 367, 1525, 739), 22, fill=(16, 27, 37), outline=(93, 78, 51), width=2)
    label(d, (801, 395), 'FRESH SANDBOX  ·  DESTROYED AFTER EACH RUN', AMBER, 15)
    controls = [('Network', 'none'), ('Root filesystem', 'read-only'), ('Memory', '512 MB'), ('CPU', '0.5 core'), ('Process cap', '48'), ('Deadline', '15 sec'), ('UID', '65534'), ('Secrets', 'none')]
    for i, (a,b) in enumerate(controls):
        col, row = i % 2, i // 2
        x, y = 802 + col*340, 456 + row*62
        rounded(d, (x,y,x+310,y+46), 9, fill=PANEL2, outline=LINE, width=1)
        d.text((x+13,y+11), a, font=font(14), fill=MUTED)
        d.text((x+295,y+10), b, font=font(15, True, True), fill=TEAL if b in ('none','read-only') else WHITE, anchor='ra')
    return im


def slide_demo():
    im, d = base('03  /  VISIBLE PROOF', 'A judge can inspect every claim', 'The sample dataset is fictional. The figures below are expected sample output; the demo should be judged against the actual run shown in the app.')
    rounded(d, (75, 368, 770, 767), 22)
    label(d, (110, 394), 'EXPECTED OUTPUT  ·  SAMPLE CSV', TEAL, 15)
    d.text((111, 448), 'Studio Mic · $10,500', font=font(35, True), fill=WHITE)
    d.text((111, 500), 'Largest revenue in the included sample', font=font(19), fill=MUTED)
    # bar chart
    bars = [('Orbit Mouse', 4690, BLUE), ('Keypad Mini', 5810, AMBER), ('Studio Mic', 10500, TEAL)]
    for i, (name, value, col) in enumerate(bars):
        y = 570 + i*55
        d.text((112, y), name, font=font(16), fill=MUTED)
        barw = int(260 * value / 10500)
        d.rounded_rectangle((303,y+1,303+barw,y+27), radius=8, fill=col)
        d.text((671,y), f'${value:,}', font=font(16, True, True), fill=WHITE, anchor='ra')
    d.text((111, 730), 'Expected totals for the built-in fictional sample.', font=font(13), fill=(122, 143, 151))
    rounded(d, (808, 368, 1525, 767), 22)
    label(d, (844, 394), 'LOCAL CONTAINMENT PROBE  ·  VERIFY DEPLOYMENT', AMBER, 13)
    checks = [
        ('Outbound network', 'BLOCKED', 'network_mode=none'),
        ('Write outside workspace', 'DENIED', 'read-only root filesystem'),
        ('Inference key in sandbox', 'NOT PRESENT', 'separate container environment'),
        ('Temporary task volume', 'REMOVED', 'cleanup after execution'),
    ]
    y=459
    for title, result, evidence in checks:
        d.ellipse((850,y+4,872,y+26), fill=(39,78,64), outline=TEAL, width=1)
        d.text((856,y+5),'✓',font=font(14,True),fill=TEAL)
        d.text((890,y),title,font=font(17,True),fill=WHITE)
        d.text((1469,y),result,font=font(13,True,True),fill=TEAL,anchor='ra')
        d.text((890,y+27),evidence,font=font(13),fill=MUTED)
        y+=70
    return im


def slide_limits():
    im, d = base('04  /  IMPLEMENTATION', 'Built for a focused public demo', 'Before final hand-in, confirm the deployed app, real Vultr inference, and the containment probe against the live VM.')
    cards = [
        ('Vultr Cloud Compute', 'Single-purpose VM hosts the web app, API, Docker control plane, and public HTTPS endpoint.', TEAL),
        ('Vultr Serverless Inference', 'Creates a task plan and Python script, then summarizes only the sandbox output.', BLUE),
        ('Disposable containers', 'One fresh Docker container and volume per task; no network route or model secret.', AMBER),
    ]
    for i,(title,desc,col) in enumerate(cards):
        x=75+i*493
        rounded(d,(x,369,x+455,565),20)
        d.text((x+25,399),title,font=font(25,True),fill=col)
        paragraph(d,(x+25,447),desc,405,18,MUTED,7)
    rounded(d,(76,613,1525,770),18,fill=(16,28,36),outline=LINE)
    label(d,(106,637),'DEMO LIMITS',AMBER,15)
    paragraph(d,(108,676),'Hackathon prototype, not a hardened multi-tenant service. No confidential or personal CSVs. The app does not retain uploads or prompts; up to five sample rows are sent to Vultr Inference after consent.',1370,19,MUTED,7)
    return im


def main():
    cover = slide_cover()
    cover.save(ROOT / 'assets' / 'linkops-cover.png', optimize=True)
    slides = [slide_cover(), slide_workflow(), slide_containment(), slide_demo(), slide_limits()]
    pdf = ROOT / 'output' / 'pdf' / 'LinkOps_Presentation.pdf'
    pdf.parent.mkdir(parents=True, exist_ok=True)
    slides[0].save(pdf, 'PDF', resolution=144, save_all=True, append_images=slides[1:])
    print(f'Wrote cover ({W}x{H}) and {len(slides)} slides to {pdf.name}')


if __name__ == '__main__':
    main()
