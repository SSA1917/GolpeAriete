#Implementacion metodo de las caracteristicas

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
#SE tiene en cuenta dos condiciones de borde aguas arriba con un reservorio y aguas abajo con una valvula de cierre

class MetodoCaracteristicas:
    def __init__(self):
        
        #Tuberia
        self.Longitud = 0
        self.Radio = 0
        self.Area = 0
        self.fFriccion = 0#Factor de friccionde Darcy
        self.TcTiempoCierre = 6#Tiempo de cierre de la valvula
        
        #Flujo
        self.cCEleridad = 1000#Velocidad de onda de sobre presion
        #Secciones Matrices de n dimensiones
        self.Qcaudal = 0#Caudal en cada momento y seccion 
        self.Hcarga = 0#Carga en cada momento y seccion
        self.Cp = 0#Cp en cada momento y seccion
        
        #Variables metodo de caracteristicas
        self.DX = 0#Longitud de cada tramo
        self.DT = 0#Incremento de tiempo
        self.Ch = 0#Contante
        self.R = 0#Constante

        #Presentacion
        self.Dates = {}
    #Calculos
    def Geometria(self, Longitud, Diametro, nTramos, fFriccion):
        
        self.Radio = Diametro/2
        self.Longitud = Longitud
        self.fFriccion = fFriccion

        self.Area = math.pi*self.Radio**2#Seccion circular

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
            
            self.Hcarga[v][0] = self.Hcarga[0][0]-(v)*self.R*self.Qcaudal[0][0]**2#Carga incial en cada seccion
        
            self.Qcaudal[v][0] = QcaudalInicial#Caudal Inicial en cada seccion


    def Calculos(self,Columnas,Filas):  #Para un Reservorio con carga constante en la primera y una valvula de cierre en la ultima seccion
        Time = 0
        for j in range(1,Filas-1,1):    
            #Caudal Primera Seccion 
            self.Qcaudal[0][j] = (self.Hcarga[0][j-1]-self.Hcarga[1][j-1]-self.Qcaudal[1][j-1]*( self.R*self.Qcaudal[1][j-1] - self.Ch))/self.Ch 
                        
            for i in range(1,Columnas-2,1):

                #Qcaudal,Hcarga,Cp en Secciones Intermedias
                self.Cp[i][j] = (self.Hcarga[i-1][j-1]+self.Qcaudal[i-1][j-1]*(self.Ch-self.R*self.Qcaudal[i-1][j-1]))

                self.Hcarga[i][j] = 0.5*(self.Cp[i][j]+self.Hcarga[i+1][j-1]+self.Qcaudal[i+1][j-1]*(self.R*self.Qcaudal[i+1][j-1]-self.Ch))
                
                self.Qcaudal[i][j] = (self.Cp[i][j]-self.Hcarga[i][j])/self.Ch
                        
            #Qcaudal,Cp, Hcarga Ultima Seccion
            if(Time >= 6):
                self.Qcaudal[5][j] = 0
            else:
                self.Qcaudal[5][j] = (1-((j)/self.TcTiempoCierre) )*self.Qcaudal[0][0]
            self.Cp[5][j] = self.Hcarga[5-1][j-1] + self.Qcaudal[5-1][j-1]*(self.Ch-self.R*self.Qcaudal[5-1][j-1])
            self.Hcarga[5][j] = self.Cp[5][j]-self.Ch*self.Qcaudal[5-1][j]
            
            Time +=1

    def Presentacion(self):
        self.Dates = {
                'H0': self.Hcarga[0],
                'Q0': self.Qcaudal[0],
                
                'H1': self.Hcarga[1],
                'Q1': self.Qcaudal[1],
                
                'H2': self.Hcarga[2],
                'Q2': self.Qcaudal[2],
                
                'H3': self.Hcarga[3],
                'Q3': self.Qcaudal[3],
                
                'H4': self.Hcarga[4],
                'Q4': self.Qcaudal[4],
                
                'H5': self.Hcarga[5],
                'Q5': self.Qcaudal[5],

                'H6': self.Hcarga[6],
                'Q6': self.Qcaudal[6],


                
            }
        
        Table = pd.DataFrame(self.Dates)
        Table.to_csv('TablaVersion1.csv')
        
        
    def Validacion(self, Filas):
        
        X = np.arange(Filas)
        fig = plt.figure()
        
        plt.plot(X,self.Dates.get('H0'), label='Seccion1')
        plt.plot(X,self.Dates.get('H1'), label='Seccion2')
        plt.plot(X,self.Dates.get('H2'), label='Seccion3')
        plt.plot(X,self.Dates.get('H3'), label='Seccion4')
        plt.plot(X,self.Dates.get('H4'), label='Seccion5')
        plt.plot(X,self.Dates.get('H5'), label='Seccion6')
        plt.legend()
        plt.show()

M1 = MetodoCaracteristicas()
def Prueba(Longitud, Diametro, nTramos, fFriccion, Columnas,Filas ,HCargaInicial, QcaudalInicial):
    M1.Geometria(Longitud, Diametro, nTramos, fFriccion)#Longitud, Diametro, nTramos, fFriccion
    M1.CondicionesIniciales(Columnas,Filas,HCargaInicial,QcaudalInicial)#Columnas,Filas,HCargaInicial,QcaudalInicial
    M1.Calculos(Columnas,Filas)#Columnas,Filas
    M1.Presentacion()
    M1.Validacion(Filas)#Filas

Prueba(5000,1.8,5,0.02,7,30,80,6)#Longitud, Diametro, nTramos, fFriccion, Columnas,Filas, HCargaInicial, QcaudalInicial,