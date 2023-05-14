"""
Module where we execute our main code 

Bachelor in Computer Science and engineering / 2nd year / 2 semester / Artificial Intelligence
AI project / Markov Decision process for Temperature control

József Iván Gafo           100456709
Marcos González vallejo    100472206
"""
#Import class
from optimal_policy import OptimalPolicy

#Cells of the excell files where we find the probabilities table 
excel_on_cells="B2:B20"
excel_off_cells="B25:B43"
cells=[excel_on_cells,excel_off_cells]

#Execute our code
control_temp=OptimalPolicy(cells,12)
#The action on is 0 and cost off is 1
control_temp.calculate_optimal_policy()
