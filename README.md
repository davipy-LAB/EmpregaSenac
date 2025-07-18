# 🧑‍💼 EmpregaSenac

Uma plataforma web desenvolvida com Django para conectar empresas e candidatos de forma simples, direta e eficaz. O sistema permite que empresas publiquem vagas de emprego e que candidatos se candidatem com envio de currículos em PDF, recebendo confirmações por e-mail.

---

![Imagem do WhatsApp de 2025-07-18 à(s) 13 59 49_fd10edf9](https://github.com/user-attachments/assets/b55c273b-e607-45df-b9f3-79e257fefe16)


## 🎯 Objetivo

Criar um sistema completo de cadastro de vagas e envio de candidaturas, com foco em usabilidade, segurança, comunicação eficiente e deploy em ambiente profissional.

---

## 🧩 Funcionalidades Principais

### ✅ Cadastro e Gerenciamento de Vagas
- CRUD completo de vagas (Create, Read, Update, Delete)
- Proteção por login (somente empresas autenticadas)
- Views baseadas em classe (CBV)
- Campos: título, descrição, nível, localidade, salário e empresa

### ✅ Visualização Pública e Filtros Dinâmicos
- Página pública com todas as vagas
- Filtros por nível e localidade via query string
- Ordenação por data ou título

### ✅ Envio de Candidaturas
- Formulário com campos: nome, e-mail, vaga e upload de currículo (PDF)
- Upload seguro para a nuvem via *Cloudinary*
- Armazenamento da candidatura no banco de dados
- Envio de e-mail:
  - Para o candidato (confirmação)
  - Para o RH da empresa (dados da candidatura)

### ✅ Sistema de Autenticação
- Cadastro e login de empresas
- Acesso restrito para criação/edição de vagas e visualização de candidaturas

### ✅ Interface e UX
- Templates estilizados com *Bootstrap*
- Mensagens de feedback usando Django Messages (ex: “vaga criada com sucesso”)

### ✅ Deploy
- Hospedado no *Render*
- LINK DO DEPLOY: https://empregasenac.onrender.com/minhas-vagas/vagas/

---

