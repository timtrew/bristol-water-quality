import os, shutil

src=open('app.src.html',encoding='utf-8').read().replace('/*LEAFLET_CSS*/',open('leaflet.css',encoding='utf-8').read())
HEAD='<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
FOCUS='<script src="data.js"></script>\n<script>window.WQ_FOCUS="levels";</script>'
def page(body, extra_head=''):
    return HEAD+extra_head+body.replace('<header class="top">','</head>\n<body>\n<header class="top">',1)+'\n</body>\n</html>\n'

# Full app for local use.
open('../index.html','w',encoding='utf-8').write(page(src))
# The published Claude page opens on the Levels tab only.
focused=src.replace('<script src="data.js"></script>',FOCUS,1)
# The Levels page covers Floating Harbour sites only, so it carries the harbour name.
focused=focused.replace('<title>Bristol Water Quality</title>','<title>Bristol Harbour Water Quality</title>',1).replace('<h1>Bristol <span>Water Quality</span>','<h1>Bristol Harbour <span>Water Quality</span>',1)
open('artifact.html','w',encoding='utf-8').write(focused)
# The GitHub Pages site (separate public repo next to this one): Levels page, asked not to be indexed.
site=os.path.join('..','..','bristol-harbour-water-quality')
if os.path.isdir(site):
    open(os.path.join(site,'index.html'),'w',encoding='utf-8').write(page(focused,'<meta name="robots" content="noindex, nofollow">\n'))
    shutil.copyfile('../data.js',os.path.join(site,'data.js'))
