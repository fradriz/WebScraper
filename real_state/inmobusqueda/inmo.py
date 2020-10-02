import time
import requests
from bs4 import BeautifulSoup
from utils.finance import get_dollar_info

def inmobusqueda():
    usd_rate_change = get_dollar_info()

    URL = 'https://www.inmobusqueda.com.ar/departamento-enbarrio-tribunales-en-capital-federal-90000-200000-dolares.html'
    # URL = 'https://www.inmobusqueda.com.ar/propiedades-enbarrio-nunez-en-capital-federal-pagina-2.html'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Buscando en el Developer Tool de Chrome veo que esta clase me interesa
    web_elems = soup.find_all(class_='letra2 cajaPremiumResultados ResultadoCaja')

    count = 0
    source = URL
    header = ('address', 'offer_type', 'house_type', 'area', 'room_num', 'price_u$d', 'price_$',
              'u$d_rate_change', 'source', 'description', 'last_update', 'add_id', 'time_stamp')
    print(header)
    print('_.' * 15)

    dt_format = "%Y-%m-%d %H:%M:%S"
    time_stamp = time.strftime(dt_format, time.gmtime(time.time()))

    for elem in web_elems:
        # Each elem is a new BeautifulSoup object.
        # You can use the same methods on it as you did before.
        ficha = elem.find('div', class_='resultadoTipo').find('a').text.split(" en ")
        address = ficha[0]
        offer_type = ficha[1].strip() if len(ficha) > 1 else None
        # ----
        gral_desc = elem.find('div', class_='resultadoLocalidad').find('div').text
        house_type = gral_desc.split()[0]
        # ----
        features = elem.find('div', class_='resultadopublica').text.strip()
        ff = features.split()
        last_update = ff[-1]
        add_id = ff[-2]
        area = ff[ff.index('mts') - 1]
        aux_garage_index = ff.index('Garage') if 'Garage' in ff else None
        garage = ff[aux_garage_index + 1] if aux_garage_index else None

        if 'Monoamb' in ff:
            room_num = 1
        else:
            aux_amb_ii = ff.index('Dorm')
            if aux_amb_ii:
                room_num = int(ff[aux_amb_ii - 1]) + 1
            else:
                room_num = None
                # ----
        location_elem = elem.find('div', class_='resultadoPrecio')
        desc = elem.find('div', class_='resultadoDescripcion')

        if 'u$d' in location_elem.text:
            price_usd = float(location_elem.text.replace('u$d', '').replace('.', ''))
            price_s = int(price_usd * usd_rate_change)

        row = (address, offer_type, house_type, area, room_num, price_usd, price_s, usd_rate_change,
               source, desc.text, last_update, add_id, time_stamp)

        # print('_'*30)
        print(row)
        print('_' * 30)
        count += 1

    print(f"Total adds:{count}")
