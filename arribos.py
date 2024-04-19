import requests
from bs4 import BeautifulSoup
import json

# URL de la página web
url = "https://www.aeropuertosargentina.com/jujuy"

# Diccionario de mapeo de códigos de línea aérea a nombres de aerolíneas
mapeo_lineas_aereas = {
    "AR": "Aerolineas Argentinas",
    "WJ": "Jet Smart",
    "FO": "Flybondi"
}

# Lista para almacenar los datos de arribos
datos_arribos = []

# Realiza una solicitud HTTP GET para obtener el contenido de la página
response = requests.get(url)

# Verifica si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Obtiene el contenido HTML de la página
    html = response.text

    # Parsea el contenido HTML
    soup = BeautifulSoup(html, "html.parser")

    # Encuentra el div de arribos por su id
    div_arribos = soup.find("div", {"id": "arribos"})

    # Verifica si se encontró el div de arribos
    if div_arribos:
        # Busca la tabla de arribos dentro del div
        tabla_arribos = div_arribos.find("table", {"class": "scrollvuelos-main"})

        # Verifica si la tabla de arribos se encontró
        if tabla_arribos:
            # Encuentra todas las filas de la tabla de arribos
            filas = tabla_arribos.find_all("tr", {"class": "popup"})

            # Verifica si se encontraron filas
            if filas:
                # Itera a través de las filas de la tabla
                for fila in filas:
                    hora = fila.find("td", {"class": "hora stda"}).text.strip()
                    vuelo = fila.find("td", {"class": "vuelo"}).text.strip()
                    codigo_linea_aerea = vuelo.split()[0]  # Obtiene el código de línea aérea del número de vuelo

                    # Busca el código en el diccionario de mapeo
                    if codigo_linea_aerea in mapeo_lineas_aereas:
                        linea_aerea = mapeo_lineas_aereas[codigo_linea_aerea]
                    else:
                        linea_aerea = "Desconocida"  # En caso de código de línea aérea desconocido

                    origen = fila.find("td", {"class": "ciudad"}).text.strip()
                    
                    # Verifica si se encontró el elemento terminal
                    terminal_elem = fila.find("td", {"class": "termsec terminal"})
                    if terminal_elem:
                        terminal = terminal_elem.text.strip()
                    else:
                        terminal = "No disponible"

                    estima = fila.find("td", {"class": "estima"}).text.strip()
                    estado = fila.find("td", {"class": "status"}).find("div", {"class": "statusText"}).text.strip()

                    # Crea un diccionario con los datos y agrégalo a la lista
                    datos_arribos.append({
                        "Hora": hora,
                        "Vuelo": vuelo,
                        "Linea Aerea": linea_aerea,
                        "Ciudad": origen,
                        "Estima": estima,
                        "Terminal": terminal,
                        "Estado": estado
                    })

                # Crea un diccionario con el título y los datos
                arribos_dict = {
                    "Titulo": "Arribos a Jujuy",
                    "Datos": datos_arribos
                }

                # Escribe los datos en un archivo JSON
                with open(r"D:\Proyectos\VUELOS\arribos_jujuy.json", "w", encoding="utf-8") as json_file:
                    json.dump(arribos_dict, json_file, ensure_ascii=False, indent=4)

                print("Los datos de arribos se han guardado en arribos_jujuy.json con el titulo 'Arribos a Jujuy'.")
            else:
                print("No se encontraron filas en la tabla de arribos.")
        else:
            print("No se encontro la tabla de arribos dentro del div en la pagina web.")
    else:
        print("No se encontro el div de arribos en la pagina web.")
else:
    print("La solicitud HTTP no fue exitosa. Verifica la URL o la conexion a Internet.")
