src=open('app.src.html',encoding='utf-8').read().replace('/*LEAFLET_CSS*/',open('leaflet.css',encoding='utf-8').read())
open('artifact.html','w',encoding='utf-8').write(src)
open('../index.html','w',encoding='utf-8').write('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'+src.replace('<header class="top">','</head>\n<body>\n<header class="top">',1)+'\n</body>\n</html>\n')
