class PointTool(QgsMapToolEmitPoint):
    def __init__(self, canvas):
        self.canvas = canvas
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.disconnect_signal = False

    def canvasPressEvent(self, event):
        if not self.disconnect_signal:
            point = self.toMapCoordinates(event.pos())
            print("Coordenadas do ponto clicado:", point.x(), ",", point.y())
            self.disconnect_signal = True
            self.deactivate()
            self.canvas.setCursor(Qt.ArrowCursor)

point_tool = PointTool(iface.mapCanvas())
iface.mapCanvas().setMapTool(point_tool)
