# Hint: from collections import deque
from Interface import *
from collections import deque


# = = = = = = = QUESTION 1  = = = = = = = #


def consistent(assignment, csp, var, value) :
    """
    Checks if a value assigned to a variable is consistent with all binary constraints in a problem.
    Do not assign value to var.
    Only check if this value would be consistent or not.
    If the other variable for a constraint is not assigned,
    then the new value is consistent with the constraint.

    Args:
        assignment (Assignment): the partial assignment
        csp (ConstraintSatisfactionProblem): the problem definition
        var (string): the variable that would be assigned
        value (value): the value that would be assigned to the variable
    Returns:
        boolean
        True if the value would be consistent with all currently assigned values, False otherwise
    """
    # TODO: Question 1
    allbinaryConstraints = csp.binaryConstraints
    for binaryConstraints in allbinaryConstraints :
        if binaryConstraints.affects(var) :
            otherVariable = binaryConstraints.otherVariable(var)
            otherValue = assignment.assignedValues[otherVariable]
            if not binaryConstraints.isSatisfied(value, otherValue) :
                return False
    return True


def recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod) :
    """
    Recursive backtracking algorithm.
    A new assignment should not be created.
    The assignment passed in should have its domains updated with inferences.
    In the case that a recursive call returns failure or a variable assignment is incorrect,
    the inferences made along the way should be reversed.
    See maintainArcConsistency and forwardChecking for the format of inferences.

    Examples of the functions to be passed in:
    orderValuesMethod: orderValues, leastConstrainingValuesHeuristic
    selectVariableMethod: chooseFirstVariable, minimumRemainingValuesHeuristic
    inferenceMethod: noInferences, maintainArcConsistency, forwardChecking

    Args:
        assignment (Assignment): a partial assignment to expand upon
        csp (ConstraintSatisfactionProblem): the problem definition
        orderValuesMethod (function<assignment, csp, variable> returns list<value>):
            a function to decide the next value to try
        selectVariableMethod (function<assignment, csp> returns variable):
            a function to decide which variable to assign next
        inferenceMethod (function<assignment, csp, variable, value> returns set<variable, value>):
            a function to specify what type of inferences to use
    Returns:
        Assignment
        A completed and consistent assignment. None if no solution exists.
    """
    # TODO: Question 1
    # if assignment.isComplete():
    #     return assignment
    # var = selectVariableMethod(assignment, csp)
    # if var==None:
    #     return None
    # for value in orderValuesMethod(assignment, csp, var):
    #     if consistent(assignment, csp, var, value):
    #         assignment.assignedValues[var] = value
    #     result = recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod)
    #     if result != None:
    #         return result
    #     assignment.assignedValues[var] = None
    # return None
    if assignment.isComplete() :
        return assignment
    var = selectVariableMethod(assignment, csp)
    if var == None :
        return None
    for value in orderValuesMethod(assignment, csp, var) :
        if consistent(assignment, csp, var, value) :
            assignment.assignedValues[var] = value
            inferences = inferenceMethod(assignment, csp, var, value)
            if inferences is not None :
                result = recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod,
                                               inferenceMethod)
                if result is not None :
                    return result
                # add inferences to assignment ??
                if inferences :
                    for inference in inferences :
                        assignment.varDomains[inference[0]].add(inference[1])
        assignment.assignedValues[var] = None
    return None


def eliminateUnaryConstraints(assignment, csp) :
    """
    Uses unary constraints to eleminate values from an assignment.

    Args:
        assignment (Assignment): a partial assignment to expand upon
        csp (ConstraintSatisfactionProblem): the problem definition
    Returns:
        Assignment
        An assignment with domains restricted by unary constraints. None if no solution exists.
    """
    domains = assignment.varDomains
    for var in domains :
        for constraint in (c for c in csp.unaryConstraints if c.affects(var)) :
            for value in (v for v in list(domains[var]) if not constraint.isSatisfied(v)) :
                domains[var].remove(value)
                # Failure due to invalid assignment
                if len(domains[var]) == 0 :
                    return None
    return assignment


def chooseFirstVariable(assignment, csp) :
    """
    Trivial method for choosing the next variable to assign.
    Uses no heuristics.
    """
    for var in csp.varDomains :
        if not assignment.isAssigned(var) :
            return var


# = = = = = = = QUESTION 2  = = = = = = = #


def minimumRemainingValuesHeuristic(assignment, csp) :
    """
    Selects the next variable to try to give a value to in an assignment.
    Uses minimum remaining values heuristic to pick a variable. Use degree heuristic for breaking ties.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
    Returns:
        the next variable to assign
    """
    nextVar = None
    domains = assignment.varDomains

    # TODO: Question 2
    next = (None, float('inf'))  # a tuple of (var,DomainSize)
    for var in domains :
        if not assignment.isAssigned(var) :  # an unassigned var
            if len(domains[var]) < next[1] :
                next = (var, len(domains[var]))
    return next[0]


