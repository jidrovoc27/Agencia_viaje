import sys
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from datetime import *

from odontologico.forms import ConsultaForm
from odontologico.funciones import add_data_aplication
from odontologico.models import *


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def view_atender_cita(request):
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
            if peticion == 'atender_consulta':
                try:
                    form = ConsultaForm(request.POST, request.FILES)
                    if form.is_valid():
                        colores = request.POST.getlist('color[]')
                        partes = request.POST.getlist('identificador[]')
                        odontograma = Odontograma(TP18=colores[0], BP18=colores[1],
                                                  RP18=colores[2], LP18=colores[3], CP18=colores[4], CP17=colores[5],
                                                  TP17=colores[6], BP17=colores[7], RP17=colores[8], LP17=colores[9],
                                                  CP16=colores[10], TP16=colores[11], BP16=colores[12],
                                                  RP16=colores[13],
                                                  LP16=colores[14], CP15=colores[15], TP15=colores[16],
                                                  BP15=colores[17],
                                                  RP15=colores[18], LP15=colores[19], CP14=colores[20],
                                                  TP14=colores[21],
                                                  BP14=colores[22], RP14=colores[23], LP14=colores[24],
                                                  CP13=colores[25],
                                                  TP13=colores[26], BP13=colores[27], RP13=colores[28],
                                                  LP13=colores[29],
                                                  CP12=colores[30], TP12=colores[31], BP12=colores[32],
                                                  RP12=colores[33],
                                                  LP12=colores[34], CP11=colores[35], TP11=colores[36],
                                                  BP11=colores[37],
                                                  RP11=colores[38], LP11=colores[39], CP55=colores[40],
                                                  TP55=colores[41],
                                                  BP55=colores[42], RP55=colores[43], LP55=colores[44],
                                                  CP54=colores[45],
                                                  TP54=colores[46], BP54=colores[47], RP54=colores[48],
                                                  LP54=colores[49],
                                                  CP53=colores[50], TP53=colores[51], BP53=colores[52],
                                                  RP53=colores[53],
                                                  LP53=colores[54], CP52=colores[55], TP52=colores[56],
                                                  BP52=colores[57],
                                                  RP52=colores[58], LP52=colores[59], CP51=colores[60],
                                                  TP51=colores[61],
                                                  BP51=colores[62], RP51=colores[63], LP51=colores[64],
                                                  CP85=colores[65],
                                                  TP85=colores[66], BP85=colores[67], RP85=colores[68],
                                                  LP85=colores[69],
                                                  CP84=colores[70], TP84=colores[71], BP84=colores[72],
                                                  RP84=colores[73],
                                                  LP84=colores[74], CP83=colores[75], TP83=colores[76],
                                                  BP83=colores[77],
                                                  RP83=colores[78], LP83=colores[79], CP82=colores[80],
                                                  TP82=colores[81],
                                                  BP82=colores[82], RP82=colores[83], LP82=colores[84],
                                                  CP81=colores[85],
                                                  TP81=colores[86], BP81=colores[87], RP81=colores[88],
                                                  LP81=colores[89],
                                                  CP48=colores[90], TP48=colores[91], BP48=colores[92],
                                                  RP48=colores[93],
                                                  LP48=colores[94], CP47=colores[95], TP47=colores[96],
                                                  BP47=colores[97],
                                                  RP47=colores[98], LP47=colores[99], CP46=colores[100],
                                                  TP46=colores[101],
                                                  BP46=colores[102], RP46=colores[103], LP46=colores[104],
                                                  CP45=colores[105], TP45=colores[106], BP45=colores[107],
                                                  RP45=colores[108], LP45=colores[109], CP44=colores[110],
                                                  TP44=colores[111], BP44=colores[112], RP44=colores[113],
                                                  LP44=colores[114], CP43=colores[115], TP43=colores[116],
                                                  BP43=colores[117], RP43=colores[118], LP43=colores[119],
                                                  CP42=colores[120], TP42=colores[121], BP42=colores[122],
                                                  RP42=colores[123], LP42=colores[124], CP41=colores[125],
                                                  TP41=colores[126], BP41=colores[127], RP41=colores[128],
                                                  LP41=colores[129], CP21=colores[130], TP21=colores[131],
                                                  BP21=colores[132], RP21=colores[133], LP21=colores[134],
                                                  CP22=colores[135], TP22=colores[136], BP22=colores[137],
                                                  RP22=colores[138], LP22=colores[139], CP23=colores[140],
                                                  TP23=colores[141], BP23=colores[142], RP23=colores[143],
                                                  LP23=colores[144], CP24=colores[145], TP24=colores[146],
                                                  BP24=colores[147], RP24=colores[148], LP24=colores[149],
                                                  CP25=colores[150], TP25=colores[151], BP25=colores[152],
                                                  RP25=colores[153], LP25=colores[154], CP26=colores[155],
                                                  TP26=colores[156], BP26=colores[157], RP26=colores[158],
                                                  LP26=colores[159], CP27=colores[160], TP27=colores[161],
                                                  BP27=colores[162], RP27=colores[163], LP27=colores[164],
                                                  CP28=colores[165], TP28=colores[166], BP28=colores[167],
                                                  RP28=colores[168], LP28=colores[169], CP61=colores[170],
                                                  TP61=colores[171], BP61=colores[172], RP61=colores[173],
                                                  LP61=colores[174], CP62=colores[175], TP62=colores[176],
                                                  BP62=colores[177], RP62=colores[178], LP62=colores[179],
                                                  CP63=colores[180], TP63=colores[181], BP63=colores[182],
                                                  RP63=colores[183], LP63=colores[184], CP64=colores[185],
                                                  TP64=colores[186], BP64=colores[187], RP64=colores[188],
                                                  LP64=colores[189], CP65=colores[190], TP65=colores[191],
                                                  BP65=colores[192], RP65=colores[193], LP65=colores[194],
                                                  CP71=colores[195], TP71=colores[196], BP71=colores[197],
                                                  RP71=colores[198], LP71=colores[199], CP72=colores[200],
                                                  TP72=colores[201], BP72=colores[202], RP72=colores[203],
                                                  LP72=colores[204], CP73=colores[205], TP73=colores[206],
                                                  BP73=colores[207], RP73=colores[208], LP73=colores[209],
                                                  CP74=colores[210], TP74=colores[211], BP74=colores[212],
                                                  RP74=colores[213], LP74=colores[214], CP75=colores[215],
                                                  TP75=colores[216], BP75=colores[217], RP75=colores[218],
                                                  LP75=colores[219], CP31=colores[220], TP31=colores[221],
                                                  BP31=colores[222], RP31=colores[223], LP31=colores[224],
                                                  CP32=colores[225], TP32=colores[226], BP32=colores[227],
                                                  RP32=colores[228], LP32=colores[229], CP33=colores[230],
                                                  TP33=colores[231], BP33=colores[232], RP33=colores[233],
                                                  LP33=colores[234], CP34=colores[235], TP34=colores[236],
                                                  BP34=colores[237], RP34=colores[238], LP34=colores[239],
                                                  CP35=colores[240], TP35=colores[241], BP35=colores[242],
                                                  RP35=colores[243], LP35=colores[244], CP36=colores[245],
                                                  TP36=colores[246], BP36=colores[247], RP36=colores[248],
                                                  LP36=colores[249], CP37=colores[250], TP37=colores[251],
                                                  BP37=colores[252], RP37=colores[253], LP37=colores[254],
                                                  CP38=colores[255], TP38=colores[256], BP38=colores[257],
                                                  RP38=colores[258], LP38=colores[259])





                        cita = AgendarCita.objects.get(pk=request.POST['id'])
                        cita.estado_cita = 1
                        cita.save(request)
                        verificarsinotieneodontograma = Odontograma.objects.filter(status=True, paciente=cita.paciente)
                        actualizarodontograma = False
                        if not verificarsinotieneodontograma:
                            odontograma.tipo = 1
                        else:
                            odontograma_principal = Odontograma.objects.get(paciente=cita.paciente, tipo = 1, status=True)

                            if not colores[0] == 'white':
                                odontograma_principal.TP18 = colores[0]
                                actualizarodontograma = True

                            if not colores[1] == 'white':
                                odontograma_principal.BP18 = colores[1]
                                actualizarodontograma = True

                            if not colores[2] == 'white':
                                odontograma_principal.RP18 = colores[2]
                                actualizarodontograma = True

                            if not colores[3] == 'white':
                                odontograma_principal.LP18 = colores[3]
                                actualizarodontograma = True

                            if not colores[4] == 'white':
                                odontograma_principal.CP18 = colores[4]
                                actualizarodontograma = True

                            if not colores[5] == 'white':
                                odontograma_principal.CP17 = colores[5]
                                actualizarodontograma = True

                            if not colores[6] == 'white':
                                odontograma_principal.TP17 = colores[6]
                                actualizarodontograma = True

                            if not colores[7] == 'white':
                                odontograma_principal.BP17 = colores[7]
                                actualizarodontograma = True

                            if not colores[8] == 'white':
                                odontograma_principal.RP17 = colores[8]
                                actualizarodontograma = True

                            if not colores[9] == 'white':
                                odontograma_principal.LP17 = colores[9]
                                actualizarodontograma = True

                            if not colores[10] == 'white':
                                odontograma_principal.CP16 = colores[10]
                                actualizarodontograma = True

                            if not colores[11] == 'white':
                                odontograma_principal.TP16 = colores[11]
                                actualizarodontograma = True
                            if not colores[12] == 'white':
                                odontograma_principal.BP16 = colores[12]
                                actualizarodontograma = True
                            if not colores[13] == 'white':
                                odontograma_principal.RP16 = colores[13]
                                actualizarodontograma = True
                            if not colores[14] == 'white':
                                odontograma_principal.LP16 = colores[14]
                                actualizarodontograma = True
                            if not colores[15] == 'white':
                                odontograma_principal.CP15 = colores[15]
                                actualizarodontograma = True
                            if not colores[16] == 'white':
                                odontograma_principal.TP15 = colores[16]
                                actualizarodontograma = True
                            if not colores[17] == 'white':
                                odontograma_principal.BP15 = colores[17]
                                actualizarodontograma = True
                            if not colores[18] == 'white':
                                odontograma_principal.RP15 = colores[18]
                                actualizarodontograma = True
                            if not colores[19] == 'white':
                                odontograma_principal.LP15 = colores[19]
                                actualizarodontograma = True
                            if not colores[20] == 'white':
                                odontograma_principal.CP14 = colores[20]
                                actualizarodontograma = True
                            if not colores[21] == 'white':
                                odontograma_principal.TP14 = colores[21]
                                actualizarodontograma = True
                            if not colores[22] == 'white':
                                odontograma_principal.BP14 = colores[22]
                                actualizarodontograma = True
                            if not colores[23] == 'white':
                                odontograma_principal.RP14 = colores[23]
                                actualizarodontograma = True
                            if not colores[24] == 'white':
                                odontograma_principal.LP14 = colores[24]
                                actualizarodontograma = True
                            if not colores[25] == 'white':
                                odontograma_principal.CP13 = colores[25]
                                actualizarodontograma = True
                            if not colores[26] == 'white':
                                odontograma_principal.TP13 = colores[26]
                                actualizarodontograma = True
                            if not colores[27] == 'white':
                                odontograma_principal.BP13 = colores[27]
                                actualizarodontograma = True
                            if not colores[28] == 'white':
                                odontograma_principal.RP13 = colores[28]
                                actualizarodontograma = True

                            if not colores[29] == 'white':
                                odontograma_principal.LP13 = colores[29]
                                actualizarodontograma = True
                            if not colores[30] == 'white':
                                odontograma_principal.CP12 = colores[30]
                                actualizarodontograma = True
                            if not colores[31] == 'white':
                                odontograma_principal.TP12 = colores[31]
                                actualizarodontograma = True
                            if not colores[32] == 'white':
                                odontograma_principal.BP12 = colores[32]
                                actualizarodontograma = True
                            if not colores[33] == 'white':
                                odontograma_principal.RP12 = colores[33]
                                actualizarodontograma = True
                            if not colores[34] == 'white':
                                odontograma_principal.LP12 = colores[34]
                                actualizarodontograma = True
                            if not colores[35] == 'white':
                                odontograma_principal.CP11 = colores[35]
                                actualizarodontograma = True
                            if not colores[36] == 'white':
                                odontograma_principal.TP11 = colores[36]
                                actualizarodontograma = True
                            if not colores[37] == 'white':
                                odontograma_principal.BP11 = colores[37]
                                actualizarodontograma = True
                            if not colores[38] == 'white':
                                odontograma_principal.RP11 = colores[38]
                                actualizarodontograma = True
                            if not colores[39] == 'white':
                                odontograma_principal.LP11 = colores[39]
                                actualizarodontograma = True
                            if not colores[40] == 'white':
                                odontograma_principal.CP55 = colores[40]
                                actualizarodontograma = True
                            if not colores[41] == 'white':
                                odontograma_principal.TP55 = colores[41]
                                actualizarodontograma = True
                            if not colores[42] == 'white':
                                odontograma_principal.BP55 = colores[42]
                                actualizarodontograma = True
                            if not colores[43] == 'white':
                                odontograma_principal.RP55 = colores[43]
                                actualizarodontograma = True
                            if not colores[44] == 'white':
                                odontograma_principal.LP55 = colores[44]
                                actualizarodontograma = True
                            if not colores[45] == 'white':
                                odontograma_principal.CP54 = colores[45]
                                actualizarodontograma = True
                            if not colores[46] == 'white':
                                odontograma_principal.TP54 = colores[46]
                                actualizarodontograma = True
                            if not colores[47] == 'white':
                                odontograma_principal.BP54 = colores[47]
                                actualizarodontograma = True
                            if not colores[48] == 'white':
                                odontograma_principal.RP54 = colores[48]
                                actualizarodontograma = True
                            if not colores[49] == 'white':
                                odontograma_principal.LP54 = colores[49]
                                actualizarodontograma = True
                            if not colores[50] == 'white':
                                odontograma_principal.CP53 = colores[50]
                                actualizarodontograma = True
                            if not colores[51] == 'white':
                                odontograma_principal.TP53 = colores[51]
                                actualizarodontograma = True
                            if not colores[52] == 'white':
                                odontograma_principal.BP53 = colores[52]
                                actualizarodontograma = True
                            if not colores[53] == 'white':
                                odontograma_principal.RP53 = colores[53]
                                actualizarodontograma = True
                            if not colores[54] == 'white':
                                odontograma_principal.LP53 = colores[54]
                                actualizarodontograma = True
                            if not colores[55] == 'white':
                                odontograma_principal.CP52 = colores[55]
                                actualizarodontograma = True
                            if not colores[56] == 'white':
                                odontograma_principal.TP52 = colores[56]
                                actualizarodontograma = True
                            if not colores[57] == 'white':
                                odontograma_principal.BP52 = colores[57]
                                actualizarodontograma = True
                            if not colores[58] == 'white':
                                odontograma_principal.RP52 = colores[58]
                                actualizarodontograma = True
                            if not colores[59] == 'white':
                                odontograma_principal.LP52 = colores[59]
                                actualizarodontograma = True
                            if not colores[60] == 'white':
                                odontograma_principal.CP51 = colores[60]
                                actualizarodontograma = True
                            if not colores[61] == 'white':
                                odontograma_principal.TP51 = colores[61]
                                actualizarodontograma = True
                            if not colores[62] == 'white':
                                odontograma_principal.BP51 = colores[62]
                                actualizarodontograma = True
                            if not colores[63] == 'white':
                                odontograma_principal.RP51 = colores[63]
                                actualizarodontograma = True
                            if not colores[64] == 'white':
                                odontograma_principal.LP51 = colores[64]
                                actualizarodontograma = True
                            if not colores[65] == 'white':
                                odontograma_principal.CP85 = colores[65]
                                actualizarodontograma = True
                            if not colores[66] == 'white':
                                odontograma_principal.TP85 = colores[66]
                                actualizarodontograma = True
                            if not colores[67] == 'white':
                                odontograma_principal.BP85 = colores[67]
                                actualizarodontograma = True
                            if not colores[68] == 'white':
                                odontograma_principal.RP85 = colores[68]
                                actualizarodontograma = True
                            if not colores[69] == 'white':
                                odontograma_principal.LP85 = colores[69]
                                actualizarodontograma = True
                            if not colores[70] == 'white':
                                odontograma_principal.CP84 = colores[70]
                                actualizarodontograma = True
                            if not colores[71] == 'white':
                                odontograma_principal.TP84 = colores[71]
                                actualizarodontograma = True
                            if not colores[72] == 'white':
                                odontograma_principal.BP84 = colores[72]
                                actualizarodontograma = True
                            if not colores[73] == 'white':
                                odontograma_principal.RP84 = colores[73]
                                actualizarodontograma = True
                            if not colores[74] == 'white':
                                odontograma_principal.LP84 = colores[74]
                                actualizarodontograma = True
                            if not colores[75] == 'white':
                                odontograma_principal.CP83 = colores[75]
                                actualizarodontograma = True
                            if not colores[76] == 'white':
                                odontograma_principal.TP83 = colores[76]
                                actualizarodontograma = True
                            if not colores[77] == 'white':
                                odontograma_principal.BP83 = colores[77]
                                actualizarodontograma = True
                            if not colores[78] == 'white':
                                odontograma_principal.RP83 = colores[78]
                                actualizarodontograma = True
                            if not colores[79] == 'white':
                                odontograma_principal.LP83 = colores[79]
                                actualizarodontograma = True
                            if not colores[80] == 'white':
                                odontograma_principal.CP82 = colores[80]
                                actualizarodontograma = True
                            if not colores[81] == 'white':
                                odontograma_principal.TP82 = colores[81]
                                actualizarodontograma = True
                            if not colores[82] == 'white':
                                odontograma_principal.BP82 = colores[82]
                                actualizarodontograma = True
                            if not colores[83] == 'white':
                                odontograma_principal.RP82 = colores[83]
                                actualizarodontograma = True
                            if not colores[84] == 'white':
                                odontograma_principal.LP82 = colores[84]
                                actualizarodontograma = True
                            if not colores[85] == 'white':
                                odontograma_principal.CP81 = colores[85]
                                actualizarodontograma = True
                            if not colores[86] == 'white':
                                odontograma_principal.TP81 = colores[86]
                                actualizarodontograma = True
                            if not colores[87] == 'white':
                                odontograma_principal.BP81 = colores[87]
                                actualizarodontograma = True
                            if not colores[88] == 'white':
                                odontograma_principal.RP81 = colores[88]
                                actualizarodontograma = True
                            if not colores[89] == 'white':
                                odontograma_principal.LP81 = colores[89]
                                actualizarodontograma = True
                            if not colores[90] == 'white':
                                odontograma_principal.CP48 = colores[90]
                                actualizarodontograma = True
                            if not colores[91] == 'white':
                                odontograma_principal.TP48 = colores[91]
                                actualizarodontograma = True
                            if not colores[92] == 'white':
                                odontograma_principal.BP48 = colores[92]
                                actualizarodontograma = True
                            if not colores[93] == 'white':
                                odontograma_principal.RP48 = colores[93]
                                actualizarodontograma = True
                            if not colores[94] == 'white':
                                odontograma_principal.LP48 = colores[94]
                                actualizarodontograma = True
                            if not colores[95] == 'white':
                                odontograma_principal.CP47 = colores[95]
                                actualizarodontograma = True
                            if not colores[96] == 'white':
                                odontograma_principal.TP47 = colores[96]
                                actualizarodontograma = True
                            if not colores[97] == 'white':
                                odontograma_principal.BP47 = colores[97]
                                actualizarodontograma = True
                            if not colores[98] == 'white':
                                odontograma_principal.RP47 = colores[98]
                                actualizarodontograma = True
                            if not colores[99] == 'white':
                                odontograma_principal.LP47 = colores[99]
                                actualizarodontograma = True
                            if not colores[100] == 'white':
                                odontograma_principal.CP46 = colores[100]
                                actualizarodontograma = True
                            if not colores[101] == 'white':
                                odontograma_principal.TP46 = colores[101]
                                actualizarodontograma = True
                            if not colores[102] == 'white':
                                odontograma_principal.BP46 = colores[102]
                                actualizarodontograma = True
                            if not colores[103] == 'white':
                                odontograma_principal.RP46 = colores[103]
                                actualizarodontograma = True
                            if not colores[104] == 'white':
                                odontograma_principal.LP46 = colores[104]
                                actualizarodontograma = True
                            if not colores[105] == 'white':
                                odontograma_principal.CP45 = colores[105]
                                actualizarodontograma = True
                            if not colores[106] == 'white':
                                odontograma_principal.TP45 = colores[106]
                                actualizarodontograma = True
                            if not colores[107] == 'white':
                                odontograma_principal.BP45 = colores[107]
                                actualizarodontograma = True

                            if not colores[108] == 'white':
                                odontograma_principal.RP45 = colores[108]
                                actualizarodontograma = True
                            if not colores[109] == 'white':
                                odontograma_principal.LP45 = colores[109]
                                actualizarodontograma = True
                            if not colores[110] == 'white':
                                odontograma_principal.CP44 = colores[110]
                                actualizarodontograma = True
                            if not colores[111] == 'white':
                                odontograma_principal.TP44 = colores[111]
                                actualizarodontograma = True
                            if not colores[112] == 'white':
                                odontograma_principal.BP44 = colores[112]
                                actualizarodontograma = True
                            if not colores[113] == 'white':
                                odontograma_principal.RP44 = colores[113]
                                actualizarodontograma = True
                            if not colores[114] == 'white':
                                odontograma_principal.LP44 = colores[114]
                                actualizarodontograma = True
                            if not colores[115] == 'white':
                                odontograma_principal.CP43 = colores[115]
                                actualizarodontograma = True
                            if not colores[116] == 'white':
                                odontograma_principal.TP43 = colores[116]
                                actualizarodontograma = True
                            if not colores[117] == 'white':
                                odontograma_principal.BP43 = colores[117]
                                actualizarodontograma = True
                            if not colores[118] == 'white':
                                odontograma_principal.RP43 = colores[118]
                                actualizarodontograma = True
                            if not colores[119] == 'white':
                                odontograma_principal.LP43 = colores[119]
                                actualizarodontograma = True
                            if not colores[120] == 'white':
                                odontograma_principal.CP42 = colores[120]
                                actualizarodontograma = True
                            if not colores[121] == 'white':
                                odontograma_principal.TP42 = colores[121]
                                actualizarodontograma = True
                            if not colores[122] == 'white':
                                odontograma_principal.BP42 = colores[122]
                                actualizarodontograma = True
                            if not colores[123] == 'white':
                                odontograma_principal.RP42 = colores[123]
                                actualizarodontograma = True
                            if not colores[124] == 'white':
                                odontograma_principal.LP42 = colores[124]
                                actualizarodontograma = True
                            if not colores[125] == 'white':
                                odontograma_principal.CP41 = colores[125]
                                actualizarodontograma = True
                            if not colores[126] == 'white':
                                odontograma_principal.TP41 = colores[126]
                                actualizarodontograma = True
                            if not colores[127] == 'white':
                                odontograma_principal.BP41 = colores[127]
                                actualizarodontograma = True
                            if not colores[128] == 'white':
                                odontograma_principal.RP41 = colores[128]
                                actualizarodontograma = True
                            if not colores[129] == 'white':
                                odontograma_principal.LP41 = colores[129]
                                actualizarodontograma = True
                            if not colores[130] == 'white':
                                odontograma_principal.CP21 = colores[130]
                                actualizarodontograma = True
                            if not colores[131] == 'white':
                                odontograma_principal.TP21 = colores[131]
                                actualizarodontograma = True
                            if not colores[132] == 'white':
                                odontograma_principal.BP21 = colores[132]
                                actualizarodontograma = True
                            if not colores[133] == 'white':
                                odontograma_principal.RP21 = colores[133]
                                actualizarodontograma = True
                            if not colores[134] == 'white':
                                odontograma_principal.LP21 = colores[134]
                                actualizarodontograma = True
                            if not colores[135] == 'white':
                                odontograma_principal.CP22 = colores[135]
                                actualizarodontograma = True
                            if not colores[136] == 'white':
                                odontograma_principal.TP22 = colores[136]
                                actualizarodontograma = True
                            if not colores[137] == 'white':
                                odontograma_principal.BP22 = colores[137]
                                actualizarodontograma = True
                            if not colores[138] == 'white':
                                odontograma_principal.RP22 = colores[138]
                                actualizarodontograma = True
                            if not colores[139] == 'white':
                                odontograma_principal.LP22 = colores[139]
                                actualizarodontograma = True
                            if not colores[140] == 'white':
                                odontograma_principal.CP23 = colores[140]
                                actualizarodontograma = True
                            if not colores[141] == 'white':
                                odontograma_principal.TP23 = colores[141]
                                actualizarodontograma = True
                            if not colores[142] == 'white':
                                odontograma_principal.BP23 = colores[142]
                                actualizarodontograma = True
                            if not colores[143] == 'white':
                                odontograma_principal.RP23 = colores[143]
                                actualizarodontograma = True
                            if not colores[144] == 'white':
                                odontograma_principal.LP23 = colores[144]
                                actualizarodontograma = True
                            if not colores[145] == 'white':
                                odontograma_principal.CP24 = colores[145]
                                actualizarodontograma = True
                            if not colores[146] == 'white':
                                odontograma_principal.TP24 = colores[146]
                                actualizarodontograma = True
                            if not colores[147] == 'white':
                                odontograma_principal.BP24 = colores[147]
                                actualizarodontograma = True
                            if not colores[148] == 'white':
                                odontograma_principal.RP24 = colores[148]
                                actualizarodontograma = True
                            if not colores[149] == 'white':
                                odontograma_principal.LP24 = colores[149]
                                actualizarodontograma = True
                            if not colores[150] == 'white':
                                odontograma_principal.CP25 = colores[150]
                                actualizarodontograma = True
                            if not colores[151] == 'white':
                                odontograma_principal.TP25 = colores[151]
                                actualizarodontograma = True
                            if not colores[152] == 'white':
                                odontograma_principal.BP25 = colores[152]
                                actualizarodontograma = True
                            if not colores[153] == 'white':
                                odontograma_principal.RP25 = colores[153]
                                actualizarodontograma = True
                            if not colores[154] == 'white':
                                odontograma_principal.LP25 = colores[154]
                                actualizarodontograma = True
                            if not colores[155] == 'white':
                                odontograma_principal.CP26 = colores[155]
                                actualizarodontograma = True
                            if not colores[156] == 'white':
                                odontograma_principal.TP26 = colores[156]
                                actualizarodontograma = True
                            if not colores[157] == 'white':
                                odontograma_principal.BP26 = colores[157]
                                actualizarodontograma = True
                            if not colores[158] == 'white':
                                odontograma_principal.RP26 = colores[158]
                                actualizarodontograma = True
                            if not colores[159] == 'white':
                                odontograma_principal.LP26 = colores[159]
                                actualizarodontograma = True
                            if not colores[160] == 'white':
                                odontograma_principal.CP27 = colores[160]
                                actualizarodontograma = True
                            if not colores[161] == 'white':
                                odontograma_principal.TP27 = colores[161]
                                actualizarodontograma = True
                            if not colores[162] == 'white':
                                odontograma_principal.BP27 = colores[162]
                                actualizarodontograma = True
                            if not colores[163] == 'white':
                                odontograma_principal.RP27 = colores[163]
                                actualizarodontograma = True
                            if not colores[164] == 'white':
                                odontograma_principal.LP27 = colores[164]
                                actualizarodontograma = True
                            if not colores[165] == 'white':
                                odontograma_principal.CP28 = colores[165]
                                actualizarodontograma = True
                            if not colores[166] == 'white':
                                odontograma_principal.TP28 = colores[166]
                                actualizarodontograma = True
                            if not colores[167] == 'white':
                                odontograma_principal.BP28 = colores[167]
                                actualizarodontograma = True
                            if not colores[168] == 'white':
                                odontograma_principal.RP28 = colores[168]
                                actualizarodontograma = True

                            if not colores[169] == 'white':
                                odontograma_principal.LP28 = colores[169]
                                actualizarodontograma = True
                            if not colores[170] == 'white':
                                odontograma_principal.CP61 = colores[170]
                                actualizarodontograma = True
                            if not colores[171] == 'white':
                                odontograma_principal.TP61 = colores[171]
                                actualizarodontograma = True
                            if not colores[172] == 'white':
                                odontograma_principal.BP61 = colores[172]
                                actualizarodontograma = True
                            if not colores[173] == 'white':
                                odontograma_principal.RP61 = colores[173]
                                actualizarodontograma = True
                            if not colores[174] == 'white':
                                odontograma_principal.LP61 = colores[174]
                                actualizarodontograma = True
                            if not colores[175] == 'white':
                                odontograma_principal.CP62 = colores[175]
                                actualizarodontograma = True
                            if not colores[176] == 'white':
                                odontograma_principal.TP62 = colores[176]
                                actualizarodontograma = True
                            if not colores[177] == 'white':
                                odontograma_principal.BP62 = colores[177]
                                actualizarodontograma = True
                            if not colores[178] == 'white':
                                odontograma_principal.RP62 = colores[178]
                                actualizarodontograma = True
                            if not colores[179] == 'white':
                                odontograma_principal.LP62 = colores[179]
                                actualizarodontograma = True
                            if not colores[180] == 'white':
                                odontograma_principal.CP63 = colores[180]
                                actualizarodontograma = True
                            if not colores[181] == 'white':
                                odontograma_principal.TP63 = colores[181]
                                actualizarodontograma = True
                            if not colores[182] == 'white':
                                odontograma_principal.BP63 = colores[182]
                                actualizarodontograma = True
                            if not colores[183] == 'white':
                                odontograma_principal.RP63 = colores[183]
                                actualizarodontograma = True
                            if not colores[184] == 'white':
                                odontograma_principal.LP63 = colores[184]
                                actualizarodontograma = True
                            if not colores[185] == 'white':
                                odontograma_principal.CP64 = colores[185]
                                actualizarodontograma = True
                            if not colores[186] == 'white':
                                odontograma_principal.TP64 = colores[186]
                                actualizarodontograma = True
                            if not colores[187] == 'white':
                                odontograma_principal.BP64 = colores[187]
                                actualizarodontograma = True
                            if not colores[188] == 'white':
                                odontograma_principal.RP64 = colores[188]
                                actualizarodontograma = True
                            if not colores[189] == 'white':
                                odontograma_principal.LP64 = colores[189]
                                actualizarodontograma = True
                            if not colores[190] == 'white':
                                odontograma_principal.CP65 = colores[190]
                                actualizarodontograma = True
                            if not colores[191] == 'white':
                                odontograma_principal.TP65 = colores[191]
                                actualizarodontograma = True
                            if not colores[192] == 'white':
                                odontograma_principal.BP65 = colores[192]
                                actualizarodontograma = True
                            if not colores[193] == 'white':
                                odontograma_principal.RP65 = colores[193]
                                actualizarodontograma = True
                            if not colores[194] == 'white':
                                odontograma_principal.LP65 = colores[194]
                                actualizarodontograma = True
                            if not colores[195] == 'white':
                                odontograma_principal.CP71 = colores[195]
                                actualizarodontograma = True
                            if not colores[196] == 'white':
                                odontograma_principal.TP71 = colores[196]
                                actualizarodontograma = True
                            if not colores[197] == 'white':
                                odontograma_principal.BP71 = colores[197]
                                actualizarodontograma = True
                            if not colores[198] == 'white':
                                odontograma_principal.RP71 = colores[198]
                                actualizarodontograma = True
                            if not colores[199] == 'white':
                                odontograma_principal.LP71 = colores[199]
                                actualizarodontograma = True
                            if not colores[200] == 'white':
                                odontograma_principal.CP72 = colores[200]
                                actualizarodontograma = True
                            if not colores[201] == 'white':
                                odontograma_principal.TP72 = colores[201]
                                actualizarodontograma = True
                            if not colores[202] == 'white':
                                odontograma_principal.BP72 = colores[202]
                                actualizarodontograma = True
                            if not colores[203] == 'white':
                                odontograma_principal.RP72 = colores[203]
                                actualizarodontograma = True
                            if not colores[204] == 'white':
                                odontograma_principal.LP72 = colores[204]
                                actualizarodontograma = True
                            if not colores[205] == 'white':
                                odontograma_principal.CP73 = colores[205]
                                actualizarodontograma = True
                            if not colores[206] == 'white':
                                odontograma_principal.TP73 = colores[206]
                                actualizarodontograma = True
                            if not colores[207] == 'white':
                                odontograma_principal.BP73 = colores[207]
                                actualizarodontograma = True
                            if not colores[208] == 'white':
                                odontograma_principal.RP73 = colores[208]
                                actualizarodontograma = True
                            if not colores[209] == 'white':
                                odontograma_principal.LP73 = colores[209]
                                actualizarodontograma = True
                            if not colores[210] == 'white':
                                odontograma_principal.CP74 = colores[210]
                                actualizarodontograma = True
                            if not colores[211] == 'white':
                                odontograma_principal.TP74 = colores[211]
                                actualizarodontograma = True

                            if not colores[212] == 'white':
                                odontograma_principal.BP74 = colores[212]
                                actualizarodontograma = True
                            if not colores[213] == 'white':
                                odontograma_principal.RP74 = colores[213]
                                actualizarodontograma = True
                            if not colores[214] == 'white':
                                odontograma_principal.LP74 = colores[214]
                                actualizarodontograma = True
                            if not colores[215] == 'white':
                                odontograma_principal.CP75 = colores[215]
                                actualizarodontograma = True
                            if not colores[216] == 'white':
                                odontograma_principal.TP75 = colores[216]
                                actualizarodontograma = True
                            if not colores[217] == 'white':
                                odontograma_principal.BP75 = colores[217]
                                actualizarodontograma = True
                            if not colores[218] == 'white':
                                odontograma_principal.RP75 = colores[218]
                                actualizarodontograma = True
                            if not colores[219] == 'white':
                                odontograma_principal.LP75 = colores[219]
                                actualizarodontograma = True
                            if not colores[220] == 'white':
                                odontograma_principal.CP31 = colores[220]
                                actualizarodontograma = True
                            if not colores[221] == 'white':
                                odontograma_principal.TP31 = colores[221]
                                actualizarodontograma = True
                            if not colores[222] == 'white':
                                odontograma_principal.BP31 = colores[222]
                                actualizarodontograma = True
                            if not colores[223] == 'white':
                                odontograma_principal.RP31 = colores[223]
                                actualizarodontograma = True
                            if not colores[224] == 'white':
                                odontograma_principal.LP31 = colores[224]
                                actualizarodontograma = True
                            if not colores[225] == 'white':
                                odontograma_principal.CP32 = colores[225]
                                actualizarodontograma = True
                            if not colores[226] == 'white':
                                odontograma_principal.TP32 = colores[226]
                                actualizarodontograma = True
                            if not colores[227] == 'white':
                                odontograma_principal.BP32 = colores[227]
                                actualizarodontograma = True
                            if not colores[228] == 'white':
                                odontograma_principal.RP32 = colores[228]
                                actualizarodontograma = True
                            if not colores[229] == 'white':
                                odontograma_principal.LP32 = colores[229]
                                actualizarodontograma = True
                            if not colores[230] == 'white':
                                odontograma_principal.CP33 = colores[230]
                                actualizarodontograma = True
                            if not colores[231] == 'white':
                                odontograma_principal.TP33 = colores[231]
                                actualizarodontograma = True
                            if not colores[232] == 'white':
                                odontograma_principal.BP33 = colores[232]
                                actualizarodontograma = True
                            if not colores[233] == 'white':
                                odontograma_principal.RP33 = colores[233]
                                actualizarodontograma = True
                            if not colores[234] == 'white':
                                odontograma_principal.LP33 = colores[234]
                                actualizarodontograma = True
                            if not colores[235] == 'white':
                                odontograma_principal.CP34 = colores[235]
                                actualizarodontograma = True
                            if not colores[236] == 'white':
                                odontograma_principal.TP34 = colores[236]
                                actualizarodontograma = True
                            if not colores[237] == 'white':
                                odontograma_principal.BP34 = colores[237]
                                actualizarodontograma = True
                            if not colores[238] == 'white':
                                odontograma_principal.RP34 = colores[238]
                                actualizarodontograma = True
                            if not colores[239] == 'white':
                                odontograma_principal.LP34 = colores[239]
                                actualizarodontograma = True
                            if not colores[240] == 'white':
                                odontograma_principal.CP35 = colores[240]
                                actualizarodontograma = True
                            if not colores[241] == 'white':
                                odontograma_principal.TP35 = colores[241]
                                actualizarodontograma = True
                            if not colores[242] == 'white':
                                odontograma_principal.BP35 = colores[242]
                                actualizarodontograma = True
                            if not colores[243] == 'white':
                                odontograma_principal.RP35 = colores[243]
                                actualizarodontograma = True
                            if not colores[244] == 'white':
                                odontograma_principal.LP35 = colores[244]
                                actualizarodontograma = True
                            if not colores[245] == 'white':
                                odontograma_principal.CP36 = colores[245]
                                actualizarodontograma = True
                            if not colores[246] == 'white':
                                odontograma_principal.TP36 = colores[246]
                                actualizarodontograma = True
                            if not colores[247] == 'white':
                                odontograma_principal.BP36 = colores[247]
                                actualizarodontograma = True
                            if not colores[248] == 'white':
                                odontograma_principal.RP36 = colores[248]
                                actualizarodontograma = True
                            if not colores[249] == 'white':
                                odontograma_principal.LP36 = colores[249]
                                actualizarodontograma = True
                            if not colores[250] == 'white':
                                odontograma_principal.CP37 = colores[250]
                                actualizarodontograma = True
                            if not colores[251] == 'white':
                                odontograma_principal.TP37 = colores[251]
                                actualizarodontograma = True
                            if not colores[252] == 'white':
                                odontograma_principal.BP37 = colores[252]
                                actualizarodontograma = True
                            if not colores[253] == 'white':
                                odontograma_principal.RP37 = colores[253]
                                actualizarodontograma = True
                            if not colores[254] == 'white':
                                odontograma_principal.LP37 = colores[254]
                                actualizarodontograma = True
                            if not colores[255] == 'white':
                                odontograma_principal.CP38 = colores[255]
                                actualizarodontograma = True
                            if not colores[256] == 'white':
                                odontograma_principal.TP38 = colores[256]
                                actualizarodontograma = True
                            if not colores[257] == 'white':
                                odontograma_principal.BP38 = colores[257]
                                actualizarodontograma = True
                            if not colores[258] == 'white':
                                odontograma_principal.RP38 = colores[258]
                                actualizarodontograma = True
                            if not colores[259] == 'white':
                                odontograma_principal.LP38 = colores[259]
                                actualizarodontograma = True

                        if actualizarodontograma:
                            odontograma_principal.save()

                            # verificarsinotieneodontograma = Odontograma.objects.get(status=True, paciente=cita.paciente,
                            #                                                         tipo=1)
                            odontograma.tipo = 2
                        odontograma.paciente = cita.paciente
                        odontograma.save(request)
                        consulta = Consulta(
                            paciente=cita.paciente,
                            doctor=cita.doctor,
                            motivo_consulta = form.cleaned_data['motivoconsulta'],
                            descripcion_problema = form.cleaned_data['descripcionmotivo'],
                            diagnostico_previo=form.cleaned_data['diagnostico'],
                            observacion = form.cleaned_data['observaciondiagnostico'],
                            temperatura=form.cleaned_data['temperatura'],
                            respiracion=form.cleaned_data['respiracion'],
                            presion_arterial=form.cleaned_data['presionarterial'],
                            pulso=form.cleaned_data['pulso'],
                            frec_respiratoria=form.cleaned_data['frecuenciarespiratoria'],
                            frec_cardiaca=form.cleaned_data['frecuenciacardiaca'],
                            odontograma=odontograma,
                            # observacion=form.cleaned_data['observacion'],
                        )
                        consulta.save(request)
                        # consulta.tratamientos.clear()
                        # for foo in form.cleaned_data['tratamientos']:
                        #     consulta.tratamientos.add(foo)
                        for foo in form.cleaned_data['tratamientos']:
                            consultatratamiento = ConsultaTratamientoPaciente(consultas=consulta,
                                                                       tratamientos=foo)
                            consultatratamiento.save(request)
                        rubrogenerado = Rubro(paciente_id=int(request.POST['idpaciente']),
                                              consulta_id=consulta.id,
                                              nombre=consulta.motivo_consulta,
                                              valor=consulta.obtener_costototal(),
                                              fecha=datetime.now().date(),
                        )
                        rubrogenerado.save(request)
                    '''
                    #realizar el guardado de la consulta - diagnostico previo - tratamiento y odontograma
                    '''

                    return JsonResponse({"respuesta": True, "mensaje": "Se registro correctamente la consulta."})
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
            if peticion == 'atender_consulta':
                try:
                    data['titulo'] = 'Consulta'
                    data['titulo_formulario'] = 'Formulario de atención de consulta a paciente'
                    data['peticion'] = 'atender_consulta'
                    data['persona_logeado'] = persona_logeado
                    data['cita'] = cita = AgendarCita.objects.get(pk=request.GET['id'])
                    form2 = ConsultaForm()
                    data['form2'] = form2
                    return render(request, "atender_cita/consulta.html", data)
                except Exception as ex:
                    transaction.set_rollback(True)
                    pass

            if peticion == 'enviar_correo':
                try:
                    from django.conf import settings
                    from django.core.mail import send_mail
                    data['cita'] = cita = AgendarCita.objects.get(pk=request.GET['id'])

                    titulo_del_correo = 'RECORDATORIO / CITA MÉDICA / ODONTÓLOGO :)'
                    cuerpo_del_correo = 'Hola, este es un correo enviado por el sistema odontologico, se le recuerda que tiene una cita planificada para la fecha: %s y horario : %s.  Por favor no contestar a este correo.' % (
                    cita.fecha, cita.horario)
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
                data['titulo'] = 'Citas Planificadas'
                data['titulo_tabla'] = 'Lista  de citas'
                data['persona_logeado'] = persona_logeado
                if not persona_logeado =='SUPERADMINISTRADOR':
                    lista = AgendarCita.objects.filter(status=True,doctor__persona= persona_logeado ).order_by('-estado_cita')
                else:
                    lista = AgendarCita.objects.filter(status=True).order_by('fecha')

                paginator = Paginator(lista, 15)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                data['page_obj'] = page_obj

                return render(request, "atender_cita/view.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
