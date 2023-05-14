"""
Module where we find the class Optimal policy

Bachelor in Computer Science and engineering / 2nd year / 2 semester / Artificial Intelligence
AI project / Markov Decision process for Temperature control

József Iván Gafo           100456709
Marcos González vallejo    100472206
"""
#we improt libraries
from decimal import Decimal
import xlwings as xw
from optimal_policy_exception import OptimalPolicyException

#Global Variables
EXCEL_PATH="ia_prob.xlsx"
EXCEL_SHEETS="ia_prob"


class OptimalPolicy():
    """
    Description: This class is in charge of calculating the optimal policy for n actions
    """
    #Set up
    def __init__(self,excel_cells_list:list,desired_temp:int)->None:
        """
        Description: The set up is in charge of preparing our class to calculate the optimal policy.
        Inputs:
        excel_cells_list: list containing strings where we find excell cells to extract the proability table .
        desired_temp: The desired temperature node that the user wants to calculate the optimal policy.
        Outputs:
        NONE.
        """
        #Activated to observe all the process to calculate the optimal policy or for debugging
        #Prints if true it will print all intermidiate calculations
        #If false it only prints the final result
        self._print=False
        self._max_limit_it=1_000_000_000
        #Precision for oour operations
        self._precision=7

        #Initialized all necessary variables to calculate the optimal policy
        self._cost_list=[]
        self._prob_table=[]
        #node where we want the desired temperature , calculated with: node=16+tn*12=22
        self._desired_temp=desired_temp

        #We create the cost list asking the user
        num_of_actions=len(excel_cells_list)
        self._create_cost_list(num_of_actions)

        #We extract the data from the excel
        self._extract_excel_data(excel_cells_list)
        self._length=len(self._prob_table[0])

        #Print the table if the parameter is activated
        if self._print:
            self._print_table()

    #Main code  
    def calculate_optimal_policy(self):
        """
        Description: Main function that is in charge of doing the optimal policy for every node.
        Inputs:
        None.
        Outputs:
        None.
        """
        #We calculate the values
        self._calculate_values()
        #Now we do the optimal policy for each node
        policy = []
        print_policy=[]
        for tn in range(self._length):    
            policy.append(self._optimal_policy(tn))
            node=16+tn*0.5
            print_policy.append("node %s: %d"%(str(node),policy[tn]) )
        #finally we print the final result
        print("The optimal policy for each node is: ",print_policy)
        return policy

    #Functions that are used on the self.calculate_optimal_policy

    def _calculate_values(self)->None:
        """
        Description: This method is in charge of calculating all the 
        values to later calculate the optimal policy.
        Inputs:
        None.
        Outputs:
        None.
        """
        #Variables for calculate the values
        value=[]
        prev_values=[]
        for _ in range(self._length):
            #We make so that the values are different from prev_values at the start
            value.append("0")
            prev_values.append("-1")
        iteration=1
        #We do operations until value == prev_value or we exceed the max iteration limit
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
        """
        Description: This method is in charge of calculating the bellman equation for the node tn .
        Inputs:
        tn: node that we want to calculate the stochastic domain.
        prev_values: a list conataining the previous values that were calculated on the previous iteration.
        Iteration: Integer that contains the number of iteration .
        Outputs:
        It returns a string containg the result of the bellman equation formula.
        """
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
        """
        Description: This method is in charge of calculating the stochastic domain for the node tn for an specific action.
        Inputs:
        prob_table: a list containing the probabilities for every node of an specdific action.
        tn: node that we want to calculate the stochastic domain.
        prev_values: a list conataining the previous values that were calculated on the previous iteration.
        cost: a float that contains the cost of the action.
        Outputs:
        It returns a float containg the result of the stochastic domain formula.
        """
        #Declare variables
        length=len(prob_table)
        accumulated_sum=Decimal(str(cost))
        #We use decimal class to have more precision when using float numbers
        #The float numbers must be of type str when introduce on the decimal class to mantain the precision
        for tnplus1 in range(length):
            accumulated_sum+=Decimal(str(prob_table[tn][tnplus1]))*Decimal(prev_values[tnplus1])

        #We return the stochastic domain result
        return float(accumulated_sum)
    
    def _optimal_policy(self,tn)->int:
        """
        Description: This method is in charge of calculating the optimal policy equation for the node tn .
        Inputs:
        tn: node that we want to calculate the optimal policy.
        Outputs:
        It returns a integer that contains the optimal policy action number  for the node tn.
        """
        #We declare variables that will be used on the conditionals
        best_action_value=999999999999999999999999999999999999999999
        best_action=-1
        #We calculate the stochastic domain of every action on the node Tn and  save the best action
        for action in range(len(self._cost_list)):
            action_value=self._stochastic_domain(self._prob_table[action],tn,self._values,self._cost_list[action])

            #If we found a better action with a lower value action
            if best_action_value>action_value:
                best_action_value=action_value
                best_action=action

        #Check if we found our optimal policy for the node tn
        if best_action<0:
            raise OptimalPolicyException("[ERROR] We cannot find the best action ")

        if self._print:
            #alculate the temperature node
            node=16+tn*0.5
            print("For node %s the best action is number: %d. "%(str(node),best_action))
        #We return the result
        return  best_action

    #Functions that are used on the init of the class

    def _extract_excel_data(self,excel_cells_list:list)->None:
        """
        Description: This method is in charge of extracting 
        the probabilities tables of every action on self._prob_table.
        Inputs:
        excel_cells_list: Is a list where it contains the excel cells for every action.
        Outputs:
        None.
        """
        #We open the excel file 
        try:
            excel=xw.Book(EXCEL_PATH).sheets[EXCEL_SHEETS]
        except FileNotFoundError as my_error:
            raise OptimalPolicyException("[ERROR] Excel file not found") from my_error
        
        #We iterate to open all the probabilities tables
        for cells_of_action in excel_cells_list:
            
            #We extract the data
            try:
                #Append the probability table on  self._prob_table
                self._prob_table.append(excel.range(cells_of_action).expand().value)
            except Exception as my_error:
                excel.book.close()
                raise OptimalPolicyException("[ERROR] Error extracting the data from the excel file") from my_error
            #We append it on the probability table
            
        #We close the excel file
        excel.book.close()
        
    def _print_table(self)->None:
        """
        Description: This method is in charge of printing the tables of probabilities for evry action.
        Inputs:
        None.
        Outputs:
        None.
        """
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

    def _create_cost_list(self,number_of_actions:int)->None:
        """
        Description: This method is in charge of asking the user the cost of every action.
        Inputs:
        number_of_actions: Is an integer containg the number of actions that are currently on the program.
        Outputs:
        None.
        """
        for i in range(number_of_actions):
            try:
                cost=float(input("what is the cost for the action %d: "%(i)))
            except ValueError as my_error:
                raise OptimalPolicyException("[ERROR] The cost must be a float") from my_error
            self._cost_list.append(cost)
        