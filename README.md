# Optimistic Assignment Pessimistic Selection (OAPS) Boolean SAT-solver
This algorithm follows the DPLL method of SAT solving.

## Optimistic Assignment
Like Chaff’s VSIDS SAT solver, variable $x_i$ will be assigned to be True or False so that we can maximize the number of clauses that are satisfied (accounting for all previous assignments)
Thus we heuristically assign truth value to x_i in order to maximize our chance that we get a solution to the SAT problem. In this sense, our assignment is optimisitc.

## Pessimistic Selection
### Sketchy Description
This is where our algorithm differs from other algorithms. When deciding next variable to choose from, we seek for variable that will give us trouble.
Let us take a look at clauses that are still active (not yet satisfied based on previous assignments). Suppose that there is an active clause that only depends on $x_i$. 
Then $x_i$ will give us most trouble in the sense that there is only one allowed assignment to $x_i$. When we pessimistically choose variables, we aim to maximize the number of clauses where all of the variables in question are assigned. 
### Formal Algorithm
Let $N<sub>i,k</sub>$ be number of active clauses that has $k$ variables that haven't been assigned yet and contains $x_i$ (or its negation).
$x_i$ with the highest value for $N<sub>i,1</sub>$ will be chosen. Ties will be broken with $N<sub>i,2</sub>$, $N<sub>i,3</sub>$ ... and so forth. 
(We could also come up with a score that is a function of these variables but preliminary experiment shows tie breaker system works best)
### Intuitive Argument for Why Pessimistic Selection Help Performance
Pessimistic variable selection allows us to resolve active clauses that has very few unassigned variables. These type of clauses are more "urgent" since there is less opportunity for these clauses to be satisfied later on.
Also, clauses that are left over are the ones that are most "independent" of variables we have already assigned to.
### Probability Argument
Suppose that we have $k$ clauses of length $l_1, ..., l_k$. Then what is the probability of a random assignment of all variables satisfying all clauses? 
Well, assuming independence, we get the approximation of $\prod_i^k \frac{2^l_i - 1}{2^l_i}$. By using pessimistic selection, we reduce the number of active clauses with small number of variables.
In fact, Chaff's selection algorithm is also an approximation of branch to a path that is most likely to get a solution.
Wait... why not just approximate probability...?
