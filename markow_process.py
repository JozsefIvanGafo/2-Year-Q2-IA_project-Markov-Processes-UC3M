"""file that contains the class for the MarkovDecision"""
import xlwings as xw
from temperature_exception import ControlTemperatureException



class TemperatureControl():
    """Class containing methods for markov decisions process for temperature control"""
    def __init__(self,
                 excel_path:str,
                 excel_sheets:str,
                 range_on:str,
                 range_off:str,
                 action_cost_on:int, 
                 action_cost_off:int
                 ):
        #Catch errors if any when opening the file
        try:
            self._excel=xw.Book(excel_path).sheets[excel_sheets]
        except FileNotFoundError as my_error:
            raise ControlTemperatureException("Excel file not found") from my_error
        
        #extracted data list
        self._table_on=self._extract_data(range_on)
        self._table_off=self._extract_data(range_off)
        #Length of nodes
        self._len=len(self._table_on)

        #The cost of action
        self._action_cost_on=action_cost_on
        self._action_cost_off=action_cost_off

        #Initial values
        self._v_on=[]
        self._v_off=[]
        #Create a list for each node that has value 0
        for i in range(self._len):
            self._v_on.append(0)
            self._v_off.append(0)


    def optimal_policy(self):
        """Method that is in charge of obtaining the optimal policy for each node"""
        pass


    def _bellman_eq(self,node):
        """Method that calculates the bellman value after n iterations for a node"""
        v_on_before=-1
        v_off_before=-1
        #It will iterate until we find a V that is adequate
        while v_on_before!=self._v_on[node] or v_off_before!=self._v_off[node]:
            #We change the values of v_XX_before
            v_on_before=self._v_on[node]
            v_off_before=self._v_off[node]
            #We calculate for the action on
            self._v_on[node]= self._stochastic_domain(node,self._action_cost_on,self._v_on)
            self._v_off[node]= self._stochastic_domain(node,self._action_cost_off,self._v_off)
            
        
            

    
    def _stochastic_domain(self,node,cost,data_row):
        """Method that is in charge of performing the stochastic domain formula"""
        pass




    def _extract_data(self,excel_range):
        """Method that is in charge of extracting the data of a excel file into  a nested list""" 
        #We return the data extracted from the selected range
        return self._excel.range(excel_range)
              
    @property
    def table_on(self):
        """We make read only the self._table_on"""
        return self._table_on
    @property
    def table_off(self):
        """We make read only the self._table_off"""
        return self._table_off
    @property
    def action_cost_on(self):
        """We make read only the self._action_cost_on"""
        return self._action_cost_on
    @property
    def action_cost_off(self):
        """We make read only the self._action_cost_on"""
        return self._action_cost_off
    