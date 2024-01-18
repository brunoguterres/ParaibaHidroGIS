import requests
from qgis.core import QgsVectorLayer

def importar_camada_ottobacias(parametros_conexao, nome_camada_ottobacias):
#   função de carregamento de camadas vetorial de ottobacias do banco
    uri = QgsDataSourceUri()
    uri.setConnection(parametros_conexao['host_bd'], parametros_conexao['porta_bd'], parametros_conexao['nome_bd'], parametros_conexao['usuario_bd'], parametros_conexao['senha_bd'])
    uri.setDataSource(parametros_conexao['schema_bd'], nome_camada_ottobacias, 'geom')
    ottobacias = QgsVectorLayer(uri.uri(False), 'camada_ottobacias', 'postgres')
    ottobacias.renderer().symbol().setColor(QColor(200, 200, 200, 10))
    QgsProject.instance().addMapLayer(ottobacias)
    print('\n''-> Importação da camada de ottobacias realizada.')
    return ottobacias

def importar_camada_ottotrechos(parametros_conexao, nome_camada_ottotrechos):
#   função de carregamento de camadas vetorial de ottotrechos do banco
    uri = QgsDataSourceUri()
    uri.setConnection(parametros_conexao['host_bd'], parametros_conexao['porta_bd'], parametros_conexao['nome_bd'], parametros_conexao['usuario_bd'], parametros_conexao['senha_bd'])
    uri.setDataSource(parametros_conexao['schema_bd'], nome_camada_ottotrechos, 'geom')
    ottotrechos = QgsVectorLayer(uri.uri(False), 'camada_ottotrechos', 'postgres')
    ottotrechos.renderer().symbol().setColor(QColor(0, 150, 255))
    QgsProject.instance().addMapLayer(ottotrechos)
    print('\n''-> Importação da camada de ottotrechos realizada.')
    return ottotrechos

def importar_disponibilidade_hidrica(parametros_conexao, schema_bd, nome_camada_disp):
#   função de carregamento de camadas vetorial de disponibilidade hídrica do banco
    uri = QgsDataSourceUri()
    uri.setConnection(parametros_conexao['host_bd'], parametros_conexao['porta_bd'], parametros_conexao['nome_bd'], parametros_conexao['usuario_bd'], parametros_conexao['senha_bd'])
    uri.setDataSource(parametros_conexao['schema_bd'], nome_camada_disp, 'geom')
    disponibilidade_hidrica = QgsVectorLayer(uri.uri(False), 'camada_disp_hid', 'postgres')
    QgsProject.instance().addMapLayer(disponibilidade_hidrica, False)  # Camada adicionada, mas não visível.
    print('\n''-> Importação da camada de disponibilidade hídrica realizada.')
    return disponibilidade_hidrica

def importar_captacoes(parametros_conexao, nome_camada_outorgas):
#   função de carregamento de camadas vetorial de outorgas de captação do banco
    uri = QgsDataSourceUri()
    uri.setConnection(parametros_conexao['host_bd'], parametros_conexao['porta_bd'], parametros_conexao['nome_bd'], parametros_conexao['usuario_bd'], parametros_conexao['senha_bd'])
    uri.setDataSource(parametros_conexao['schema_bd'], nome_camada_outorgas, 'geom')
    outorgas = QgsVectorLayer(uri.uri(False), 'camada_outorgas', 'postgres')
    QgsProject.instance().addMapLayer(outorgas, True) 
    print('\n''-> Importação da camada de captações realizada.')
    return outorgas

def importar_camada_fundo():
#   função de carregamento da camada de plano de fundo
    service_url = 'mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}'
    service_uri = 'type=xyz&zmin=0&zmax=21&url=https://'+requests.utils.quote(service_url)
    iface.addRasterLayer(service_uri, 'Google_Road', 'wms')

### EXECUÇÃO ###

# IMPORTAÇÃO DE CAMADA DE FUNDO #
importar_camada_fundo()
print('\n''-> Camada de fundo adicionada.')

# IMPORTAÇÃO CAMADAS DA BACIA DE INTERESSE #
nome_camada_ottobacias = 'ottobacias_pb_5k'
nome_camada_ottotrechos = 'ottotrechos_pb_5k'
nome_camada_disp = 'disp_hid_pb_5k'
nome_camada_outorgas = 'outorgas_pb'
ottobacias = importar_camada_ottobacias(parametros_conexao, nome_camada_ottobacias)
ottotrechos = importar_camada_ottotrechos(parametros_conexao, nome_camada_ottotrechos)
print('\n''-> Seleção das camadas da bacia realizada.')