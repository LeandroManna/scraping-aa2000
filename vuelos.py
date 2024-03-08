import requests
from bs4 import BeautifulSoup
import json

def obtener_datos_vuelos(url, tabla_id, archivo_json, titulo_json, mapeo_lineas_aereas):
    # Lista para almacenar los datos de vuelos
    datos_vuelos = []

    # Realiza una solicitud HTTP GET para obtener el contenido de la página
    response = requests.get(url)

    # Verifica si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Obtiene el contenido HTML de la página
        html = response.text

        # Parsea el contenido HTML
        soup = BeautifulSoup(html, "html.parser")

        # Encuentra la tabla de vuelos por su id
        tabla_vuelos = soup.find("div", {"id": tabla_id}).find("table", {"class": "scrollvuelos-main"})

        # Verifica si la tabla de vuelos se encontró
        if tabla_vuelos:
            # Itera a través de las filas de la tabla
            for fila in tabla_vuelos.find("tbody", {"class": "longtable"}).find_all("tr", {"class": "popup"}):
                hora = fila.find("td", {"class": "hora stda"}).text.strip()
                vuelo = fila.find("td", {"class": "vuelo"}).text.strip()
                codigo_linea_aerea = vuelo.split()[0]  # Obtiene el código de línea aérea del número de vuelo

                # Busca el código en el diccionario de mapeo
                if codigo_linea_aerea in mapeo_lineas_aereas:
                    linea_aerea = mapeo_lineas_aereas[codigo_linea_aerea]
                else:
                    linea_aerea = "Desconocida"  # En caso de código de línea aérea desconocido

                ciudad = fila.find("td", {"class": "ciudad"}).text.strip()
                estima = fila.find("td", {"class": "estima"}).text.strip()
                terminal = fila.find("td", {"class": "termsec terminal"}).text.strip()
                estado = fila.find("td", {"class": "status"}).find("div", {"class": "statusText"}).text.strip()

                # Crea un diccionario con los datos y agrégalo a la lista
                datos_vuelos.append({
                    "Hora": hora,
                    "Vuelo": vuelo,
                    "Línea Aérea": linea_aerea,
                    "Ciudad": ciudad,
                    "Estima": estima,
                    "Terminal": terminal,
                    "Estado": estado
                })

            # Crea un diccionario con el título y los datos
            vuelos_dict = {
                "Título": titulo_json,
                "Datos": datos_vuelos
            }

            # Escribe los datos en un archivo JSON
            with open(archivo_json, "w", encoding="utf-8") as json_file:
                json.dump(vuelos_dict, json_file, ensure_ascii=False, indent=4)

            print(f"Los datos de {titulo_json} se han guardado en {archivo_json} con el título '{titulo_json}'.")
        else:
            print(f"No se encontró la tabla de {titulo_json} en la página web.")
    else:
        print("La solicitud HTTP no fue exitosa. Verifica la URL o la conexión a Internet.")

# URL de la página web
url_jujuy = "https://www.aa2000.com.ar/jujuy"

# Diccionario de mapeo de códigos de línea aérea a nombres de aerolíneas
mapeo_lineas_aereas = {
    "AR": "Aerolíneas Argentinas",
    "WJ": "Jet Smart",
    "FO": "Flybondi"
}

# Obtener datos de arribos
obtener_datos_vuelos(url_jujuy, "arribos", "arribos_jujuy.json", "Arribos a Jujuy", mapeo_lineas_aereas)

# Obtener datos de partidas
obtener_datos_vuelos(url_jujuy, "partidas", "partidas_jujuy.json", "Partidas desde Jujuy", mapeo_lineas_aereas)
