import xlwings as xw
from temperature_exception import ControlTemperatureException

#Declare global variables of our program for our markov process
EXCEL_PATH="prueba.xlsx"#"ia_prob.xlsx"
EXCEL_SHEETS="Sheet1"#"ia_prob"
EXCEL_ON_CELLS="B2:B20"
EXCEL_OFF_CELLS="B25:B43"
COST_ON=1
COST_OFF=1
PRECISION=4


class Controltemperature():

    def __init__(self,precision,cost_on,cost_of) -> None:
        #How accurate we want our iterations to be
        self.precision=precision
        self._value=[]
        self.cost=[cost_on,cost_of]
        #The initial values for each node
        for i in range(19):
            self._value.append("0")
        

    def optimal_policy(self):
        """Main code"""
        #We extract the data
        self._extract_data()
        #We print the tables of probabilities
        self._print_on_off_list()
        #We calculate the values to later do the optimal policy
        self._bellman_eq()

    def _bellman_eq(self):
        """Calculate the final value of on and off for all the nodes"""
        #We define a variable to have the previous value
        before_value=[]
        for j in range(self._length):
            before_value.append("-1")
            before_value.append("-1")
        iteration=1
        for i in range (5):
        #while str(self._value)!=str(before_value):
            print("Iteration: ",iteration)
            iteration+=1
            for i in range(self._length):
                before_value[i]=self._value[i][:self.precision]
            node=16.0
            for j in range(self._length):
                operation1=self._stochastic_domain(self.cost[0],j,self._table_on_list)
                operation2=self._stochastic_domain(self.cost[0],j,self._table_off_list)
                minimum=min(operation1,operation2)
                self._value[j]=str(minimum)[:self.precision]
                print("V(node%s)%s= min(%s ,%s)= %s"% (str(node)[:4],
                                                       str(iteration)[:self.precision],
                                                       str(operation1)[:self.precision],
                                                       str(operation2)[:self.precision],
                                                       str(self._value[j])))
                node+=0.5
            

    def _stochastic_domain(self,cost,node,data_list):
        #Copy the values not the address
        value=cost
        """for j in range(self._length):
            prev=value
            value+=float(self._value[node])*float(data_list[node][j])
            print("value(%s)=prev(%s)+ Vn-1(%s)*prob(%s)"%(value,prev,self._value[node],data_list[node][j]))"""
        
        return value#test
        total=cost
        for node in range(self._length):
            pass

            
    
        

    def _extract_data(self):
        """This function is in charge of extracting the data from the excel file"""
        #We open the excel file
        try:
            excel=xw.Book(EXCEL_PATH).sheets[EXCEL_SHEETS]
        except FileNotFoundError as my_error:
            raise ControlTemperatureException("Excel file not found") from my_error

        #We extract the information from the excel files
        self._table_on_list=excel.range(EXCEL_ON_CELLS).expand().value
        self._table_off_list=excel.range(EXCEL_OFF_CELLS).expand().value
        #declare variable for the length of the
        #  list
        self._length=len(self._table_on_list)

    def _print_on_off_list(self):
        """Method in charge of printing all the tables of probabilities"""
        print("on_table")
        self._print_table(self._table_on_list)
        print("--------------------------------------------------")
        print("off table")
        self._print_table(self._table_off_list)

    def _print_table(self,table):
        node=16
        text="Tn+1/Tn "
        for i in range(self._length):
            text+=" "+ str(node)
            node+=0.5
        print(text)
        node=16
        for i in range(self._length):
            print(node," ",table[i])
            node+=0.5


#Here we execute our main code
code=Controltemperature(precision=PRECISION,
                        cost_on=COST_ON,
                        cost_of=COST_OFF)
code.optimal_policy()


