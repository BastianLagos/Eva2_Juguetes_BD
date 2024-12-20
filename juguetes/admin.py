from django.contrib import admin

from juguetes.models import Usuario, Origen , Historial, Tipo, Juguete

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['id','nombre_usuario','password_usuario']
    
class OrigenAdmin(admin.ModelAdmin):
    list_display = ['id','nombre_origen']
    
class TipoAdmin(admin.ModelAdmin):
    list_display = ['id','nombre_tipo']

class JugueteAdmin(admin.ModelAdmin):
    list_display = ['id','codigo','nombre','precio','disponibilidad','origen','cantidad','tipo','marca']
    
class HistorialAdmin(admin.ModelAdmin):
    list_display = ['id','usuario','accion_historial','tabla_historial','fecha_hora_historial']



admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Origen, OrigenAdmin)
admin.site.register(Tipo, TipoAdmin)
admin.site.register(Historial, HistorialAdmin)
admin.site.register(Juguete, JugueteAdmin)
    
