import numpy as np
import matplotlib.pyplot as plt
import copy
import sys

n_clauses = 300
n_vars = 100


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
            self.literals = {}
            return True, None

        del self.literals[var]

        if len(self.literals) == 1:
            # We have an implication
            var, neg = list(self.literals.items())[0]
            
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

        if self.literals[var] ^ value:
            # satified !
            return 0
        
        elif (len(self.literals) <= 1):
            # can't be satisfied !
            return -np.inf
        else:
            num_possibilities = 2 ** (len(self.literals) - 1)
            return np.log( (num_possibilities - 1) / num_possibilities)

# TODO get log prob based on implication as well...?
def get_log_prob(clauses, var, value):
    log_prob = 0
    for clause in clauses:
        clause_log_prob = clause.log_prob(var, value)
        if clause_log_prob == -np.inf:
            return -np.inf
        log_prob += clause_log_prob

    return log_prob

# computes the variable, and the assignment to go for
def get_random_branch(clauses, unassigned_vars):
    return np.random.choice(list(unassigned_vars)), np.random.choice([True, False])
    

def get_chaff_branch(clause, unassigned_vars):
    max_count = 0
    max_assignment = (None, None)
    for var in unassigned_vars:
        for value in [True, False]:
            count = 0
            for clause in clauses:
                if var in clause.literals and clause.literals[var] ^ value:
                    count += 1
                    
            if count > max_count:
                max_count = count
                max_assignment = (var, value)
                
    return max_assignment

def get_max_prob_branch(clauses, unassigned_vars):
    max_log_prob = -np.inf
    max_assignment = (None, None)
    min_log_prob = 0
    for var in unassigned_vars:
        for value in [True, False]:
            log_prob = get_log_prob(clauses, var, value)
            #print(log_prob)
            if log_prob > max_log_prob:
                max_log_prob = log_prob
                max_assignment = (var, value)
                
            if log_prob < min_log_prob:
                min_log_prob = log_prob
                
    #print(max_log_prob, min_log_prob, len(clauses) )

    #print(max_log_prob)
    return max_assignment



solution = [None for i in range(n_vars)]
wrong_sol_count = 0

#returns processed clauses and False if contradiction
def process_clauses(clauses, var, value):
    solution[var] = value
    processed_clauses = []
    implications = []

    for clause in clauses:
        # will throw exception if clause can not be assigned!
        satisfied, implication = clause.assign(var, value)

        if implication != None:
            implications.append(implication)

        if not satisfied:
            if clause.UNSAT():
                return [], False
            
            processed_clauses.append(clause) #TODO tab this

    # if we have implications, we need to apply them again
    for implication in implications:
        processed_clauses, satisfiable = process_clauses(processed_clauses, var, value)
        if not satisfiable:
            return [], False

    return processed_clauses, True

# copy the clauses and only keep active ones
def do_recursion(clauses, unused_var, branch_func):
    global wrong_sol_count
    wrong_sol_count += 1
    
    sys.stdout.write('\r')
    sys.stdout.write("%d" % (wrong_sol_count))
    
    if len(clauses) == 0:
        return True

    if len(unused_var) == 0:
        # no more variables but we have un satisfied clauses
        return False
    
    var, value = branch_func(clauses, unused_var)
    if var == None:
        return False
    unused_var.remove(var)

    # because process_clauses modifies input, we need to save the clauses
    processed_clauses, satisfiable = process_clauses(copy.deepcopy(clauses), var, value)
    #print('first satisfiable', satisfiable, len(unused_var))
    if satisfiable:
        if do_recursion(processed_clauses, copy.deepcopy(unused_var), branch_func):
            return True

    value = True ^ value # since previous value didn't work, we need to flip it
    # Because we can't back propogate anymore, we don't need to save the clauses
    processed_clauses, satisfiable = process_clauses(clauses, var, value)
    #print('second satisfiable', satisfiable, len(unused_var))
    if satisfiable:
        if do_recursion(processed_clauses, copy.deepcopy(unused_var), branch_func):
            return True
        
    unused_var.add(var)

    return False

def make_clauses(n_vars, n_clauses):
    clauses = []
    for i in range(n_clauses):
        clause_size = np.random.choice(np.arange(3, 4))
        clauses.append(Clause(np.random.permutation(n_vars)[:clause_size], 
                              np.random.choice([True, False], clause_size)))
        
    return clauses


def check_sol(SAT, clauses):
    if not SAT:
        # Can't really check...
        return True
    
    for clause in clauses:
        clause_sat = False
        for var, neg in clause.literals.items():
            if solution[var] != None and solution[var] ^ neg:
                clause_sat = True
                break
                
        if not clause_sat:
            return False
        
    return True

clauses = make_clauses(n_vars, n_clauses)
unused_var = {i for i in range(n_vars)}

def check_branching(name, branch_func):
    global wrong_sol_count
    wrong_sol_count = 0
    SAT = do_recursion(copy.deepcopy(clauses), copy.deepcopy(unused_var), branch_func)
    print(" - num recursion called")
    print(name, SAT, wrong_sol_count)
    if not check_sol(SAT, clauses):
        print(name, 'incorrectly returned SAT')



#check_branching("random", get_random_branch)
check_branching("max_prob", get_max_prob_branch)
check_branching("chaff", get_chaff_branch)
