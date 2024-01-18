/*CREATE TABLE uniao_cobacia AS*/
SELECT 
    t.cobacia,
    t.cotrecho,
    t.nutrjus,
    o.vazao_horaria_m3h,
	d."Q95NAT"
FROM 
    ottotrechos_pb_5k t
LEFT JOIN 
    outorgas_agregadas o ON t.cobacia = o.cobacia  
LEFT JOIN 
    disp_hid_pb_5k d ON t.cobacia = d.cobacia;