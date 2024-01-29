import csv
import os
import time
import requests
from bs4 import BeautifulSoup
from utils.finance import get_dollar_info


def realstate_search(url: str, base_output_path: str):
    print(f"- Getting real state information from {url}")
    print(f"- Saving it in {base_output_path}")
    usd_rate = get_dollar_info()

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Using the Chrome Developer Tool: This is the class that holds each property information.
    web_elems = soup.find_all(class_='letra2 cajaPremiumResultados ResultadoCaja')

    count = 0
    source_url = url
    header = ('source_id', 'address', 'op_type', 'house_type', 'area', 'room_num', 'Price (USD)',
              'USD/m', 'USD_rate', 'source_url', 'description', 'last_update', 'time_stamp')

    dt_format = "%Y-%m-%d %H:%M:%S"
    time_stamp = time.strftime(dt_format, time.gmtime(time.time()))

    for elem in web_elems:
        # Each elem is a new BeautifulSoup object.
        ficha = elem.find('div', class_='resultadoTipo').find('a').text.split(" en ")
        address = ficha[0]
        op_type = ficha[1].strip() if len(ficha) > 1 else None
        # ----
        gral_desc = elem.find('div', class_='resultadoLocalidad').find('div').text
        house_type = gral_desc.split()[0]
        # ----
        features = elem.find('div', class_='resultadopublica').text.strip()
        ff = features.split()
        last_update = ff[-1]
        source_id = ff[-2]
        area = ff[ff.index('mts') - 1]
        # aux_garage_index = ff.index('Garage') if 'Garage' in ff else None
        # garage = ff[aux_garage_index + 1] if aux_garage_index else None

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

        price_usd = price_s = 0
        if 'u$d' in location_elem.text:
            price_usd = int(location_elem.text.replace('u$d', '').replace('.', ''))
            # price_s = int(price_usd * usd_rate)

        usd_per_m = int(price_usd//float(area))
        row = (source_id, address, op_type, house_type, area, room_num, f"{price_usd:,}", usd_per_m,
               usd_rate, source_url, desc.text, last_update, time_stamp)

        # print('_'*30)
        # print(row)
        # print('_' * 30)
        count += 1

        # Path to your CSV file
        # csv_file_path = '/Users/facundoradrizzani/PycharmProjects/jupyter/dev/WebScraper/output.csv'
        site = 'inmobusqueda'
        dt_format = "%Y%m%d"
        partition = 'site=' + site + '/yyyymmdd=' + time.strftime(dt_format, time.gmtime(time.time()))
        csv_file_path = base_output_path + partition

        # Creating the path if does not exist
        os.makedirs(csv_file_path, exist_ok=True)

        csv_file_path = csv_file_path + '/properties.csv'
        # Open the CSV file in append mode
        with open(csv_file_path, 'a', newline='') as file:
            writer = csv.writer(file)

            # Check if the file is empty (no header present)
            is_empty = file.tell() == 0

            # Write the header if the file is empty
            if is_empty:
                writer.writerow(header)

            # Append the row to the CSV file
            writer.writerow(row)

    print(f"Total adds:{count}")
