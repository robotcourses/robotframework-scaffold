# 🤖 Robot Framework Scaffold

Uma ferramenta de linha de comando (CLI) interativa para criar projetos baseados em Robot Framework de forma rápida, padronizada e com boas práticas desde o início.

## 🔍 Sumário
- [🤖 Robot Framework Scaffold](#-robot-framework-scaffold)
  - [🔍 Sumário](#-sumário)
  - [🚀 O que é?](#-o-que-é)
  - [✅ Funcionalidades](#-funcionalidades)
  - [🛠️ Requisitos](#️-requisitos)
  - [📦 Instalção](#-instalção)
  - [✌️ Utilização](#️-utilização)
  - [📁 Estrutura Gerada](#-estrutura-gerada)
    - [🦾 User Keywords Embaracadas](#-user-keywords-embaracadas)
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
- Instalação automática das bibliotecas essenciais com base no tipo de projeto.
- Criação de ambiente virtual com venv ou Poetry.
- Geração do pyproject.toml com dependências e informações do projeto. (Caso escolha o Poetrt)
- Compatível com as boas práticas de desenvolvimento e organização de testes com Robot Framework.
- Suporte a múltiplas bibliotecas de automação web.
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

[Em Construção]

## 📁 Estrutura Gerada
A estrutura do projeto é criada de forma modular, respeitando o tipo escolhido durante a criação. Veja abaixo exemplos para cada tipo:

- 🔌 Projeto API

```
.
├───resources/
│   ├───common/
│   ├───connections/
│   ├───data/
│   ├───routes/
│   └───utils/
├───tests/
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

### 🦾 User Keywords Embaracadas

[EM CONSTRUÇÃO]


## 💡 Dicas

Se você estiver usando VSCode, o ambiente .venv será detectado automaticamente.

Para ativar o ambiente com venv, use:

- **Windows:** `.venv\Scripts\activate`

- **Unix/macOS:** `source .venv/bin/activate`


## 📄 Licença
Este projeto está licenciado sob a licença MIT.