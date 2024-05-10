import argparse


def random_header(index):
    return f"h{index+1}"


parser = argparse.ArgumentParser(description='CSV Reader')
parser.add_argument('--header', action='store_true',
                    help='Generate random headers')
parser.add_argument('--fldata', action='store_true',
                    help='The first line contains data')
parser.add_argument('--csv-file', '-f', type=str,
                    required=True, help='Path to the CSV file (e.g., /path/to/file.csv)')
parser.add_argument('--delimiter', '-d', type=str, default=',',
                    help='Delimiter used in the CSV file (default: ,) eg: python script_csv.py --csv-file /ruta/al/archivo.csv --delimiter \';\''
                    )
parser.add_argument('--usage', action='help', help="""The index of the record starts at 0, please enter a number to search for the entered index. If the script is executed without flags, it will assume the first line as the header. If --fldata is used, it will use the first line as the header but retain the row as data, meaning it will be duplicated in the header.""")

args = parser.parse_args()


class CSVObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def read_csv_file(file_path, random_headers, fldata, delimiter):
    objects = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

        if random_headers:
            headers = [random_header(i) for i in range(
                len(lines[0].strip().split(delimiter)))]
            data_lines = lines if fldata else lines[1:]
        else:
            headers = [strip_quotes(field)
                       for field in lines[0].strip().split(delimiter)]
            data_lines = lines[1:] if not fldata else lines

        for line in data_lines:
            values = parse_line(line.strip(), delimiter)
            data = {headers[i]: values[i]
                    for i in range(min(len(headers), len(values)))}
            obj = CSVObject(**data)
            objects.append(obj)

    return objects


def strip_quotes(value):
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    elif value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    else:
        return value


def parse_line(line, delimiter):
    values = []
    current_value = ""
    quote_char = None
    for char in line:
        if char == "'" or char == '"':
            if quote_char is None:
                quote_char = char
            elif quote_char == char:
                quote_char = None
        elif char == delimiter and quote_char is None:
            values.append(current_value)
            current_value = ""
        else:
            current_value += char
    if current_value:
        values.append(current_value)
    return [strip_quotes(value) for value in values]


if __name__ == '__main__':
    args = parser.parse_args()

    csv_file_path = args.csv_file
    csv_objects = read_csv_file(
        csv_file_path, args.header, args.fldata, args.delimiter)

    while True:
        search_index = input(
            "Ingrese el índice del objeto a buscar (q para salir): ")
        if search_index.lower() == 'q':
            break
        try:
            index = int(search_index)
            if index >= len(csv_objects):
                print("Índice fuera de rango.")
            else:
                obj = csv_objects[index]
                print(f"Objeto {index}:")
                for key, value in obj.__dict__.items():
                    print(f"{key}: {value}")
                print()
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número o 'q' para salir.")
