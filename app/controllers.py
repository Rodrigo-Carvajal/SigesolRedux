from app import app, db, login_manager
from flask import Flask, render_template, request, url_for, redirect, session, flash, Blueprint
from flask_login import login_required, login_user
from app.models import Usuario, Solicitud, Estado, get_users, get_solicitudes, get_estados

#Blueprint de la applicación
sigesolBP = Blueprint('app', __name__)

#####     Rutas     #####
#RUTAS PRINCIPALES Y DE AUTH
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        nombreUsuario = request.form['nombreUsuario']
        contrasena = request.form['contrasena']
        user = Usuario.query.filter_by(nombreUsuario=nombreUsuario).first()
        if user:
            if user.contrasena == contrasena:
                login_user(user)
                if user.rol == 'Administrador':
                    return redirect(url_for('admin'))
                elif user.rol == 'OIRS':
                    return redirect(url_for('oirs'))
                elif user.rol == 'Funcionario':
                    return redirect(url_for('funcionario'))
                elif user.rol == "Secretaria":
                    return redirect(url_for('secretaria'))
                else:
                    flash("Usuario no cuenta con rol, contactar con administrador", 'warning')
                    return redirect(url_for('login'))
            else:
                flash("Contraseña incorrecta", 'danger')
                return redirect(url_for('login'))
        else:
            flash("Nombre de usuario incorrecto", 'danger')
            return redirect(url_for('login'))
    return render_template('views/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

#RUTAS ADMINISTRADOR
@app.route('/admin', methods=['GET','POST'])
@login_required
def admin():
    usuarios = get_users()
    solicitudes = get_solicitudes()
    return render_template('views/admin/admin.html', usuarios=usuarios, solicitudes=solicitudes)

@app.route('/adminCrudUsuarios', methods=['GET','POST'])
@login_required
def adminCrudUsuarios():
    usuarios = get_users()
    if request.method == "POST":
        user = Usuario(
            id = Usuario.id,
            nombreUsuario = request.form['nombreUsuario'],
            contrasena = request.form['contrasena'],
            rol = request.form['rol'],
            nombreCompleto = request.form['nombreCompleto'],
            departamento = request.form['departamento'],
            unidad = request.form['unidad']
        )
        db.session.add(user)
        db.session.commit()
        flash("¡Usuario creado exitosamente!", 'success')
        return redirect(url_for('adminCrudUsuarios'))
    return render_template('views/admin/adminCrudUsuarios.html', usuarios=usuarios)

@app.route('/adminCrudSolicitudes', methods=['GET','POST'])
@login_required
def adminCrudSolicitudes():
    solicitudes = get_solicitudes()
    current_time = datetime.now().time().strftime('%H:%M')
    if request.method == "POST":
        solicitud = Solicitud(
            idSolicitud= request.form['idSolicitud'],
            numero = request.form['numero'],
            fechaDeIngreso = request.form['fechaDeIngreso'],
            horaDeIngreso = request.form['horaDeIngreso'],
            fechaDeVencimiento = request.form['fechaDeVencimiento'],
            nombreSolicitante = request.form['nombreSolicitante'],
            materia = request.form['materia'],
            tipo = request.form['tipo'],
            departamento = request.form['departamento'],
            unidad = request.form['unidad'],
            usuarioID = request.form['funcionario']
        )
        db.session.add(solicitud)
        db.session.commit()
        flash("¡Solicitud creada exitosamente!", 'success')
        return redirect(url_for('adminCrudSolicitudes'))
    return render_template('views/admin/adminCrudSolicitudes.html', solicitudes=solicitudes, current_time=current_time)

#RUTAS OIRS
@app.route('/oirs', methods=['GET','POST'])
@login_required
def oirs():
    solicitudes = get_solicitudes()    
    return render_template('views/oirs/oirs.html', solicitudes=solicitudes)

@app.route('/oirsCrudSolicitudes', methods=['GET','POST'])
@login_required
def oirsCrudSolicitudes():
    solicitudes = get_solicitudes()
    current_time = datetime.now().time().strftime('%H:%M')
    if request.method == "POST":        
        solicitud = Solicitud(
            idSolicitud= request.form['idSolicitud'],
            numero = request.form['numero'],
            fechaDeIngreso = request.form['fechaDeIngreso'],
            horaDeIngreso = request.form['horaDeIngreso'],
            fechaDeVencimiento = request.form['fechaDeVencimiento'],
            nombreSolicitante = request.form['nombreSolicitante'],
            materia = request.form['materia'],
            tipo = request.form['tipo'],
            departamento = request.form['departamento'],
            unidad = request.form['unidad'],
            usuarioID = request.form['funcionario']
        )
        db.session.add(solicitud)
        db.session.commit()
        flash("¡Solicitud creada exitosamente!", 'success')
        return redirect(url_for('oirsCrudSolicitudes'))
    return render_template('views/oirs/oirsCrudSolicitudes.html', solicitudes=solicitudes, current_time=current_time)

#RUTAS SECRETARÍA
@app.route('/secretaria', methods=['GET','POST'])
@login_required
def secretaria():
    return render_template('/views/secretaria/secretaria.html')

@app.route('/secreSolIngresadas', methods=['GET','POST'])
@login_required
def secreSolIngresadas():
    solicitudes = get_solicitudes()
    if request.method == "POST":
        idSolicitud = request.form['idSolicitud']
        return render_template('views/secretaria/asignarUnidad/'.format(idSolicitud))
    return render_template('views/secretaria/secreSolIngresadas.html', solicitudes=solicitudes)

@app.route('/asignarUnidad/<string:nombreUsuario>/<int:idSolicitud>', methods=['GET','POST'])
@login_required
def asignarUnidad(nombreUsuario, idSolicitud):
    if request.method == "POST":
        solicitud = db.session.execute(db.select(Solicitud).filter_by(idSolicitud=idSolicitud)).scalar_one()
        unidad = request.form['unidad']
        solicitud.unidad = unidad
        estado = Estado(
            idInternoDepto = request.form['idInternoDepto'],
            fkIdSolicitud = idSolicitud,
            nombreUsuario = nombreUsuario,
            idModificacion = request.form['idModificacion'],
            descripcionProceso = request.form['descripcionProceso'],
            fechaModificacion = request.form['fechaModificacion'],
            designadoA = solicitud.unidad,
            estadoActual = request.form['estadoActual']
        )
        db.session.add(estado)
        db.session.commit()
        return redirect(url_for('secreSolIngresadas'))
    solicitud = db.session.execute(db.select(Solicitud).filter_by(idSolicitud=idSolicitud)).scalar_one()
    estado = Estado.query.filter_by(fkIdSolicitud = idSolicitud).first()
    return render_template('views/secretaria/asignarUnidad.html', solicitud=solicitud, estado=estado)
        
@app.route('/<string:departamento>/<string:unidad>', methods=['GET','POST'])
@login_required
def solicitudesunidad(departamento, unidad):
    solicitudes = get_solicitudes()
    return render_template('/views/secretaria/solicitudesUnidad.html', solicitudes=solicitudes, departamento=departamento, unidad=unidad)

@app.route('/estadoSolicitud/<int:idSolicitud>', methods=['GET','POST'])
@login_required
def estadoSolicitud(idSolicitud):    
    solicitud = db.session.execute(db.select(Solicitud).filter_by(idSolicitud=idSolicitud)).scalar_one()
    estado = db.session.execute(db.select(Estado).filter_by(fkIdSolicitud=idSolicitud)).scalar_one()
    estados = get_estados()
    return render_template('views/secretaria/estadoSolicitud.html', solicitud=solicitud, estado=estado, estados=estados, idSolicitud=idSolicitud, fkIdSolicitud=idSolicitud)

#RUTAS FUNCIONARIO
@app.route('/funcionario', methods=['GET','POST'])
@login_required
def funcionario():
    return render_template('views/funcionario/funcionario.html')

@app.route('/funSolIngresadas', methods=['GET','POST'])
@login_required
def funSolIngresadas():
    solicitudes = get_solicitudes()
    return render_template('/views/funcionario/funSolIngresadas.html', solicitudes=solicitudes)

@app.route('/funSolPendientes', methods=['GET','POST'])
@login_required
def funSolPendientes():
    solicitudes = get_solicitudes()
    return render_template('/views/funcionario/funSolPendientes.html', solicitudes=solicitudes)

@app.route('/gestionarSolicitud/<int:id>/<int:idSolicitud>/<string:departamento>/<string:unidad>', methods=['GET','POST'])
@login_required
def gestionarSolicitud(id, idSolicitud, departamento, unidad):
    solicitud = db.session.execute(db.select(Solicitud).filter_by(idSolicitud=idSolicitud)).scalar_one()
    if request.method == 'POST':
        estado = Estado(
            idInternoDepto = request.form['idInternoDepto'],
            idModificacion = request.form['idModificacion'],
            fkIdSolicitud = request.form['fkIdSolicitud'],
            nombreUsuario = request.form['nombreUsuario'],
            descripcionProceso = request.form['descripcionProceso'],
            fechaModificacion = request.form['fechaModificacion'],
            designadoA = request.form['designadoA'],
            estadoActual = request.form['estadoActual']
        )
        db.session.commit()
        solicitudes = get_solicitudes()
        return render_template('views/funcionario/funSolIngresadas.html',solicitudes=solicitudes)
    estado = db.session.execute(db.select(Estado).filter_by(fkIdSolicitud=idSolicitud)).scalar_one()
    return render_template('views/funcionario/gestionarSolicitud.html', id=id, idSolicitud=idSolicitud, solicitud=solicitud, estado=estado, departamento=departamento, unidad=unidad)


#####     Rutas CRUD     #####

###   UPDATES   ###
#UPDATE USUARIO
@app.route('/editu/<int:id>', methods=['GET','POST'])
@login_required
def edit_usuario(id):
    if request.method == 'POST':
        usuario = db.session.execute(db.select(Usuario).filter_by(id=id)).scalar_one()
        usuario.nombreUsuario = request.form['nombreUsuario']
        usuario.contrasena = request.form['contrasena']
        usuario.nombreCompleto = request.form['nombreCompleto']
        usuario.rol = request.form['rol']
        usuario.departamento = request.form['departamento']
        usuario.unidad = request.form['unidad']
        db.session.commit()
        flash("¡Usuario editado exitosamente!", 'primary')
        return redirect(url_for('adminCrudUsuarios'))
    usuario = db.session.execute(db.select(Usuario).filter_by(id=id)).scalar_one()
    return render_template('views/admin/editarUsuario.html', usuario=usuario)

#UPDATE SOLICITUD(Admin)
#Edit de solicitud que redirige a la vista de Admin
@app.route('/aedits/<int:idSolicitud>', methods=['GET','POST'])
@login_required
def Aedit_solicitud(idSolicitud):
    if request.method == 'POST':
        solicitud = db.session.execute(db.select(Solicitud).filter_by(idSolicitud=idSolicitud)).scalar_one()
        solicitud.numero = request.form['numero']
        solicitud.fechaDeIngreso = request.form['fechaDeIngreso']
        solicitud.fechaDeVencimiento = request.form['fechaDeVencimiento']
        solicitud.nombreSolicitante = request.form['nombreSolicitante']
        solicitud.materia = request.form['materia']
        solicitud.tipo = request.form['tipo']
        solicitud.departamento = request.form['departamento']
        solicitud.usuarioID = request.form['funcionario']
        db.session.commit()
        return redirect(url_for('adminCrudSolicitudes'))
    solicitud = db.session.execute(db.select(Solicitud).filter_by(idSolicitud=idSolicitud)).scalar_one()
    return render_template('views/editarSolicitud.html',solicitud=solicitud)


#UPDATE SOLICITUD(OIRS)
#Edit de solicitud que redirige a la vista de OIRS
@app.route('/oedits/<int:idSolicitud>', methods=['GET','POST']) 
@login_required
def Oedit_solicitud(idSolicitud):
    if request.method == 'POST':
        solicitud = db.session.execute(db.select(Solicitud).filter_by(idSolicitud=idSolicitud)).scalar_one()
        solicitud.numero = request.form['numero']
        solicitud.fechaDeIngreso = request.form['fechaDeIngreso']
        solicitud.fechaDeVencimiento = request.form['fechaDeVencimiento']
        solicitud.nombreSolicitante = request.form['nombreSolicitante']
        solicitud.materia = request.form['materia']
        solicitud.tipo = request.form['tipo']
        solicitud.departamento = request.form['departamento']
        solicitud.usuarioID = request.form['funcionario']
        db.session.commit()
        return redirect(url_for('oirsCrudSolicitudes'))
    solicitud = db.session.execute(db.select(Solicitud).filter_by(idSolicitud=idSolicitud)).scalar_one()
    return render_template('views/editarSolicitud.html',solicitud=solicitud)


###   DELETES   ###
#DELETE SOLICITUD(Admin)
@app.route('/adeletes/<int:idSolicitud>')
@login_required
def adeletes(idSolicitud):
    estado = Estado.query.filter_by(fkIdSolicitud=idSolicitud).first()
    solicitud = db.session.execute(db.select(Solicitud).filter_by(idSolicitud=idSolicitud)).scalar_one()
    if estado == None:
        db.session.delete(solicitud)
        db.session.commit()
        flash("¡Solcitiud eliminada exitosamente!",'warning')
    else:
        db.session.delete(solicitud)
        db.session.delete(estado)
        db.session.commit()
        flash("¡Solcitiud eliminada exitosamente!",'warning')
    solicitudes = get_solicitudes()
    return redirect(url_for('adminCrudSolicitudes', solicitudes=solicitudes))

#DELETE SOLICITUD(Oirs)
@app.route('/odeletes/<int:idSolicitud>')
@login_required
def odeletes(idSolicitud):
    estado = Estado.query.filter_by(fkIdSolicitud=idSolicitud).first()
    solicitud = db.session.execute(db.select(Solicitud).filter_by(idSolicitud=idSolicitud)).scalar_one()
    if estado == None:
        db.session.delete(solicitud)
        db.session.commit()
        flash("¡Solicitud eliminada exitosamente!",'warning')
    else:
        db.session.delete(solicitud)
        db.session.delete(estado)
        db.session.commit()
        flash("¡Solicitud eliminada exitosamente!",'warning')
    solicitudes = get_solicitudes()
    return redirect(url_for('oirsCrudSolicitudes', solicitudes=solicitudes))

#DELETE USUARIO
@app.route('/deleteu/<int:id>')
@login_required
def delete_usuario(id):
    usuario = db.session.execute(db.select(Usuario).filter_by(id=id)).scalar_one()
    db.session.delete(usuario)
    db.session.commit()
    flash("¡Usuario eliminado exitosamente!",'danger')
    usuarios = get_users()
    return redirect(url_for('adminCrudUsuarios', usuarios=usuarios))