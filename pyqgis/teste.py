# Defina o nome da camada e o nome do atributo que você deseja obter
nome_camada = "ottobacias_icr"
nome_atributo = "cobacia"

# Obtenha a camada
camada = QgsProject.instance().mapLayersByName('ottobacias_icr')[0]

# Crie uma ferramenta de identificação de feição
class MapToolIdentify(QgsMapToolIdentifyFeature):
    def __init__(self, canvas, layer):
        super().__init__(canvas)
        self.layer = layer

    def canvasReleaseEvent(self, event):
        # Chame o método da superclasse para realizar a identificação da feição
        super().canvasReleaseEvent(event)
        # Obtenha a feição identificada
        feicao = self.identify(event.x(), event.y(), [self.layer], QgsMapToolIdentifyFeature.TopDownAll)[0].mFeature
        # Obtenha o valor do atributo específico da feição
        valor_atributo = feicao.attribute(nome_atributo)
        # Imprima o valor do atributo na console
        print(f"Valor do atributo '{nome_atributo}' da feição selecionada: {valor_atributo}")

# Inicialize a ferramenta de identificação de feição
canvas = iface.mapCanvas()
map_tool = MapToolIdentify(canvas, camada)
canvas.setMapTool(map_tool)

