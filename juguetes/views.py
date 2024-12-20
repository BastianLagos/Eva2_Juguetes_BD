from django.shortcuts import render
from .models import Juguete
from juguetes.models import Usuario, Origen, Tipo, Historial, Juguete
from datetime import datetime

#-----------MENU OPERADOR----------------------

# FUNCION PARA MOSTRAR EL MENU OPERADOR
def mostrarMenuOperador(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True:
        if nomUsuario.upper() != "ADMIN":
            datos = { 'nomUsuario' : nomUsuario }
            return render(request, 'menu_operador.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Permisos Suficientes Para Acceder!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)


# FUNCION PARA MOSTRAR EL FORMULARIO DE REGISTRO
def mostrarFormularioRegistro(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["nomUsuario"].upper() != "ADMIN":
            opcionesOrigen = Origen.objects.all().values().order_by("nombre_origen")
            opcionesTipo = Tipo.objects.all().values().order_by("nombre_tipo")
            datos = { 
                'nomUsuario' : request.session["nomUsuario"],
                'opcionesOrigen' : opcionesOrigen,
                'opcionesTipo' : opcionesTipo
            }
            return render(request, 'form_registrar.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Permisos Suficientes Para Acceder!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)

# FUNCION PARA MOSTRAR EL LISTADO
def mostrarListado(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True:
        if nomUsuario.upper() != "ADMIN":
            jugue = Juguete.objects.select_related("origen","tipo").all().order_by("nombre")
            datos = {'jugue' : jugue,'nomUsuario' : nomUsuario}
            return render(request, "listado.html", datos)
        else:
            datos = { 'r2' : 'No Tiene Permisos Suficientes Para Acceder!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)
  


#FUNCIÓN PARA INSERTAR JUGUETE

def insertarJuguete(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True:
        if nomUsuario.upper() != "ADMIN":
            if request.method == "POST":
                cod = request.POST['txtcod']
                nom = request.POST['txtnom'].upper()
                pre = request.POST['txtpre']
                dis = request.POST['opdis']
                ori = request.POST['cboori']
                can = request.POST['txtcan']
                tip = request.POST['cbotip']
                mar = request.POST['txtmar']

                comprobarCodigo = Juguete.objects.filter(nombre=nom)
                if comprobarCodigo:
                    opcionesOrigen = Origen.objects.all().values().order_by("nombre_origen")
                    opcionesTipo = Tipo.objects.all().values().order_by("nombre_tipo")
                    datos = {
                        'nomUsuario' : request.session["nomUsuario"],
                        'opcionesOrigen' : opcionesOrigen,
                        'opcionesTipo' : opcionesTipo,
                        'r2' : 'El Codigo del Juguete ya Existe!!'
                    }
                    return render(request, 'form_registrar.html', datos)

                else:
                    
                    jugue = Juguete(codigo=cod, nombre=nom, precio=pre, disponibilidad=dis, origen_id=ori, cantidad=can, tipo_id=tip, marca=mar)
                    jugue.save()

                    # Se registra en la tabla historial.
                    accion = "Insert realizado ("+str(nom.lower())+")"
                    tabla = "Juguete"
                    fechayhora = datetime.now()
                    usuario = request.session["idUsuario"]
                    his = Historial(accion_historial=accion, tabla_historial=tabla, fecha_hora_historial=fechayhora, usuario_id=usuario)
                    his.save()

                    opcionesOrigen = Origen.objects.all().values().order_by("nombre_origen")
                    opcionesTipo = Tipo.objects.all().values().order_by("nombre_tipo")
                    datos = {
                        'nomUsuario' : request.session["nomUsuario"],
                        'opcionesOrigen' : opcionesOrigen,
                        'opcionesTipo' : opcionesTipo,
                        'r' : 'Juguete ('+str(nom)+') Registrado Correctamente!!'
                    }
                    return render(request, 'form_registrar.html', datos)

            else:
                opcionesOrigen = Origen.objects.all().values().order_by("nombre_origen")
                opcionesTipo = Tipo.objects.all().values().order_by("nombre_tipo")
                datos = {
                    'nomUsuario' : request.session["nomUsuario"],
                    'opcionesOrigen' : opcionesOrigen,
                    'opcionesTipo' : opcionesTipo,
                    'r2' : 'Debe Presionar El Botón Para Registrar Juguetes!!'
                }
                return render(request, 'form_registrars.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Permisos Suficientes Para Acceder!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)


# FUNCION PARA ELIMINAR JUGUETE
def eliminarJuguete(request, id):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True:
        if nomUsuario.upper() != "ADMIN":
            try:
                jugue = Juguete.objects.get(id=id)
                nom = jugue.nombre
                jugue.delete()
                # Se registra en la tabla historial.
                accion = "Eliminación realizada ("+str(nom.lower())+")"
                tabla = "Juguete"
                fechayhora = datetime.now()
                usuario = request.session["idUsuario"]
                his = Historial(accion_historial=accion, tabla_historial=tabla, fecha_hora_historial=fechayhora, usuario_id=usuario)
                his.save()
                jugue = Juguete.objects.all().values()
                datos = {'jugue' : jugue, 'r3':'Se Elimino Correctamente el Juguete!!','nomUsuario' : nomUsuario}
                return render(request, "listado.html", datos)
            except:
                jugue = Juguete.objects.all().values()
                datos = {'jugue' : jugue, 'r4':'No se Pudo Eliminar el Juguete!!'}
                return render(request, "listado.html", datos)
        else:
            datos = { 'r2' : 'No Tiene Permisos Suficientes Para Acceder!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)


#FUNCION PARA MOSTRAR EL FORMULARIO DE ACTUALIZAR
def mostrarFormularioActualizar(request, id):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True:
        if nomUsuario.upper() != "ADMIN":
            jugue = Juguete.objects.get(id=id)
            encontrado = Juguete.objects.get(id=id)
            opcionesOrigen = Origen.objects.all().values().order_by("nombre_origen")
            opcionesTipo= Tipo.objects.all().values().order_by("nombre_tipo")
            datos = { 
                'nomUsuario' : request.session["nomUsuario"],
                'jugue' : jugue,
                'encontrado' : encontrado,
                'opcionesOrigen' : opcionesOrigen,
                'opcionesTipo' : opcionesTipo
            }
            return render(request, 'form_actualizar.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Permisos Suficientes Para Acceder!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)

def actualizarJuguete(request, id):
    try:
        if request.method == "POST":
            cod = request.POST['txtcod']
            nom = request.POST['txtnom']
            pre = request.POST['txtpre']
            dis = request.POST['opdis']
            ori = request.POST['cboori']
            can = request.POST['txtcan']
            tip = request.POST['cbotip']
            mar = request.POST['txtmar']

            jugue = Juguete.objects.get(id=id)
            jugue.codigo = cod
            jugue.nombre = nom
            jugue.precio = pre
            jugue.disponibilidad = dis
            jugue.origen_id = ori
            jugue.cantidad = can
            jugue.tipo_id = tip
            jugue.marca = mar
            jugue.save()

            # Se registra en la tabla historial.
            accion = "Actualización realizada ("+str(nom.lower())+")"
            tabla = "Juguete"
            fechayhora = datetime.now()
            usuario = request.session["idUsuario"]
            his = Historial(accion_historial=accion, tabla_historial=tabla, fecha_hora_historial=fechayhora, usuario_id=usuario)
            his.save()

            jugue = Juguete.objects.select_related("origen","tipo").all().order_by("nombre")
            datos = {
                'nomUsuario' : request.session["nomUsuario"],
                'jugue' : jugue,
                'r' : 'Datos De Juguetes ('+str(id)+') Modificados Correctamente!!'
            }
            return render(request, 'listado.html', datos)

        else:
            jugue = Juguete.objects.select_related("origen","tipo").all().order_by("nombre")
            datos = {
                'nomUsuario' : request.session["nomUsuario"],
                'jugue' : jugue,
                'r2' : 'El ID ('+str(id)+') No Existe. Imposible Mostrar Datos!!'
            }
            return render(request, 'listado.html', datos)

    except:
        jugue = Juguete.objects.select_related("origen","tipo").all().order_by("nombre")
        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'jugue' : jugue,
            'r2' : 'El ID ('+str(id)+') Ya Existe. Imposible Actualizar!!'
        }
        return render(request, 'listado.html', datos)



#--------------------------------------------------------------------------------

#------------------------INDEX---------------------------------

def mostrarIndex(request):
    return render(request,'index.html')

def iniciarSesion(request):
    if request.method == "POST":
        nom = request.POST["txtusu"]
        pas = request.POST["txtpas"]

        comprobarLogin = Usuario.objects.filter(nombre_usuario=nom, password_usuario=pas).values()

        if comprobarLogin:
            request.session["estadoSesion"] = True
            request.session["idUsuario"] = comprobarLogin[0]['id']
            request.session["nomUsuario"] = nom.upper()

            datos = { 'nomUsuario' : nom.upper() }


            # Se registra en la tabla historial.
            accion = "Inicia Sesión"
            tabla = ""
            fechayhora = datetime.now()
            usuario = request.session["idUsuario"]
            his = Historial(accion_historial=accion, tabla_historial=tabla, fecha_hora_historial=fechayhora, usuario_id=usuario)
            his.save()


            if nom.upper() == "ADMIN":
                return render(request, 'menu_admin.html', datos)
            else:
                return render(request, 'menu_operador.html', datos)
        
        else:
            datos = { 'r2' : 'Error De Usuario y/o Contraseña!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'No Se Puede Procesar La Solicitud!!' }
        return render(request, 'index.html', datos)

def cerrarSesion(request):
    try:

        # Se registra en la tabla historial.
        accion = "Cierra Sesión"
        tabla = ""
        fechayhora = datetime.now()
        usuario = request.session["idUsuario"]
        his = Historial(accion_historial=accion, tabla_historial=tabla, fecha_hora_historial=fechayhora, usuario_id=usuario)
        his.save()

        del request.session["estadoSesion"]
        del request.session["idUsuario"]
        del request.session["nomUsuario"]

        return render(request, 'index.html')
    except:
        return render(request, 'index.html')
#--------------------------------------------------------------------------------

#---------------------------MENU ADMIN-------------------------------

def mostrarMenuAdmin(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":
            datos = { 'nomUsuario' : nomUsuario }
            return render(request, 'menu_admin.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Permisos Suficientes Para Acceder!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)


def mostrarFormOrigen(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":

            ori = Origen.objects.all().values().order_by("nombre_origen")

            datos = { 'nomUsuario' : nomUsuario, 'ori' : ori }

            return render(request, 'form_registro_combo1.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Permisos Suficientes Para Acceder!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)

def registrarOrigen(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":
                if request.method == "POST":
                    nom = request.POST["txtori"].upper()

                    comprobarOrigen = Origen.objects.filter(nombre_origen=nom)
                    if comprobarOrigen:

                        ori = Origen.objects.all().values().order_by("nombre_origen")

                        datos = { 
                            'nomUsuario' : request.session["nomUsuario"],
                            'ori' : ori,
                            'r2' : 'El Origen ('+str(nom.upper())+') Ya Existe!!' 
                        }
                        return render(request, 'form_registro_combo1.html', datos)    

                    else:

                        ori = Origen(nombre_origen=nom)
                        ori.save()


                        # Se registra en la tabla historial.
                        accion = "Insert realizado ("+str(nom.lower())+")"
                        tabla = "Origen"
                        fechayhora = datetime.now()
                        usuario = request.session["idUsuario"]
                        his = Historial(accion_historial=accion, tabla_historial=tabla, fecha_hora_historial=fechayhora, usuario_id=usuario)
                        his.save()


                        ori = Origen.objects.all().values().order_by("nombre_origen")
                        datos = {
                            'nomUsuario' : request.session["nomUsuario"], 
                            'ori' : ori, 
                            'r' : 'Origen ('+str(nom.upper())+' )Registrado Correctamente!!!!'
                        }
                        return render(request, 'form_registro_combo1.html', datos)

                else:
                    ori = Origen.objects.all().values().order_by("nombre_origen")
                    datos = {
                        'nomUsuario' : request.session["nomUsuario"], 
                        'ori' : ori, 
                        'r2' : 'Debe Presionar El Boton Para Registrar Un Origen!!'
                    }
                    return render(request, 'form_registro_combo1.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Permisos Suficientes Para Acceder!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)

def mostrarFormActualizarOrigen(request, id):
        try:
            estadoSesion = request.session.get("estadoSesion")
            if estadoSesion is True:
                nomUsuario = request.session.get("nomUsuario")
                if nomUsuario == "ADMIN":
                    
                    encontrado = Origen.objects.get(id=id)
                    ori = Origen.objects.all().values().order_by("nombre_origen")
                    datos = {
                        'nomUsuario' : request.session["nomUsuario"],
                        'encontrado' : encontrado,
                        'ori' : ori,                    
                    }
                    return render(request, 'form_actualizar_origen.html', datos)


                else:
                    ori = Origen.objects.all().values().order_by("nombre_origen")
                    datos = {
                        'nomUsuario' : request.session["nomUsuario"],
                        'ori' : ori,
                        'r2' : 'No Tiene Los Permisos Para Realizar La Acción!!'
                    }
                    return render(request, 'form_registro_combo1.html', datos)
            
            else:

                ori = Origen.objects.all().values().order_by("nombre_origen")
                datos = {
                    'nomUsuario' : request.session["nomUsuario"],
                    'ori' : ori,
                    'r2' : 'Debe Iniciar Sesión Para Acceder!!'
                }
                return render(request, 'index.html', datos)

        except:
            ori = Origen.objects.all().values().order_by("nombre_origen")

            datos = {
                'nomUsuario' : request.session["nomUsuario"],
                'ori' : ori,
                'r2' : 'El ID ('+str(id)+') No Existe. Imposible Actualizar!!'
            }

            return render(request, 'form_registro_combo1.html', datos)

def actualizarOrigen(request, id):
    try:
        nom = request.POST["txtori"]

        ori = Origen.objects.get(id=id)
        ori.nombre_origen = nom.upper()
        ori.save()

        # Se registra en la tabla historial.
        accion = "Actualización realizada ("+str(nom.lower())+")"
        tabla = "Origen"
        fechayhora = datetime.now()
        usuario = request.session["idUsuario"]
        his = Historial(accion_historial=accion, tabla_historial=tabla, fecha_hora_historial=fechayhora, usuario_id=usuario)
        his.save()

        ori = Origen.objects.all().values().order_by("nombre_origen")

        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'ori' : ori,
            'r' : 'Datos Modificados Correctamente!!'
        }

        return render(request, 'form_registro_combo1.html', datos)

    except:
        ori = Origen.objects.all().values().order_by("nombre_origen")

        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'ori' : ori,
            'r2' : 'El ID ('+str(id)+') No Existe. Imposible Actualizar!!'
        }

        return render(request, 'form_registro_combo1.html', datos)

def eliminarOrigen(request, id):
    try:
        ori = Origen.objects.get(id=id)
        nom = ori.nombre_origen
        ori.delete()

        # Se registra en la tabla historial.
        accion = "Eliminación realizada ("+str(nom.lower())+")"
        tabla = "Origen"
        fechayhora = datetime.now()
        usuario = request.session["idUsuario"]
        his = Historial(accion_historial=accion, tabla_historial=tabla, fecha_hora_historial=fechayhora, usuario_id=usuario)
        his.save()

        ori = Origen.objects.all().values().order_by("nombre_origen")
        datos = {
            'nomUsuario' : request.session["nomUsuario"], 
            'ori' : ori, 
            'r' : 'Registro ('+str(nom.upper())+') Eliminado Correctamente!!!!'
        }
        return render(request, 'form_registro_combo1.html', datos)

    except:

        ori = Origen.objects.all().values().order_by("nombre_origen")
        datos = {
            'nomUsuario' : request.session["nomUsuario"], 
            'ori' : ori, 
            'r2' : 'El ID ('+str(id)+') No Existe. Imposible Eliminar!!'
        }
        return render(request, 'form_registro_combo1.html', datos)


#--------------------------------------------------------------------------------

def mostrarFormTipo(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":

            tip = Tipo.objects.all().values().order_by("nombre_tipo")

            datos = { 'nomUsuario' : nomUsuario, 'tip' : tip }

            return render(request, 'form_registro_combo2.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Permisos Suficientes Para Acceder!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)

def registrarTipo(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":
                if request.method == "POST":
                    nom = request.POST["txttip"].upper()

                    comprobarTipo = Tipo.objects.filter(nombre_tipo=nom)
                    if comprobarTipo:

                        tip = Tipo.objects.all().values().order_by("nombre_tipo")

                        datos = { 
                            'nomUsuario' : request.session["nomUsuario"],
                            'tip' : tip,
                            'r2' : 'El Tipo ('+str(nom.upper())+') Ya Existe!!' 
                        }
                        return render(request, 'form_registro_combo2.html', datos)    

                    else:

                        tip = Tipo(nombre_tipo=nom)
                        tip.save()


                        # Se registra en la tabla historial.
                        accion = "Insert realizado ("+str(nom.lower())+")"
                        tabla = "Tipo"
                        fechayhora = datetime.now()
                        usuario = request.session["idUsuario"]
                        his = Historial(accion_historial=accion, tabla_historial=tabla, fecha_hora_historial=fechayhora, usuario_id=usuario)
                        his.save()


                        tip = Tipo.objects.all().values().order_by("nombre_tipo")
                        datos = {
                            'nomUsuario' : request.session["nomUsuario"], 
                            'tip' : tip, 
                            'r' : 'Tipo ('+str(nom.upper())+' ) Registrado Correctamente!!!!'
                        }
                        return render(request, 'form_registro_combo2.html', datos)

                else:
                    tip = Tipo.objects.all().values().order_by("nombre_tipo")
                    datos = {
                        'nomUsuario' : request.session["nomUsuario"], 
                        'tip' : tip, 
                        'r2' : 'Debe Presionar El Boton Para Registrar Un Tipo!!'
                    }
                    return render(request, 'form_registro_combo2.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Permisos Suficientes Para Acceder!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)

def mostrarFormActualizarTipo(request, id):
        try:
            estadoSesion = request.session.get("estadoSesion")
            if estadoSesion is True:
                nomUsuario = request.session.get("nomUsuario")
                if nomUsuario == "ADMIN":
                    
                    encontrado = Tipo.objects.get(id=id)
                    tip = Tipo.objects.all().values().order_by("nombre_tipo")
                    datos = {
                        'nomUsuario' : request.session["nomUsuario"],
                        'encontrado' : encontrado,
                        'tip' : tip,                    
                    }
                    return render(request, 'form_actualizar_tipo.html', datos)


                else:
                    tip = Tipo.objects.all().values().order_by("nombre_tipo")
                    datos = {
                        'nomUsuario' : request.session["nomUsuario"],
                        'tip' : tip,
                        'r2' : 'No Tiene Los Permisos Para Realizar La Acción!!'
                    }
                    return render(request, 'form_registro_combo2.html', datos)
            
            else:

                tip = Tipo.objects.all().values().order_by("nombre_tipo")
                datos = {
                    'nomUsuario' : request.session["nomUsuario"],
                    'tip' : tip,
                    'r2' : 'Debe Iniciar Sesión Para Acceder!!'
                }
                return render(request, 'index.html', datos)

        except:
            tip = Tipo.objects.all().values().order_by("nombre_tipo")

            datos = {
                'nomUsuario' : request.session["nomUsuario"],
                'tip' : tip,
                'r2' : 'El ID ('+str(id)+') No Existe. Imposible Actualizar!!'
            }

            return render(request, 'form_registro_combo2.html', datos)

def actualizarTipo(request, id):
    try:
        nom = request.POST["txttip"]

        tip = Tipo.objects.get(id=id)
        tip.nombre_tipo = nom.upper()
        tip.save()

        # Se registra en la tabla historial.
        accion = "Actualización realizada ("+str(nom.lower())+")"
        tabla = "Tipo"
        fechayhora = datetime.now()
        usuario = request.session["idUsuario"]
        his = Historial(accion_historial=accion, tabla_historial=tabla, fecha_hora_historial=fechayhora, usuario_id=usuario)
        his.save()

        tip = Tipo.objects.all().values().order_by("nombre_tipo")

        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'tip' : tip,
            'r' : 'Datos Modificados Correctamente!!'
        }

        return render(request, 'form_registro_combo2.html', datos)

    except:
        tip = Tipo.objects.all().values().order_by("nombre_tipo")

        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'tip' : tip,
            'r2' : 'El ID ('+str(id)+') No Existe. Imposible Actualizar!!'
        }

        return render(request, 'form_registro_combo2.html', datos)

def eliminarTipo(request, id):
    try:
        tip = Tipo.objects.get(id=id)
        nom = tip.nombre_tipo
        tip.delete()

        # Se registra en la tabla historial.
        accion = "Eliminación realizada ("+str(nom.lower())+")"
        tabla = "Tipo"
        fechayhora = datetime.now()
        usuario = request.session["idUsuario"]
        his = Historial(accion_historial=accion, tabla_historial=tabla, fecha_hora_historial=fechayhora, usuario_id=usuario)
        his.save()

        tip = Tipo.objects.all().values().order_by("nombre_tipo")
        datos = {
            'nomUsuario' : request.session["nomUsuario"], 
            'tip' : tip, 
            'r' : 'Registro ('+str(nom.upper())+') Eliminado Correctamente!!!!'
        }
        return render(request, 'form_registro_combo2.html', datos)

    except:

        tip = Tipo.objects.all().values().order_by("nombre_tipo")
        datos = {
            'nomUsuario' : request.session["nomUsuario"], 
            'tip' : tip, 
            'r2' : 'El ID ('+str(id)+') No Existe. Imposible Eliminar!!'
        }
        return render(request, 'form_registro_combo2.html', datos)

#----------------------------------------------------------------------

def mostrarListarHistorial(request):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            if request.session["nomUsuario"].upper() == "ADMIN":
                his = Historial.objects.select_related("usuario").all().order_by("-fecha_hora_historial")
                datos = {
                    'nomUsuario' : request.session["nomUsuario"],
                    'his' : his
                }
                return render(request, 'listar_historial.html', datos)

            else:
                datos = { 'r2' : 'No Tiene Permisos Suficientes Para Acceder!!' }
                return render(request, 'index.html', datos)

        else:
            datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
            return render(request, 'index.html', datos)

    except:
        datos = { 'r2' : 'Error Al Obtener Historial!!' }
        return render(request, 'index.html', datos)
