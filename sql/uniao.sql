SELECT 
    camada_ottotrechos.cobacia,
    camada_ottotrechos.cotrecho,
    camada_ottotrechos.nutrjus,
	disp_hid_pb_5k.cobacia,
	disp_hid_pb_5k.Q95NAT
FROM 
    camada_ottotrechos
LEFT JOIN disp_hid_pb_5k
	ON camada_ottotrechos.cobacia = disp_hid_pb_5k.cobacia;