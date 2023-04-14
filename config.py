#Creación de clase Config:
class Config:
    SECRET_KEY = '484267d6-5754-4b52-b66e-7da05e5ab7bd'

#Clase usada para la configuración de la aplicación en desarrollo:
class DevelopmentConfig():
    DEBUG=True    

#Diccionario de las distintas configuraciones existentes:    
config = {
    'development': DevelopmentConfig
    
}