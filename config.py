class Config:
    SECRET_KEY = 'nbadsjb813bnjc'

class DevelopmentConfig():
    DEBUG = True
    host = '0.0.0.0'
    
config = {
    'development': DevelopmentConfig
    
}