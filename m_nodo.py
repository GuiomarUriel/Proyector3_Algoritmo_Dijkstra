class nodo:
    def __init__(self,id):
        self.id=id
        self.vecinos=[]
    
    def __repr__(self):
        return repr(self.id)