import sys

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import PasswordChangeView
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy

from aplication import settings
from odontologico.forms import RegistroUsuarioForm, CambiarContraseñaForm
from odontologico.funciones import add_data_aplication
from odontologico.models import Modulo, Persona, Paciente, PersonaPerfil, AccesoModulo


# cambiar contraseña
class PasswordChangeView(PasswordChangeView):
    template_name = 'registration/cambiarcontrasena.html'
    form_class = CambiarContraseñaForm
    success_url = reverse_lazy('logout_usuario')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['titulo'] = "Cambiar Contraseña"
        return context


@transaction.atomic()
def login_usuario(request):
    global ex
    data = {}
    if request.method == 'POST':
        if 'peticion' in request.POST:
            peticion = request.POST['peticion']
            if peticion == 'login_usuario':
                try:
                    usuario = authenticate(username=request.POST['usuario'].lower().strip(), password=request.POST['clave'])
                    if usuario is not None:
                        if usuario.is_active:
                            login(request, usuario)
                            return JsonResponse({"respuesta": True, "url": settings.LOGIN_REDIRECT_URL})
                        else:
                            return JsonResponse({"respuesta": False, 'mensaje': u'Inicio de sesión incorrecto, usuario no activo.'})
                    else:
                        return JsonResponse({"respuesta": False,'mensaje': u'Inicio de sesión incorrecto, usuario o clave no coinciden.'})
                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse(
                        {"respuesta": False, "mensaje": "Error al iniciar sesión, intentelo más tarde."})
        return JsonResponse({"respuesta": False, "mensaje": "acción Incorrecta."})
    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']
        else:
            try:
                if 'persona' in request.session:
                    return HttpResponseRedirect("/")
                data['titulo'] = 'Inicio de sesión'
                data['request'] = request
                return render(request, "registration/login.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))


def logout_usuario(request):
    logout(request)
    return HttpResponseRedirect("/login")

@transaction.atomic()
def registrate(request):
    global ex
    data = {}
    if request.method == 'POST':
        if 'peticion' in request.POST:
            peticion = request.POST['peticion']
            if peticion == 'registrarpaciente':
                try:
                    if request.session.get('id') != None:  # Regístrese solo cuando no haya iniciado sesión
                        return JsonResponse({"respuesta": False, "mensaje": "Ya tiene sesión iniciada."})
                    form = RegistroUsuarioForm(request.POST)

                    if form.is_valid():
                        username = form.cleaned_data['username']
                        password = form.cleaned_data['password1']
                        nombre1 = form.cleaned_data['nombre1']
                        nombre2 = form.cleaned_data['nombre2']
                        apellido1 = form.cleaned_data['apellido1']
                        apellido2 = form.cleaned_data['apellido2']
                        cedula = form.cleaned_data['cedula']
                        genero = form.cleaned_data['genero']
                        telefono_movil = form.cleaned_data['telefono_movil']
                        telefono_convencional = form.cleaned_data['telefono_convencional']
                        email = form.cleaned_data['email']
                        username = username.strip()  # Eliminar espacios y líneas nuevas
                        password = password.strip()
                        usuario = User.objects.create_user(username, email, password)
                        usuario.save()

                        grupo = Group.objects.get(pk=4)  # PACIENTE
                        grupo.user_set.add(usuario)

                        persona = Persona(
                            usuario=usuario,
                            nombre1=nombre1,
                            nombre2=nombre2,
                            apellido1=apellido1,
                            apellido2=apellido2,
                            email=email,
                            cedula=cedula,
                            genero=genero,
                            telefono_movil=telefono_movil,
                            telefono_convencional=telefono_convencional
                        )
                        persona.save(request)

                        persona_perfil = PersonaPerfil(
                            persona=persona,
                            is_paciente=True
                        )
                        persona_perfil.save(request)

                        paciente = Paciente(
                            persona=persona
                        )
                        paciente.save(request)
                        return redirect('/login/')

                    else:
                        return render(request, "registration/registrate.html", {'form': form})
                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})
        return JsonResponse({"respuesta": False, "mensaje": "No se ha encontrado respuesta."})

    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']

            if peticion == 'validar_cedula':
                cedula = request.GET['cedula']
                persona = Persona.objects.filter(status=True, cedula=cedula)
                if persona.exists():
                    return JsonResponse({"respuesta": True, 'mensaje': 'Cédula ya existe'})
                else:
                    return JsonResponse({"respuesta": False, 'mensaje': ''})

            if peticion == 'validar_usuario':
                usuario = request.GET['usuario']
                persona = User.objects.filter(username=usuario)
                if persona.exists():
                    return JsonResponse({"respuesta": True, 'mensaje': 'Usuario ya existe'})
                else:
                    return JsonResponse({"respuesta": False, 'mensaje': ''})

            if peticion == 'validar_email':
                correo = request.GET['email']
                email = Persona.objects.filter(email=correo, status=True)
                if email.exists():
                    return JsonResponse({"respuesta": True, 'mensaje': 'Email ya existe'})
                else:
                    return JsonResponse({"respuesta": False, 'mensaje': ''})


        else:
            data['form'] = RegistroUsuarioForm()

    return render(request, "registration/registrate.html", data)


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def dashboard(request):
    global ex
    data = {}
    add_data_aplication(request, data)
    usuario_logeado = request.user
    if  Persona.objects.filter(usuario=usuario_logeado, status=True).exists():
        persona_logeado = Persona.objects.get(usuario=usuario_logeado, status=True)
    else:
        persona_logeado = 'SUPERADMINISTRADOR'

    if request.method == 'POST':
        if 'peticion' in request.POST:
            peticion = request.POST['peticion']
    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']

        else:
            try:
                data['titulo'] = 'Menú principal'
                mis_perfiles = None
                #obtener perfiles
                if not 'SUPERADMINISTRADOR' == persona_logeado:
                    mis_perfiles = PersonaPerfil.objects.filter(status=True, persona=persona_logeado)
                    data['mis_perfiles'] = mis_perfiles

                #obtener modulos
                if usuario_logeado.is_superuser:
                    modulos = Modulo.objects.filter(status=True,activo=True)

                else:
                    menu = AccesoModulo.objects.values_list('modulo_id').filter(status = True, activo = True ,grupo__in = usuario_logeado.groups.all())
                    modulos = Modulo.objects.filter(status=True, activo=True, pk__in = menu )
                data['persona_logeado'] = persona_logeado
                data['modulos'] = modulos
                return render(request, "registration/dashboard.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
