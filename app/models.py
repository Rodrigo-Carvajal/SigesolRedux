#Importaciones necesarias para el trabajo de este módulo:
from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

#Modelos
class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombreUsuario = db.Column(db.String(20), unique=True, nullable=False)
    contrasena = db.Column(db.String(102), nullable=False)
    rol = db.Column(db.String(20), nullable=False)
    nombreCompleto = db.Column(db.String(50), nullable=False)
    departamento = db.Column(db.String(60), nullable=False)
    unidad = db.Column(db.String(60), nullable=False)
    solicitudes = db.relationship('Solicitud', backref='usuario', lazy=True)
    estados = db.relationship('Estado', backref='usuario', lazy=True)

    def __init__(self, id, nombreUsuario, contrasena, rol, nombreCompleto, departamento, unidad):
        self.id = id
        self.nombreUsuario = nombreUsuario
        self.contrasena = contrasena
        self.rol = rol
        self.nombreCompleto = nombreCompleto
        self.departamento = departamento
        self.unidad = unidad

    def get_id(self):
        return (self.id)

    def __repr__(self):
        return f"Usuario('{self.nombreUsuario}')"

class Solicitud(db.Model):
    __tablename__ = 'solicitudes'
    idSolicitud = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), nullable=False)
    fechaDeIngreso = db.Column(db.Date, default=datetime.now().strftime('%d-%m-%Y'), nullable=False)
    horaDeIngreso = db.Column(db.Time, nullable=False)
    fechaDeVencimiento = db.Column(db.Date, default=datetime.now().strftime('%d-%m-%Y'), nullable=False)
    nombreSolicitante = db.Column(db.String(30), nullable=False)
    materia = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    departamento = db.Column(db.String(60), nullable=False)
    unidad = db.Column(db.String(60))
    documento = db.Column(db.String(100))
    activa = db.Column(db.Boolean, default=True, nullable=False)
    usuarioID = db.Column(db.String(30), db.ForeignKey('usuarios.nombreUsuario'), nullable=False)
    estados = db.relationship('Estado', backref='solicitud', lazy=True)

    def __init__(self, idSolicitud, numero, fechaDeIngreso, horaDeIngreso, fechaDeVencimiento, nombreSolicitante, materia, tipo, departamento, unidad, documento, usuarioID):
        self.idSolicitud = idSolicitud
        self.numero = numero
        self.fechaDeIngreso = fechaDeIngreso
        self.horaDeIngreso = horaDeIngreso
        self.fechaDeVencimiento = fechaDeVencimiento
        self.nombreSolicitante = nombreSolicitante
        self.materia = materia
        self.tipo = tipo
        self.departamento = departamento
        self.unidad = unidad
        self.documento = documento
        self.usuarioID = usuarioID

    def __repr__(self):
        return f"Solicitud('{self.idSolicitud}','{self.numero}','{self.fechaDeIngreso}','{self.fechaDeVencimiento}','{self.nombreSolicitante}','{self.materia}','{self.tipo}','{self.departamento}','{self.unidad}','{self.usuarioID}')"

class Estado(db.Model):
    __tablename__ = 'estadoSolicitudes'
    fkIdSolicitud = db.Column(db.Integer, db.ForeignKey('solicitudes.idSolicitud'), primary_key=True, nullable=False)
    idInternoDepto = db.Column(db.Integer, nullable=False, autoincrement=True, unique=True)
    idModificacion = db.Column(db.Integer, primary_key=True)
    nombreUsuario = db.Column(db.String(20), db.ForeignKey('usuarios.nombreUsuario'), nullable=False)
    descripcionProceso = db.Column(db.String(100), nullable=False)
    fechaModificacion = db.Column(db.Date, default=datetime.now().strftime('%d-%m-%Y'), nullable=False)
    designadoA = db.Column(db.String(60), nullable=False)
    estadoActual = db.Column(db.String(20), nullable=False)

    def __init__(self, idInternoDepto, fkIdSolicitud, idModificacion, nombreUsuario, descripcionProceso, fechaModificacion, designadoA, estadoActual):
        self.idInternoDepto = idInternoDepto
        self.fkIdSolicitud = fkIdSolicitud
        self.idModificacion = idModificacion
        self.nombreUsuario = nombreUsuario
        self.descripcionProceso = descripcionProceso
        self.fechaModificacion = fechaModificacion
        self.designadoA = designadoA
        self.estadoActual = estadoActual
    
    def generar_id_interno(self):
        ultima_solicitud = Solicitud.query.filter_by(idInternoDepto=self.idInternoDepto).order_by(Solicitud.idInternoDepto.desc()).first()
        if ultima_solicitud is None:
            return f'{self.departamento.abreviacion}-001'
        else:
            ultimo_id = int(ultima_solicitud.id_interno.split('-')[-1])
            nuevo_id = ultimo_id + 1
            return f'{self.departamento.abreviacion}-{nuevo_id:03d}'

    def __repr__(self):
        return f"Estado de la solicitud('{self.idInternoDepto}','{self.fkIdSolicitud}' modificada N° '{self.idModificacion}' realizada por el usuario '{self.nombreUsuario}' en la fecha '{self.fechaModificacion}','{self.estado}','{self.designadoA}')"

###   Funciones   ###
#Funcion que retorna todos los usuarios registrados en la base de datos
def get_users():
    usuarios = []
    all_usuarios = db.session.execute(db.select(Usuario).order_by(Usuario.id)).scalars()
    for user in all_usuarios:
        usuarios.append({"id":user.id, "nombreUsuario":user.nombreUsuario, "rol":user.rol, "nombreCompleto":user.nombreCompleto, "departamento":user.departamento, "unidad":user.unidad})
    return usuarios

#Funcion que retorna todos las solicitudes registrados en la base de datos
def get_solicitudes():
    solicitudes = []
    #all_solicitudes = Solicitud.query.all()
    all_solicitudes = db.session.execute(db.select(Solicitud).order_by(Solicitud.idSolicitud)).scalars()
    for solicitud in all_solicitudes:
        solicitudes.append({"idSolicitud":solicitud.idSolicitud, "numero":solicitud.numero, "fechaDeIngreso":solicitud.fechaDeIngreso, "horaDeIngreso":solicitud.horaDeIngreso, "fechaDeVencimiento":solicitud.fechaDeVencimiento, "nombreSolicitante":solicitud.nombreSolicitante, "materia":solicitud.materia, "tipo":solicitud.tipo, "departamento":solicitud.departamento, "unidad":solicitud.unidad, "documento":solicitud.documento, "usuarioID":solicitud.usuarioID})
    return solicitudes

#Función que retorna todos los estados de una solicitud
def get_estados():
    estados = []
    #all_solicitudes = Solicitud.query.all()
    all_estados = db.session.execute(db.select(Estado).order_by(Estado.fkIdSolicitud)).scalars()
    for estado in all_estados:
        estados.append({"idInternoDepto":estado.idInternoDepto, "fkIdSolicitud":estado.fkIdSolicitud, "idModificacion":estado.idModificacion, "nombreUsuario":estado.nombreUsuario, "descripcionProceso":estado.descripcionProceso, "fechaModificacion":estado.fechaModificacion, "designadoA":estado.designadoA, "estadoActual":estado.estadoActual})
    return estados

@login_manager.user_loader
def load_user(id):
    usuario = Usuario.query.filter_by(id=id).first()
    return usuario