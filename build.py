"""Build both portfolio formats from content/. Python 3.10+; no website runtime."""
from pathlib import Path
import json, re, shutil, html, sys
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dist-public'
H = html.escape

def load_projects(profile):
    projects = []
    for slug in profile['projects']:
        path = ROOT / 'content/projects' / (slug + '.md')
        raw = path.read_text(encoding='utf-8')
        parts = raw.split('---', 2)
        if len(parts) != 3 or parts[0].strip():
            raise ValueError(f'{path}: expected JSON front matter between --- lines')
        p = json.loads(parts[1])
        for key in ('slug','title','subtitle','category','summary','role','metrics','tags','images','source','review_status'):
            if not p.get(key): raise ValueError(f'{path}: missing {key}')
        if p['slug'] != slug or not re.fullmatch(r'[a-z0-9-]+',slug):
            raise ValueError(f'{path}: invalid or mismatched slug')
        p['sections'] = []
        for section in re.split(r'^## ', parts[2], flags=re.M)[1:]:
            title, body = section.split('\n',1)
            p['sections'].append((title.strip(), body.strip()))
        if not p['sections']: raise ValueError(f'{path}: no narrative sections')
        if p.get('template') == 'combat-robot':
            for field in ('type','weight','record','competitions','energy'):
                if not p.get('robot',{}).get(field):
                    raise ValueError(f'{path}: missing robot.{field}')
        for img in p['images']:
            asset = ROOT / 'media' / img['file']
            if not asset.is_file(): raise ValueError(f'Missing image: {asset}')
            if not img.get('caption'): raise ValueError('Each image needs a caption')
        for img in p.get('gallery',[]):
            if not img.get('caption') or not (ROOT/'media'/img['file']).is_file(): raise ValueError(f'Invalid gallery image: {img}')
        for title,img in p.get('section_images',{}).items():
            if title not in [t for t,_ in p['sections']]: raise ValueError(f'Unknown section image heading: {title}')
            if not (ROOT/'media'/img['file']).is_file(): raise ValueError(f'Missing section image: {img["file"]}')
            for extra in img.get('additional',[]):
                if not (ROOT/'media'/extra['file']).is_file(): raise ValueError(f'Missing section image: {extra["file"]}')
        if p.get('template') == 'combat-robot' and 'wins' in p['robot']:
            r=p['robot']; total=r['wins']+r['losses']
            if total <= 0: raise ValueError('Robot match total must be positive')
            r['record']=f"{r['wins']}-{r['losses']}"
            r['winrate']=f"{100*r['wins']/total:.1f}% winrate"
        projects.append(p)
    return projects

def render_image(img, priority=False):
    from PIL import Image, ImageOps
    with Image.open(ROOT/'media'/img['file']) as source:
        width, height = ImageOps.exif_transpose(source).size
    loading = 'fetchpriority="high"' if priority else 'loading="lazy"'
    return f'<img src="media/{H(img["file"])}" alt="{H(img["caption"])}" width="{width}" height="{height}" {loading}>'

def image_tag(p, i=0, priority=False):
    return render_image(p['images'][i], priority)

def rich_text(text):
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', H(text), flags=re.S)

def project_sections(p):
    rows=[]
    for title,body in p['sections']:
        media=p.get('section_images',{}).get(title)
        if media:
            classes = (['text-height-image'] if media.get('match_text_height') else []) + ([media['layout_class']] if media.get('layout_class') else [])
            image_class = f' class="{H(" ".join(classes))}"' if classes else ''
            images=[media]+media.get('additional',[])
            pictures=''.join((f'<div class="section-image-item">{render_image(img)}<figcaption>{H(img["caption"])}</figcaption></div>' if media.get('show_captions') else render_image(img)) for img in images)
            visual=f'<figure{image_class}>{pictures}</figure>'
        elif p.get('hide_empty_section_images'):
            visual=''
        else:
            visual=f'<div class="section-image-slot" aria-label="Image pending for {H(title)}"><span>{H(title)}</span><small>Image coming soon</small></div>'
        paragraphs=''.join(f'<p>{rich_text(part)}</p>' for part in body.split('\n\n'))
        link=p.get('section_links',{}).get(title)
        if link:
            if not link['url'].startswith('https://'): raise ValueError('Section links must use https')
            paragraphs+=f'<p><a class="section-link" href="{H(link["url"])}" target="_blank" rel="noopener noreferrer">{H(link["label"])}</a></p>'
        section_class='project-section' if visual else 'project-section no-image'
        rows.append(f'<section class="{section_class}"><div><h2>{H(title)}</h2>{paragraphs}</div>{visual}</section>')
    return ''.join(rows)

