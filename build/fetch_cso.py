import json, urllib.request, urllib.parse
B="https://services.arcgis.com/3SZ6e0uCvPROr4mS/arcgis/rest/services/%s/FeatureServer/0/query"
svcs=["Wessex_Water_Event_Duration_Monitoring_2020_23_view","Wessex_Water_Event_Duration_Monitoring_2024_view","Wessex_Water_Event_Duration_Monitoring_2025_view","Wessex_Water_Event_Duration_Monitoring_2026_view2"]
where="OutfallLatitude>51.40 AND OutfallLatitude<51.54 AND OutfallLongitude>-2.74 AND OutfallLongitude<-2.46"
out=[]
for s in svcs:
    off=0
    while True:
        q=urllib.parse.urlencode({"where":where,"outFields":"SiteName,ReceivingWatercourse,OutfallLatitude,OutfallLongitude,EventStart,EventEnd","resultOffset":off,"resultRecordCount":2000,"orderByFields":"OBJECTID","f":"json"})
        d=json.load(urllib.request.urlopen(B%s+"?"+q))
        if 'error' in d: print(s,d['error']); break
        f=[x['attributes'] for x in d['features']]
        for a in f: a['svc']=s
        out+=f; off+=len(f)
        if not d.get('exceededTransferLimit') and len(f)<2000: break
    print(s,off)
json.dump(out,open('cso_raw.json','w'))
