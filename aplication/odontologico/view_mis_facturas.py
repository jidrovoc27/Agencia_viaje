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
from odontologico.models import Paciente, PersonaPerfil, Persona, Tratamiento, Consulta
from odontologico.view_paciente import render_pdf_view


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def view_mis_facturas(request):
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
        return JsonResponse({"respuesta": False, "mensaje": "acción Incorrecta."})
    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']
            if peticion == 'ver_factura':
                try:
                    data['titulo'] = 'Ver recibo'
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
        else:
            try:
                data['titulo'] = 'Facturas'
                data['titulo_tabla'] = 'Lista  de facturas'
                data['persona_logeado'] = persona_logeado
                paciente = Paciente.objects.get(status=True, persona = persona_logeado)
                lista = Consulta.objects.filter(status=True,paciente = paciente, cancelado =True)
                paginator = Paginator(lista, 15)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                data['page_obj'] = page_obj
                return render(request, "paciente/view_mis_facturas.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
