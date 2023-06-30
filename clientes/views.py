from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse_lazy
from . import models
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class CreateClientesView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('account_login')
    model = models.DadosClientesModel
    template_name = 'Forms/form_cliente.html'
    fields = ['razao_social', 'fantasia', 'cpf', 'cnpj', 'inscricao_estadual', 'fone',
              'email', 'cep', 'cidade', 'endereco', 'numero_casa', 'bairro']
    success_url = reverse_lazy('tabela-clientes')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['Butao'] = 'Cadastrar'
        context['TituloForm'] = 'Criar Cliente'

        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateClitenteView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('account_login')
    model = models.DadosClientesModel
    template_name = 'Forms/form_cliente.html'
    fields = ['razao_social', 'fantasia', 'cpf', 'cnpj', 'inscricao_estadual', 'fone',
              'email', 'cep', 'cidade', 'endereco', 'numero_casa', 'bairro']

    def get_success_url(self):
        perfil_id = self.kwargs['pk']
        return reverse_lazy('perfil-cliente', args=[perfil_id])

    def get_object(self, queryset=None):
        object = get_object_or_404(
            models.DadosClientesModel.objects.filter(user=self.request.user), pk=self.kwargs['pk'])
        return object

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['Butao'] = 'Atualizar'
        context['TituloForm'] = 'Atualizar Cliente'
        return context


class DeleteCliente(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('account_login')
    model = models.DadosClientesModel
    template_name = 'Forms/form_deletar_cliente.html'
    success_url = reverse_lazy('tabela-clientes')

    def get_object(self, queryset=None):
        object = get_object_or_404(
            models.DadosClientesModel.objects.filter(user=self.request.user), pk=self.kwargs['pk'])
        return object


def TabelaClientesView(request):
    dados_clientes = models.DadosClientesModel.objects.filter(
        user=request.user)
    return render(request, 'paginas/tabela_clientes.html',
                  {'dados_clientes': dados_clientes})


class CriarProdutoCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('account_login')
    queryset = models.ProdutoModel.objects.all()
    fields = ['nome']
    template_name = 'Forms/form_produto.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['TituloForm'] = 'Crie agora seu produto'
        context['Butao'] = 'Criar'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditarProdutoUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('account_login')
    queryset = models.ProdutoModel.objects.all()
    fields = ['nome']
    template_name = 'Forms/form_produto.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['TituloForm'] = 'Editar produto'
        context['Butao'] = 'Editar'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_object(self, queryset=None):
        object = get_object_or_404(
            models.ProdutoModel.objects.filter(user=self.request.user), pk=self.kwargs['pk'])
        return object


class DeletarProdutoDelete(DeleteView):
    login_url = reverse_lazy('account_login')
    queryset = models.ProdutoModel.objects.all()
    template_name = 'Forms/form_deletar.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['TituloForm'] = 'Deseja deletar o produto?'
        return context

    def get_object(self, queryset=None):
        object = get_object_or_404(
            models.ProdutoModel.objects.filter(user=self.request.user), pk=self.kwargs['pk'])
        return object


@login_required(login_url='account_login')
def PerfilClienteView(request, id):
    perfil = get_object_or_404(
        models.DadosClientesModel.objects.filter(user=request.user), pk=id)
    return render(request, 'paginas/perfil_cliente.html', {'perfil': perfil})


class CreatePedidoView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('account_login')
    model = models.PedidoModel
    fields = ['cliente', 'valor_total']
    success_url = reverse_lazy('tabela-pedido')
    template_name = 'Forms/form_pedido.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['cliente'].queryset = form.fields['cliente'].queryset.filter(
            user=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['Butao'] = 'Criar'
        context['TituloForm'] = 'Criar Pedido'
        return context


class UpdatePedidoView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('account_login')
    model = models.PedidoModel
    fields = ['cliente', 'valor_total']
    success_url = reverse_lazy('tabela-pedido')
    template_name = 'Forms/form_pedido.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['cliente'].queryset = form.fields['cliente'].queryset.filter(
            user=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['Butao'] = 'Atualizar'
        context['TituloForm'] = 'Atualizar Pedido'
        return context

    def get_object(self, queryset=None):
        object = get_object_or_404(
            models.PedidoModel.objects.filter(user=self.request.user), pk=self.kwargs['pk'])
        return object


class DeletePedidoView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('account_login')
    model = models.PedidoModel
    success_url = reverse_lazy('tabela-pedido')
    template_name = 'Forms/form_deletar_pedido.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['TituloForm'] = 'Deseja finalizar o pedido?'
        context['Button'] = 'Finalizar'
        return context

    def get_object(self, queryset=None):
        object = get_object_or_404(
            models.PedidoModel.objects.filter(user=self.request.user), pk=self.kwargs['pk'])
        return object


@login_required(login_url='account_login')
def TabelaPedidoView(request):
    pedidos = models.PedidoModel.objects.filter(user=request.user)

    return render(request, 'paginas/tabela_pedidos.html', {'pedidos': pedidos},)


class CreateAdicionarProduto(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('account_login')
    model = models.ItemPedidoModel
    fields = ['pedido', 'produto', 'quantidade', 'valor']
    success_url = reverse_lazy('tabela-pedido')
    template_name = 'Forms/form_itens.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['produto'].queryset = form.fields['produto'].queryset.filter(
            user=self.request.user)
        form.fields['pedido'].queryset = form.fields['pedido'].queryset.filter(
            user=self.request.user)

        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['Butao'] = 'Criar'
        context['TituloForm'] = 'Adicionar item'

        return context


@login_required(login_url='account_login')
def ItensPedido(request, pedido_id):
    pedido = get_object_or_404(
        models.PedidoModel, user=request.user, pk=pedido_id)
    itens_pedido = pedido.itempedidomodel_set.all()

    context = {
        'pedido': pedido,
        'itens_pedido': itens_pedido
    }

    return render(request, 'paginas/tabela_itens_pedido.html', context)


@login_required(login_url='account_login')
def excluir_item_pedido(request, pedido_id, item_id):
    item = get_object_or_404(models.ItemPedidoModel.objects.filter(user=request.user),
                             pedido_id=pedido_id, id=item_id)

    if request.method == 'POST':
        item.delete()
        return redirect('itens_pedido', pedido_id=pedido_id)

    context = {
        'item': item,
        'pedido_id': pedido_id
    }

    return render(request, 'Forms/form_deletar_item.html', context)
