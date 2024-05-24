# Informe ao QGIS que a camada destino foi alterada
camada_destino.updateExtents()

# Atualize a interface do usuário do QGIS
iface.layerTreeView().refreshLayerSymbology(camada_destino.id())

# Crie um provedor de dados para a camada destino
provedor_camada_destino = camada_destino.dataProvider()

# Obter a camada do projeto pelo nome
camada = QgsProject.instance().mapLayersByName('nome_da_camada')[0]

# Adicionar o campo à camada
camada.dataProvider().addAttributes([campo])

# Atualizar a camada para que as mudanças sejam refletidas
camada.updateFields()
