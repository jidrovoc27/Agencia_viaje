import sys
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

from odontologico.forms import PersonaForm, AgendarCitaForm, AgendarCitaOnlineForm
from odontologico.funciones import add_data_aplication
from odontologico.models import PersonaPerfil, Persona, Asistente, AgendarCita, Paciente


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def view_agendar_cita_online(request):
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
                    form = AgendarCitaOnlineForm(request.POST, request.FILES)

                    if form.is_valid():
                        existe_cita_agendada = False
                        if AgendarCita.objects.filter(status=True, estado_cita=2, horario=form.cleaned_data['hora_cita'], fecha=form.cleaned_data['fecha_cita'],doctor=form.cleaned_data['doctor']).exists():
                            existe_cita_agendada = True

                        if existe_cita_agendada:
                            return JsonResponse({"respuesta": False, "mensaje": "Lo siento, no esta disponible ese horario."})


                        paciente = Paciente.objects.get(persona = persona_logeado, status = True)
                        doctor = form.cleaned_data['doctor']
                        fecha_cita = form.cleaned_data['fecha_cita']
                        hora_cita = form.cleaned_data['hora_cita']

                        cita = AgendarCita(
                            paciente=paciente,
                            doctor=doctor,
                            fecha=fecha_cita,
                            horario=hora_cita,
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
                    form = AgendarCitaOnlineForm()
                    data['form'] = form
                    return render(request, "agendar_cita/add_cita_online.html", data)
                except Exception as ex:
                    transaction.set_rollback(True)
                    pass


        else:
            try:
                data['titulo'] = 'Agendar Cita'
                data['titulo_tabla'] = 'Mis citas médicas'
                data['persona_logeado'] = persona_logeado
                if persona_logeado == 'SUPERADMINISTRADOR':
                    lista =None
                    data['existe_cita_medica_pendiente'] =True
                    data['page_obj'] = None
                else:
                    lista = AgendarCita.objects.filter(status=True,paciente__persona = persona_logeado ).order_by('id')
                    data['existe_cita_medica_pendiente'] =  existe_cita_medica_pendiente = AgendarCita.objects.filter(status=True,paciente__persona = persona_logeado ,estado_cita = 2).exists()
                    paginator = Paginator(lista, 15)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    data['page_obj'] = page_obj
                return render(request, "agendar_cita/view_cita_online.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
