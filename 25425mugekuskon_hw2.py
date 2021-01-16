#Muge Kuskon 25425
from ortools.sat.python import cp_model
from itertools import groupby

class SolutionPrinter(cp_model.CpSolverSolutionCallback):
  """Print intermediate solutions."""

  def __init__(self, variables):
    cp_model.CpSolverSolutionCallback.__init__(self)
    self.__variables = variables
    
    self.__solution_count = 0
    
  def OnSolutionCallback(self):
    self.__solution_count += 1
    board_size_row = int(len(self.__variables)**(1/2))# row's length
    board_size_col = int(len(self.__variables)**(1/2)) # column's length
    
    matrix = [ self.__variables[i:i+board_size_col] for i in range(0,len(self.__variables),board_size_col) ]
    
    for i in range(board_size_row):
        for j in range(board_size_col):
            
            print(self.Value(matrix[i][j]), end=" ")
        print()
    print()

  def SolutionCount(self):
    return self.__solution_count



def Solve(inputlength,RowConstraints,ColumnConstraints, Blocks):

    #create a model
    aquarium = cp_model.CpModel()
    rows = inputlength
    columns = inputlength
    

    
    
    
    # Initialize all variables.(Cells are our variables)
    cells = [aquarium.NewIntVar(0, 1, "[%s, %s]" %(i,j))for i in range(inputlength) for j in range(inputlength)]
            
    #print(cells)
    


    
     #Initialize all the constraints.

    ic = 0 #increment cells.
    for x in range(rows):#rows and columns have the same number of elements.

        #For every row, the total number of water-filled cells should be equal to the # given.
        aquarium.Add( sum(cells[ic : ic + rows]) == RowConstraints[x])
        
        #For every column, the total number of water-filled cells should be equal to the # given.
        aquarium.Add(sum(cells[x : rows*columns : columns]) == ColumnConstraints[x])

        ic += rows
        
    
    
    
    ConstList =[]
    #Horizontal Constraint created
    
    for i in range(0,rows):#For every row check the  adjacent cells (horizontally).

        c = 0
        j = 1
        for _ in range(1, len(Blocks[i])):
    
            if(Blocks[i][c]==Blocks[i][j]):#If adjacent cells belong to the same block, then have to add a constraint.
                #print("SAME:", Blocks[i][c])
                cellvalue1 = i*inputlength + c
                cellvalue2 = i*inputlength + j
                ConstList.append(cells[cellvalue1])#add corresponding values, ths will be the index in the cells list where we had all of our variables.
                ConstList.append(cells[cellvalue2])
               
                aquarium.AddAllowedAssignments(ConstList,[[0]*2, [1]*2])#They are both empty or both full.
                #print(ConstList)
                ConstList=[]
            c += 1
            j += 1



    #Vertical Constraint created
            
    for x in range(0,columns):

        
        c = 0
        
        for _ in range(0, len(Blocks[x])):

            if(x+1 < inputlength):#need to add for not having a error of index.
                 
                if(Blocks[x][c]==Blocks[x+1][c]):#check if two vertically adjacent cells belong to the same group or not.
                    #print("Same:", Blocks[i][c])
                    cellvalue1 = x*inputlength + c
                    cellvalue2 = (x+1)*inputlength + c #add corresponding values, ths will be the index in the cells list where we had all of our variables.
                    ConstList.append(cells[cellvalue1])
                    ConstList.append(cells[cellvalue2])
                   
                    aquarium.AddForbiddenAssignments(ConstList,[[1,0]])#The one on the top cannot be full when the one below is empty. 
                    #print(ConstList)
                    ConstList=[]
                c += 1
                
    
                        
                    

    #Print the solutions.
    solver = cp_model.CpSolver()
    solution_printer = SolutionPrinter(cells)
    status = solver.SearchForAllSolutions(aquarium, solution_printer)

    



#Example 1 
Blocks =[["1","2","3","3","3","3"],
         ["1","2","1","1","1","3"],
         ["1","1","1","4","4","3"],
         ["1","1","1","4","3","3"],
         ["5","1","6","4","3","3"],
         ["5","1","6","4","3","3"]]


RowConstraints = [1,1,2,4,5,5]
ColumnConstraints = [3,5,1,4,3,2]
inputlength=6


