from datetime import datetime, timedelta
import pandas as pd
import json

class Dataset:
    def __init__(self, path):
        self.path = path
        self.general    = pd.read_excel(path, sheet_name='General')
        self.bus        = pd.read_excel(path, sheet_name='Bus')
        self.branches   = pd.read_excel(path, sheet_name='Branches')
        self.profile    = pd.read_excel(path, sheet_name='Profile')
        self.bess       = pd.read_excel(path, sheet_name='BESS')
        self.gen        = pd.read_excel(path, sheet_name='Gen')
        self.load       = pd.read_excel(path, sheet_name='Load')
        self.evcs       = pd.read_excel(path, sheet_name='EVCS')
        self.ev         = pd.read_excel(path, sheet_name='EV')
        self.dg         = pd.read_excel(path, sheet_name='DG')
        self.cost       = pd.read_excel(path, sheet_name='Costs')
        self.prob       = pd.read_excel(path, sheet_name='Probability')
        return

class General:
    def __init__(self, data):
        self.Δt = int(data.general.loc[data.general['Parameter'] == 'Timestep [minutes]', 'Value'].values[0])
        
        

        return

class Sets:
    def __init__(self, data, general):
        self.T  = self.timestamps(general.Δt)
        self.N  = [str(x) for x in data.bus.Bus.values]
        self.L  = [] #[('1', '2'), ('2', '3'), ('3', '4'), ('4', '5')] 
        self.B  = [] #ID do BESS
        self.O  = [] #horário das contingências
        self.S  = []
        self.Y  = []
        self.GD = []
        return
    
    def timestamps(self, Δt):
        T = list()
        t = datetime.strptime('00:00', "%H:%M")
        while t < datetime.strptime('23:59', "%H:%M"):
            T.append(t.strftime("%H:%M"))
            t += timedelta(minutes= Δt) 
        return T
    



class Parameters:
    def __init__(self, data):
        # find row that 
        self.general = General(data)
        self.sets = Sets(data, self.general)


        a = 1

        
        



if __name__ == '__main__':
    dataset = Dataset('dataset/data.xlsx')
    param = Parameters(dataset)

    a = 1