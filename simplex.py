import numpy as np #for matrix operations
import csv 
from tkinter import messagebox 

#read csv file and build the intial tableau based on the selected projects
def readAndBuild(checkbox_vars):
    try:
        #reead the CSV file
        with open('tableau.csv', 'r') as file: #open csv
            csv_reader = csv.reader(file) #create csv reader
            headers = next(csv_reader) #skip header row, it's just labels
            all_rows = list(csv_reader) #list of all rows
        
        #list of all checkbox indexes where project is selcted
        selected_indices = []
        for i, var in checkbox_vars.items():
            if var.get(): # if the checkbox is checked
                selected_indices.append(i)
        
        #if there is no selected, display warning
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select at least one project!")
            return None
        
        #extract only the selected project rows
        selected_project_rows = []
        for i in selected_indices:
            if i < len(all_rows) - 1: #excluding the last row
                selected_project_rows.append(all_rows[i])
        
        obj_row = all_rows[-1] #extract objective row
        
        #build the simplex tableau
        simplex_data = []
        pollutantants = 10 #number of columns
        
        #loops through the selcted rows
        #dynamically build elements of each rows of the project
        for row_num, project_row in enumerate(selected_project_rows):
            new_row = [] #storage for elements of each rows (removed not included col)
            
            #add first 10 column (pollutants)
            for col in range(1, pollutantants + 1):
                new_row.append(float(project_row[col])) #add to the new row
            
            #additionalll slack variables to limit atmost 20 per projects
            for selected in selected_indices:
                new_row.append(-1 if selected == selected_indices[row_num] else 0)
            
            #x variables
            for selected in selected_indices:
                new_row.append(1 if selected == selected_indices[row_num] else 0)
            
            #add Z column and RHS
            new_row.append(0) #0 intially for z
            new_row.append(float(project_row[-1])) #last element
            
            simplex_data.append(new_row) #append to the simplex data
        
        #build the last row or the objective row
        obj_new_row = []
        
        #pollutants
        for col_idx in range(1, pollutantants + 1):
            obj_new_row.append(float(obj_row[col_idx])) #add
        
        obj_new_row.extend([20] * len(selected_indices)) # additional
        obj_new_row.extend([0] * len(selected_indices)) # desicion
        obj_new_row.extend([1, 0]) #Z and RHS
        
        simplex_data.append(obj_new_row)
        
        return simplex_data #return the intial tableau
    
    #error handling
    except FileNotFoundError:
        messagebox.showerror("File Error", "tableau.csv file not found!")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        return None

#get the basic solution for iterations except last iteration
def basic_solutions(iterations_list):
    allBasicSolutions = [] #storgae for all the basic sol

    #dimensions of tableau
    tableauShape = iterations_list[0] #refrencc intial tableau
    numRows, numCols = tableauShape.shape
    solVars = numCols - 1 #number of elements of basic sol exclude rhs
    numConstraintRows = numRows - 1 #num of row exlude obj

    #iterate through each tableau in the list
    for tableau in iterations_list:
        current_basic_solution = np.zeros(solVars) # np initilized all as 0
        
        #iterate through each variable column 
        for j in range(solVars):
            numZero = 0 
            numOne = 0 
            onePosition = -1 #row index of the 1
            
            #count 0s and 1s in the constraint rows 
            for i in range(numConstraintRows): 
                if np.isclose(tableau[i, j], 0): #isclose() for comparison
                    numZero += 1
                elif np.isclose(tableau[i, j], 1):
                    numOne += 1
                    onePosition = i #row where 1 is loacted
                
            #check for the basic variable condition
            if numZero == (numConstraintRows - 1) and numOne == 1:
                current_basic_solution[j] = tableau[onePosition, numCols - 1] #get the value of RHS
            #else remain 0
                
        allBasicSolutions.append(current_basic_solution.copy())
    return allBasicSolutions

#simplex method
#returns dictionaries finaltableau, basicSolution, Z, all iterations
def Simplex(tableau):
    tableau = np.array(tableau, dtype=float) #convert list to numpy array for matrix operation
    numRows, numCols = tableau.shape #tableau dimension
    noNegative = False #indicate if the last row has negative values
    
    #store all iterations
    iterations = [tableau.copy()] #store initial tableau

    #simplex iterations
    while not noNegative: #while there is stilll negative
        Objective = tableau[numRows - 1, :numCols - 1] #last row exclude last column (RHS)

        #check if optimal
        if np.min(Objective) >= 0: #if all >= 0, optimal solution reach
            noNegative = True #update all obj are positive
            break

        #index of most negative value or the lowest
        pivotCol = np.argmin(Objective) #argmin returns the index of smallest elemet
        pivotRow = None #initialize pivotrow and minimum ratio
        minRatio = None

        #ratio test
        for i in range(numRows - 1):
            if tableau[i, pivotCol] > 0: #avoid division by zero or negative/ get only positive
                ratio = tableau[i, numCols - 1] / tableau[i, pivotCol] #numcols-1 -> last column
                    #base case            
                if (pivotRow == None) or (ratio < minRatio):
                    minRatio = ratio #updates
                    pivotRow = i #index of candidate for pivot
        
        #kkapag wla ng valid na pivot row
        if pivotRow == None:
            #infeasible, just return what we have
            iteration_basic = basic_solutions(iterations) #basic solution ng tableasu
            
            return { #return necessary for show tableau (in dictionary)
                "iterations": iterations,
                "iterBasicSolution": iteration_basic,
                "infeasible": True #mark as infeasible for show tableau reference
            }

        #if may valid pivot row pa
        #Gauss-Jordan elimination
        pivotElement = tableau[pivotRow, pivotCol]
        tableau[pivotRow, :] = tableau[pivotRow, :] / pivotElement #normalize pivot row

        for i in range(numRows):
            if i != pivotRow: #for all rows except pivot row
                multiplier = tableau[i, pivotCol] #multiplier for the current row
                tableau[i, :] -= tableau[pivotRow, :] * multiplier #update row

        iterations.append(tableau.copy()) #store iteration tableau
    
    #calculate basic solutions for all iterations except last
    iteration_basic = basic_solutions(iterations)
    
    #extracts final tableau
    finalTableau = tableau.copy()
    
    #basic solution for final tableau
    basicSolution = iteration_basic[-1] 
    
    #optimal cost/value
    Z = tableau[numRows - 1, numCols - 1]

    #return necessary for dsiplay in gui
    return {
        "finalTableau": finalTableau,
        "finalBasicSolution": basicSolution,
        "Z": Z,
        "iterations": iterations,
        "iterBasicSolution": iteration_basic,
        "infeasible": False
    }
