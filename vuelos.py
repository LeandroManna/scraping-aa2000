import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def extraer_datos(url, tipo):
    # Diccionario de mapeo de códigos de línea aérea a nombres de aerolíneas
    mapeo_lineas_aereas = {
        "AR": "Aerolineas Argentinas",
        "WJ": "Jet Smart",
        "FO": "Flybondi"
    }

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

        # Encuentra el div de arribos o partidas por su id
        if tipo == "arribos":
            div_vuelos = soup.find("div", {"id": "arribos"})
            titulo = "Arribos a Jujuy"
            archivo = "arribos_jujuy.json"
        elif tipo == "partidas":
            div_vuelos = soup.find("div", {"id": "partidas"})
            titulo = "Partidas desde Jujuy"
            archivo = "partidas_jujuy.json"

        # Verifica si se encontró el div de vuelos
        if div_vuelos:
            # Busca la tabla de vuelos dentro del div
            tabla_vuelos = div_vuelos.find("table", {"class": "scrollvuelos-main"})

            # Verifica si la tabla de vuelos se encontró
            if tabla_vuelos:
                # Encuentra todas las filas de la tabla de vuelos
                filas = tabla_vuelos.find_all("tr", {"class": "popup"})

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

                        if tipo == "arribos":
                            origen_destino = fila.find("td", {"class": "ciudad"}).text.strip()
                        elif tipo == "partidas":
                            origen_destino = fila.find("td", {"class": "ciudad"}).text.strip()

                        # Verifica si se encontró el elemento terminal
                        terminal_elem = fila.find("td", {"class": "termsec terminal"})
                        if terminal_elem:
                            terminal = terminal_elem.text.strip()
                        else:
                            terminal = "No disponible"

                        estima = fila.find("td", {"class": "estima"}).text.strip()
                        estado = fila.find("td", {"class": "status"}).find("div", {"class": "statusText"}).text.strip()

                        # Crea un diccionario con los datos y agrégalo a la lista
                        datos_vuelos.append({
                            "Hora": hora,
                            "Vuelo": vuelo,
                            "Linea Aerea": linea_aerea,
                            "Ciudad": origen_destino,
                            "Estima": estima,
                            "Terminal": terminal,
                            "Estado": estado
                        })

                    # Obtiene la fecha y hora de la última modificación del archivo
                    fecha_modificacion = datetime.fromtimestamp(os.path.getmtime(archivo)).strftime('%d/%m/%Y %H:%M')

                    # Crea un diccionario con el título, la fecha de modificación y los datos
                    vuelos_dict = {
                        "Titulo": titulo,
                        "Fecha_Modificacion": fecha_modificacion,
                        "Datos": datos_vuelos
                    }

                    # Escribe los datos en un archivo JSON
                    with open(f"D:/Proyectos/VUELOS/{archivo}", "w", encoding="utf-8") as json_file:
                        json.dump(vuelos_dict, json_file, ensure_ascii=False, indent=4)

                    print(f"Los datos de {tipo} se han guardado en {archivo} con el titulo '{titulo}'.")
                    print(f"Fecha y hora de la última modificación de {archivo}: {fecha_modificacion}")
                else:
                    print(f"No se encontraron filas en la tabla de {tipo}.")
            else:
                print(f"No se encontro la tabla de {tipo} dentro del div en la pagina web.")
        else:
            print(f"No se encontro el div de {tipo} en la pagina web.")
    else:
        print("La solicitud HTTP no fue exitosa. Verifica la URL o la conexion a Internet.")

# Ejemplo de uso
extraer_datos("https://www.aeropuertosargentina.com/jujuy", "arribos")
extraer_datos("https://www.aeropuertosargentina.com/jujuy", "partidas")
