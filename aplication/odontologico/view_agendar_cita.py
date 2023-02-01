import sys
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

from odontologico.forms import PersonaForm, AgendarCitaForm
from odontologico.funciones import add_data_aplication
from odontologico.models import PersonaPerfil, Persona, Asistente, AgendarCita


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def view_agendar_cita(request):
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

            if peticion == 'add_cita':
                try:
                    form = AgendarCitaForm(request.POST, request.FILES)
                    if form.is_valid():
                        paciente = form.cleaned_data['paciente']
                        doctor = form.cleaned_data['doctor']
                        fecha_cita = form.cleaned_data['fecha_cita']
                        hora_cita = form.cleaned_data['hora_cita']
                        descripcion = form.cleaned_data['descripcion']

                        cita = AgendarCita(
                            paciente=paciente,
                            doctor=doctor,
                            fecha=fecha_cita,
                            horario=hora_cita,
                            descripcion=descripcion,
                            estado_cita = 2 #estado pendiente
                        )
                        cita.save(request)


                        return JsonResponse({"respuesta": True, "mensaje": "Registro guardado correctamente."})
                    else:
                        return JsonResponse(
                            {"respuesta": False, "mensaje": "Ha ocurrido un error al enviar los datos."})


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'edit_cita':
                try:
                    form = AgendarCitaForm(request.POST, request.FILES)
                    if form.is_valid():
                        cita = AgendarCita.objects.get(pk=request.POST['id'])
                        cita.paciente = form.cleaned_data['paciente']
                        cita.doctor = form.cleaned_data['doctor']
                        cita.fecha = form.cleaned_data['fecha_cita']
                        cita.horario = form.cleaned_data['hora_cita']
                        cita.descripcion = form.cleaned_data['descripcion']
                        cita.save(request)
                        return JsonResponse({"respuesta": True, "mensaje": "Registro Modificado correctamente."})


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'eliminar_cita':
                try:
                    with transaction.atomic():
                        registro = AgendarCita.objects.get(pk=request.POST['id'])
                        registro.status = False
                        registro.save(request)
                        return JsonResponse({"respuesta": True, "mensaje": "Registro eliminado correctamente."})

                except Exception as ex:
                    pass

            if peticion == 'anular_cita':
                try:
                    with transaction.atomic():
                        registro = AgendarCita.objects.get(pk=request.POST['id'])
                        registro.estado_cita = 3
                        registro.save(request)
                        return JsonResponse({"respuesta": True, "mensaje": "Cita anulada correctamente."})

                except Exception as ex:
                    pass
        return JsonResponse({"respuesta": False, "mensaje": "acción Incorrecta."})
    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']

            if peticion == 'add_cita':
                try:
                    data['titulo'] = 'Agendar nueva cita'
                    data['titulo_formulario'] = 'Formulario de registro de citas'
                    data['peticion'] = 'add_cita'
                    data['persona_logeado'] = persona_logeado
                    form = AgendarCitaForm()
                    data['form'] = form
                    return render(request, "agendar_cita/add_cita.html", data)
                except Exception as ex:
                    transaction.set_rollback(True)
                    pass

            if peticion == 'edit_cita':
                try:
                    data['titulo'] = 'Editar cita'
                    data['titulo_formulario'] = 'Formulario de editar cita'
                    data['peticion'] = 'edit_cita'
                    data['persona_logeado'] = persona_logeado
                    data['cita'] = cita = AgendarCita.objects.get(pk=request.GET['id'])
                    form = AgendarCitaForm(initial={
                        'paciente': cita.paciente,
                        'doctor': cita.doctor,
                        'fecha_cita': cita.fecha,
                        'hora_cita': cita.horario,
                        'descripcion' : cita.descripcion

                    })
                    form.editar()
                    data['form'] = form
                    return render(request, "agendar_cita/edit_cita.html", data)
                except Exception as ex:
                    pass

            if peticion == 'enviar_correo':
                try:
                    from django.conf import settings
                    from django.core.mail import send_mail
                    data['cita'] = cita = AgendarCita.objects.get(pk=request.GET['id'])

                    titulo_del_correo =  'RECORDATORIO / CITA MÉDICA / ODONTÓLOGO :)'
                    cuerpo_del_correo =  'Hola, este es un correo enviado por el sistema odontologico, se le recuerda que tiene una cita planificada para la fecha: %s y horario : %s.  Por favor no contestar a este correo.' %(cita.fecha, cita.horario)
                    send_mail(
                        titulo_del_correo,
                        cuerpo_del_correo,
                        settings.EMAIL_HOST_USER,
                        [cita.paciente.persona.email],
                        fail_silently=False
                    )
                    return JsonResponse({"respuesta": True, "mensaje": "recordatorio enviado correctamente."})
                except Exception as ex:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

        else:
            try:
                data['titulo'] = 'Agendar Cita'
                data['titulo_tabla'] = 'Lista  de citas'
                data['persona_logeado'] = persona_logeado
                lista = AgendarCita.objects.filter(status=True).order_by('id')
                paginator = Paginator(lista, 15)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                data['page_obj'] = page_obj
                return render(request, "agendar_cita/view.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
