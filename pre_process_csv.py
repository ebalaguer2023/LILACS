import re
import os

# Archivo inicial
base_file = 'C:/LILACS_17_06_2025.csv'  # Entrada original (puede estar en otra ruta)

# Lista de reemplazos (patrón, reemplazo)
replacements = [
    (r'""""', '|'),
    (r'"""', '|'),
    (r'""', '|')
]

def replaceregexp(fin_path, fout_path, regexp, regnew):
    count = 0
    with open(fin_path, "rt", encoding="utf-8") as fin, \
         open(fout_path, "w", encoding="utf-8") as fout:
        
        for line in fin:
            if re.search(regexp, line):
                print(count, ' ', line)
                count += 1
                line = re.sub(regexp, regnew, line)
                print(line)
            fout.write(line)
    return count

# Proceso en cadena
current_file = base_file
total_replacements = 0

for idx, (pattern, new_val) in enumerate(replacements, start=1):
    # Solo el nombre base, sin ruta
    name, ext = os.path.splitext(os.path.basename(base_file))
    next_file = f"{name}_step{idx}{ext}"  # Guardado en directorio actual
    
    total_replacements += replaceregexp(current_file, next_file, pattern, new_val) 
    if idx>1: 
        os.remove(current_file)
    current_file = next_file  # Para la siguiente iteración
        

print(f"Registros modificados en total: {total_replacements}")
print(f"Archivo final: {current_file}")


