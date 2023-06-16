import os

from jobs.real_state_search import realstate_search


def main():
    """
    Main ETL job definition: Process CWR files
    :return: None
    """
    home = os.environ['HOME']

    URL = 'https://www.inmobusqueda.com.ar/departamento-enbarrio-tribunales-en-capital-federal-90000-200000-dolares.html'
    # URL = 'https://www.inmobusqueda.com.ar/propiedades-enbarrio-nunez-en-capital-federal-pagina-2.html'

    base_output_path = home + '/PycharmProjects/jupyter/dev/WebScraper/data_output/'
    realstate_search(url=URL, base_output_path=base_output_path)


if __name__ == '__main__':
    main()
