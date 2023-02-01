import sys
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

from aplication.settings import MEDIA_URL
from odontologico.forms import ModuloForm
from odontologico.funciones import add_data_aplication
from odontologico.models import Modulo, Persona


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def view_modulo(request):
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
            if peticion == 'add_modulo':
                try:
                    form = ModuloForm(request.POST, request.FILES)
                    if form.is_valid():
                        campos_repetidos = list()

                        if Modulo.objects.values('id').filter(nombre=form.cleaned_data['nombre']).exists():
                            campos_repetidos.append(form['nombre'].name)
                        if Modulo.objects.values('id').filter(ruta=form.cleaned_data['ruta']).exists():
                            campos_repetidos.append(form['ruta'].name)
                        if campos_repetidos:
                            return JsonResponse({"respuesta": False, "mensaje": "registro ya existe.",'repetidos':campos_repetidos})
                        modulo = Modulo(
                            nombre=form.cleaned_data['nombre'],
                            descripcion=form.cleaned_data['descripcion'],
                            icono=form.cleaned_data['icono'],
                            ruta=form.cleaned_data['ruta'],
                            activo=form.cleaned_data['activo']
                        )
                        modulo.save(request)
                        return JsonResponse({"respuesta": True, "mensaje": "Registro guardado correctamente."})

                    else:
                        return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error al enviar los datos."})

                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'edit_modulo':
                try:
                    form = ModuloForm(request.POST, request.FILES)
                    form.editar()
                    if form.is_valid():
                        campos_repetidos = list()
                        if Modulo.objects.values('id').filter(nombre=form.cleaned_data['nombre']).exclude(pk=request.POST['id']).exists():
                            campos_repetidos.append(form['nombre'].name)
                        if Modulo.objects.values('id').filter(ruta=form.cleaned_data['ruta']).exclude(pk=request.POST['id']).exists():
                            campos_repetidos.append(form['ruta'].name)
                        if campos_repetidos:
                            return JsonResponse({"respuesta": False, "mensaje": "registro ya existe.",
                                                     'repetidos': campos_repetidos})
                        modulo = Modulo.objects.get(pk=request.POST['id'])
                        modulo.nombre = form.cleaned_data['nombre']
                        modulo.descripcion = form.cleaned_data['descripcion']
                        if form.cleaned_data['icono']:
                            modulo.icono = form.cleaned_data['icono']
                        else:
                            modulo.icono = request.POST['imagen_ruta']
                        modulo.ruta = form.cleaned_data['ruta']
                        modulo.activo = form.cleaned_data['activo']
                        modulo.save(request)

                        return JsonResponse({"respuesta": True, "mensaje": "Registro Modificado correctamente."})


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'eliminar_modulo':
                try:
                    with transaction.atomic():
                        registro = Modulo.objects.get(pk=request.POST['id'])
                        registro.status = False
                        registro.save(request)
                        return JsonResponse({"respuesta": True, "mensaje": "Registro eliminado correctamente."})

                except Exception as ex:
                    pass

        return JsonResponse({"respuesta": False, "mensaje": "No se ha encontrado respuesta."})
    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']
            if peticion == 'add_modulo':
                try:
                    data['titulo'] = 'Agregar nuevo módulo'
                    data['titulo_formulario'] = 'Formulario de registro de Módulo'
                    data['peticion'] = 'add_modulo'
                    data['persona_logeado'] = persona_logeado
                    form= ModuloForm()
                    form.add()
                    data['form'] = form
                    return render(request, "conf_sistema/add_modulo.html", data)
                except Exception as ex:
                    pass


            if peticion == 'edit_modulo':
                try:
                    data['titulo'] = 'Editar módulo'
                    data['titulo_formulario'] = 'Formulario de editar Módulo'
                    data['peticion'] = 'edit_modulo'
                    data['persona_logeado'] = persona_logeado
                    data['MEDIA_URL'] = MEDIA_URL
                    data['modulo'] = modulo = Modulo.objects.get(pk=request.GET['id'])
                    data['form'] = form = ModuloForm(initial=model_to_dict(modulo))
                    return render(request, "conf_sistema/edit_modulo.html", data)
                except Exception as ex:
                    pass

        else:
            try:
                data['titulo'] = 'Configuración de Módulos'
                data['titulo_tabla'] = 'Lista  de Módulos'
                data['persona_logeado'] = persona_logeado
                lista = Modulo.objects.filter(status=True).order_by('id')
                paginator = Paginator(lista, 15)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                data['page_obj'] = page_obj
                return render(request, "conf_sistema/view_modulo.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
