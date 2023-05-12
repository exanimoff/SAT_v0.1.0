from enum import Enum, auto
from time import perf_counter


class RecType(Enum):
    FALSE = auto()
    TRUE = auto()
    BOTH = auto()


## RecType используется для определения типов записей (record types) в NextRec,
# чтобы указать, какие ветви должны быть продолжены в алгоритме DPLL.
## RecType определяет три возможных значения: FALSE, TRUE и BOTH, которые указывают,
# должны ли ветви быть продолжены, только если литерал является ложным, только если он истинен, или в обоих случаях.
## RecType не используется явно где-либо в коде. Однако он используется неявно в методе get_next_rec,
# который возвращает объект NextRec, содержащий литерал и его тип (одно из значений RecType).
## Позже этот объект используется в функции gen_branch, которая определяет,
# какие литералы должны быть добавлены к ветви, в зависимости от типа NextRec.

class NextRec:
    def __init__(self, var, rec_type):
        self.var = var
        self.type = rec_type


## С помощью класса NextRec мы можем получить следующую переменную,
# которая будет использоваться для дальнейшего выполнения алгоритма.


def set_check(c, var_list):
    for c_ in var_list:
        if c == c_:
            return False
    return True


def get_next_rec(clause, vars):
    c = '?'
    clause_vars = []

    for lit in clause:
        clause_vars += lit

    clause_vars = [i.lower() for i in clause_vars]

    for i in range(len(vars)):
        if not set_check(vars[i], clause_vars):
            c = vars[i]
            break

    return NextRec(c, RecType.BOTH)


def gen_branch(clause, next_rec, bool):
    branch = []

    if bool:
        for lit in clause:
            if not set_check(next_rec.var, lit):
                continue
            temp = lit.copy()
            if (biba := next_rec.var.upper()) in temp:
                temp.remove(biba)

            if set_check(temp, branch):
                branch.append(temp)
    else:
        for lit in clause:
            if not set_check(next_rec.var.upper(), lit):
                continue
            temp = lit.copy()
            if (biba := next_rec.var) in temp:
                temp.remove(biba)

            if set_check(temp, branch):
                branch.append(temp)

    return branch


def set_inter(inter, vars, var, bool):
    for i in range(len(vars)):
        if vars[i] == var:
            inter[i] = 1 if bool else 0


def base_dpll(clause, vars, inter):
    if len(clause) == 0:
        with open("output.txt", 'w', encoding='UTF-8') as f:
            f.write(str(vars) + '\n')
            f.write(str(inter) + '\n')
        return True
    else:
        for lit in clause:
            if not lit:
                return False

    next_rec = get_next_rec(clause, vars)

    if next_rec.type == RecType.TRUE or next_rec.type == RecType.BOTH:
        true_branch = gen_branch(clause, next_rec, True)
        set_inter(inter, vars, next_rec.var, True)

        if base_dpll(true_branch, vars, inter):
            return True

    if next_rec.type == RecType.FALSE or next_rec.type == RecType.BOTH:
        false_branch = gen_branch(clause, next_rec, False)
        set_inter(inter, vars, next_rec.var, False)

        if base_dpll(false_branch, vars, inter):
            return True

    return False


def dpll(clause, vars):
    inter = []
    for _ in vars:
        inter.append(-1)
    base_dpll(clause, vars, inter)
    return


def main():
    with open('input.txt', encoding='UTF-8') as f:
        args = f.readline().strip().split()
        g_args = []
        g_vars = []
        for arg in args:
            nums_of_arg = arg.lower().strip().split('x')[1:]
            xes = [c for c in arg if c == 'X' or c == 'x']
            g_args.append([a[0] + a[1] for a in zip(xes, nums_of_arg)])
            g_vars.extend([a[0] + a[1] for a in zip([c.lower() for c in arg if c == 'X' or c == 'x'], nums_of_arg)])
        g_vars = sorted(list(set(g_vars)))
    t = perf_counter()
    dpll(g_args, g_vars)
    print(perf_counter() - t)


if __name__ == '__main__':
    main()
