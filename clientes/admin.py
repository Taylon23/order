from django.contrib import admin
from . import models

admin.site.register(models.DadosClientesModel)
admin.site.register(models.ProdutoModel)
admin.site.register(models.PedidoModel)
admin.site.register(models.ItemPedidoModel)