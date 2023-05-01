#we improt libraries
import xlwings as xw
from temperature_exception import ControlTemperatureException
from decimal import Decimal

#Define variables for the program
EXCEL_PATH="prueba.xlsx"#"ia_prob.xlsx"
EXCEL_SHEETS="Sheet1"#"ia_prob"
EXCEL_ON_CELLS="B2:B20"
EXCEL_OFF_CELLS="B25:B43"
COST_ON=10
COST_OFF=3
DESIRED_TEMPT=22
#Activated to observe all the process to calculate the optimal policy or for debugging
PRINT=True
CALCULATIONS=True
MAX_LIMIT_IT=5

#Define functions
def stochastic_domain(prob_table,tn,prev_values,cost)->float:
    #Declare variables
    length=len(prob_table)
    accumulated_sum=cost
    text=" %d +"%(cost)
    #We use decimal class to have more precision when using float numbers
    #The float numbers must be of type str when introduce on the decimal class to mantain the precision
    for tnplus1 in range(length):
        accumulated_sum+=Decimal(str(prob_table[tn][tnplus1]))*Decimal(prev_values[tnplus1])
        if PRINT and CALCULATIONS:
            text+=" %s * %s +"%(str(prob_table[tn][tnplus1]),prev_values[tnplus1])
    if PRINT and CALCULATIONS:
        print(text[:-1])
        print("equal to %s"%(float(accumulated_sum)))
    #We return the accumulative sum without adding the cost
    return float(accumulated_sum)

def belman_eq(prob_on_table:list,prob_off_table:list,tn:int,prev_values:list,iteration)->str:
    #We do the stochastic domain equation for each action
    on_action_value=stochastic_domain(prob_on_table,tn,prev_values,COST_ON)
    if PRINT:
        print("--------")
    off_action_value=stochastic_domain(prob_off_table,tn,prev_values,COST_OFF)
    #The we calculate the min and print it and then return the min
    result=str(min(on_action_value,off_action_value))
    node=16+tn*0.5
    if PRINT:
        print("V%d(node%s)= min(%s ,%s)= %s"% (iteration,str(node),on_action_value,off_action_value,result)) 
        print("------------------------------------------------")
    return result

def optimal_policy():
    pass

def print_table(table:list)->None:
    """Function that prints the tables of probabilities"""
    length=len(table)
    node=16
    text="Tn+1/Tn "
    for i in range(length):
        text+=" "+ str(node)
        node+=0.5
    print(text)
    node=16
    for i in range(length):
        print(node," ",table[i])
        node+=0.5


#Here we execute the main function
#We open the excel file
try:
    excel=xw.Book(EXCEL_PATH).sheets[EXCEL_SHEETS]
except FileNotFoundError as my_error:
    raise ControlTemperatureException("[ERROR] Excel file not found") from my_error
#We extract the data
try:
    prob_on_table=excel.range(EXCEL_ON_CELLS).expand().value
    prob_off_table=excel.range(EXCEL_OFF_CELLS).expand().value
except Exception as my_error:
    excel.book.close()
    raise ControlTemperatureException("[ERROR] Error extracting the data from the excel file") from my_error
#We close the excel file
excel.book.close()


#We print the table of probabilities
if PRINT:
    print("on_table")
    print_table(prob_on_table)
    print("--------------------------------------------------")
    print("off table")
    print_table(prob_off_table)

#Now we will do multiple iterations with the bellman and stochastic equation to extract the final values for each node
#we define variables for the iterations and bellman eq.
before_value=[]
value=[]
iteration=1
#formula for the precision for our operations
prec=max(len(str(COST_OFF)),len(str(COST_ON)))+7
length=len(prob_on_table)
for i in range(length):
    #We use strings because we can decise with wich precision our program work e.g value[0][:7]!=value[0][:9]
    before_value.append("-1")
    value.append("0")
#We start to do the iterations
while str(value)!=str(before_value) and iteration<=MAX_LIMIT_IT:
    if PRINT:
        print("#######################################################################")
        print("Iteration: ", iteration)
        print("value %s"%str(value))
        print("before_values %s"%(before_value))
        print("")
    #We equalize the previous value with the most recents
    #We don't want to do a light copy since we are interested in the values and not the addresses to the values
    for i in  range(length):
        before_value[i]=value[i][:prec]
    #We use the belman equation for each node
    for node in range(length):
        value[node]=belman_eq(prob_on_table=prob_on_table,
                    prob_off_table=prob_off_table,
                    tn=node,
                    prev_values=before_value,
                    iteration=iteration)[:prec]
    #We go the the next iteration
    iteration+=1
#Print final values
if PRINT:
    print("#######################################################################")
    print("Iteration: ", iteration)
    print("value %s"%str(value))
    print("before_values %s"%(before_value))
    print("")

