import sys
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.db import transaction
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

from odontologico.forms import PersonaForm, TratamientoForm, HorarioHoraForm
from odontologico.funciones import add_data_aplication
from odontologico.models import Paciente, PersonaPerfil, Persona, Tratamiento, Horario_hora


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def view_horas_atencion(request):
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

            if peticion == 'add_horario':
                try:
                    form = HorarioHoraForm(request.POST, request.FILES)
                    if form.is_valid():
                        hora_inicio = form.cleaned_data['hora_inicio']
                        hora_fin = form.cleaned_data['hora_fin']
                        activo = form.cleaned_data['activo']

                        horario = Horario_hora(
                            hora_inicio=hora_inicio,
                            hora_fin=hora_fin,
                            activo=activo
                        )

                        horario.save(request)

                        return JsonResponse({"respuesta": True, "mensaje": "Registro guardado correctamente."})
                    else:
                       return JsonResponse(  {"respuesta": False, "mensaje": "Ha ocurrido un error al enviar los datos."})


                except Exception as ex:
                   transaction.set_rollback(True)
                   return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'edit_horario':
                try:
                    form = HorarioHoraForm(request.POST, request.FILES)
                    if form.is_valid():
                        horario = Horario_hora.objects.get(pk=request.POST['id'])
                        horario.hora_inicio = request.POST['hora_inicio']
                        horario.hora_fin = request.POST['hora_fin']
                        try:
                            if request.POST['activo'] == 'on':
                                valor =True
                            else:
                                valor =False
                        except:
                            valor = False
                        horario.activo = valor
                        horario.save(request)
                        return JsonResponse({"respuesta": True, "mensaje": "Registro Modificado correctamente."})


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'eliminar_horario':
                try:
                    with transaction.atomic():
                        registro = Horario_hora.objects.get(pk=request.POST['id'])
                        registro.status = False
                        registro.save(request)
                        return JsonResponse({"respuesta": True, "mensaje": "Registro eliminado correctamente."})

                except Exception as ex:
                    pass
        return JsonResponse({"respuesta": False, "mensaje": "acción Incorrecta."})
    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']
            if peticion == 'add_horario':
                try:
                    data['titulo'] = 'Agregar nuevo horario'
                    data['titulo_formulario'] = 'Formulario de registro de horarios'
                    data['peticion'] = 'add_horario'
                    form = HorarioHoraForm()
                    data['form'] = form
                    return render(request, "horario/add_horario.html", data)
                except Exception as ex:
                    transaction.set_rollback(True)
                    pass

            if peticion == 'edit_horario':
                try:
                    data['titulo'] = 'Editar horario'
                    data['titulo_formulario'] = 'Formulario de editar horario'
                    data['peticion'] = 'edit_horario'
                    data['horario'] = horario = Horario_hora.objects.get(pk=request.GET['id'])
                    form = HorarioHoraForm(initial={
                        'hora_inicio':horario.hora_inicio,
                        'hora_fin': horario.hora_fin,
                        'activo': horario.activo,

                    })
                    data['form'] = form
                    return render(request, "horario/edit_horario.html", data)
                except Exception as ex:
                    pass

        else:
            try:
                data['titulo'] = 'Horarios de Atención'
                data['titulo_tabla'] = 'Lista  de horarios disponibles'
                data['persona_logeado'] = persona_logeado
                lista = Horario_hora.objects.filter(status=True).order_by('id')
                paginator = Paginator(lista, 15)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                data['page_obj'] = page_obj
                return render(request, "horario/view.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