'''
#Example 1 
Blocks =[["1","2","3","3","3","3"],
         ["1","2","1","1","1","3"],
         ["1","1","1","4","4","3"],
         ["1","1","1","4","3","3"],
         ["5","1","6","4","3","3"],
         ["5","1","6","4","3","3"]]


RowConstraints = [1,1,2,4,5,5]
ColumnConstraints = [3,5,1,4,3,2]
inputlength=6





#Example 2
Blocks =[["1","1","2","2","3","3"],
         ["1","1","4","4","4","3"],
         ["5","1","1","1","4","3"],
         ["5","1","1","5","6","3"],
         ["5","5","5","5","6","3"],
         ["5","5","5","6","6","3"]]

RowConstraints=[2,4,5,3,1,4]
ColumnConstraints=[1,3,5,3,2,5]
inputlength=6




#example 3 :

Blocks =[["1","1","1","5","5","5"],
         ["2","1","5","5","6","5"],
         ["2","1","1","5","6","5"],
         ["2","1","1","5","3","4"],
         ["2","1","1","5","3","4"],
         ["2","2","2","2","3","4"]]


RowConstraints=[3,1,5,3,4,2]
ColumnConstraints=[1,5,4,3,3,2]
inputlength=6



#Example 5: Easy 10x10
Blocks =[["1","1","1","1","4","4","4","4","5","5"],
         ["2","2","1","1","4","5","5","5","5","5"],
         ["1","1","1","3","4","5","5","5","6","6"],
         ["3","3","3","3","4","4","4","5","6","6"],
         ["3","3","11","11","12","4","4","4","5","6"],
         ["3","3","11","12","12","12","12","5","5","6"],
         ["3","7","11","11","13","13","12","12","5","6"],
         ["7","7","8","13","13","12","12","5","5","5"],
         ["7","7","8","13","13","13","12","12","9","9"],
         ["7","7","7","13","10","10","10","10","10","10"]]


RowConstraints=[4,2,3,1,3,1,2,6,7,9]
ColumnConstraints=[5,6,6,2,1,2,3,5,3,5]

inputlength=10


#Example 5: Normal 10x10
Blocks =[["1","1","1","1","2","3","3","4","5","5"],
         ["6","2","2","2","2","3","3","4","7","5"],
         ["6","8","8","9","2","2","2","7","7","5"],
         ["6","6","10","9","2","2","11","11","5","5"],
         ["6","6","10","12","12","12","12","13","5","13"],
         ["14","10","10","15","12","12","12","13","13","13"],
         ["14","10","15","15","16","12","17","17","17","17"],
         ["10","10","16","16","16","12","17","17","17","18"],
         ["19","10","20","18","18","12","17","18","18","18"],
         ["19","20","20","18","18","18","18","18","18","18"]]


RowConstraints=[3,4,8,5,3,3,3,6,3,2]
ColumnConstraints=[2,3,5,4,3,5,6,6,5,1]

inputlength=10




#Example 6: HARD 6X6 
Blocks =[["1","2","2","3","4","4"],
         ["5","5","5","6","7","7"],
         ["8","8","5","6","9","10"],
         ["11","11","12","12","9","10"],
         ["13","14","14","15","15","15"],
         ["16","18","14","14","17","17"]]


RowConstraints = [4,2,4,4,1,4]
ColumnConstraints = [5,3,1,1,5,4]
inputlength=6


#Example 7: Hard 15x15
Blocks =[["1","1","2","2","3","4","4","4","5","6","7","7","7","8","8"],
         ["9","1","9","10","3","4","4","11","5","6","12","12","7","8","8"],
         ["9","9","9","10","3","3","13","11","5","12","12","7","7","8","8"],
         ["14","14","14","15","15","16","13","13","5","5","7","7","7","8","8"],
         ["14","14","14","14","14","16","16","16","16","17","7","7","18","8","19"],
         ["20","20","20","20","21","22","22","22","17","17","23","18","18","18","19"],
         ["20","24","20","25","21","21","22","26","27","27","23","18","19","19","19"],
         ["28","24","24","25","21","22","22","26","19","19","19","19","19","29","19"],
         ["28","28","24","25","21","21","22","30","30","30","19","29","29","29","32"],
         ["28","28","24","25","33","21","37","37","30","35","35","35","36","36","32"],
         ["28","25","25","25","33","33","37","37","30","35","35","38","39","39","32"],
         ["28","28","28","40","33","33","33","33","41","41","38","38","39","42","42"],
         ["43","28","40","40","48","48","33","33","33","33","38","38","39","42","42"],
         ["43","40","40","40","48","44","44","44","44","44","44","45","46","46","47"],
         ["43","40","40","40","48","48","48","48","48","44","45","45","45","47","47"]]


RowConstraints=[4,9,10,9,2,5,7,4,10,11,11,7,10,9,10]
ColumnConstraints=[4,5,6,5,3,7,10,11,10,13,10,10,10,8,6]

inputlength=15





'''



Solve(inputlength,RowConstraints,ColumnConstraints, Blocks)

