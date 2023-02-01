from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User

from odontologico.models import Modulo, Genero, Persona, Paciente, PersonaPerfil, AccesoModulo, Horario_hora, \
    AgendarCita, TiempoAntesRecordatorioCorreo, Tratamiento, Pago

admin.site.unregister(User)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username','is_staff','is_active','is_superuser','date_joined',)
    search_fields = ('username',)
    list_filter = ('is_staff', 'is_active', 'is_superuser',)

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    '''Admin View for Menu'''

    list_display = ('nombre','descripcion','icono','ruta','activo','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    list_filter = ('nombre','descripcion','activo',)
    search_fields = ('nombre','descripcion',)

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    '''Admin View for Genero'''

    list_display = ('nombre','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    list_filter = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    '''Admin View for Persona'''

    list_display = ('usuario','nombres','apellidos','cedula','genero','telefono_movil','telefono_convencional','email','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    search_fields = ('apellido1','apellido2','email',)

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    '''Admin View for Paciente'''

    list_display = ('persona','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    list_filter = ('persona',)
    search_fields = ('persona',)

@admin.register(PersonaPerfil)
class PersonaPerfilAdmin(admin.ModelAdmin):
    list_display = ('persona','is_paciente','is_administrador','is_especialista','is_asistente','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    search_fields = ('persona',)


@admin.register(AccesoModulo)
class AccesoModuloAdmin(admin.ModelAdmin):
    list_display = ('grupo','modulo','activo','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    search_fields = ('grupo','modulo',)

@admin.register(Horario_hora)
class Horario_horaAdmin(admin.ModelAdmin):
    list_display = ('hora_inicio','hora_fin','activo','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    search_fields = ('hora_inicio','hora_fin',)

@admin.register(AgendarCita)
class AgendarCitaAdmin(admin.ModelAdmin):
    list_display = ('paciente','doctor','fecha','horario','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    search_fields = ('paciente','doctor','fecha','horario',)

admin.site.register(Tratamiento)
admin.site.register(Pago)