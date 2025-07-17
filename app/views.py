# app/views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin # Para proteger as rotas
from .models import Vaga, Empresa
from .forms import VagaForm
from django.shortcuts import get_object_or_404, render # Render já estava, mantendo
from django.contrib import messages
from django.http import Http404 # Adicionado para a exceção
from .models import Vaga, Empresa, Candidatura #
from .forms import VagaForm, CandidaturaForm #
from django.shortcuts import get_object_or_404, render #
from django.contrib import messages
from django.http import Http404 # Garanta que Http404 está importado


# Mixin para garantir que apenas a empresa dona da vaga possa manipulá-la
class EmpresaProprietariaMixin:
    def get_queryset(self):
        # Filtra as vagas para mostrar apenas as da empresa do usuário logado
        # Adição de verificação para garantir que o usuário tenha um perfil de empresa
        if not hasattr(self.request.user, 'empresa_profile'):
            return self.model.objects.none() # Retorna um queryset vazio se não houver empresa
        return self.model.objects.filter(empresa__user=self.request.user)

    # REMOVIDO O form_valid DAQUI!
    # def form_valid(self, form):
    #     empresa = get_object_or_404(Empresa, user=self.request.user)
    #     form.instance.empresa = empresa
    #     return super().form_valid(form)

    def get_object(self, queryset=None):
        # Garante que o usuário só possa editar/deletar suas próprias vagas
        obj = super().get_object(queryset)
        # Verifica se o objeto existe e se o usuário logado é o dono da empresa da vaga
        if obj.empresa.user != self.request.user:
            messages.error(self.request, "Você não tem permissão para acessar esta vaga.")
            raise Http404("Vaga não encontrada ou acesso não permitido.") # Levanta um 404
        return obj

# ----------------------------------------------------
# Views para Gerenciamento de Vagas pela Empresa (CRUD)
# ----------------------------------------------------

# Lista as vagas da empresa logada
class VagaListView(LoginRequiredMixin, EmpresaProprietariaMixin, ListView):
    model = Vaga
    template_name = 'app/vaga_list.html'
    context_object_name = 'vagas'


# Cria uma nova vaga
class VagaCreateView(LoginRequiredMixin, EmpresaProprietariaMixin, CreateView):
    model = Vaga
    form_class = VagaForm
    template_name = 'app/vaga_form.html'
    success_url = reverse_lazy('vaga_list')

    def form_valid(self, form):
        # Lógica para associar a vaga à empresa do usuário logado APENAS AQUI
        empresa = get_object_or_404(Empresa, user=self.request.user)
        form.instance.empresa = empresa
        messages.success(self.request, "Vaga criada com sucesso!")
        return super().form_valid(form)


# Edita uma vaga existente
class VagaUpdateView(LoginRequiredMixin, EmpresaProprietariaMixin, UpdateView):
    model = Vaga
    form_class = VagaForm
    template_name = 'app/vaga_form.html'
    success_url = reverse_lazy('vaga_list')

    def form_valid(self, form):
        # Lógica para associar a vaga à empresa do usuário logado APENAS AQUI
        # (Embora para Update, o form.instance.empresa já existiria, manter aqui é seguro)
        empresa = get_object_or_404(Empresa, user=self.request.user)
        form.instance.empresa = empresa
        messages.success(self.request, "Vaga atualizada com sucesso!")
        return super().form_valid(form)


# Deleta uma vaga
class VagaDeleteView(LoginRequiredMixin, EmpresaProprietariaMixin, DeleteView):
    model = Vaga
    template_name = 'app/vaga_confirm_delete.html'
    success_url = reverse_lazy('vaga_list')

    # NÃO COLOQUE O MÉTODO form_valid AQUI COM form.instance.empresa = ...
    # O form_valid para DeleteView apenas executa a ação de deleção.
    def form_valid(self, form):
        # Esta linha ainda é necessária para processar a exclusão e redirecionar
        # e para exibir a mensagem de sucesso.
        messages.success(self.request, "Vaga excluída com sucesso!")
        return super().form_valid(form)
    
# ----------------------------------------------------
# Views para Autenticação e Cadastro
# ----------------------------------------------------

from django.contrib.auth import login # Importa a função login
from .forms import EmpresaSignUpForm # Importa o formulário de cadastro de empresa

