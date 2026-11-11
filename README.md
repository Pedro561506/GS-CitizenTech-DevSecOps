# GS-CitizenTech-DevSecOps
Global Solution FIAP 2026 - Pipeline DevSecOps CI/CD para API CitizenTech com FastAPI, Jenkins, SonarQube, Trivy e Docker.
# CitizenTech — CivicLens DevSecOps

**Global Solution FIAP 2026 — DevOps & DevSecOps**

## Sobre o projeto

Este projeto apresenta uma API simplificada de gerenciamento de ocorrências urbanas, desenvolvida com Python e FastAPI, no contexto da Global Solution CitizenTech.

A proposta é demonstrar a aplicação de práticas DevSecOps por meio de uma pipeline CI/CD, integrando testes automatizados, análise de qualidade, segurança, construção de imagens Docker, publicação e deploy.

O projeto utiliza como referência a proposta do [CivicLens](https://github.com/tejasbhor/Civiclens), uma plataforma open source de gerenciamento de ocorrências urbanas.

## Tecnologias

- Python e FastAPI
- Pytest
- Git e GitHub
- Docker e Docker Compose
- Jenkins
- SonarQube
- Trivy
- Docker Hub

## Endpoints

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/health` | Verifica o funcionamento da API |
| GET | `/ocorrencias` | Retorna a lista de ocorrências urbanas |

## Execução local

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

Inicie a aplicação:

```powershell
python -m uvicorn app.main:app --reload
```

A documentação estará disponível em:

`http://localhost:8000/docs`

## Execução com Docker

Construa a imagem:

```powershell
docker build -t citizentech-api:v1 .
```

Execute o container:

```powershell
docker run -d --name citizentech-api -p 8000:8000 citizentech-api:v1
```

## Testes automatizados

Instale as dependências de desenvolvimento:

```powershell
python -m pip install -r requirements-dev.txt
```

Execute:

```powershell
python -m pytest -v
```

## Pipeline DevSecOps

O fluxo previsto é:

GitHub → Jenkins → Testes → SonarQube → Quality Gate → Docker Build → Trivy → Docker Hub → Docker Compose → Validação.

**Status:** integração CI/CD em desenvolvimento.

## Participantes

- Pedro de Carvalho Gonçalves (561506)
- Edmário Santos (565486)
- Kaue Lima (562071)
- Turma: 2TCNPZ-2026

## Referência e licença

Projeto acadêmico desenvolvido com referência ao CivicLens. Caso código do projeto original seja reutilizado, serão preservados os avisos de copyright e os termos da licença MIT correspondentes.

Pipeline CI/CD com Jenkins e verificacao automatica de alteracoes no GitHub.
