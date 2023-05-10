from sympy import *
from sympy.logic.boolalg import to_cnf
import random

# Генерация случайного логического выражения
def generate_expression(variables):
    if len(variables) == 1:
        return variables[0]
    op = random.choice(['&', '|', '>>', '<<', '^'])
    if op == '&':
        return And(generate_expression(variables[:len(variables)//2]), generate_expression(variables[len(variables)//2:]))
    elif op == '|':
        return Or(generate_expression(variables[:len(variables)//2]), generate_expression(variables[len(variables)//2:]))
    elif op == '>>':
        return Implies(generate_expression(variables[:len(variables)//2]), generate_expression(variables[len(variables)//2:]))
    elif op == '<<':
        return Implies(generate_expression(variables[len(variables)//2:]), generate_expression(variables[:len(variables)//2]))
    elif op == '^':
        return Xor(generate_expression(variables[:len(variables)//2]), generate_expression(variables[len(variables)//2:]))

# Генерация случайной логической формулы в КНФ
def generate_knf_formula(num_vars, num_clauses, clause_size):
    variables = symbols('a:%d' % num_vars)
    clauses = []
    for _ in range(num_clauses):
        clause = []
        while len(clause) < clause_size:
            var = random.choice(variables)
            if random.random() < 0.5:
                var = Not(var)
            if var not in clause:
                clause.append(var)
        clauses.append(Or(*clause))
    expr = And(*clauses)
    cnf_expr = to_cnf(expr)
    return cnf_expr

# Пример использования
cnf_expr = generate_knf_formula(50, 20, 6)
print(cnf_expr)