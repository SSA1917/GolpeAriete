#Implementacion metodo de las caracteristicas
import pandas as pd
import numpy as np
import math
#SE tiene en cuenta dos condiciones de borde aguas arriba con un reservorio y aguas abajo con una valvula de cierre

class MetodoCaracteristicas:
    def __init__(self):
        
        self.Time = []
        self.Section = []
        #Variables
        #Tuberia
        self.Longitud = 0
        self.Radio = 0
        self.Area = 0
        self.fFriccion = 0
        self.TcTiempoCierre = 6
        
        #Flujo
        self.cCEleridad = 1000#Velocidad de onda de sobre presion
        #Secciones
        self.Qcaudal = 0
        self.Hcarga = 0
        self.Cp = 0
        
        #Variables metodo de caracteristicas
        self.DX = 0
        self.DT = 0
        self.Ch = 0
        self.R = 0
    #Calculos
    def Geometria(self, Longitud, Diametro, nTramos, fFriccion):
        
        self.Radio = Diametro/2
        self.Longitud = Longitud
        self.fFriccion = fFriccion

        self.Area = math.pi*self.Radio**2

        self.DX = Longitud/nTramos
        self.DT = Longitud/(self.cCEleridad*nTramos)#Paso de tiempo
        self.Ch = self.cCEleridad/(9.8*self.Area)
        self.R = fFriccion*self.DX/(2*9.8*self.Area**2)
        
        
    def CondicionesIniciales(self,Columnas,Filas,HCargaInicial,QcaudalInicial):

        self.Hcarga = np.zeros((Columnas,Filas))#NumeroSecciones,NumeroFila o paso de tiempo
        self.Qcaudal = np.zeros((Columnas,Filas))#NumeroSecciones,NumeroFila o paso de tiempo
        self.Cp = np.zeros((Columnas,Filas))#NumeroSecciones,NumeroFila o paso de tiempo
        
        self.Hcarga[0].fill(HCargaInicial)#Para una carga incial constante en el tiempo
 
        
        for v in range(0,Columnas,1):
            #Hcarga Inicial
            
            self.Hcarga[v][0] = self.Hcarga[0][0]-(v)*self.R*self.Qcaudal[0][0]**2
        
            self.Qcaudal[v][0] = QcaudalInicial


    def Calculos(self,Columnas,Filas):  #Para un Reservorio con carga constante en la primera y una valvula de cierre en la ultima seccion

        for j in range(1,Filas-1,1):    
            #Caudal Primera Seccion 
            self.Qcaudal[0][j] = (self.Hcarga[0][j-1]-self.Hcarga[1][j-1]-self.Qcaudal[1][j-1]*( self.R*self.Qcaudal[1][j-1] - self.Ch))/self.Ch 
            for i in range(1,Columnas-1,1):

                #Qcaudal Secciones Intermedias
                self.Cp[i][j] = (self.Hcarga[i-1][j-1]+self.Qcaudal[i-1][j-1]*(self.Ch-self.R*self.Qcaudal[i-1][j-1]))

                self.Hcarga[i][j] = (0.5*(self.Cp[i][j]+self.Hcarga[i+1][j-1]+self.Qcaudal[i+1][j-1]*(self.R*self.Qcaudal[i+1][j-1]-self.Ch)))     

                self.Qcaudal[i][j] = (self.Cp[i][j]-self.Hcarga[i][j])/self.Ch

            #Qcaudal Ultima Seccion
            self.Qcaudal[6][j] = (1-((j-1)/self.TcTiempoCierre) )*self.Qcaudal[0][0]
            self.Cp[6][j] = self.Hcarga[i-1][j-1] + self.Qcaudal[i-1][j-1]*(self.Ch-self.R*self.Qcaudal[i-1][j-1])
            self.Hcarga[6][j] = self.Cp[i][j]-self.Ch*self.Qcaudal[i-1][j]

    def Presentacion(self):
        dates = {
            #"Time": self.Time,
            "H1": self.Hcarga[0],
            "Q1": self.Qcaudal[0],
            "H2": self.Hcarga[1],
            "Q2": self.Qcaudal[1],
            "H3": self.Hcarga[2],
            "Q3": self.Qcaudal[2],
            "H4": self.Hcarga[3],
            "Q4": self.Qcaudal[3],
            "H5": self.Hcarga[4],
            "Q5": self.Qcaudal[4],
            "H6": self.Hcarga[5],
            "Q6": self.Qcaudal[5],
        }
        Table = pd.DataFrame(dates)
        print(Table)

M1 = MetodoCaracteristicas()
def Prueba():
    M1.Geometria(5000,1.8,5,0.02)
    M1.CondicionesIniciales(7,15,80,6)
    M1.Calculos(7,15)
    M1.Presentacion()

Prueba()