def page(profile, title, body, home=False, project=None):
    links = ''.join(f'<a href="{H(link["url"])}"' + (' target="_blank" rel="noopener noreferrer"' if link['url'].startswith('https://') else '') + f'>{H(link["label"])}</a>' for link in profile['links'])
    description = project['summary'] if project else profile['intro']
    page_title = f'{title} | {profile["name"]}'
    image_url = 'https://manans.tech/media/' + project['images'][0]['file'] if project else ''
    social_image = f'<meta property="og:image" content="{H(image_url)}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{H(image_url)}">' if image_url else '<meta name="twitter:card" content="summary">'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{H(page_title)}</title><meta name="description" content="{H(description)}"><meta property="og:type" content="website"><meta property="og:title" content="{H(page_title)}"><meta property="og:description" content="{H(description)}"><meta name="twitter:title" content="{H(page_title)}"><meta name="twitter:description" content="{H(description)}">{social_image}<link rel="stylesheet" href="style.css"></head><body><a class="skip" href="#main">Skip to content</a><header><a class="wordmark" href="index.html">{H(profile["name"]).upper()}<span>ENGINEERING PORTFOLIO</span></a><nav aria-label="Main navigation"><div class="projects-nav"><a href="index.html#work">Projects</a><details><summary aria-label="Show project categories" aria-controls="projects-menu">▾</summary></details><div class="projects-menu" id="projects-menu"><a href="combat-robotics.html">Combat Robotics</a></div></div>{links}</nav></header><main id="main">{body}</main><footer><span>{H(profile["name"])} / Robotics &amp; Engineering</span></footer><script src="navigation.js" defer></script></body></html>'''

def build_web(profile, projects):
    cards=''
    robot_cards=''
    for i,p in enumerate(projects,1):
        cards+=f'''<a class="project-card" href="{p['slug']}.html"><div class="card-image">{image_tag(p)}</div><div class="card-meta"><span>{H(p['category'])}</span><span>Explore project ↗</span></div><h3>{H(p['title'])}</h3><p>{H(p['summary'])}</p></a>'''
        if p.get('template') == 'combat-robot':
            robot_cards+=f'''<a class="project-card" href="{p['slug']}.html"><div class="card-image">{image_tag(p)}</div><div class="card-meta"><span>{H(p['category'])}</span><span>Explore project ↗</span></div><h3>{H(p['title'])}</h3><p>{H(p['summary'])}</p></a>'''
        metrics=''.join(f'<div><strong>{H(a)}</strong><span>{H(b)}</span></div>' for a,b in p['metrics'])
        sections=project_sections(p)
        gallery_images=p.get('gallery',p['images'][1:])
        gallery=''.join(f'<figure>{render_image(img)}<figcaption>{H(img["caption"])}</figcaption></figure>' for img in gallery_images)
        if gallery: gallery='<section class="gallery-section"><h2>Image gallery</h2><div class="gallery">'+gallery+'</div></section>'
        body=f'''<div class="project-heading"><a href="index.html#work">← Selected work</a><p class="eyebrow">{H(p['category'])}</p><h1>{H(p['title'])}</h1><p class="project-dates">{H(p.get('dates',''))}</p><p class="lead">{H(p['subtitle'])}</p><p>{H(p['role'])}</p></div><div class="project-hero">{image_tag(p)}</div><div class="metrics">{metrics}</div><div class="story"><div>{sections}</div><aside><h2>Skills used</h2>{''.join(f'<span class="tag">{H(t)}</span>' for t in p['tags'])}<p class="note">{H(p['review_status'])}</p></aside></div>{gallery}'''
        if p.get('template') == 'combat-robot' or p.get('overview_specs'):
            if p.get('template') == 'combat-robot':
                robot = p['robot']
                facts = [('Type & weight', robot['type'] + ' · ' + robot['weight']), ('Version', robot.get('version','')), ('Win record (' + robot.get('version','') + ')', robot['record'] + ' · ' + robot.get('winrate','')), ('Competitions (' + robot.get('version','') + ')', robot['competitions']), ('Energy stored', robot['energy'])]
            else:
                facts = p['overview_specs']
            lead_caption = f'<figcaption>{H(p["images"][0]["caption"])}</figcaption>' if p['images'][0].get('show_caption',True) else ''
            role_html = '<br>'.join(H(line) for line in p['role'].splitlines())
            review_note = f'<p class="note">{H(p["review_status"])}</p>' if p.get('show_review_note',True) else ''
            stats = ''.join(f'<div><dt>{H(label)}</dt><dd>{H(value)}</dd></div>' for label,value in facts)
            body = f'''<div class="project-heading"><a href="index.html#work">← Selected work</a><p class="eyebrow">{H(p['category'])}</p><h1>{H(p['title'])}</h1><p class="project-dates">{H(p.get('dates',''))}</p></div><div class="robot-overview"><figure><div class="robot-image">{image_tag(p, priority=True)}</div>{lead_caption}</figure><aside class="robot-facts"><p class="eyebrow">{H(p.get('overview_title','ROBOT AT A GLANCE'))}</p><dl>{stats}</dl></aside></div><div class="story"><div class="role-skills"><section class="project-role"><h2>My role</h2><p>{role_html}</p></section><aside><h2>Skills used</h2>{''.join(f'<span class="tag">{H(t)}</span>' for t in p['tags'])}{review_note}</aside></div>{sections}</div>{gallery}'''
        project_page = page(profile,p['title'],body,project=p).replace('</body>', '<script src="image-viewer.js" defer></script></body>')
        (OUT / (p['slug']+'.html')).write_text(project_page,encoding='utf-8')
    body=f'''<section class="hero"><div><h1>{H(profile['title'])}</h1><p class="lead">{H(profile['intro'])}</p><a class="button" href="#work">Explore the work ↓</a><a class="text-link" href="portfolio.pdf">Download portfolio ↗</a></div><figure>{image_tag(projects[0], priority=True)}</figure></section><section id="work"><div class="section-heading"><h2>Explore my projects.</h2></div><div class="projects">{cards}</div></section><section class="closing homepage-contact" aria-labelledby="contact-title"><div><h2 id="contact-title">Get in touch</h2><a class="section-link" href="mailto:{H(profile["email"])}">{H(profile["email"])}</a></div><a class="button" href="portfolio.pdf">View portfolio PDF <span aria-hidden="true">↗</span></a></section>'''
    (OUT/'index.html').write_text(page(profile,'Home',body,True),encoding='utf-8')
    robot_body=f'''<div class="project-heading"><a href="index.html#work">← All projects</a><p class="eyebrow">PROJECTS</p><h1>Combat Robotics</h1><p class="lead">Explore the robots, design decisions, and competition experience behind each build.</p></div><div class="projects category-projects">{robot_cards}</div>'''
    (OUT/'combat-robotics.html').write_text(page(profile,'Combat Robotics',robot_body),encoding='utf-8')
    shutil.copy(ROOT/'templates/style.css', OUT/'style.css')
    shutil.copy(ROOT/'templates/image-viewer.js', OUT/'image-viewer.js')
    shutil.copy(ROOT/'templates/navigation.js', OUT/'navigation.js')

def build_pdf(profile, projects):
    from reportlab.lib.pagesizes import landscape, letter
    W,H=landscape(letter); c=canvas.Canvas(str(OUT/'portfolio.pdf'),pagesize=(W,H))
    c.setTitle(profile['name']+' | Engineering Portfolio'); c.setAuthor(profile['name'])
    ink=HexColor('#162d30'); green=HexColor('#176b60'); muted=HexColor('#576a67')
    style=ParagraphStyle('body',fontName='Helvetica',fontSize=10,leading=14,textColor=ink,spaceAfter=0)
    label=ParagraphStyle('label',parent=style,fontSize=9,leading=12,textColor=muted)
    def normalize(s): return s.replace('–','-').replace('—','-').replace('×','x').replace('’',"'").replace('“','"').replace('”','"')
    def paragraph(text,x,top,width,sty=style):
        p=Paragraph(rich_text(normalize(text)).replace('\n','<br/>'),sty); _,h=p.wrap(width,1000); p.drawOn(c,x,top-h); return h
    page_no=0
    def begin(title, dates='', continued=False):
        nonlocal page_no
        page_no+=1; c.setFillColor(HexColor('#faf9f5')); c.rect(0,0,W,H,fill=1,stroke=0)
        c.setFillColor(green); c.setFont('Helvetica-Bold',9); c.drawString(36,H-31,'MANAN SINGH / ENGINEERING PORTFOLIO')
        c.setFillColor(ink); c.setFont('Helvetica-Bold',25 if continued else 29); c.drawString(36,H-69,normalize(title)+(' / continued' if continued else ''))
        if dates: c.setFillColor(muted); c.setFont('Helvetica',9); c.drawString(36,H-86,normalize(dates))
    def end():
        c.setFillColor(muted); c.setFont('Helvetica',8); c.drawString(36,22,'Manan Singh / Engineering Portfolio'); c.drawRightString(W-36,22,str(page_no)); c.showPage()
    def photo(img,x,y,w,h):
        from PIL import Image, ImageOps
        from io import BytesIO
        im=ImageOps.exif_transpose(Image.open(ROOT/'media'/img['file'])); im.thumbnail((1400,1050)); buf=BytesIO()
        if 'A' in im.getbands(): im.save(buf,format='PNG',optimize=True)
        else: im.convert('RGB').save(buf,format='JPEG',quality=85,optimize=True)
        buf.seek(0); c.drawImage(ImageReader(buf),x,y,width=w,height=h,preserveAspectRatio=True,anchor='c',mask='auto')
    for p in sorted(projects, key=lambda project: project['slug'] == 'arena'):
        begin(p['title'],p.get('dates',''))
        photo(p['images'][0],38,210,365,285)
        x=430; y=H-116
        c.setFillColor(green); c.setFont('Helvetica-Bold',10); c.drawString(x,y,'AT A GLANCE'); y-=20
        if p.get('overview_specs'): facts=p['overview_specs']
        else:
            r=p['robot']; facts=[('Type & weight',r['type']+' / '+r['weight']),('Version',r.get('version','')),('Win record',r['record']+' / '+r.get('winrate','')),('Competitions',r['competitions']),('Energy stored',r['energy'])]
        for k,v in facts:
            paragraph(k.upper(),x,y,320,label); y-=13
            h=paragraph(str(v),x,y,320); y-=h+12
        c.setFillColor(ink); c.setFont('Helvetica-Bold',12); c.drawString(38,170,'My role')
        h=paragraph(p['role'],38,155,W-76)
        if h>75: raise ValueError('Role too long: '+p['slug'])
        end()
        sections=p['sections']
        for start in range(0,len(sections),2):
            begin(p['title'],continued=True)
            for j,(title,body) in enumerate(sections[start:start+2]):
                top=H-103-j*225
                c.setFillColor(ink); c.setFont('Helvetica-Bold',14); c.drawString(38,top,normalize(title))
                media=p.get('section_images',{}).get(title); textwidth=365 if media else W-76
                h=paragraph(body,38,top-13,textwidth)
                if h>188: raise ValueError('Section too long: '+p['slug']+' / '+title)
                if media:
                    imgs=[media]+media.get('additional',[]); boxx=435; boxw=W-38-boxx
                    if len(imgs)==1: photo(imgs[0],boxx,top-183,boxw,180)
                    else:
                        for k,img in enumerate(imgs[:3]): photo(img,boxx+k*boxw/len(imgs),top-175,boxw/len(imgs)-4,155)
                link=p.get('section_links',{}).get(title)
                if link and h<155:
                    c.setFillColor(green); c.setFont('Helvetica',9); c.drawString(38,top-23-h,normalize(link['label']).replace(' ↗','')); c.linkURL(link['url'],(38,top-27-h,300,top-14-h),relative=0)
            end()
    c.save()

def main():
    profile=json.loads((ROOT/'content/profile.json').read_text(encoding='utf-8'))
    projects=load_projects(profile)
    OUT.mkdir(exist_ok=True)
    # Remove generated pages for projects no longer selected for publication.
    active_pages={project['slug']+'.html' for project in projects}|{'index.html','combat-robotics.html'}
    for old_page in OUT.glob('*.html'):
        if old_page.name not in active_pages: old_page.unlink()
    (OUT/'media').mkdir(exist_ok=True)
    for project in projects:
        assets=project['images'][:1]+project.get('gallery',[])
        for entry in project.get('section_images',{}).values(): assets += [entry]+entry.get('additional',[])
        for asset in assets: shutil.copy2(ROOT/'media'/asset['file'],OUT/'media'/asset['file'])
    shutil.copytree(ROOT/'documents',OUT/'documents',dirs_exist_ok=True)
    build_web(profile,projects)
    if '--web-only' not in sys.argv: build_pdf(profile,projects)
    (OUT/'.nojekyll').touch()

    print(f'Built {len(projects)} projects, website, and {len(projects)}-page PDF in {OUT}')

if __name__=='__main__': main()
