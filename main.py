from markow_process import TemperatureControl
#Declare parameters
excel_path="ia_prob.xlsx"
excel_sheets="ia_prob"
excel_range_of_action_on="B2:B20"
excel_range_of_action_off="B25:B43"
action_cost_on=1
action_cost_off=1

#We exceute our main code
#We create the object with the selected parameters
tempreature_control= TemperatureControl(excel_path,
                                        excel_sheets,
                                        excel_range_of_action_on,
                                        excel_range_of_action_off,
                                        action_cost_on,
                                        action_cost_off)
tempreature_control.optimal_policy()