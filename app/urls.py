# app/urls.py
from django.urls import path
from . import views # Importa as views do seu app

urlpatterns = [
    # Rotas para o CRUD de Vagas
    path('vagas/', views.VagaListView.as_view(), name='vaga_list'),
    path('vagas/nova/', views.VagaCreateView.as_view(), name='vaga_create'),
    path('vagas/<int:pk>/editar/', views.VagaUpdateView.as_view(), name='vaga_update'),
    path('vagas/<int:pk>/excluir/', views.VagaDeleteView.as_view(), name='vaga_delete'),
    path('cadastro-empresa/', views.EmpresaSignUpView.as_view(), name='cadastro_empresa'),
    path('vagas-publicas/', views.VagaPublicaListView.as_view(), name='vagas_publicas'),
    path('vagas-publicas/<int:pk>/candidatar/', views.CandidaturaCreateView.as_view(), name='candidatar_vaga')
]