class EmpresaSignUpView(CreateView):
    form_class = EmpresaSignUpForm # Usa o formulário que acabamos de criar
    template_name = 'app/cadastro_empresa.html' # Template para o formulário de cadastro
    success_url = reverse_lazy('vaga_list') # Redireciona para a lista de vagas após o cadastro

    def form_valid(self, form):
        response = super().form_valid(form)
        # Loga o usuário imediatamente após o cadastro bem-sucedido
        login(self.request, self.object)
        messages.success(self.request, "Cadastro realizado com sucesso! Bem-vindo(a) ao EmpregaSenac.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Cadastre sua Empresa"
        return context
    
# app/views.py

# ... (Seus imports, EmpresaProprietariaMixin, VagaListView, VagaCreateView, VagaUpdateView, VagaDeleteView, EmpresaSignUpView existentes) ...

# ----------------------------------------------------
# Views para Visualização Pública de Vagas e Filtros
# ----------------------------------------------------

class VagaPublicaListView(ListView):
    model = Vaga
    template_name = 'app/vagas_publicas_list.html'
    context_object_name = 'vagas_publicas' # Um nome diferente para evitar conflitos se você usar includes

    def get_queryset(self):
        queryset = super().get_queryset().filter(ativa=True) # Apenas vagas ativas

        # Filtro por Nível
        nivel = self.request.GET.get('nivel')
        if nivel:
            queryset = queryset.filter(nivel=nivel)

        # Filtro por Localidade
        localidade = self.request.GET.get('localidade')
        if localidade:
            queryset = queryset.filter(localidade__icontains=localidade) # __icontains para busca parcial e case-insensitive

        # Ordenação
        ordenar_por = self.request.GET.get('ordenar_por')
        if ordenar_por:
            if ordenar_por == 'salario_asc':
                queryset = queryset.order_by('salario')
            elif ordenar_por == 'salario_desc':
                queryset = queryset.order_by('-salario')
            elif ordenar_por == 'titulo_asc':
                queryset = queryset.order_by('titulo')
            elif ordenar_por == 'titulo_desc':
                queryset = queryset.order_by('-titulo')
            # Data de publicação já é padrão no Meta do modelo Vaga
            # elif ordenar_por == 'data_desc':
            #    queryset = queryset.order_by('-data_publicacao')
            # elif ordenar_por == 'data_asc':
            #    queryset = queryset.order_by('data_publicacao')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adiciona os valores dos filtros atuais para preencher o formulário
        context['niveis'] = Vaga.NIVEL_CHOICES # Passa as opções de nível para o template
        context['selected_nivel'] = self.request.GET.get('nivel', '')
        context['selected_localidade'] = self.request.GET.get('localidade', '')
        context['selected_ordenar_por'] = self.request.GET.get('ordenar_por', '')
        return context
    
# ----------------------------------------------------
# View para Candidatura Pública
# ----------------------------------------------------

class CandidaturaCreateView(CreateView):
    model = Candidatura #
    form_class = CandidaturaForm #
    template_name = 'app/candidatura_form.html' # Vamos criar este template
    # success_url será definido no form_valid para redirecionar para a vaga,
    # ou para uma página de confirmação.

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Passa a instância da vaga para o formulário, se necessário para alguma validação
        # ou apenas para ter certeza de que o formulário está ciente da vaga
        # self.vaga é definido em get_context_data ou get_object
        if hasattr(self, 'vaga'):
            kwargs['initial'] = {'vaga': self.vaga}
        return kwargs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obter a vaga a partir da URL (pk)
        vaga_pk = self.kwargs.get('pk')
        self.vaga = get_object_or_404(Vaga, pk=vaga_pk, ativa=True) # Apenas vagas ativas
        context['vaga'] = self.vaga
        context['title'] = f"Candidatar-se para: {self.vaga.titulo}"
        return context

    def form_valid(self, form):
        # A vaga foi obtida em get_context_data
        form.instance.vaga = self.vaga
        messages.success(self.request, "Sua candidatura foi enviada com sucesso!")
        return super().form_valid(form)

    def get_success_url(self):
        # Redireciona de volta para a página de detalhes da vaga ou para a lista de vagas públicas
        # por enquanto, redireciona para a lista de vagas públicas.
        return reverse_lazy('vagas_publicas')
        # Alternativamente, para uma página de detalhes da vaga (se você criar uma):
        # return reverse_lazy('vaga_detalhe_publico', kwargs={'pk': self.v.pk})
# ----------------------------------------------------
