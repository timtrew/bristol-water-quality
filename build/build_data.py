import csv, json, math, collections, datetime as dt
SRC='../data/Surface_Water_Quality.csv'
EPOCH=dt.date(1994,1,1)
def merc2ll(x,y):
    return round(math.degrees(math.atan(math.sinh(y/6378137))),5), round(math.degrees(x/6378137),5)
rows=list(csv.DictReader(open(SRC,encoding='utf-8-sig')))
PARAMS=[k for k in rows[0] if k not in ('X','Y','OBJECTID','Site_name','River','Site_ID','Date','EASTING','NORTHING')]
sites={};order=[]
for r in rows:
    sid=r['Site_ID']
    if sid not in sites:
        lat,lon=merc2ll(float(r['X']),float(r['Y']))
        sites[sid]={'id':sid,'name':r['Site_name'].strip(),'river':r['River'].strip().replace('BrIslington','Brislington'),'lat':lat,'lon':lon,'e':int(r['EASTING']),'n':int(r['NORTHING'])}
        order.append(sid)
order.sort(key=lambda s:(s[0],int(''.join(c for c in s[1:] if c.isdigit())),s))
idx={s:i for i,s in enumerate(order)}
samples=[]
for r in rows:
    d=dt.date(int(r['Date'][:4]),int(r['Date'][5:7]),int(r['Date'][8:10]))
    s={'s':idx[r['Site_ID']],'d':(d-EPOCH).days,'t':r['Date'][11:16]}
    for i,p in enumerate(PARAMS):
        if r[p]!='':
            v=float(r[p]); s[i]=int(v) if v==int(v) else round(v,3)
    samples.append(s)
samples.sort(key=lambda s:(s['d'],s['s']))
# rain
rj=json.load(open('rain.json'))
rs=dt.date.fromisoformat(rj['daily']['time'][0])
rain=[round(x or 0,1) for x in rj['daily']['precipitation_sum']]
# cso
raw=json.load(open('cso_raw.json'))
rank={'2026':4,'2025':3,'2024':2,'2020':1}
ov={}
for a in raw:
    n=' '.join(a['SiteName'].split()).upper()
    rk=rank[[k for k in rank if k in a['svc']][0]]
    o=ov.setdefault(n,{'name':n,'wc':'', 'lat':0,'lon':0,'rk':0,'ev':[]})
    if rk>=o['rk']:
        o.update(rk=rk,lat=round(a['OutfallLatitude'],5),lon=round(a['OutfallLongitude'],5),wc=' '.join((a['ReceivingWatercourse'] or '').split()).upper())
    if a['EventStart'] and a['EventEnd'] and a['EventEnd']>a['EventStart']:
        o['ev'].append((a['EventStart']//60000,a['EventEnd']//60000))
ovs=sorted(ov.values(),key=lambda o:o['name'])
csodaily=[]  # [ovIdx, day, minutes]
csoinfo=[]
EP_MIN=int(dt.datetime(1994,1,1,tzinfo=dt.timezone.utc).timestamp()//60)
for i,o in enumerate(ovs):
    ev=sorted(set(o['ev'])); merged=[]
    for s,e in ev:
        if merged and s<=merged[-1][1]: merged[-1][1]=max(merged[-1][1],e)
        else: merged.append([s,e])
    days=collections.Counter()
    for s,e in merged:
        s-=EP_MIN; e-=EP_MIN
        while s<e:
            d=s//1440; nxt=min(e,(d+1)*1440); days[d]+=nxt-s; s=nxt
    for d,m in sorted(days.items()): csodaily.append([i,d,m])
    tot=sum(e-s for s,e in merged)
    csoinfo.append({'name':o['name'].title(),'wc':o['wc'].title(),'lat':o['lat'],'lon':o['lon'],'spills':len(merged),'hours':round(tot/60)})
# waterways
def rdp(pts,eps):
    if len(pts)<3: return pts
    (x1,y1),(x2,y2)=pts[0],pts[-1]; dx,dy=x2-x1,y2-y1; L=math.hypot(dx,dy) or 1e-12
    dmax,ix=0,0
    for i in range(1,len(pts)-1):
        x,y=pts[i]; d=abs(dy*x-dx*y+x2*y1-y2*x1)/L
        if d>dmax: dmax,ix=d,i
    if dmax>eps: return rdp(pts[:ix+1],eps)[:-1]+rdp(pts[ix:],eps)
    return [pts[0],pts[-1]]
w=json.load(open('waterways.json'))
lines=[];polys=[]
for e in w['elements']:
    if 'geometry' not in e: continue
    pts=[(round(g['lat'],5),round(g['lon'],5)) for g in e['geometry']]
    t=e['tags']; kind=t.get('waterway')
    if kind in ('river','canal','stream'):
        lines.append({'k':kind[0],'n':t.get('name',''),'p':rdp(pts,0.00006)})
    else:
        polys.append({'n':t.get('name',''),'p':rdp(pts,0.00003)})
out={'epoch':'1994-01-01','params':PARAMS,'sites':[sites[s] for s in order],'samples':samples,
     'rainStart':(rs-EPOCH).days,'rain':rain,'rainSource':'Open-Meteo historical weather API (ERA5 reanalysis), 51.455N 2.59W',
     'overflows':csoinfo,'csoDaily':csodaily,'csoRange':['2020-01-01','2026-06-30'],
     'waterLines':lines,'waterPolys':polys}
s=json.dumps(out,separators=(',',':'))
open('../data.js','w').write('window.WQ_DATA='+s+';')
print(len(s)/1e6,'MB', len(samples),len(csoinfo),len(csodaily),len(lines),len(polys))
