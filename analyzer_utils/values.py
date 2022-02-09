from array import array

class IPv4:
    
    def __init__(self) -> None:
        pass

class Port():
    '''A 2-bytes value.
    0 -> 65535'''
    MIN = 0
    MAX = 65535
    
    def __init__(self, value: int) -> None:

        if not 0 <= value <= 65535:
            raise TypeError(f'A port must be an integer between {self.MIN} and {self.MAX}')

        self.value = value
    
    


        
