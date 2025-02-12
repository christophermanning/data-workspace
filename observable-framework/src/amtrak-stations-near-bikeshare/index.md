# Amtrak Stations Near Bikeshare

```js
// notifies a parent iframe to resize
const observer = new ResizeObserver(([entry]) => parent.postMessage({height: entry.target.offsetHeight}, "*"));
observer.observe(document.documentElement);

import {link, citation} from "../util.js";

import.meta.resolve("npm:us-atlas@3.0.1/states-10m.json")
const us = await fetch("../_npm/us-atlas@3.0.1/states-10m.json").then((d) => d.json());
let states = topojson.feature(us, us.objects.states);

const db = FileAttachment("../data/amtrak-stations-near-bikeshare.sqlite3").sqlite();
```

```js
// multiple station queries to prevent circular definition
const amtrak_stations_map = await db.query(`
select
location
,station_id
,bikeshare_name
,lat
,lon
,count(*) as num_bikeshare_stations
from amtrak_stations s
left join bikeshare_stations b using(station_id)
where dist <= ${maxDistance}
and station_id ${selectedStationsList}
group by 1,2,3,4,5
`)
```

```js
const amtrak_stations = await db.query(`
select
location
,station_id
,bikeshare_name
,lat
,lon
,count(*) as num_bikeshare_stations
from amtrak_stations s
left join bikeshare_stations b using(station_id)
where dist <= ${maxDistance}
group by 1,2,3,4,5
`)
```

```js
const amtrak_stations_geojson = amtrak_stations_map.map(d => {
    return {
        type: "Feature",
        geometry: {type : "Point", coordinates: [d.lon, d.lat] },
        properties: {...d }
    }
})
```

```js
let geojson = await db.query(`
select name, geom
from amtrak_routes
`)
geojson = geojson.map(d => {
    let gj = JSON.parse(d.geom)
    gj.route = d.name
    return gj
})
```

```js
const plot = Plot.plot({
  projection: "albers",
  marks: [
    Plot.geo(states, { fill: "white", stroke: "#e2e2e2" }),
    Plot.geo(geojson, { strokeWidth: 2, stroke: "route", tip: { anchor: "top", fontSize: 15 } }),
    Plot.dot(amtrak_stations_geojson, Plot.centroid({stroke: "black", fill: "white", strokeWidth: 2, r: 5, symbol: "circle"  })),
    Plot.tip(amtrak_stations_geojson, Plot.pointer(Plot.centroid({fontSize: 15, title: (d) => `${d.properties.location} - ${d.properties.station_id} Amtrak station\n${d.properties.num_bikeshare_stations} nearby ${d.properties.bikeshare_name} bikeshare stations`}))),
    Plot.text([`Route colors are selected randomly\nto distinguish between different routes.`], { x:20, frameAnchor: "bottom", textAnchor: "start" })
  ],
  height: 500,
  width: 800,
  margin: 50
})
display(plot)
```

### Amtrak Stations

```js
const maxDistance = view(Inputs.range([1, 400], {label: "Max Distance (meters)", value: 400, step: 1}));
```

```js
const selectedStationsInput = Inputs.table(amtrak_stations, {
    header: {station_id: "Amtrak Station", location: "City, State", bikeshare_name: "Bikeshare System", num_bikeshare_stations: "Nearby Stations"},
    columns: ["station_id", "location", "bikeshare_name", "num_bikeshare_stations"],
    layout: "auto",
    sort: "location",
    format: {
        station_id: (d, i, a) => {
            return html`${link(d, `https://www.openstreetmap.org/?mlat=${a[i].lat}&mlon=${a[i].lon}#map=18/${a[i].lat}/${a[i].lon}&layers=Y`, "View in OpenStreetMap")}`
        },
    }
})
display(selectedStationsInput)
const selectedStations = Generators.input(selectedStationsInput)
```

```js
let selectedStationsList = selectedStations.map(d=>`"${d.station_id}"`)
if(selectedStationsList.length == 0) {
    selectedStationsList = 'is null'
} else {
    selectedStationsList = `in(${selectedStationsList})`
}
```

<div class="note small">
Built with ${link("Observable Framework", "https://observablehq.com/platform/framework")},
${link("Observable Plot", "https://observablehq.com/plot/")}, and 
${link("SQLite Wasm", "https://www.npmjs.com/package/@sqlite.org/sqlite-wasm")}.


<p><h3>References</h3>
<ul>
<li>${citation("U.S. Atlas TopoJSON", "https://www.npmjs.com/package/us-atlas", "npm", "April 19, 2023")}.
<li>${citation("Locations of Docked Bikeshare Stations by System and Year", "https://data.bts.gov/Bicycles-and-Pedestrians/Locations-of-Docked-Bikeshare-Stations-by-System-a/7m5x-ubud/about_data", "Bureau of Transportation Statistics", "August 21, 2024")}.
<li>${citation("Amtrak Routes", "https://geodata.bts.gov/datasets/usdot::amtrak-routes/about", "Bureau of Transportation Statistics", "March 01, 2024")}.
<li>${citation("Amtrak Stations", "https://geodata.bts.gov/datasets/usdot::amtrak-stations/about", "Bureau of Transportation Statistics", "January 30, 2025")}.
</div>
