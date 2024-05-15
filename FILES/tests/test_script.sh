#!/bin/bash

# Verificar si la carpeta LOGS existe, si no, crearla
if [ ! -d "LOGS" ]; then
    mkdir "LOGS"
fi

# Combinaciones de flags
flags=("" "--header" "--fldata" "--header --fldata" "-d ';'" "-d ','" "-d ';' --header" "-d ',' --header" "-d ';' --fldata" "-d ',' --fldata" "-d ';' --header --fldata" "-d ',' --header --fldata")

# Indices a ingresar
indices=("0" "1" "2" "q")

# Ruta del archivo de salida (relativa a la carpeta principal del proyecto)
output_file="LOGS/output.txt"

# Obtener el nombre del archivo de script y el archivo CSV desde los argumentos
file_name="script_csv.py"
csv_file=""
for arg in "$@"; do
    if [[ "$arg" == --file_name=* ]]; then
        file_name="${arg#--file_name=}"
    elif [[ "$arg" == --csv-file=* ]]; then
        csv_file="${arg#--csv-file=}"
    fi
done

# Iterar sobre las combinaciones de flags
for i in "${!flags[@]}"; do
    flag_combination="${flags[$i]}"

    # Escribir el separador y el encabezado de prueba
    printf "\n------------------------\nEjecutando %s con flags: %s y archivo CSV: %s\n------------------------\n" "$file_name" "$flag_combination" "$csv_file" >> "$output_file"

    # Ejecutar el script con las flags correspondientes
    (
        for index in "${indices[@]}"; do
            echo "$index"
        done
    ) | python "$file_name" --csv-file "$csv_file" $flag_combination >> "$output_file" 2>&1
done