class RequiredComponentNotExist(Exception):
    """Exception raised for errors in the input salary.

    Attributes:
        folder -- folder in which component does not exist 
        component -- component which does not exist 
        message -- explanation of the error
    """

    def __init__(self, folder, component, message=None):
        self.message = message
        if message is None:
            self.message = f"Required component in {folder} does not exist: {component}"
        super().__init__(self.message)

class DuplicateComponent(Exception):
    """Exception raised for errors in the input salary.

    Attributes:
        folder -- folder in which component duplicated 
        component -- component which duplicated 
        message -- explanation of the error
    """

    def __init__(self, folder, component, message=None):
        self.message = message
        if message is None:
            self.message = f"There are more than one of the following component in {folder}: {component}"
        super().__init__(self.message)
