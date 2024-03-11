class MapToolIdentify(QgsMapToolIdentifyFeature):
    def __init__(self, canvas, ottobacias_icr):
        super().__init__(canvas)
        self.layer = ottobacias_icr

    def canvasReleaseEvent(self, event):
        super().canvasReleaseEvent(event)
        feicao = self.identify(event.x(), event.y(), [self.layer], QgsMapToolIdentifyFeature.TopDownAll)[0].mFeature
        bacia_selecionada = feicao.attribute('cobacia')
        canvas.setMapTool(QgsMapToolPan(canvas))
        print(bacia_selecionada)


### EXECUÇÃO ###

canvas = iface.mapCanvas()
map_tool = MapToolIdentify(canvas, ottobacias_icr)
canvas.setMapTool(map_tool)

