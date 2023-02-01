import sys
import io
import xlsxwriter
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse, HttpResponse, response
from django.shortcuts import render
from django.template.loader import get_template

from odontologico.forms import PersonaForm, FiltroForm
from odontologico.funciones import add_data_aplication
from odontologico.models import Persona, Doctor, Paciente, Tratamiento, Consulta, Asistente


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def view_reportes(request):
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
            if peticion == 'filtro_reporte':
                try:
                    form = FiltroForm(request.POST)

                    if form.is_valid():
                        fecha_inicio = form.cleaned_data['fecha_inicio']
                        fecha_fin = form.cleaned_data['fecha_fin']
                        especialista =form.cleaned_data['especialista']

                        filtro = Consulta.objects.filter(status =True,doctor = especialista,fecha__gte=fecha_inicio,fecha__lte=fecha_fin)

                        output = io.BytesIO()
                        # Create an new Excel file and add a worksheet.
                        workbook = xlsxwriter.Workbook(output)
                        worksheet = workbook.add_worksheet()

                        # Widen the first column to make the text clearer.
                        worksheet.set_column('A:A', 50)
                        worksheet.set_column('B:B', 50)
                        worksheet.set_column('C:C', 50)
                        worksheet.set_column('D:D', 50)
                        worksheet.set_column('E:E', 50)
                        worksheet.set_column('F:F', 50)
                        worksheet.set_column('G:G', 50)

                        # Add a bold format to use to highlight cells.

                        # Write some simple text.
                        worksheet.write('A1', 'Fecha')
                        worksheet.write('B1', 'Nombres y apellidos')
                        worksheet.write('C1', 'Correo electrónico')
                        worksheet.write('D1', 'cédula')
                        worksheet.write('E1', 'género')
                        worksheet.write('F1', 'movil')
                        worksheet.write('G1', 'Doctor')

                        # Text with formatting.
                        row = 2
                        for a in filtro:
                            worksheet.write('A%s' % row, a.fecha.__str__())
                            worksheet.write('B%s' % row, a.paciente.persona.__str__())
                            worksheet.write('C%s' % row, a.paciente.persona.email.__str__())
                            worksheet.write('D%s' % row, a.paciente.persona.cedula.__str__())
                            worksheet.write('E%s' % row, a.paciente.persona.genero.__str__())
                            worksheet.write('F%s' % row, '0' + a.paciente.persona.telefono_movil.__str__())
                            worksheet.write('G%s' % row, a.doctor.__str__())
                            row += 1
                        workbook.close()
                        # Rewind the buffer.
                        output.seek(0)

                        # Set up the Http response.
                        filename = 'reporte.xlsx'
                        response = HttpResponse(
                            output,
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                        )
                        response['Content-Disposition'] = 'attachment; filename=%s' % filename

                        return response


                except Exception as ex:
                    pass
        return JsonResponse({"respuesta": False, "mensaje": "acción Incorrecta."})
    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']

            if peticion == 'reporte_pacientes':
                try:
                    fila = Paciente.objects.filter(status=True)
                    output = io.BytesIO()
                    # Create an new Excel file and add a worksheet.
                    workbook = xlsxwriter.Workbook(output)
                    worksheet = workbook.add_worksheet()

                    # Widen the first column to make the text clearer.
                    worksheet.set_column('A:A', 50)
                    worksheet.set_column('B:B', 50)
                    worksheet.set_column('C:C', 50)
                    worksheet.set_column('D:D', 50)
                    worksheet.set_column('E:E', 50)
                    worksheet.set_column('F:F', 50)

                    # Add a bold format to use to highlight cells.


                    # Write some simple text.
                    worksheet.write('A1', 'Nombres y apellidos')
                    worksheet.write('B1', 'Correo electrónico')
                    worksheet.write('C1', 'cédula')
                    worksheet.write('D1', 'género')
                    worksheet.write('E1', 'movil')

                    # Text with formatting.
                    row = 2
                    for a in fila:
                        worksheet.write('A%s' % row, a.persona.__str__())
                        worksheet.write('B%s' % row, a.persona.email.__str__())
                        worksheet.write('C%s' % row, a.persona.cedula.__str__())
                        worksheet.write('D%s' % row, a.persona.genero.__str__())
                        worksheet.write('E%s' % row, '0'+a.persona.telefono_movil.__str__())
                        row+=1
                    workbook.close()
                    # Rewind the buffer.
                    output.seek(0)

                    # Set up the Http response.
                    filename = 'reporte_pacientes.xlsx'
                    response = HttpResponse(
                        output,
                        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
                    response['Content-Disposition'] = 'attachment; filename=%s' % filename

                    return response


                except Exception as ex:
                    pass

            if peticion == 'reporte_asistentes':
                try:
                    fila = Asistente.objects.filter(status=True)

                    output = io.BytesIO()
                    # Create an new Excel file and add a worksheet.
                    workbook = xlsxwriter.Workbook(output)
                    worksheet = workbook.add_worksheet()

                    # Widen the first column to make the text clearer.
                    worksheet.set_column('A:A', 50)
                    worksheet.set_column('B:B', 50)
                    worksheet.set_column('C:C', 50)
                    worksheet.set_column('D:D', 50)
                    worksheet.set_column('E:E', 50)
                    worksheet.set_column('F:F', 50)

                    # Add a bold format to use to highlight cells.

                    # Write some simple text.
                    worksheet.write('A1', 'Nombres y apellidos')
                    worksheet.write('B1', 'Correo electrónico')
                    worksheet.write('C1', 'cédula')
                    worksheet.write('D1', 'género')
                    worksheet.write('E1', 'movil')

                    # Text with formatting.
                    row = 2
                    for a in fila:
                        worksheet.write('A%s' % row, a.persona.__str__())
                        worksheet.write('B%s' % row, a.persona.email.__str__())
                        worksheet.write('C%s' % row, a.persona.cedula.__str__())
                        worksheet.write('D%s' % row, a.persona.genero.__str__())
                        worksheet.write('E%s' % row, '0' + a.persona.telefono_movil.__str__())
                        row += 1
                    workbook.close()
                    # Rewind the buffer.
                    output.seek(0)

                    # Set up the Http response.
                    filename = 'reporte_asistentes.xlsx'
                    response = HttpResponse(
                        output,
                        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
                    response['Content-Disposition'] = 'attachment; filename=%s' % filename

                    return response


                except Exception as ex:
                    pass

            if peticion == 'reporte_especialistas':
                try:
                    fila = Doctor.objects.filter(status=True)

                    output = io.BytesIO()
                    # Create an new Excel file and add a worksheet.
                    workbook = xlsxwriter.Workbook(output)
                    worksheet = workbook.add_worksheet()

                    # Widen the first column to make the text clearer.
                    worksheet.set_column('A:A', 50)
                    worksheet.set_column('B:B', 50)
                    worksheet.set_column('C:C', 50)
                    worksheet.set_column('D:D', 50)
                    worksheet.set_column('E:E', 50)
                    worksheet.set_column('F:F', 50)

                    # Add a bold format to use to highlight cells.

                    # Write some simple text.
                    worksheet.write('A1', 'Nombres y apellidos')
                    worksheet.write('B1', 'Correo electrónico')
                    worksheet.write('C1', 'cédula')
                    worksheet.write('D1', 'género')
                    worksheet.write('E1', 'movil')

                    # Text with formatting.
                    row = 2
                    for a in fila:
                        worksheet.write('A%s' % row, a.persona.__str__())
                        worksheet.write('B%s' % row, a.persona.email.__str__())
                        worksheet.write('C%s' % row, a.persona.cedula.__str__())
                        worksheet.write('D%s' % row, a.persona.genero.__str__())
                        worksheet.write('E%s' % row, '0' + a.persona.telefono_movil.__str__())
                        row += 1
                    workbook.close()
                    # Rewind the buffer.
                    output.seek(0)

                    # Set up the Http response.
                    filename = 'reporte_especialistas.xlsx'
                    response = HttpResponse(
                        output,
                        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
                    response['Content-Disposition'] = 'attachment; filename=%s' % filename

                    return response

                except Exception as ex:
                    pass

            if peticion == 'reporte_tratamiento':
                try:
                    fila = Tratamiento.objects.filter(status=True)

                    output = io.BytesIO()
                    # Create an new Excel file and add a worksheet.
                    workbook = xlsxwriter.Workbook(output)
                    worksheet = workbook.add_worksheet()

                    # Widen the first column to make the text clearer.
                    worksheet.set_column('A:A', 60)
                    worksheet.set_column('B:B', 50)


                    # Add a bold format to use to highlight cells.

                    # Write some simple text.
                    worksheet.write('A1', 'Nombre')
                    worksheet.write('B1', 'Costo')


                    # Text with formatting.
                    row = 2
                    for a in fila:
                        worksheet.write('A%s' % row, a.nombre.__str__())
                        worksheet.write('B%s' % row, a.costo.__str__())

                        row += 1
                    workbook.close()
                    # Rewind the buffer.
                    output.seek(0)

                    # Set up the Http response.
                    filename = 'reporte_tratamientos.xlsx'
                    response = HttpResponse(
                        output,
                        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
                    response['Content-Disposition'] = 'attachment; filename=%s' % filename

                    return response

                except Exception as ex:
                    pass

            if peticion == 'reporte_tratamiento_por_paciente':
                try:
                    fila = Consulta.objects.raw()
                        # 'SELECT trat.id, trat.nombre, ( SELECT  COUNT(c.consulta_id) AS paciente FROM odontologico_consulta_tratamientos c WHERE c.tratamiento_id=trat.id group by c.tratamiento_id ) AS cantidad_pacientes FROM  odontologico_tratamiento trat ')

                    output = io.BytesIO()
                    # Create an new Excel file and add a worksheet.
                    workbook = xlsxwriter.Workbook(output)
                    worksheet = workbook.add_worksheet()

                    # Widen the first column to make the text clearer.
                    worksheet.set_column('A:A', 50)
                    worksheet.set_column('B:B', 60)


                    # Add a bold format to use to highlight cells.

                    # Write some simple text.
                    worksheet.write('A1', 'Tratamiento')
                    worksheet.write('B1', 'Cantidad de pacientes que se han realizado el tratamiento')


                    # Text with formatting.
                    row = 2
                    for a in fila:
                        if a.cantidad_pacientes is None:
                            valor = '0'
                        else:
                            valor = a.cantidad_pacientes.__str__()
                        worksheet.write('A%s' % row, a.nombre.__str__())
                        worksheet.write('B%s' % row, valor)

                        row += 1
                    workbook.close()
                    # Rewind the buffer.
                    output.seek(0)

                    # Set up the Http response.
                    filename = 'reporte_tratamientos_por_pacientes.xlsx'
                    response = HttpResponse(
                        output,
                        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
                    response['Content-Disposition'] = 'attachment; filename=%s' % filename

                    return response

                except Exception as ex:
                    pass


            if peticion == 'reporte_filtro':
                try:
                    form = FiltroForm()
                    data['form'] = form
                    template = get_template("reportes/modal/filtro.html")
                    return JsonResponse({"respuesta": True, 'data': template.render(data)})
                except Exception as ex:
                    pass


        else:
            try:
                data['titulo'] = 'Reportes'
                data['persona_logeado'] = persona_logeado
                data['pacientes_masculino']  = pacientes_masculino = Paciente.objects.filter(status=True, persona__genero__pk = 1).count()
                data['pacientes_femenino'] =pacientes_femenino = Paciente.objects.filter(status=True, persona__genero__pk = 2).count()

                #pacientes por tratamientos
                data['tratamientos'] = tratamientos = Tratamiento.objects.filter(status = True)
                # data['consultas'] =consultas = Consulta.objects.raw('SELECT trat.id, trat.nombre, ( SELECT  COUNT(c.consulta_id) AS paciente FROM odontologico_consulta_tratamientos c WHERE c.tratamiento_id=trat.id group by c.tratamiento_id ) AS cantidad_pacientes FROM  odontologico_tratamiento trat ')
                consultas = []
                tratamientos = []
                cantidad_pacientes = []
                for c in consultas:

                    tratamientos.append(c.nombre)
                    if c.cantidad_pacientes is None:
                        valor = 0
                    else:
                        valor =c.cantidad_pacientes
                    cantidad_pacientes.append(valor)
                data['tratamientos'] =tratamientos
                data['cantidad_pacientes'] =cantidad_pacientes
                return render(request, "reportes/view.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
