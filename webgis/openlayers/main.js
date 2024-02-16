var mapView = new ol.View ({
    center: ol.proj.fromLonLat([-36.6, -7.2]),
    zoom: 8.6,
});

var map = new ol.Map({
    target: 'map',
    view: mapView,
});

var osmTile = new ol.layer.Tile ({
    title: 'Open Street Map',
    visible: true,
    opacity: 0.8,
    source: new ol.source.OSM(),
});
map.addLayer(osmTile);

var divisasEstaduais = new ol.layer.Tile({
    title: "Divisas Estaduais da Paraíba",
    source: new ol.source.TileWMS({
        url: 'http://10.5.3.18:8080/geoserver/prh_rpb/wms',
        params: {'LAYERS':'prh_rpb:divisas_estaduais', 'TILED':true},
        serverType: 'geoserver',
        visible: true,
    }),
});
map.addLayer(divisasEstaduais);

var hidrografiaPrincipal = new ol.layer.Tile({
    title: "Hidrografia principal",
    source: new ol.source.TileWMS({
        url: 'http://10.5.3.18:8080/geoserver/prh_rpb/wms',
        params: {'LAYERS':'prh_rpb:hidrografia_principal', 'TILED':true},
        serverType: 'geoserver',
        visible: true,
    }),
});
map.addLayer(hidrografiaPrincipal);

var acudes = new ol.layer.Tile({
    title: "Açudes",
    source: new ol.source.TileWMS({
        url: 'http://10.5.3.18:8080/geoserver/prh_rpb/wms',
        params: {'LAYERS':'prh_rpb:acudes', 'TILED':true},
        serverType: 'geoserver',
        visible: true,
    }),
});
map.addLayer(acudes);

var subBacias = new ol.layer.Tile({
    title: "Sub bacias do Rio Paraíba",
    source: new ol.source.TileWMS({
        url: 'http://10.5.3.18:8080/geoserver/prh_rpb/wms',
        params: {'LAYERS':'prh_rpb:sub_bacias_rpb', 'TILED':true},
        serverType: 'geoserver',
        visible: true,
    }),
});
map.addLayer(subBacias);

var bacia = new ol.layer.Tile({
    title: "Bacia do Rio Paraíba",
    source: new ol.source.TileWMS({
        url: 'http://10.5.3.18:8080/geoserver/prh_rpb/wms',
        params: {'LAYERS':'prh_rpb:bacia_rpb', 'TILED':true},
        serverType: 'geoserver',
        visible: true,
    }),
});
map.addLayer(bacia);