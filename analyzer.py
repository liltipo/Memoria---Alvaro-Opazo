import os
import csv
import ast
import radon.complexity as radon_cc
import radon.metrics as radon_halstead
import radon.raw as radon_raw
from cognitive_complexity.api import get_cognitive_complexity

# Configuración de carpetas
INPUT_FOLDER = "codigos_estudiantes"
OUTPUT_FILE = "resultados_metricas.csv"

class ASTCounter(ast.NodeVisitor):
    """Cuenta estructuras básicas de control para detectar 'parches' o uso de IA (Sintaxis Alienígena)."""
    def __init__(self):
        self.stats = {
            "num_while": 0,
            "num_for": 0,
            "num_if": 0,
            "num_list_comp": 0,
            "num_funciones_propias": 0
        }

    def visit_While(self, node):
        self.stats["num_while"] += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.stats["num_for"] += 1
        self.generic_visit(node)

    def visit_If(self, node):
        self.stats["num_if"] += 1
        self.generic_visit(node)

    def visit_ListComp(self, node):
        self.stats["num_list_comp"] += 1
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        if node.name != "wrapper_student_code": 
            self.stats["num_funciones_propias"] += 1
        self.generic_visit(node)


def analizar_archivo(filepath):
    filename = os.path.basename(filepath)
    
    # 1. Lectura del archivo
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw_code = f.read()
    except Exception as e:
        return {"archivo": filename, "estado": f"Error lectura: {str(e)}", "compila": "N/A"}

    # 2. Envoltura del código (Wrapping) - CORREGIDO: Manejo seguro de líneas vacías
    lineas_indentadas = ["    " + line if line.strip() else "" for line in raw_code.split('\n')]
    wrapped_code = "def wrapper_student_code():\n" + "\n".join(lineas_indentadas)
    
    # Estructura base del resultado
    resultados = {
        "archivo": filename, 
        "estado": "OK",
        "compila": "Sí",
        "LOC": 0,
        "num_while": "N/A",
        "num_for": "N/A",
        "num_if": "N/A",
        "num_list_comp": "N/A",
        "num_funciones_propias": "N/A",
        "McCabe_CC": "N/A",
        "Cognitive_CC": "N/A",
        "Halstead_Vocabulario": "N/A",
        "Halstead_Volumen": "N/A",
        "Halstead_Dificultad": "N/A",
        "Halstead_Esfuerzo": "N/A"
    }
    
    # 3. Líneas de código lógicas (LOC)
    # Funciona estáticamente como texto plano, sobrevive a errores de sintaxis
    try:
        raw_metrics = radon_raw.analyze(raw_code)
        resultados["LOC"] = raw_metrics.lloc
    except:
        pass

    # 4. Validar compilación y extraer métricas del AST
    try:
        tree = ast.parse(wrapped_code)
        
        # Si pasa el parseo, el código COMPILA. 
        counter = ASTCounter()
        counter.visit(tree)
        resultados.update(counter.stats)

        # Métrica Ciclomática (McCabe)
        try:
            blocks = radon_cc.cc_visit(wrapped_code)
            resultados["McCabe_CC"] = sum([b.complexity for b in blocks])
        except:
            resultados["McCabe_CC"] = 0

        # Métrica Cognitiva (Campbell)
        try:
            func_node = tree.body[0] 
            resultados["Cognitive_CC"] = get_cognitive_complexity(func_node)
        except:
            resultados["Cognitive_CC"] = 0

    except SyntaxError:
        # EL CÓDIGO NO COMPILA
        resultados["compila"] = "No"
        resultados["estado"] = "Error de Sintaxis"

    # 5. Métricas de Halstead (Esfuerzo Léxico)
    # Halstead funciona mediante tokens, por lo que a menudo rescata datos incluso si el AST falla.
    try:
        h_report = radon_halstead.h_visit(raw_code)
        resultados["Halstead_Vocabulario"] = h_report[0].vocabulary
        resultados["Halstead_Volumen"] = round(h_report[0].volume, 2)
        resultados["Halstead_Dificultad"] = round(h_report[0].difficulty, 2)
        resultados["Halstead_Esfuerzo"] = round(h_report[0].effort, 2)
    except Exception:
        pass

    return resultados


def main():
    if not os.path.exists(INPUT_FOLDER):
        os.makedirs(INPUT_FOLDER)
        print(f"Carpeta '{INPUT_FOLDER}' creada. Añade tus archivos .py y ejecuta nuevamente.")
        return

    archivos =[f for f in os.listdir(INPUT_FOLDER) if f.endswith(".py")]
    if not archivos:
        print(f"No hay archivos .py para analizar en la carpeta '{INPUT_FOLDER}'.")
        return

    reporte =[]
    print("Iniciando análisis automatizado de código...")
    
    for archivo in archivos:
        path = os.path.join(INPUT_FOLDER, archivo)
        metricas = analizar_archivo(path)
        reporte.append(metricas)
        print(f" -> Procesado: {archivo} | Compila: {metricas['compila']} | Estado: {metricas['estado']}")

    # Exportar a CSV
    if reporte:
        columnas = list(reporte[0].keys())
        
        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=columnas)
            writer.writeheader()
            for fila in reporte:
                writer.writerow({col: fila.get(col, "N/A") for col in columnas})
                
        print(f"\n¡Análisis completado! Resultados guardados en '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    main()