def orderValues(assignment, csp, var) :
    """
    Trivial method for ordering values to assign.
    Uses no heuristics.
    """
    return list(assignment.varDomains[var])


# = = = = = = = QUESTION 3  = = = = = = = #


def leastConstrainingValuesHeuristic(assignment, csp, var) :
    """
    Creates an ordered list of the remaining values left for a given variable.
    Values should be attempted in the order returned.
    The least constraining value should be at the front of the list.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
        var (string): the variable to be assigned the values
    Returns:
        list<values>
        a list of the possible values ordered by the least constraining value heuristic
    """
    # TODO: Question 3
    orderTuple = []
    for value in assignment.varDomains[var] :
        cnt = 0
        for binaryConstraints in csp.binaryConstraints :
            if binaryConstraints.affects(var) :
                otherVariable = binaryConstraints.otherVariable(var)
                for othervalue in assignment.varDomains[otherVariable] :
                    if not binaryConstraints.isSatisfied(value, othervalue) :
                        cnt += 1
        orderTuple.append((cnt, value))
    orderTuple.sort()  # ascending order
    orderList = [tuple[1] for tuple in orderTuple]
    return orderList


def noInferences(assignment, csp, var, value) :
    """
    Trivial method for making no inferences.
    """
    return set([])


# = = = = = = = QUESTION 4  = = = = = = = #


def forwardChecking(assignment, csp, var, value) :
    """
    Implements the forward checking algorithm.
    Each inference should take the form of (variable, value)
    where the value is being removed from the domain of variable.
    This format is important so that the inferences can be reversed
    if they result in a conflicting partial assignment.
    If the algorithm reveals an inconsistency,
    any inferences made should be reversed before ending the function.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
        var (string): the variable that has just been assigned a value
        value (string): the value that has just been assigned
    Returns:
        set< tuple<variable, value> >
        the inferences made in this call or None if inconsistent assignment
    """
    inferences = set([])

    # TODO: Question 4
    if not consistent(assignment, csp, var, value) :
        return None
    for binaryConstraint in csp.binaryConstraints :
        if binaryConstraint.affects(var) :
            otherVariable = binaryConstraint.otherVariable(var)
            if not assignment.isAssigned(otherVariable) :
                inconValue = 0
                for otherValue in assignment.varDomains[otherVariable] :
                    if not binaryConstraint.isSatisfied(value, otherValue) :
                        inferences.add((otherVariable, otherValue))
                        inconValue += 1
                if inconValue == len(assignment.varDomains[otherVariable]) :
                    return None
    for tuple in inferences :
        assignment.varDomains[tuple[0]].remove(tuple[1])
    return inferences


# = = = = = = = QUESTION 5  = = = = = = = #


def revise(assignment, csp, var1, var2, constraint) :
    """
    Helper function to maintainArcConsistency and AC3.
    Remove values from var2 domain if constraint cannot be satisfied.
    Each inference should take the form of (variable, value)
    where the value is being removed from the domain of variable.
    This format is important so that the inferences can be reversed
    if they result in a conflicting partial assignment.
    If the algorithm reveals an inconsistency,
    any inferences made should be reversed before ending the function.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
        var1 (string): the variable with consistent values
        var2 (string): the variable that should have inconsistent values removed
        constraint (BinaryConstraint): the constraint connecting var1 and var2
    Returns:
        set<tuple<variable, value>>
        the inferences made in this call or None if inconsistent assignment
    """
    inferences = set([])

    # TODO: Question 5
    cntvar2 = 0
    for value in assignment.varDomains[var2] :
        cnt = 0
        for valuey in assignment.varDomains[var1] :
            if constraint.isSatisfied(value, valuey) :
                break
            cnt += 1
        if cnt == len(assignment.varDomains[var1]) :  # no value of var1 can consist
            # assignment.varDomains[var2].remove(value)
            inferences.add((var2, value))
            cntvar2 += 1
    if cntvar2 == len(assignment.varDomains[var2]) :
        # if no value in var2 left, then reverse and return None
        return None
    for tuple in inferences :
        assignment.varDomains[tuple[0]].remove(tuple[1])
    return inferences


