import os
import sys
from io import StringIO

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.staticfiles import finders
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.db import transaction
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from xhtml2pdf import pisa

from aplication import settings
from aplication.settings import BASE_DIR
from odontologico.forms import PersonaForm, ConsultaForm, AbonarCuotaForm, DocumentoForm
from odontologico.funciones import add_data_aplication
from odontologico.models import *

def create_mail(user_mail, subject, template_name, context):
    template = get_template(template_name)
    content = template.render(context)

    message = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[
            user_mail
        ],
        cc=[]
    )

    message.attach_alternative(content, 'text/html')
    return message
def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    path_uri = str(BASE_DIR) + str(uri)
    result = finders.find(path_uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path




def render_pdf_view(template_paths,data):
    template_path = template_paths
    context = data
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="factura.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def view_paciente(request):
    global ex
    data = {}
    add_data_aplication(request, data)
    usuario_logeado = request.user
    if Persona.objects.filter(usuario=usuario_logeado, status=True).exists():
        persona_logeado = Persona.objects.get(usuario=usuario_logeado, status=True)
    else:
        persona_logeado = 'SUPERADMINISTRADOR'

    if request.method == 'POST':
        if 'peticion' in request.POST:
            peticion = request.POST['peticion']

            if peticion == 'add_cliente':
                try:
                    form = PersonaForm(request.POST, request.FILES)
                    if form.is_valid():

                        campos_repetidos = list()

                        if Persona.objects.values('id').filter(cedula=form.cleaned_data['cedula'], status=True).exists():
                            campos_repetidos.append(form['cedula'].name)
                        if Persona.objects.values('id').filter(email=form.cleaned_data['email'], status=True).exists():
                            campos_repetidos.append(form['email'].name)
                        if campos_repetidos:
                            return JsonResponse(
                                {"respuesta": False, "mensaje": "registro ya existe.", 'repetidos': campos_repetidos})
                        username = form.cleaned_data['nombres']
                        password = form.cleaned_data['nombres'].replace(' ','')
                        nombres = form.cleaned_data['nombres']
                        # nombre2 = form.cleaned_data['nombre2']
                        apellidos = form.cleaned_data['apellidos']
                        # apellido2 = form.cleaned_data['apellido2']
                        cedula = form.cleaned_data['cedula']
                        genero = form.cleaned_data['genero']
                        ciudad = form.cleaned_data['ciudad']
                        direccion = form.cleaned_data['direccion']
                        referencia = form.cleaned_data['referencia']
                        telefono_movil = form.cleaned_data['telefono_movil']
                        telefono_convencional = form.cleaned_data['telefono_convencional']
                        email = form.cleaned_data['email']
                        username = form.cleaned_data['nombres'].replace(' ','').lower()  # Eliminar espacios y líneas nuevas
                        password = password.lower()
                        usuario = User.objects.create_user(username, email, password)
                        usuario.save()

                        grupo = Group.objects.get(pk=4)  # PACIENTE
                        grupo.user_set.add(usuario)

                        persona = Persona(
                            usuario=usuario,
                            nombres=nombres,
                            # nombre2=nombre2,
                            apellidos=apellidos,
                            # apellido2=apellido2,
                            email=email,
                            cedula=cedula,
                            genero=genero,
                            telefono_movil=telefono_movil,
                            telefono_convencional=telefono_convencional,
                            ciudad=ciudad,
                            direccion=direccion,
                            referencia=referencia
                        )
                        persona.save(request)

                        persona_perfil = PersonaPerfil(
                            persona=persona,
                            is_paciente=True
                        )

                        persona_perfil.save(request)

                        paciente = Paciente(
                            persona=persona
                        )
                        paciente.save(request)
                        return JsonResponse({"respuesta": True, "mensaje": "Registro guardado correctamente."})
                    else:
                       return JsonResponse(  {"respuesta": False, "mensaje": "Ha ocurrido un error al enviar los datos."})


                except Exception as ex:
                   transaction.set_rollback(True)
                   return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'edit_paciente':
                try:
                    form = PersonaForm(request.POST, request.FILES)
                    if form.is_valid():
                        paciente = Paciente.objects.get(pk=request.POST['id'])
                        persona = Persona.objects.get(pk = paciente.persona_id)
                        persona.nombre1 =request.POST['nombre1']
                        persona.nombre2 =request.POST['nombre2']
                        persona.apellido1=request.POST['apellido1']
                        persona.apellido2=request.POST['apellido2']
                        persona.email=request.POST['email']
                        persona.cedula=request.POST['cedula']
                        persona.genero_id=request.POST['genero']
                        persona.ciudad=request.POST['ciudad']
                        persona.direccion=request.POST['direccion']
                        persona.referencia=request.POST['referencia']
                        persona.telefono_movil=request.POST['telefono_movil']
                        persona.telefono_convencional=request.POST['telefono_convencional']
                        persona.save(request)
                        return JsonResponse({"respuesta": True, "mensaje": "Registro Modificado correctamente."})


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'abonar_cuota':
                try:
                    form = AbonarCuotaForm(request.POST, request.FILES)
                    if form.is_valid():
                        abono = form.cleaned_data['abono']
                        consulta = Consulta.objects.get(pk=request.POST['id'])
                        if not abono > consulta.obtener_saldo_pendiente():
                            abono = AbonoPago(
                                consulta=consulta,
                                abono=abono,

                            )
                            abono.save(request)

                        if consulta.obtener_saldo_pendiente() == 0:
                            consulta.cancelado = True
                            consulta.save(request)

                        return redirect('/pacientes/?peticion=consultas_realizadas&id=%s' % consulta.paciente_id)


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})


            if peticion == 'eliminar_paciente':
                try:
                    with transaction.atomic():
                        registro = Paciente.objects.get(pk=request.POST['id'])
                        persona = Persona.objects.get(pk=registro.persona_id)
                        persona.status = False
                        persona.save()
                        registro.status = False
                        registro.save(request)
                        return JsonResponse({"respuesta": True, "mensaje": "Registro eliminado correctamente."})

                except Exception as ex:
                    pass

            if peticion == 'add_documento':
                try:
                    form = DocumentoForm(request.POST, request.FILES)
                    archivo = None
                    if form.is_valid():
                        if 'archivo' in request.FILES:
                            archivo = request.FILES['archivo']
                        registrodocumento = Documentos(nombre=form.cleaned_data['nombre'],
                                                       archivo=archivo,
                                                       paciente_id=int(request.POST['id']))
                        registrodocumento.save()
                    return redirect('/pacientes/?peticion=submenu_documentos&id=%s' % request.POST['id'])
                except Exception as ex:
                    pass
        return JsonResponse({"respuesta": False, "mensaje": "acción Incorrecta."})
    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']
            if peticion == 'add_cliente':
                try:
                    data['titulo'] = 'Agregar nuevo cliente'
                    data['titulo_formulario'] = 'Formulario de registro de cliente'
                    data['peticion'] = 'add_cliente'
                    form = PersonaForm()
                    data['form'] = form
                    return render(request, "paciente/add_paciente.html", data)
                except Exception as ex:
                    transaction.set_rollback(True)
                    pass

            if peticion == 'consultas_realizadas':
                try:
                    data['titulo'] = 'Consultas realizadas'
                    data['titulo_formulario'] = 'Odontograma'
                    data['peticion'] = 'consultas_realizadas'
                    lista = Consulta.objects.filter(status=True,paciente__id = request.GET['id'])
                    paginator = Paginator(lista, 15)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    data['page_obj'] = page_obj
                    return render(request, "paciente/consultas_realizadas.html", data)
                except Exception as ex:
                    transaction.set_rollback(True)
                    pass

            if peticion == 'historial_clinico':
                try:
                    data['titulo'] = 'Historial clínico'
                    data['paciente_id'] = paciente_id = request.GET['id']
                    data['datos_paciente'] = Paciente.objects.get(id=paciente_id)
                    return render(request, "paciente/menu_historial_clinico/datos_paciente.html", data)
                except Exception as ex:
                    transaction.set_rollback(True)
                    pass

            if peticion == 'submenu_consultasrealizadas':
                try:
                    data['titulo'] = 'Historial clínico'
                    data['titulo_tabla'] = 'Consultas realizadas'
                    data['paciente_id'] = paciente_id = request.GET['id']
                    lista = Consulta.objects.filter(status=True, paciente__id=request.GET['id'], odontograma__tipo=2)
                    paginator = Paginator(lista, 15)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    data['page_obj'] = page_obj
                    return render(request, "paciente/menu_historial_clinico/consultas_realizadas.html", data)
                except Exception as ex:
                    transaction.set_rollback(True)
                    pass

            if peticion == 'submenu_tratamientos':
                try:
                    data['titulo'] = 'Historial clínico'
                    data['titulo_tabla'] = 'Tratamientos realizados'
                    data['paciente_id'] = paciente_id = request.GET['id']
                    lista_consultas = Consulta.objects.filter(status=True, paciente__id=request.GET['id']).values_list('id')
                    lista_tratamientosrealizados = ConsultaTratamientoPaciente.objects.filter(status=True, consultas_id__in=lista_consultas)
                    paginator = Paginator(lista_tratamientosrealizados, 15)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    data['page_obj'] = page_obj
                    return render(request, "paciente/menu_historial_clinico/tratamientos_realizados.html", data)
                except Exception as ex:
                    transaction.set_rollback(True)
                    pass

            if peticion == 'submenu_consulta_odontograma':
                try:
                    data['titulo'] = 'Historial clínico'
                    data['paciente_id'] = paciente_id = request.GET['id']
                    data['consulta'] = consulta = Consulta.objects.get(pk=request.GET['idconsulta'])
                    data['histoColores'] = odontograma = consulta.odontograma
                    return render(request, "paciente/menu_historial_clinico/consulta_odontograma.html", data)
                except Exception as ex:
                    transaction.set_rollback(True)
                    pass

            if peticion == 'submenu_odontograma_general':
                try:
                    data['titulo'] = 'Historial clínico'
                    data['paciente_id'] = paciente_id = request.GET['id']
                    odontograma = Odontograma.objects.filter(paciente_id=paciente_id, tipo=1, status=True)
                    data['tieneodontogramaprincipal'] = False
                    if odontograma:
                        data['histoColores'] = odontograma[0]
                        data['tieneodontogramaprincipal'] = True
                    return render(request, "paciente/menu_historial_clinico/odontograma_general.html", data)
                except Exception as ex:
                    transaction.set_rollback(True)
                    pass

            if peticion == 'submenu_documentos':
                try:
                    data['titulo'] = 'Documentos'
                    data['titulo_tabla'] = 'Documentos'
                    data['paciente_id'] = paciente_id = request.GET['id']
                    lista = Documentos.objects.filter(paciente_id=paciente_id, status=True)
                    paginator = Paginator(lista, 15)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    data['page_obj'] = page_obj
                    return render(request, "paciente/menu_historial_clinico/documentos.html", data)
                except Exception as ex:
                    transaction.set_rollback(True)
                    pass

            if peticion == 'add_documento':
                try:
                    form = DocumentoForm()
                    data['paciente_id'] = paciente_id = int(request.GET['paciente_id'])
                    data['form'] = form
                    data['peticion'] = 'add_documento'
                    template = get_template('paciente/menu_historial_clinico/modal/formadddocumento.html')
                    return JsonResponse({"result": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            if peticion == 'edit_paciente':
                try:
                    data['titulo'] = 'Editar paciente'
                    data['titulo_formulario'] = 'Formulario de editar paciente'
                    data['peticion'] = 'edit_paciente'
                    data['paciente'] = paciente = Paciente.objects.get(pk=request.GET['id'])
                    form = PersonaForm(initial={
                        'nombre1':paciente.persona.nombre1,
                        'nombre2': paciente.persona.nombre2,
                        'apellido1': paciente.persona.apellido1,
                        'apellido2': paciente.persona.apellido2,
                        'email': paciente.persona.email,
                        'cedula': paciente.persona.cedula,
                        'genero': paciente.persona.genero,
                        'ciudad':paciente.persona.ciudad,
                        'direccion':paciente.persona.direccion,
                        'referencia':paciente.persona.referencia,
                        'telefono_movil': paciente.persona.telefono_movil,
                        'telefono_convencional': paciente.persona.telefono_convencional
                    })
                    form.editar()
                    data['form'] = form
                    return render(request, "paciente/edit_paciente.html", data)
                except Exception as ex:
                    pass

            if peticion == 'ver_odontograma':
                try:
                    data['titulo'] = 'Ver consulta'
                    data['titulo_formulario'] = 'Ver consulta'
                    data['consulta'] = consulta = Consulta.objects.get(pk=request.GET['id'])
                    data['histoColores'] = odontograma= consulta.odontograma

                    return render(request, "paciente/ver_consulta.html", data)
                except Exception as ex:
                    pass

            if peticion == 'ver_factura':
                try:
                    data['titulo'] = 'Ver factura'
                    data['factura'] = factura = Consulta.objects.get(pk=request.GET['id'])

                    return render(request, "paciente/ver_factura.html", data)
                except Exception as ex:
                    pass

            if peticion == 'descargar_factura':
                try:
                    data['titulo'] = 'factura'
                    data['factura'] = factura = Consulta.objects.get(pk=request.GET['id'])

                    return render_pdf_view('paciente/factura_pdf.html', data)
                except Exception as ex:
                    pass

            if peticion == 'generar_certificado':
                try:
                    # data['titulo'] = 'factura'
                    # data['factura'] = factura = Consulta.objects.get(pk=request.GET['id'])

                    return render_pdf_view('paciente/certificado_medico.html', data)
                except Exception as ex:
                    pass

            if peticion == 'enviar_factura':

                try:
                    from django.conf import settings
                    from django.core.mail import send_mail
                    factura = Consulta.objects.get(pk=request.GET['id'])
                    mail = create_mail(
                        factura.paciente.persona.email,
                        'Esta es tu factura por la consulta realizada en el centro odontologico',
                        'factura.html',
                        {
                            'factura': factura
                        }
                    )

                    mail.send(fail_silently=False)

                    return JsonResponse({"respuesta": True, "mensaje": "Factura enviado correctamente."})
                except Exception as ex:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))


            if peticion == 'descargar_odontograma':
                try:
                    data['titulo'] = 'Ver consulta'
                    data['titulo_formulario'] = 'Ver consulta'
                    data['consulta'] = consulta = Consulta.objects.get(pk=request.GET['id'])
                    data['histoColores'] = odontograma = consulta.odontograma

                    return render(request, 'paciente/odontograma_pdf.html', data)
                except Exception as ex:
                    pass

            if peticion == 'historial_abono_cuota':
                try:
                    data['historial_abono'] = historial_abono = AbonoPago.objects.filter(status=True,consulta_id= request.GET['id'])
                    data['consulta'] = Consulta.objects.get(pk= request.GET['id'])
                    template = get_template("paciente/modal/historial_abono.html")
                    return JsonResponse({"respuesta": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            if peticion == 'abonar_cuota':
                try:
                    data['consulta'] = consulta = Consulta.objects.get(pk=request.GET['id'])
                    form = AbonarCuotaForm()
                    data['form'] = form
                    data['peticion'] = 'abonar_cuota'
                    template = get_template("paciente/modal/formAbonarCuota.html")
                    return JsonResponse({"respuesta": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            if peticion == 'enviar_correo':
                try:
                    from django.conf import settings
                    from django.core.mail import send_mail

                    send_mail(
                        'Título del correo',
                        'Hola, este correo es enviado desde un post en PyWombat. 🐍',
                        settings.EMAIL_HOST_USER,
                        ['nelson-emelec@live.com'],
                        fail_silently=False
                    )
                except Exception as ex:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

            if peticion == 'validar_cedula':
                cedula = request.GET['cedula']
                persona = Persona.objects.filter(status=True, cedula=cedula)
                if persona.exists():
                    return JsonResponse({"respuesta": True, 'mensaje': 'Cédula ya existe'})
                else:
                    return JsonResponse({"respuesta": False, 'mensaje': ''})

            if peticion == 'validar_usuario':
                usuario = request.GET['usuario']
                persona = User.objects.filter(username=usuario)
                if persona.exists():
                    return JsonResponse({"respuesta": True, 'mensaje': 'Usuario ya existe'})
                else:
                    return JsonResponse({"respuesta": False, 'mensaje': ''})

            if peticion == 'validar_email':
                correo = request.GET['email']
                email = Persona.objects.filter(email=correo, status=True)
                if email.exists():
                    return JsonResponse({"respuesta": True, 'mensaje': 'Email ya existe'})
                else:
                    return JsonResponse({"respuesta": False, 'mensaje': ''})


        else:
            try:
                data['titulo'] = 'Clientes'
                data['titulo_tabla'] = 'Lista  de Clientes'
                data['persona_logeado'] = persona_logeado
                lista = Paciente.objects.filter(status=True).order_by('id')
                paginator = Paginator(lista, 15)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                data['page_obj'] = page_obj
                return render(request, "paciente/view.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
