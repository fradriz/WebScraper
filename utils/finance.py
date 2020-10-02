import requests

# Cotización del dolar
# Oficial site: https://estadisticasbcra.com/api/documentacion
# But..
#   Need to get a token by subscribing (don't want to do it for now)
#   Only oficial information, no dolar blue ..

"""
URL = 'https://www.dolarsi.com/api/api.php?type=valoresprincipales'
{'casa': {'compra': '72,390', 'venta': '77,390', 'agencia': '349', 'nombre': 'Dolar Oficial', 'variacion': '-0,040', 
'ventaCero': 'TRUE', 'decimales': '3'}}
---
{'casa': {'compra': '127,000', 'venta': '132,000', 'agencia': '310', 'nombre': 'Dolar Blue', 'variacion': '-0,750', 
'ventaCero': 'TRUE', 'decimales': '3'}}
"""


def get_dollar_info():
    usd_rate_change = 0

    URL = 'https://www.dolarsi.com/api/api.php?type=valoresprincipales'
    resp = requests.get(URL)

    for r in resp.json():
        casa = r['casa']
        if 'Blue' in casa['nombre']:
            print(f"compra dolar blue:{casa['compra']}")
            print(f"venta dolar blue:{casa['venta']}")
            # Taking 'venta' value of Dolar Blue
            usd_rate_change = float(casa['venta'].replace(',', '.'))
            print(f"venta dolar blue:{usd_rate_change}")

    return usd_rate_change

