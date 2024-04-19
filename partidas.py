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

# Lista para almacenar los datos de partidas
datos_partidas = []

# Realiza una solicitud HTTP GET para obtener el contenido de la página
response = requests.get(url)

# Verifica si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Obtiene el contenido HTML de la página
    html = response.text

    # Parsea el contenido HTML
    soup = BeautifulSoup(html, "html.parser")

    # Encuentra el div de partidas por su id
    div_partidas = soup.find("div", {"id": "partidas"})

    # Verifica si se encontró el div de partidas
    if div_partidas:
        # Busca la tabla de partidas dentro del div
        tabla_partidas = div_partidas.find("table", {"class": "scrollvuelos-main"})

        # Verifica si la tabla de partidas se encontró
        if tabla_partidas:
            # Encuentra todas las filas de la tabla de partidas
            filas = tabla_partidas.find_all("tr", {"class": "popup"})

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

                    destino = fila.find("td", {"class": "ciudad"}).text.strip()
                    
                    # Verifica si se encontró el elemento terminal
                    terminal_elem = fila.find("td", {"class": "termsec terminal"})
                    if terminal_elem:
                        terminal = terminal_elem.text.strip()
                    else:
                        terminal = "No disponible"

                    estima = fila.find("td", {"class": "estima"}).text.strip()
                    estado = fila.find("td", {"class": "status"}).find("div", {"class": "statusText"}).text.strip()

                    # Crea un diccionario con los datos y agrégalo a la lista
                    datos_partidas.append({
                        "Hora": hora,
                        "Vuelo": vuelo,
                        "Linea Aerea": linea_aerea,
                        "Destino": destino,
                        "Estima": estima,
                        "Terminal": terminal,
                        "Estado": estado
                    })

                # Crea un diccionario con el título y los datos
                partidas_dict = {
                    "Titulo": "Partidas desde Jujuy",
                    "Datos": datos_partidas
                }

                # Escribe los datos en un archivo JSON
                with open(r"D:\Proyectos\VUELOS\partidas_jujuy.json", "w", encoding="utf-8") as json_file:
                    json.dump(partidas_dict, json_file, ensure_ascii=False, indent=4)


                print("Los datos de partidas se han guardado en partidas_jujuy.json con el titulo 'Partidas desde Jujuy'.")
            else:
                print("No se encontraron filas en la tabla de partidas.")
        else:
            print("No se encontro la tabla de partidas dentro del div en la pagina web.")
    else:
        print("No se encontro el div de partidas en la pagina web.")
else:
    print("La solicitud HTTP no fue exitosa. Verifica la URL o la conexion a Internet.")
