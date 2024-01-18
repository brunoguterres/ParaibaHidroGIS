var baseOpenStreetMap = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                                        maxZoom: 22,
                                        opacity: 1,
                                        attribution: '<a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
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

var sedesMunicipais = L.Geoserver.wms('http://191.252.221.146:8080/geoserver/wms', {
                                        layers: 'paraiba:sedes_municipais_pb',
                                        attribution: 'AESA',
});

var rodovias = L.Geoserver.wms('http://191.252.221.146:8080/geoserver/wms', {
                                layers: 'paraiba:rodovias_pb',
                                attribution: 'AESA',
});

var drenagemPrincipal = L.Geoserver.wms('http://191.252.221.146:8080/geoserver/wms', {
                                        layers: 'paraiba:drenagem_principal_pb',
                                        attribution: 'AESA',
});

var acudes= L.Geoserver.wms('http://191.252.221.146:8080/geoserver/wms', {
                                layers: 'paraiba:acudes_pb',
                                attribution: 'AESA',
});

var bacias = L.Geoserver.wms('http://191.252.221.146:8080/geoserver/wms', {
                                layers: 'paraiba:bacias_pb',
                                attribution: 'AESA',
});

var municipios = L.Geoserver.wms('http://191.252.221.146:8080/geoserver/wms', {
                                    layers: 'paraiba:municipios_pb',
                                    attribution: 'IBGE',
});

var estado = L.Geoserver.wms('http://191.252.221.146:8080/geoserver/wms', {
                                layers: 'paraiba:divisa_estadual_pb',
                                attribution: 'IBGE',
});

var map = L.map('map', {
                        center: [-7.2, -37],
                        zoom: 8,
                        layers: [baseOpenStreetMap,
                                estado,
                                municipios,
                                bacias,
                                acudes,
                                drenagemPrincipal,
                                rodovias]
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