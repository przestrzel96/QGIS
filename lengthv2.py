from qgis.core import QgsField, QgsExpression, QgsExpressionContext, QgsExpressionContextUtils
from qgis.gui import QgsMapCanvas

# Pobieramy aktywną warstwę
layer = iface.activeLayer()

# Dodajemy nową kolumnę na długość w metrach
pv = layer.dataProvider()
pv.addAttributes([QgsField('lenght', QVariant.Double)])
layer.updateFields()

# Tworzymy wyrażenie do obliczenia długości
expression = QgsExpression('round($length, 4)')

# Tworzymy kontekst wyrażenia
context = QgsExpressionContext()
context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))

# Edytujemy warstwę
with edit(layer):
    for feature in layer.getFeatures():
        context.setFeature(feature)
        # Obliczamy długość z wyrażeniem
        length_m = expression.evaluate(context)
        # Zapisujemy długość w kolumnie
        feature['lenght'] = length_m
        layer.updateFeature(feature)
