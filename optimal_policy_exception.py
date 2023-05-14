"""
Module where we find the code to create our own personalized exception

Bachelor in Computer Science and engineering / 2nd year / 2 semester / Artificial Intelligence
AI project / Markov Decision process for Temperature control

József Iván Gafo           100456709
Marcos González vallejo    100472206
"""
class OptimalPolicyException(Exception):
    """Personalised exception for OptimalPolicyException"""
    def __init__(self, message):
        self.__message = message
        super().__init__(self.message)

    @property
    def message(self):
        """gets the message value"""
        return self.__message

    @message.setter
    def message(self,value):
        self.__message = value
