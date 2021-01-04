import numpy as np
import matplotlib.pyplot as plt

n_clauses = 10
n_vars = 10

class Clause:
    def __init__(self, variables, negs):
        # TODO check for repeated variable
        self.literals = {var : neg for var, neg in zip(variables, negs)}

    # returns True if satified
    # second arg returns implication
    # when implication given, still considered unsatisfied
    def assign(self, var, value):
        if var not in self.literals:
            return False, None

        if self.literals[var] ^ value:
            # we are satisfied!
            self.literals = set([])
            return True, None

        self.literals.remove(var)

        if len(self.literals) == 1:
            # We have an implication
            var, neg = self.literals.items()[0]
            return False, (var, True ^ neg)

        return False, None

    # True if ran out of active literals
    def UNSAT(self):
        return len(self.literals) == 0

    # log probability of this clause being satisfied (given everything independent)
    def log_prob(self, var, value):
        if var not in self.literals:
            num_possibilities = 2 ** len(self.literals)
            return np.log( (num_possibilities - 1) / num_possibilities)

        if self.literal[var] ^ value:
            # satified !
            return 0
        else:
            # can't be satisfied !
            return -np.inf
        



def gen_clauses(n_clauses):
    # TODO implement!
    return None

clauses = []

# TODO get log prob based on implication as well...?
def get_log_prob(var, value):
    log_prob = 0
    for clause in clauses:
        clause_log_prob = clause.log_prob(var, value)
        if clause_log_prob == -np.inf:
            return -np.inf

        log_prob += clause_log_prob

    return log_prob

unassigned_vars = set([])

# computes the variable, and the assignment to go for
def get_branch(unassigned_vars):
    max_log_prob = -np.inf
    max_assignment = (None, None)
    for var in unassigned_vars:
        for value in [True, False]:
            log_prob = get_log_prob(var, value)
            if log_prob > max_log_prob:
                max_log_prob = log_prob
                max_assignment = (var, value)


    if max_assignment[0] == None:
        raise "UNSAT"

    return max_assignment

#returns processed clauses and False if contradiction
def process_clauses(clauses, var, value):
    processed_clauses = []
    implications = []

    for clause in clauses:
        # will throw exception if clause can not be assigned!
        satisfied, implication = clause.assign(var, value)
        if clause.UNSAT():
            return [], False

        if implication != None:
            implications.append(implication)

        if not satisfied:
            processed_clauses.append(clause)

    # if we have implications, we need to apply them again
    for implication in implications:
        processed_clauses, satisfiable = process_clauses(processed_clauses, var, value)
        if not satisfiable:
            return [], False

    return [], False

# copy the clauses and only keep active ones
def do_recursion(clauses, unused_var):
    if len(clauses) == 0:
        return True

    if len(unused_var) == 0:
        
    var, value = get_branch(clauses, unused_var)
    unused_var.remove(var)

    # because process_clauses modifies input, we need to save the clauses
    processed_clauses, satisfiable = process_clauses(clauses.copy(), var, value)

    if satisfiable:
        if do_recursion(processed_clauses, unused_var):
            return True

    value = True ^ value # since previous value didn't work, we need to flip it
    # Because we can't back propogate anymore, we don't need to save the clauses
    processed_clauses, satisfiable = process_clauses(clauses, var, value)
    if satisfiable:
        if do_recursion(clauses, var, value):
            return True

    return False
