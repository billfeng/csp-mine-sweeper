#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          propagator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a dead end has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one remaining variable)
        we look for unary constraints of the csp (constraints whose scope contains
        only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constraints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
         
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''
    
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with 
       only one uninstantiated variable. Remember to keep 
       track of all pruned variable,value pairs and return '''
#IMPLEMENT
    pruned = []
    # keep track of pruned values
    if newVar:
        constraints = csp.get_cons_with_var(newVar)
        # get constraints involving the variable if a variable is given
    else:
        constraints = csp.get_all_cons()
        # get all constraints if no variable is given

    for constraint in constraints:
        if constraint.get_n_unasgn() == 1:
            # iterate through all constraints with only 1 unassigned variable

            variable = constraint.get_unasgn_vars()[0]
            for d in variable.cur_domain():
                # try all the values in the domain of that variable

                variable.assign(d)
                values = []
                for var in constraint.get_scope():
                    values.append(var.get_assigned_value())
                    # fill the list "values" with assigned values of the variables in the scope of the constraint

                if not constraint.check(values):
                    variable.prune_value(d)
                    pruned.append((variable, d))
                    # if these values do not pass the constraint check, prune the assigned value from domain

                variable.unassign() # unassign variable

            if variable.cur_domain_size() == 0:
                return False, pruned
                # return false if nothing is left in domain after the prune

    return True, pruned
    # return true if there's still values left in the domain after all the prunes

def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
#IMPLEMENT
    pruned = []
    if newVar:
        constraints = csp.get_cons_with_var(newVar)
        # get constraints involving the variable if a variable is given
    else:
        constraints = csp.get_all_cons()
        # get all constraints if no variable is given

    while constraints:
        constraint = constraints.pop(0)
        # while the queue still has constraints in it, take one out and work on it

        for variable in constraint.get_scope():
            for d in variable.cur_domain():
                # iterate through all the values in the domain of the variables in the constraint

                if not constraint.has_support(variable, d):
                    variable.prune_value(d)
                    pruned.append((variable,d))
                    # prune the value from domain of variable if it has no support

                    if variable.cur_domain_size() == 0:
                        return False, pruned
                        # return false after the prune if domain becomes empty
                    else:
                        constraints += list(set(csp.get_cons_with_var(variable)) - set(constraints))
                        # otherwise add constraints involving the changed variable to the queue and continue
    return True, pruned
    # return true if supporting tuple exists in all the constraints for the changed variable
