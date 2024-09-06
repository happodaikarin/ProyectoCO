import pulp

#define el problema
prob = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# variables de decision
x = {
    'azul': pulp.LpVariable('x_azul', lowBound=0, cat='Continuous'),
    'amarilla': pulp.LpVariable('x_amarilla', lowBound=0, cat='Continuous'),
    'negra': pulp.LpVariable('x_negra', lowBound=0, cat='Continuous'),
    'blanca': pulp.LpVariable('x_blanca', lowBound=0, cat='Continuous')
}

# precio venta y costos
prices = {'azul': 20000, 'amarilla': 50000, 'negra': 30000, 'blanca': 30000}
costs = {'Materia prima 1': 1000, 'Materia prima 2': 2500, 'Materia prima 3': 4000}
availability = {'Materia prima 1': 300, 'Materia prima 2': 400, 'Materia prima 3': 520}

# materiales prima
requirements = {
    'azul': {'Materia prima 1': 2, 'Materia prima 2': 3, 'Materia prima 3': 9},
    'amarilla': {'Materia prima 1': 3, 'Materia prima 2': 9, 'Materia prima 3': 9},
    'negra': {'Materia prima 1': 2, 'Materia prima 2': 0, 'Materia prima 3': 4},
    'blanca': {'Materia prima 1': 1, 'Materia prima 2': 2, 'Materia prima 3': 0},
}

# funcuin objetivo
prob += pulp.lpSum(
    [prices[color] * x[color] - pulp.lpSum([costs[material] * requirements[color][material] for material in requirements[color]]) * x[color] for color in prices]
), "Total Profit"

# restriccion
for material in availability:
    prob += pulp.lpSum([requirements[color].get(material, 0) * x[color] for color in requirements]) <= availability[material], f"constraint_{material}"

# Solve the problem
prob.solve()

# Print the results
for variable in x.values():
    print(f"{variable.name} = {variable.varValue}")

print(f"Total ganancia: {pulp.value(prob.objective)}")
