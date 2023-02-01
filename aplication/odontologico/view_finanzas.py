import sys
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from datetime import *

from odontologico.forms import ConsultaForm, PagoForm, FacturaForm
from odontologico.funciones import add_data_aplication
from odontologico.models import AgendarCita, Persona, Odontograma, Consulta, Rubro, Pago, Paciente, Factura
from django.db.models import Sum


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def view_finanzas(request):
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
                                                     valorfinal=form.cleaned_data['valorfinal'])
                                registrarpago.save(request)
                            else:
                                registrarpago = Pago(rubro_id=int(request.POST['idrubro']),
                                                     valor=form.cleaned_data['valor'],
                                                     valorfinal=form.cleaned_data['valorfinal'])
                                registrarpago.save(request)
                            totalpagos = Pago.objects.filter(rubro_id=int(request.POST['idrubro']),status=True).aggregate(total=Sum('valorfinal'))
                            valorpagos = 0
                            if totalpagos['total']:
                                valorpagos = float(totalpagos['total'])
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

            elif peticion == 'addfactura':
                try:
                    form = FacturaForm(request.POST,request.FILES)
                    archivo = None
                    if form.is_valid():
                        if 'archivo' in request.FILES:
                           archivo = request.FILES['archivo']
                        if not persona_logeado == 'SUPERADMINISTRADOR':
                            registro_factura = Factura(pago_id=request.POST['idpago'],archivo=archivo,
                                                       persona=persona_logeado)
                            registro_factura.save(request)
                        else:
                            registro_factura = Factura(pago_id=request.POST['idpago'], archivo=archivo)
                            registro_factura.save(request)
                        return JsonResponse({"respuesta": True, "mensaje": "Factura registrada correctamente."})
                except Exception as ex:
                    pass
        return JsonResponse({"respuesta": False, "mensaje": "acción Incorrecta."})
    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']
            if peticion == 'ver_rubro':
                try:
                    data['titulo'] = 'Rubros'
                    data['paciente_rubro'] = Paciente.objects.get(id=request.GET['id'])
                    lista = Rubro.objects.filter(status=True,paciente_id=request.GET['id'])
                    paginator = Paginator(lista, 15)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    data['page_obj'] = page_obj
                    return render(request, "finanzas/rubros.html", data)
                except Exception as ex:
                    transaction.set_rollback(True)
                    pass

            elif peticion == 'ver_pagos':
                try:
                    data['titulo'] = 'Pagos'
                    data['paciente_rubro'] = Paciente.objects.get(id=request.GET['id'])
                    data['rubro_paciente'] = Rubro.objects.get(status=True, id=request.GET['idrubro'])
                    lista = Pago.objects.filter(status=True, rubro_id=request.GET['idrubro'])
                    paginator = Paginator(lista, 15)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    data['page_obj'] = page_obj
                    return render(request, "finanzas/pagos.html", data)
                except Exception as ex:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

            elif peticion == 'addpago':
                try:
                    data['titulo'] = 'Registrar nuevo pago'
                    data['titulo_formulario'] = 'Formulario de registro de paciente'
                    data['peticion'] = 'addpago'
                    data['idrubro'] = request.GET['idrubro']
                    data['id'] = request.GET['id']
                    form = PagoForm()
                    data['form'] = form
                    return render(request, "finanzas/addpago.html", data)
                except Exception as ex:
                    transaction.set_rollback(True)
                    pass

            elif peticion == 'addfactura':
                try:
                    data['titulo'] = 'Registrar nueva factura'
                    data['titulo_formulario'] = 'Formulario de registro de factura'
                    data['peticion'] = 'addfactura'
                    data['idpago'] = request.GET['idpago']
                    form = FacturaForm()
                    data['form'] = form
                    return render(request, "finanzas/addfactura.html", data)
                except Exception as ex:
                    pass

            elif peticion == 'ver_facturas':
                try:
                    data['titulo'] = 'Facturas'
                    data['paciente_rubro'] = Paciente.objects.get(id=request.GET['paciente_id'])
                    data['pago_factura'] = Pago.objects.get(id=int(request.GET['id']))
                    lista = Factura.objects.filter(status=True,pago_id=int(request.GET['id']))
                    paginator = Paginator(lista, 15)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    data['page_obj'] = page_obj
                    return render(request, "finanzas/facturas.html", data)
                except Exception as ex:
                    transaction.set_rollback(True)
                    pass


        else:
            try:
                data['titulo'] = 'Finanzas'
                data['titulo_tabla'] = 'Listado de pacientes'
                data['persona_logeado'] = persona_logeado
                lista = Paciente.objects.filter(status=True)
                paginator = Paginator(lista, 15)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                data['page_obj'] = page_obj

                return render(request, "finanzas/view.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
