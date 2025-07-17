# Importando os módulos necessários
from django import forms
from .models import Vaga

class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = ['titulo', 'descricao', 'nivel', 'localidade', 'salario', 'ativa']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 5}), # Torna o campo de descrição maior
        }
        labels = {
            'titulo': 'Título da Vaga',
            'descricao': 'Descrição Detalhada',
            'nivel': 'Nível da Vaga',
            'localidade': 'Localidade da Vaga',
            'salario': 'Salário (opcional)',
            'ativa': 'Vaga Ativa',
        }

# Importando os módulos necessários
from django import forms
from django.contrib.auth.forms import UserCreationForm # Importa o formulário de criação de usuário do Django
from .models import Vaga, Empresa # Garanta que Empresa está importada

# ... (Seu VagaForm existente aqui) ...

class EmpresaSignUpForm(UserCreationForm):
    nome_fantasia = forms.CharField(max_length=200, label="Nome da Empresa")
    cnpj = forms.CharField(max_length=18, label="CNPJ")
    descricao = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label="Descrição da Empresa")
    site = forms.URLField(required=False, label="Site da Empresa")

    class Meta(UserCreationForm.Meta):
        # Campos do modelo User que queremos usar
        model = UserCreationForm.Meta.model
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',) # Adiciona nome e email

    def save(self, commit=True):
        user = super().save(commit=False) # Salva o usuário primeiro, mas não no BD ainda
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')

        if commit:
            user.save() # Salva o usuário no banco de dados

            # Agora cria a Empresa e a vincula ao usuário
            empresa = Empresa.objects.create(
                user=user,
                nome_fantasia=self.cleaned_data['nome_fantasia'],
                cnpj=self.cleaned_data['cnpj'],
                descricao=self.cleaned_data.get('descricao', ''),
                site=self.cleaned_data.get('site', '')
            )
        return user # Retorna o objeto User criado

    # Opcional: Adicionar validação de CNPJ
    def clean_cnpj(self):
        cnpj = self.cleaned_data['cnpj']
        # Aqui você pode adicionar lógica de validação de formato de CNPJ
        # Ex: remover caracteres não numéricos
        import re
        cnpj_numerico = re.sub(r'\D', '', cnpj) # Remove tudo que não é dígito

        if Empresa.objects.filter(cnpj=cnpj_numerico).exists():
            raise forms.ValidationError("Este CNPJ já está cadastrado.")
        if len(cnpj_numerico) != 14: # CNPJ tem 14 dígitos numéricos
             raise forms.ValidationError("CNPJ inválido. Deve conter 14 dígitos numéricos.")
        return cnpj_numerico
    
from django import forms
from .models import Candidatura

class CandidaturaForm(forms.ModelForm):
    class Meta:
        model = Candidatura
        fields = '__all__'  # Ou especifique os campos desejados