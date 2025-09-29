"""este codigo de python sirve para exrtraer informacion de un archivo .gb, la informacion que se extrae se presenta en
 un archivo final de formato .tsv, donde estara tabulado por nombre, inicio, final, longitud y producto, este codigo puede ser usado
 en cualquier formato .gb.

 nombre: es el nombre del gen asociado
 inicio: es un numero el cual indica donde inicia la secuencia del gen asociado
 final: es un numero el cual indica donde finaliza la secuencia del gen asociado
 longitud: es un numero el cual indica la longitud del gen asociado
 producto: es la procteina traducida del gen asociado, en algunos casos se tendra proteinas identificadas y otras no.

 Nota: en la columna nombre, se asigna el gen, de no ser un gen identificado en este campo se agrega el tag_id

la extension .gb es un archivo que contiene informacion sobre la secuenciacion del ADN o el ARN de un organismo, este
formato contiene una serie de informacion como, autores, id, fuente, # de referencia, estado de publicacion, nombre
de los genes, ubicacion e.t.c"""

import re
import csv


# defino variables tipo lista, donde se agrega la informacion de interes.
nombre = []
inicio = []
final = []
longitud = []
producto = []


# defino una funcion que usa regex para extraer los datos numericos de interes.
def limpiar(texto: str) -> str:
    """
    Extrae la parte de la cadena que sigue el patrón:
    número..número
    y elimina todo lo demás.
    MODIFICACIÓN: Toma solo el primer rango cuando hay múltiples rangos
    """
    # Buscar el primer patrón de número..número
    patron = r'(\d+)\.\.(\d+)'
    resultado = re.search(patron, texto)
    if resultado:
        inicio = resultado.group(1)
        final = resultado.group(2)
        return f"{inicio}..{final}"
    return None  # Si no encuentra nada

# dentro de las comillas escriba el nombre de su archivo .gb
gene_ecoligb = "aureus.gb"

# se abre el archivo.
with open(gene_ecoligb) as file:
    #declaro esta variables como vacias para ir dando asignacion a medida que el codigo valla leyendo el archivo.
    gene = None
    locus = None
    product = None
    es_tRNA = False  # ← NUEVA VARIABLE PARA IDENTIFICAR tRNA

    for line in file:
        #limpia cualquier cosa antes y despues de la linea.
        line = line.strip()

        # ← NUEVO: Identificar si es un tRNA y saltarse todo el bloque
        if line.startswith("tRNA"):
            es_tRNA = True
            continue  # Saltar esta línea y las siguientes del tRNA

        # ← NUEVO: Si estamos en un bloque tRNA y encontramos otro tipo, salir del modo tRNA
        if es_tRNA and (line.startswith("gene") or line.startswith("CDS") or line.startswith("ORIGIN")):
            es_tRNA = False

        # ← NUEVO: Si estamos en modo tRNA, saltar todas las líneas
        if es_tRNA:
            continue

        # condicional que identifica donde esta la informacion de la ubicacion del gen.
        if "gene  " in line:
            line_limpia = limpiar(line)
            if line_limpia:
                dato_inicio = line_limpia.split("..")[0]
                dato_final = line_limpia.split("..")[1]
                # agrego las variables de dato_inicio/final a las listas de inicio y final respectivamente
                inicio.append(dato_inicio)
                final.append(dato_final)

        """ esta serie de condicionales se usa para identificar la informacion de interes, en este caso el nombre del 
        gen se identifica con /gene=, si no tiene nombre identifica el locus como locus_tag y identifica el producto
        del gen como /product= todo esto es devido al formato .gb"""

        if "/gene=" in line:
            gene = line.replace("/gene=","").replace('"',"")

        if "/locus_tag=" in line:
            locus = line.replace("/locus_tag=","").replace('"',"")

        if "/product=" in line:
            product = line.replace("/product=","").replace('"',"")
            producto.append(product)   # siempre lo guardamos

        # cuando termina un bloque de CDS o gene
        if line.startswith("/translation=") or line.startswith("ORIGIN"):
            if gene:
                nombre.append(gene)      # prioridad 1
            elif locus:
                nombre.append(locus)     # prioridad 2
            # reiniciamos para el siguiente bloque
            gene = None
            locus = None
            product = None

# Converti las lista inicio y final en int.
inicio = list(map(int, inicio))
final = list(map(int, final))

# se lee dato a dato de las lista inicio y final y se opera la resta.
for i in range(len(inicio)):
    longitud.append(final[i] - inicio[i])

# Guardar los resultados en un archivo TSV
with open("resultado.tsv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter="\t")
    # encabezado
    writer.writerow(["nombre", "inicio", "final", "longitud", "producto"])
    # escribir filas (usar zip para recorrer en paralelo)
    for n, i, fi, l, p in zip(nombre, inicio, final, longitud, producto):
        writer.writerow([n, i, fi, l, p])







