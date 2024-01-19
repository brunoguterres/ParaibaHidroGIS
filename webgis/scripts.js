var baseOpenStreetMap = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                                        maxZoom: 22,
                                        opacity: 1,
                                        attribution: '<a href="http://www.openstreetmap.org">OpenStreetMap</a>'
});

var baseGoogleSatelite = L.tileLayer('https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
                                        maxZoom: 22,
                                        opacity: 1,
                                        attribution: '<a href="https://www.google.com/maps">Google Satélite</a>'
});

var baseGoogleStreets = L.tileLayer('https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
                                        subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
                                        maxZoom: 22,
                                        opacity: 1,
                                        attribution: '<a href="https://www.google.com/maps">Google Streets</a>'
});

var sedesMunicipais = L.Geoserver.wms('http://10.5.3.18:8080/geoserver/wms', {
                                        layers: 'prh_rpb:loc_sedes_municipais_Paraiba_AESA_2007',
                                        attribution: 'AESA',
});

var rodovias = L.Geoserver.wms('http://10.5.3.18:8080/geoserver/wms', {
                                layers: 'prh_rpb:inf_rodovias_Paraiba_AESA_2021',
                                attribution: 'AESA',
});

var drenagemPrincipal = L.Geoserver.wms('http://10.5.3.186:8080/geoserver/wms', {
                                        layers: 'prh_rpb:hid_drenagem_principal_Paraiba_AESA_2022',
                                        attribution: 'AESA',
});

var acudes= L.Geoserver.wms('http://10.5.3.18:8080/geoserver/wms', {
                                layers: 'prh_rpb:hid_acudes_Paraiba_AESA_2022',
                                attribution: 'AESA',
});

var bacias = L.Geoserver.wms('http://10.5.3.18:8080/geoserver/wms', {
                                layers: 'prh_rpb:lim_bacias_Paraiba_AESA_2022',
                                attribution: 'AESA',
});

var municipios = L.Geoserver.wms('http://10.5.3.18:8080/geoserver/wms', {
                                    layers: 'prh_rpb:limites_municipais',
                                    attribution: '<a href="https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/15774-malhas.html">IBGE</a>',
});

var estado = L.Geoserver.wms('http://10.5.3.18:8080/geoserver/wms', {
                                layers: 'prh_rpb:limite_estadual_pb',
                                attribution: '<a href="https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/15774-malhas.html">IBGE</a>',
});

var map = L.map('map', {
                        center: [-7.2, -37],
                        zoom: 8,
                        layers: [baseOpenStreetMap,
                                municipios,
                                bacias,
                                acudes,
                                drenagemPrincipal]
});

var baseMaps = {"OpenStreetMap": baseOpenStreetMap,
                "Google Satelite": baseGoogleSatelite,
                "Google Streets": baseGoogleStreets,
};

var overlayMaps = { "Estado": estado,
                    "Municípios": municipios,
                    "Bacias": bacias,
                    "Açudes": acudes,
                    "Drenagem Principal": drenagemPrincipal,
                    "Rodovias": rodovias,
};

var layerControl = L.control.layers(baseMaps, overlayMaps);
layerControl.addTo(map);

var barraEscala = L.control.scale({
            position: 'bottomright'
});
barraEscala.addTo(map);