import tkinter as tk## crear interfaz grafica
from tkinter.scrolledtext import ScrolledText##creamos los areas de texto
from mip import Model, xsum, maximize, INTEGER ##biblioteca para  resolver problemas de programacion lineal



# Función para resolver el problema de optimización
def solve_problem():
    # Obtener y procesar la entrada del usuario
    input_data = text_area.get("1.0", tk.END).strip().split('\n')
    N = int(input_data[0])
    M = int(input_data[1])
    product = [line.split() for line in input_data[2:2+N]]
    materials = [line.split() for line in input_data[2+N:]]

    # Crear y configurar el modelo de optimización
    m = Model()
    x = [m.add_var(var_type=INTEGER, lb=0) for _ in range(N)]
    revenue = xsum(int(product[i][1]) * x[i] for i in range(N))
    cost = xsum(int(product[i][j+2]) * x[i] * int(materials[j][1]) for i in range(N) for j in range(M))
    m.objective = maximize(revenue - cost)

    # Agregar las restricciones al modelo
    for j in range(M):
        m += xsum(int(product[i][j+2]) * x[i] for i in range(N)) <= int(materials[j][2])

    # Resolver el modelo
    m.optimize()

    # Mostrar los resultados de la solución
    if m.num_solutions:
        solution_text_area.delete("1.0", tk.END)
        solution_text_area.insert("1.0", f"Ganancia total: {m.objective_value}\n")
        for i in range(N):
            solution_text_area.insert(tk.END, f"Produce {x[i].x} unidades de producto {i+1}\n")
    else:
        solution_text_area.delete("1.0", tk.END)
        solution_text_area.insert("1.0", "Solucion no encontrada")


# Función para generar datos para MiniZinc basados en la entrada del usuario
def generate_minizinc_data():
    # Obtener y procesar la entrada del usuario
    input_data = text_area.get("1.0", tk.END).strip().split('\n')
    N = int(input_data[0])  # Número de productos químicos
    M = int(input_data[1])  # Número de materias primas
    
    # Procesar los datos de los productos químicos y materias primas
    products = [line.split() for line in input_data[2:2+N]]
    materials = [line.split() for line in input_data[2+N:]]

    # Crear la cadena de datos para MiniZinc
    minizinc_data = f"N = {N};\nM = {M};\n"
    minizinc_data += f"precio = [{', '.join(product[1] for product in products)}];\n"
    minizinc_data += "costo = [|\n" + " |\n".join(', '.join(chemical[j+2] for j in range(M)) for chemical in products) + " |];\n"
    minizinc_data += f"disponibilidad = [{', '.join(material[2] for material in materials)}];\n"
    minizinc_data += f"costo_material = [{', '.join(material[1] for material in materials)}];\n"
    
    # Mostrar los datos generados en el área de texto de MiniZinc
    minizinc_text_area.delete("1.0", tk.END)
    minizinc_text_area.insert("1.0", minizinc_data)

# Configuración de la ventana principal de la interfaz gráfica
root = tk.Tk()
root.title("Optimization Solver")

# Crear y configurar los widgets de la interfaz
tk.Label(root, text="Ingrese tus datos:").pack()
text_area = ScrolledText(root, height=10)
text_area.pack()

solve_button = tk.Button(root, text="Solucionar problema", command=solve_problem)
solve_button.pack()

solution_text_area = ScrolledText(root, height=10)
solution_text_area.pack()

tk.Label(root, text="Datos MiniZinc:").pack()
minizinc_text_area = ScrolledText(root, height=10)
minizinc_text_area.pack()

generate_button = tk.Button(root, text="Generar datos MiniZinc ", command=generate_minizinc_data)
generate_button.pack()

# Iniciar la aplicación
root.mainloop()
