from django.db import models

class ModeloBase(models.Model):
    from django.contrib.auth.models import User
    usuario_creacion = models.ForeignKey(User, verbose_name='Usuario Creación', blank=True, null=True, on_delete= models.CASCADE, related_name='+', editable=False)
    fecha_creacion = models.DateTimeField(verbose_name='Fecha creación',auto_now_add=True)
    fecha_modificacion = models.DateTimeField(verbose_name='Fecha Modificación', auto_now=True)
    usuario_modificacion = models.ForeignKey(User, verbose_name='Usuario Modificación', blank=True, null=True, on_delete= models.CASCADE, related_name='+', editable=False)
    status = models.BooleanField(verbose_name="Estado del registro", default=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        usuario = None
        if len(args):
            usuario = args[0].user.id
        if self.id:
            self.usuario_modificacion_id = usuario
        else:
            self.usuario_creacion_id = usuario
        models.Model.save(self)

def add_data_aplication(request,data):
    from odontologico.models import Modulo
    if 'lista_url_ruta' not in request.session:
        request.session['lista_url_ruta'] = [['/', 'Inicio']]
    lista_url_ruta = request.session['lista_url_ruta']
    if request.method == 'GET' and request.path:
        if Modulo.objects.values("id").filter(ruta=request.path[1:],status=True).exists():
            modulo = Modulo.objects.values("ruta", "nombre").filter(status=True,ruta=request.path[1:])[0]
            ruta = ['/' + modulo['ruta'], modulo['nombre']]
            if lista_url_ruta.count(ruta) <= 0:
                if lista_url_ruta.__len__() >= 7:
                    last_ruta = lista_url_ruta[1]
                    lista_url_ruta.remove(last_ruta)
                    lista_url_ruta.append(ruta)
                else:
                    lista_url_ruta.append(ruta)
            request.session['lista_url_ruta'] = lista_url_ruta
        else:
            pass
    data["lista_url_ruta"] = lista_url_ruta
