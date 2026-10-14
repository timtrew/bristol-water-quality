# Bristol Water Quality Explorer

**Live (beta):** [Bristol Harbour Water Quality](https://timtrew.github.io/bristol-harbour-water-quality/), the Levels by year page for Floating Harbour sites, built from this repo by `build/assemble.py` into the separate [bristol-harbour-water-quality](https://github.com/timtrew/bristol-harbour-water-quality) repo.

An interactive app for exploring surface water quality samples from Bristol's Floating Harbour and rivers (1994–2026), set against daily rainfall and Wessex Water storm overflow (CSO) spills.

Open `index.html` in a browser. It needs `data.js` in the same folder and an internet connection for the chart/map libraries and street map tiles.

## What it does

- **Map**: sampling sites coloured by median level, plus 244 storm overflows sized by spill hours. Click to select sites.
- **Timeline**: samples, daily rainfall and nearby spill hours on one date axis. Detailed values or a simple Low / Elevated / High view, plus overlays of up to 5 previous years.
- **Trends**: yearly medians, trend per decade, seasonal pattern by month.
- **Levels by year**: share of Low / Elevated / High samples per year, full year or summer season (1 Apr – 31 Oct), with an option to leave out samples taken after a nearby spill.
- **Rain & spills**: how each measurement relates to rain and spills in a chosen window before sampling.
- **Events**: Bristol Harbour Festival dates (2012–2026) compared before / during / after, with your own events addable in the browser.
- **Day view** and **Samples**: search by date, site or river.

## Data sources

| Data | Source | Coverage |
|---|---|---|
| Water samples | `data/Surface_Water_Quality.csv` | 43 sites, 1994 – Sep 2026 |
| Rainfall | [Open-Meteo historical weather API](https://open-meteo.com/) (ERA5 reanalysis, central Bristol grid cell) | 1994 – present |
| Storm overflow spills | Wessex Water Event Duration Monitoring via the [Stream National Storm Overflow Hub](https://www.streamwaterdata.co.uk/pages/storm-overflows-data) | Jan 2020 – Jun 2026 |
| Waterways | © OpenStreetMap contributors | – |

Bacteria thresholds (E. coli 500 / 1,000 cfu/100 ml; enterococci 200 / 400) are indicative single-sample guides based on inland bathing water standards.

## Rebuilding the data

Requires Python 3 (standard library only).

```bash
cd build
python fetch_cso.py       # storm overflow events -> cso_raw.json (~28 MB, not committed)
python fetch_context.py   # rainfall and waterways -> rain.json, waterways.json
python build_data.py      # -> ../data.js
python assemble.py        # app.src.html -> ../index.html (and build/artifact.html)
```

Edit the app in `build/app.src.html`, then run `assemble.py`.