def maintainArcConsistency(assignment, csp, var, value) :
    """
    Implements the maintaining arc consistency algorithm.
    Inferences take the form of (variable, value)
    where the value is being removed from the domain of variable.
    This format is important so that the inferences can be reversed
    if they result in a conflicting partial assignment.
    If the algorithm reveals an inconsistency,
    and inferences made should be reversed before ending the function.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
        var (string): the variable that has just been assigned a value
        value (string): the value that has just been assigned
    Returns:
        set<<variable, value>>
        the inferences made in this call or None if inconsistent assignment
    """
    inferences = set([])
    domains = assignment.varDomains

    # TODO: Question 5
    #  Hint: implement revise first and use it as a helper function"""
    # init all the arcs
    queue = deque()

    for binaryConstraint in csp.binaryConstraints :
        if binaryConstraint.affects(var) :
            otherVariable = binaryConstraint.otherVariable(var)
            if not assignment.isAssigned(otherVariable) :
                queue.append((binaryConstraint, var, otherVariable))

    while queue.__len__() != 0 :
        constraint, var1, var2 = queue.pop()
        # var1=constraint.var1
        # var2=constraint.var2
        # cannot write like this! lost the order of var1 and var2
        revisedInference = revise(assignment, csp, var1, var2, constraint)
        if revisedInference is None :
            for tuple in inferences :
                assignment.varDomains[tuple[0]].add(tuple[1])
            return False
        inferences = inferences.union(revisedInference)
        for inference in revisedInference :
            for binaryConstraint in csp.binaryConstraints :
                if binaryConstraint.affects(inference[0]) :#and binaryConstraint != constraint :
                    otherVariable = binaryConstraint.otherVariable(var)
                    if not assignment.isAssigned(otherVariable) :
                        queue.append((binaryConstraint, inference[0], binaryConstraint.otherVariable(inference[0])))

    return inferences

# = = = = = = = QUESTION 6  = = = = = = = #


def AC3(assignment, csp) :
    """
    AC3 algorithm for constraint propagation.
    Used as a pre-processing step to reduce the problem
    before running recursive backtracking.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
    Returns:
        Assignment
        the updated assignment after inferences are made or None if an inconsistent assignment
    """
    inferences = set([])

    # TODO: Question 6
    #  Hint: implement revise first and use it as a helper function"""
    queue = deque()

    for var in csp.varDomains:
        for binaryConstraint in csp.binaryConstraints :
            if binaryConstraint.affects(var) :
                otherVariable = binaryConstraint.otherVariable(var)
                #if not assignment.isAssigned(otherVariable) :
                queue.append((binaryConstraint, var, otherVariable))

    while queue.__len__() != 0 :
        constraint, var1, var2 = queue.pop()
        # var1=constraint.var1
        # var2=constraint.var2
        # cannot write like this! lost the order of var1 and var2
        revisedInference = revise(assignment, csp, var1, var2, constraint)
        if revisedInference is None :
            for tuple in inferences :
                assignment.varDomains[tuple[0]].add(tuple[1])
            return None
        if len(revisedInference)>0: #necessary! but don't know why! fuck!
            inferences = inferences.union(revisedInference)
            # for inference in revisedInference :
            #     for binaryConstraint in csp.binaryConstraints :
            #         if binaryConstraint.affects(inference[0]) and binaryConstraint != constraint :
            #             otherVariable = binaryConstraint.otherVariable(inference[0])
            #             if not assignment.isAssigned(otherVariable) :
            #                 queue.append((binaryConstraint, inference[0], binaryConstraint.otherVariable(inference[0])))
            for binaryConstraint in csp.binaryConstraints :
                if binaryConstraint.affects(var2) :#and binaryConstraint != constraint :
                    otherVariable = binaryConstraint.otherVariable(var2)
                    if not assignment.isAssigned(otherVariable) :
                        queue.append((binaryConstraint, var2, otherVariable))
    # for tuple in inferences:
    #     assignment.varDomains[tuple[0]].remove(tuple[1])
    return assignment



def solve(csp, orderValuesMethod=leastConstrainingValuesHeuristic,
          selectVariableMethod=minimumRemainingValuesHeuristic,
          inferenceMethod=forwardChecking, useAC3=True) :
    """
    Solves a binary constraint satisfaction problem.

    Args:
        csp (ConstraintSatisfactionProblem): a CSP to be solved
        orderValuesMethod (function): a function to decide the next value to try
        selectVariableMethod (function): a function to decide which variable to assign next
        inferenceMethod (function): a function to specify what type of inferences to use
        useAC3 (boolean): specifies whether to use the AC3 pre-processing step or not
    Returns:
        dictionary<string, value>
        A map from variables to their assigned values. None if no solution exists.
    """
    assignment = Assignment(csp)

    assignment = eliminateUnaryConstraints(assignment, csp)
    if assignment is None :
        return assignment

    if useAC3 :
        assignment = AC3(assignment, csp)
        if assignment is None :
            return assignment

    assignment = recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod)
    if assignment is None :
        return assignment

    return assignment.extractSolution()
