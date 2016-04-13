# -*- coding: utf-8 -*-

""" Wyndor model from Hillier and Hillier *Introduction to Management Science*
  see http://www.ibm.com/developerworks/cloud/library/cl-optimizepythoncloud1/

    # To run this you need pyomo and the glpk solver installed #

  The Wyndor factory produces doors and windows. Each of three plants with
  different available hours can produce either doors or windows.
  To determine how to maximize the profit available in the limited amount
  of hours of production, run the following script.

  It has three main sections: model, objective, and constraint.

  The model — it's a concrete model — instantiates the data of the problem,
    such as the hours available from plants.
  The objective (which can be either to maximize or minimize) is
    to maximize profit.
  The constraint uses a CapacityRule function, written using a Python idiom
    called list comprehension.
"""

from pyomo.environ import *
from pyomo.opt import SolverFactory

Products = ['Doors', 'Windows']
ProfitRate = {'Doors': 300, 'Windows': 500}
Plants = ['Door Fab', 'Window Fab', 'Assembly']
HoursAvailable = {'Door Fab': 4, 'Window Fab': 12, 'Assembly': 18}
HoursPerUnit = {('Doors', 'Door Fab'): 1, ('Windows', 'Window Fab'): 2,
                ('Doors', 'Assembly'): 3, ('Windows', 'Assembly'): 2,
                ('Windows', 'Door Fab'): 0, ('Doors', 'Window Fab'): 0}

#Concrete Model
model = ConcreteModel()

#Decision Variables
model.WeeklyProd = Var(Products, within=NonNegativeReals)

#Objective
model.obj = Objective(
    expr=sum(ProfitRate[i] * model.WeeklyProd[i] for i in Products),
    sense=maximize)


# User Defined Capacity Rule
# Accepts a pyomo Concrete Model as the first positional argument,
# and a plant index as a second positional argument
def CapacityRule(model, p):
    return(sum(HoursPerUnit[i, p] * model.WeeklyProd[i] for i in Products)
           <= HoursAvailable[p])

# This statement is what Pyomo needs to generate one constraint for each plant
model.Capacity = Constraint(Plants, rule=CapacityRule)

# This is an optional code path that allows the script to be run outside of
# pyomo command-line. For example: python wyndor.py
if __name__ == '__main__':
    opt = SolverFactory("glpk")
    results = opt.solve(model, tee=True)
    #sends results to stdout
    #results.write()
