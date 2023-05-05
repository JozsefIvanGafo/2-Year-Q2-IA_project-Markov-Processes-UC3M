#we improt libraries
import xlwings as xw
from optimal_policy_exception import OptimalPolicyException
from decimal import Decimal

#Global Variables
EXCEL_PATH="prueba.xlsx"#"ia_prob.xlsx"
EXCEL_SHEETS="Sheet1"#"ia_prob"


class OptimalPolicy():
    def __init__(self,excel_cells_list:list,desired_temp:int):
        #Activated to observe all the process to calculate the optimal policy or for debugging
        #Prints
        self._print=True
        self._max_limit_it=1000
        #Precision for oour operations
        self._precision=10


        #Initialized all necessary variables to calculate the optimal policy
        self._cost_list=[]
        self._prob_table=[]

        #We create the cost list asking the user
        self._create_cost_list()

        #We extract the data from the excel
        self._extract_excel_data(excel_cells_list)
        self._length=len(self._prob_table[0])

        #Print the table if the parameter is activated
        if self._print:
            self._print_table()

        #node where we want the desired temperature , calculated with: node=16+tn*12=22
        self._desired_temp=desired_temp
        
    def main(self):
        #We calculate the values
        self._calculate_values()
        #Now we do the optimal policy for each node
        policy = []
        print_policy=[]
        for tn in range(self._length):    
            policy.append(self._optimal_policy(tn))
            print_policy="node %s: %d"%(str(tn),policy[tn]) 
        #finally we print the final result
        print("The optimal policy for each node is: ",print_policy)
        return policy




    #Functions that are used on the main

    def _optimal_policy(self,tn):
        action_value=[]
        #We do the stochastic domain for every action for the node tn
        for action in range(len(self._cost_list)):
            action_value.append(self._stochastic_domain(self._prob_table[action],tn,self._values,self._cost_list[action]))


        best_action=[action_value[0],0]
        for value in range(len(self._cost_list)):
            if best_action[0]<action_value[value]:
                best_action=[action_value[value],value]

        node=16+tn*0.5
        
        if self._print:
            print("For node %s the best action is number: %d. "%(node,best_action))
        #We return the result
        return  best_action

    def _calculate_values(self):
        #Variables for calculate the values
        value=[]
        prev_values=[]
        for node in range(self._length):
            #We make so that the values are different from prev_values at the start
            value.append("0")
            prev_values.append("-1")
        iteration=0
        #We do operations until value == prev_value or we 
        while str(value)!=str(prev_values) and iteration<=self._max_limit_it:
            if self._print:
                print("#######################################################################")
                print("Iteration: ", iteration)
                print("value %s"%str(value))
                print("before_values %s"%(prev_values))
                print("")
            #We equalize the previous value with the most recents
            #We don't want to do a light copy since we are interested in the values and not the addresses to the values
            for i in  range(self._length):
                prev_values[i]=value[i][:self._precision]
            #We use the belman equation for each node
            for tn in range(self._length):
                if tn !=self._desired_temp:
                    value[tn]=self._belman_eq(
                            tn=tn,
                            prev_values=prev_values,
                            iteration=iteration)[:self._precision]
            iteration+=1

        #Print final values or last value calculated
        if self._print:
            print("#######################################################################")
            print("Finished calculating the values for each node")
            print("Iteration: ", iteration-1)
            print("value %s"%str(value))
            print("before_values %s"%(prev_values))
            print("")

        #Raise error if we exceed the max number of errors
        if iteration>self._max_limit_it:
            raise OptimalPolicyException("[ERROR] Max number of iteration has been exceed it")
        
        #We copy the values to self._values
        self._values=value

    def _belman_eq(self,tn:int,prev_values:list,iteration:int)->str:
        #We do the stochastic domain equation for each action
        action_value=[]
        #We do a loop to calculate the min value for the node tn and m actions
        for action in range(len(self._cost_list)):
            action_value.append(self._stochastic_domain(self._prob_table[action],tn,prev_values,self._cost_list[action]))
            if self._print:
                print("--------")

        #The we calculate the min
        result=str(min(action_value))
        #We print the result
        if self._print:
            node=16+tn*0.5
            print("V%d(node%s)= min%s= %s"% (iteration,str(node),str(action_value),result)) 
            print("------------------------------------------------")
        #We return the result of the belman equation
        return result

    def _stochastic_domain(self, prob_table:list,tn:int,prev_values:list,cost:float)->float:
        #Declare variables
        length=len(prob_table)
        accumulated_sum=Decimal(str(cost))
        #We use decimal class to have more precision when using float numbers
        #The float numbers must be of type str when introduce on the decimal class to mantain the precision
        for tnplus1 in range(length):
            accumulated_sum+=Decimal(str(prob_table[tn][tnplus1]))*Decimal(prev_values[tnplus1])

        #We return the stochastic domain result
        return float(accumulated_sum)


    #Functions that are used on the init of the class

    def _extract_excel_data(self,excel_cells_list):
        #We open the excel file 
        try:
                excel=xw.Book(EXCEL_PATH).sheets[EXCEL_SHEETS]
        except FileNotFoundError as my_error:
            raise OptimalPolicyException("[ERROR] Excel file not found") from my_error
        
        #We iterate to open all the probabilities tables
        for cells_of_action in excel_cells_list:
            
            #We extract the data
            try:
                prob_of_action=excel.range(cells_of_action).expand().value
            except Exception as my_error:
                excel.book.close()
                raise OptimalPolicyException("[ERROR] Error extracting the data from the excel file") from my_error
            #We append it on the probability table
            self._prob_table.append(prob_of_action)
        #We close the excel file
        excel.book.close()
        
    def _print_table(self)->None:
        """Function that prints the tables of probabilities"""

        #Loop for the number of actions
        for table in range(len(self._cost_list)):
            print("------------------------------------------------------------------------------------------------------")
            print("Table of probabilities for action %d. \n"%(table))

            node=16
            text="Tn+1/Tn "
            #We print the first row
            for i in range(self._length):
                text+=" "+ str(node)
                node+=0.5
            print(text)
            node=16
            for i in range(self._length):
                print(node," ",self._prob_table[table][i])
                node+=0.5
        print("------------------------------------------------------------------------------------------------------")

    def _create_cost_list(self):
        try:
            num_actions=int(input("How many actions do you want? "))
        except ValueError as my_error:
                raise OptimalPolicyException("[ERROR] The number of actions must be an integer") from my_error
        if num_actions<2:
            raise OptimalPolicyException("[ERROR] The number of action must be bigger than 2")

        for i in range(num_actions):
            try:
                cost=float(input("what is the cost for the action %d: "%(i)))
            except ValueError as my_error:
                raise OptimalPolicyException("[ERROR] The cost must be a float") from my_error
            self._cost_list.append(cost)
        



excel_on_cells="B2:B20"
excel_off_cells="B25:B43"
cells=[excel_on_cells,excel_off_cells]
control_temp=OptimalPolicy(cells,12)
control_temp.main()