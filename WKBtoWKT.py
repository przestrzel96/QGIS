from PyQt5.QtCore import QVariant
from qgis.core import QgsField, QgsFeature, QgsGeometry
import binascii  # Do konwersji ciągu szesnastkowego WKB

warstwa = iface.activeLayer()  # Pobieranie aktywnej warstwy z interfejsu QGIS

# Sprawdzenie, czy kolumna 'WKT' już istnieje, jeśli nie, dodaj ją
if not 'WKT' in [field.name() for field in warstwa.fields()]:
    warstwa.startEditing()
    warstwa.addAttribute(QgsField('WKT', QVariant.String))
    warstwa.updateFields()

# Definiowanie funkcji generatora
def generator(lista):
    for feature in lista:
        obj_id = feature['id']  # Pobieranie wartości z kolumny 'id'
        wkb_hex_str = feature['wkb_geometry']  # Pobieranie wartości WKB (w postaci ciągu szesnastkowego) z kolumny 'wkb_geometry'

        try:
            # Konwersja ciągu szesnastkowego (hex) do bytes
            wkb_bytes = binascii.unhexlify(wkb_hex_str)

            # Tworzenie obiektu QgsGeometry
            geom = QgsGeometry()
            geom.fromWkb(wkb_bytes)

            # Konwersja QgsGeometry do WKT
            wkt = geom.asWkt()

            # Aktualizacja wartości w kolumnie 'WKT' na podstawie 'id'
            warstwa.startEditing()
            for feat in warstwa.getFeatures():
                if feat['id'] == obj_id:
                    feat['WKT'] = wkt
                    if warstwa.updateFeature(feat):
                        print("Zaktualizowano obiekt w warstwie.")
                    else:
                        print("Nie udało się zaktualizować obiektu w warstwie.")
            warstwa.commitChanges()

        except binascii.Error as e:
            print(f"Błąd konwersji WKB do WKT dla obiektu o id {obj_id}: {str(e)}")
        except Exception as e:
            print(f"Inny błąd dla obiektu o id {obj_id}: {str(e)}")

# Wywołanie generatora
generator(warstwa.getFeatures())
