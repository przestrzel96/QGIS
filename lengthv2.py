from qgis.core import *
from qgis.gui import *

# Wybieranie aktywnej warstwy
warstwa = iface.activeLayer()

# Sprawdzanie, czy istnieje kolumna 'długosc', i dodawanie jej, jeśli nie istnieje
if 'długosc' not in warstwa.fields().names():
    pv = warstwa.dataProvider()
    pv.addAttributes([QgsField('długosc', QVariant.Double)])
    warstwa.updateFields()

# Tworzenie wyrażenia do obliczania długości
expression = QgsExpression('round($length, 4)') #Obliczenie długości do 4 miejsc po przecinku
context = QgsExpressionContext() 
context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(warstwa))

# Edytowanie warstwy i obliczanie długości
with edit(warstwa):
    for f in warstwa.getFeatures():
        context.setFeature(f)
        długość_m = expression.evaluate(context)
        f['długosc'] = długość_m
        warstwa.updateFeature(f)
