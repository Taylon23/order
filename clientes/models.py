from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


class DadosClientesModel(models.Model):
    razao_social = models.CharField(max_length=100)
    fantasia = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, null=True, blank=True)
    cnpj = models.CharField(max_length=18, null=True, blank=True)
    fone = models.CharField(max_length=12, blank=True)
    email = models.CharField(max_length=100, blank=True)
    cep = models.CharField(max_length=10, blank=True)
    cidade = models.CharField(max_length=100)
    endereco = models.CharField(max_length=100)
    numero_casa = models.CharField(max_length=4)
    bairro = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    inscricao_estadual = models.CharField(max_length=18, blank=True)

    def __str__(self):
        return f'{self.razao_social}'

    def clean(self):
        cpf_existente = DadosClientesModel.objects.filter(
            cpf=self.cpf).exclude(pk=self.pk).exists() if self.cpf else False
        cnpj_existente = DadosClientesModel.objects.filter(
            inscricao_estadual=self.cnpj).exclude(pk=self.pk).exists() if self.cnpj else False
        if cpf_existente:
            raise ValidationError('Usuário com o mesmo CPF já foi cadastrado')
        if cnpj_existente:
            raise ValidationError(
                'Usuário com a mesma inscrição estadual já foi cadastrado')
        if self.cpf is not None and (len(self.cpf) != 14):
            raise ValidationError('Informe um CPF válido')
        if self.cnpj is not None and (len(self.cnpj) != 18):
            raise ValidationError('Informe um CNPJ válido')
        if len(self.fone) != 12:
            raise ValidationError('Informe um número de telefone válido')
        if self.cpf is None and self.cnpj is None:
            raise ValidationError(
                "Informe pelo menos o CPF ou a inscrição estadual")
        if self.cnpj and not self.inscricao_estadual:
            raise ValidationError('Informe a inscrição estadual')


class ProdutoModel(models.Model):
    nome = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.nome}'


class PedidoModel(models.Model):
    cliente = models.ForeignKey(DadosClientesModel, on_delete=models.CASCADE)
    valor_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    created_date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def clean(self):
        if self.valor_total < 0:
            raise ValidationError('Informe o valor maior ou igual a 0')

    def calcular_valor_total(self):
        total = 0.0
        itens_pedido = self.itempedidomodel_set.all()

        for item in itens_pedido:
            item.valor = item.produto.valor  # atribui o valor do produto ao item
            item.save()  # salva o item no banco de dados
            total += item.quantidade * item.valor

        self.valor_total = total  # Atualiza o valor_total do pedido
        self.save()  # Salva o pedido no banco de dados

        return total

    def __str__(self):
        return f'Cliente: {self.cliente} - Pedido: {self.pk}'


class ItemPedidoModel(models.Model):
    pedido = models.ForeignKey(PedidoModel, on_delete=models.CASCADE)
    produto = models.ForeignKey(ProdutoModel, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    valor_unitario = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f'Item do pedido {self.pedido.pk}: Produto: {self.produto.nome}'

    def clean(self):
        if self.quantidade <= 0:
            raise ValidationError('Informe pelo menos uma quantidade')


@receiver(post_save, sender=ItemPedidoModel)
@receiver(post_delete, sender=ItemPedidoModel)
def atualizar_valor_total_pedido(sender, instance, **kwargs):
    item_pedido = instance
    valor_unitario = item_pedido.quantidade * item_pedido.valor

    # Atualiza o campo valor_unitario do ItemPedidoModel
    ItemPedidoModel.objects.filter(pk=item_pedido.pk).update(valor_unitario=valor_unitario)

    # Atualiza o valor_total do PedidoModel
    pedido = item_pedido.pedido
    itens_pedido = pedido.itempedidomodel_set.all()
    total = sum(item.quantidade * item.valor_unitario for item in itens_pedido)
    pedido.valor_total = total
    pedido.save()
