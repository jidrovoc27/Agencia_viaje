import sys
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from datetime import *

from odontologico.forms import ConsultaForm, PagoForm
from odontologico.funciones import add_data_aplication
from odontologico.models import AgendarCita, Persona, Odontograma, Consulta, Rubro, Pago, Paciente
from django.db.models import Sum


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def view_mis_finanzas(request):
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
            if peticion == 'addpago':
                try:
                    form = PagoForm(request.POST)
                    if form.is_valid():
                        totalpagos = Pago.objects.filter(rubro_id=int(request.POST['idrubro']), status=True).aggregate(total=Sum('valorfinal'))
                        valorpagos = 0
                        if totalpagos['total']:
                            valorpagos = totalpagos['total']
                        consultarrubro = Rubro.objects.get(id=int(request.POST['idrubro']))
                        valorrestante_porpagar = float(consultarrubro.valor) - float(valorpagos)
                        if valorrestante_porpagar >= float(form.cleaned_data['valorfinal']):
                            if not persona_logeado == 'SUPERADMINISTRADOR':
                                registrarpago = Pago(persona=persona_logeado,
                                                     rubro_id=int(request.POST['idrubro']),
                                                     valor=form.cleaned_data['valor'],
                                                     subtotal_iva=form.cleaned_data['subtotal_iva'],
                                                     valorfinal=form.cleaned_data['valorfinal'])
                                registrarpago.save(request)
                            else:
                                registrarpago = Pago(rubro_id=int(request.POST['idrubro']),
                                                     valor=form.cleaned_data['valor'],
                                                     subtotal_iva=form.cleaned_data['subtotal_iva'],
                                                     valorfinal=form.cleaned_data['valorfinal'])
                                registrarpago.save(request)
                            totalpagos = Pago.objects.filter(rubro_id=int(request.POST['idrubro']),status=True).aggregate(total=Sum('valorfinal'))
                            valorpagos = 0
                            if totalpagos['total']:
                                valorpagos = float(totalpagos['total']) + float(form.cleaned_data['valorfinal'])
                            if valorpagos >= consultarrubro.valor:
                                consultarrubro.cancelado = True
                                consultarrubro.save(request)
                            return JsonResponse({"respuesta": True, "mensaje": "Pago registrado correctamente."})
                        return JsonResponse({"respuesta": False, "mensaje": "El valor cancelado supera el valor a pagar de $"+str(("{0:.2f}".format(valorrestante_porpagar)))})
                    else:
                       return JsonResponse( {"respuesta": False, "mensaje": "Por favor, complete el formulario correctamente"})


                except Exception as ex:
                   transaction.set_rollback(True)
                   return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})
        return JsonResponse({"respuesta": False, "mensaje": "acción Incorrecta."})
    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']
            if peticion == 'ver_pagos':
                try:
                    data['titulo'] = 'Pagos'
                    data['paciente_rubro'] = Paciente.objects.get(id=request.GET['id'])
                    data['rubro_paciente'] = Rubro.objects.get(status=True, id=request.GET['idrubro'])
                    lista = Pago.objects.filter(status=True, rubro_id=request.GET['idrubro'])
                    paginator = Paginator(lista, 15)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    data['page_obj'] = page_obj
                    return render(request, "mis_finanzas/pagos.html", data)
                except Exception as ex:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

        else:
            try:
                data['titulo'] = 'Mis finanzas'
                data['paciente_rubro'] = Paciente.objects.get(persona=persona_logeado)
                lista = Rubro.objects.filter(status=True, paciente__persona=persona_logeado)
                paginator = Paginator(lista, 15)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                data['page_obj'] = page_obj
                return render(request, "mis_finanzas/view.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
