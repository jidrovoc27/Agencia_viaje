import sys
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.db import transaction
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

from odontologico.forms import PersonaForm, TratamientoForm
from odontologico.funciones import add_data_aplication
from odontologico.models import Paciente, PersonaPerfil, Persona, Tratamiento


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def view_tratamiento(request):
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

            if peticion == 'add_tratamiento':
                try:
                    form = TratamientoForm(request.POST, request.FILES)
                    if form.is_valid():

                        campos_repetidos = list()

                        if Tratamiento.objects.values('id').filter(nombre=form.cleaned_data['nombre'], status=True).exists():
                            campos_repetidos.append(form['nombre'].name)

                        if campos_repetidos:
                            return JsonResponse(
                                {"respuesta": False, "mensaje": "registro ya existe.", 'repetidos': campos_repetidos})

                        nombre = form.cleaned_data['nombre']
                        costo = form.cleaned_data['costo']
                        descripcion = form.cleaned_data['descripcion']


                        tratamiento = Tratamiento(
                            nombre=nombre,
                            costo=costo,
                            descripcion = descripcion
                        )

                        tratamiento.save(request)

                        return JsonResponse({"respuesta": True, "mensaje": "Registro guardado correctamente."})
                    else:
                       return JsonResponse(  {"respuesta": False, "mensaje": "Ha ocurrido un error al enviar los datos."})


                except Exception as ex:
                   transaction.set_rollback(True)
                   return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'edit_tratamiento':
                try:
                    form = TratamientoForm(request.POST, request.FILES)
                    if form.is_valid():
                        tratamiento = Tratamiento.objects.get(pk=request.POST['id'])
                        tratamiento.nombre = request.POST['nombre']
                        tratamiento.costo = request.POST['costo']
                        tratamiento.descripcion = request.POST['descripcion']
                        tratamiento.save(request)
                        return JsonResponse({"respuesta": True, "mensaje": "Registro Modificado correctamente."})


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'eliminar_tratamiento':
                try:
                    with transaction.atomic():
                        registro = Tratamiento.objects.get(pk=request.POST['id'])
                        registro.status = False
                        registro.save(request)
                        return JsonResponse({"respuesta": True, "mensaje": "Registro eliminado correctamente."})

                except Exception as ex:
                    pass
        return JsonResponse({"respuesta": False, "mensaje": "acción Incorrecta."})
    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']
            if peticion == 'add_tratamiento':
                try:
                    data['titulo'] = 'Agregar nuevo tratamiento'
                    data['titulo_formulario'] = 'Formulario de registro de tratamiento'
                    data['peticion'] = 'add_tratamiento'
                    form = TratamientoForm()
                    data['form'] = form
                    return render(request, "tratamiento/add_tratamiento.html", data)
                except Exception as ex:
                    transaction.set_rollback(True)
                    pass

            if peticion == 'edit_tratamiento':
                try:
                    data['titulo'] = 'Editar tratamiento'
                    data['titulo_formulario'] = 'Formulario de editar tratamiento'
                    data['peticion'] = 'edit_tratamiento'
                    data['tratamiento'] = tratamiento = Tratamiento.objects.get(pk=request.GET['id'])
                    form = TratamientoForm(initial={
                        'nombre':tratamiento.nombre,
                        'costo': tratamiento.costo,
                        'descripcion': tratamiento.descripcion,

                    })
                    data['form'] = form
                    return render(request, "tratamiento/edit_tratamiento.html", data)
                except Exception as ex:
                    pass

        else:
            try:
                data['titulo'] = 'Tratamientos'
                data['titulo_tabla'] = 'Lista  de tratamientos'
                data['persona_logeado'] = persona_logeado
                lista = Tratamiento.objects.filter(status=True).order_by('id')
                paginator = Paginator(lista, 15)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                data['page_obj'] = page_obj
                return render(request, "tratamiento/view.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
