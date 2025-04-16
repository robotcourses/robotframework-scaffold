# 🤖 robotframework-scaffold

Uma ferramenta de linha de comando (CLI) interativa para criar projetos baseados em Robot Framework de forma rápida, padronizada e com boas práticas desde o início.

## 🔍 Sumário
- [🤖 robotframework-scaffold](#-robotframework-scaffold)
  - [🔍 Sumário](#-sumário)
  - [🚀 O que é?](#-o-que-é)
  - [✅ Funcionalidades](#-funcionalidades)
  - [🛠️ Requisitos](#️-requisitos)
  - [📦 Instalção](#-instalção)
  - [✌️ Utilização](#️-utilização)
  - [Vídeo](#vídeo)
  - [📁 Estrutura Gerada](#-estrutura-gerada)
  - [💡 Dicas](#-dicas)
  - [📄 Licença](#-licença)

## 🚀 O que é?

O **Robotframework-scaffold** é um gerador de estrutura de projeto para testes automatizados com **Robot Framework**, que permite escolher entre os tipos de teste mais comuns:

 - **API** (com *RequestsLibrary*)
 - **Web** (com *SeleniumLibrary* ou *BrowserLibrary*)
 - **Mobile** (com *AppiumLibrary*)

Além disso, o usuário pode escolher entre gerenciar o ambiente virtual com **Poetry** ou **venv**.

## ✅ Funcionalidades

- Criação de estrutura de pastas organizada e modular.
- [APENAS PARA API, POR ENQUANTO] Criação automática de código, com base no Swagger/OpenAPI.
- Instalação automática das bibliotecas essenciais com base no tipo de projeto.
- Criação de ambiente virtual com venv ou Poetry.
- Compatível com as boas práticas de desenvolvimento e organização de testes com Robot Framework.
- Suporte a múltiplas bibliotecas de automação web (SeleniumLibrary e BrowserLibrary).
- Experiência interativa via terminal.


## 🛠️ Requisitos

- Python 3.8 (*versão mínima suportada pelo Robot Framework 7.x*) ou superior
- Poetry (*opcional, para uso do gerenciador Poetry*)
- Acesso ao terminal ou prompt de comando


## 📦 Instalção

Você pode instalar localmente usando o  `pip` conforme abaixo:

```bash
pip install robotframework-scaffold
```

## ✌️ Utilização

O **robotframework-scaffold** segue um fluxo interativo, via terminal para criação de projetos, uma vez instalado, basta executar o seguinte comando:

```
robot-scaffold init
```

Após isso, uma série de perguntas serão realizadas para que o robotframework-scaffold entenda qual a sua necessidade. Atualmente o projeto possui suporte para API, WEB e MOBILE. Sendo que, na versão atual, apenas o fluxo de API realiza a geração automática de código, a partir de um Swagger/OpenAPI.

Para os fluxos Mobile e WEB, a geração automática de código chegará em versões futuras.

Abaixo, um breve vídeo demostrando a utilização do **robotframework-scaffold**:

<video src="doc/example_video.mp4" controls autoplay loop muted width="1920">
  Seu navegador não suporta a tag HTML5 video.
</video>

## Vídeo

[EM CONSTRUÇÃO ...]

## 📁 Estrutura Gerada
A estrutura do projeto é criada de forma modular, respeitando o tipo escolhido durante a criação. Veja abaixo exemplos para cada tipo:

- 🔌 Projeto API

```
.
├───resources/
│   ├───connections/
│   ├───data/
│   ├───routes/
│   └───utils/
├───tests/
│   ├───__init__.robot
│   .gitignore
│   base.resource
│   pyproject.toml
│   README.md
```

- 🌐 Projeto Web

```
.
├───resources/
│   ├───common/
│   ├───data/
│   ├───locators/
│   ├───pages/
│   └───utils/
├───tests/
│   .gitignore
│   base.resource
│   pyproject.toml
│   README.md
```

- 📱 Projeto Mobile

```
.   
├───resources/
│   ├───app/
│   ├───common/
│   ├───data/
│   ├───locators/
│   ├───pages/
│   └───utils/
├───tests/
│   .gitignore
│   base.resource
│   pyproject.toml
│   README.md
```

## 💡 Dicas

Se você estiver usando VSCode, o ambiente .venv será detectado automaticamente.

Para ativar o ambiente com venv, use:

- **Windows:** `.venv\Scripts\activate`

- **Unix/macOS:** `source .venv/bin/activate`


## 📄 Licença
Este projeto está licenciado sob a licença MIT.