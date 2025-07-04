# 🚀 Hackaton - HackTheData

Bem-vindo ao repositório do projeto **HackTheData**!  
Este projeto é uma API backend desenvolvida em **Python** e **Flask**, criada para atuar como um pipeline **ETL (Extract, Transform, Load)** para um dashboard de Business Intelligence em Power BI.

O objetivo é extrair dados de fontes como **Google Sheets**, **SharePoint** e **Screenshots**, processá-los com **Pandas** e disponibilizá-los em endpoints RESTful consumíveis pelo Power BI.

---

## 📌 Badges

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.x-orange.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.x-green.svg)

---

## 🎯 Sobre o Projeto

Este projeto foi desenvolvido durante uma **hackathon de análise de dados**, com foco em consolidar e tratar dados dispersos e brutos.

### 🧪 Etapas do ETL

- **Extract (Extração)**:
  - Google Sheets (Receita, Despesas, PLR)
  - SharePoint (Excel de clientes e parcelas)
  - OCR de Imagens (metas de campanha)

- **Transform (Transformação)**:
  - Conversão de valores monetários
  - Padronização de datas
  - Limpeza de dados nulos e irrelevantes
  - Reestruturação de tabelas

- **Load (Carga)**:
  - Exposição dos dados limpos via API Flask em formato JSON

---

## 📊 Arquitetura

```plaintext
[Fontes de Dados] ---> [API ETL (Flask)] ---> [Power BI]
   Google Sheets         Limpeza (Pandas)        Visualização
   SharePoint            Endpoints RESTful       Dashboards
   OCR (Imagem)
```

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.9+**
- **Flask** + Flask-Cors
- **Pandas**
- **google-api-python-client**, **google-auth-oauthlib**
- **requests**
- **cloudscraper**
- **openpyxl**

---

## ⚙️ Instalação

### 1. Clone o repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DA_PASTA_DO_PROJETO>
```

### 2. Crie um ambiente virtual

No Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

No macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

Instale:

```bash
pip install -r requirements.txt
```

---

## 🔐 Configuração

### Google Sheets

1. Crie um projeto no [Google Cloud Console](https://console.cloud.google.com/).
2. Ative a API do Google Sheets.
3. Crie uma **Conta de Serviço** e baixe a chave JSON.
4. Renomeie o arquivo para `credentials_sheets.json` e coloque na raiz do projeto.
5. Compartilhe a planilha do Google Sheets com o e-mail da conta de serviço.

### OCR (opcional)

1. Crie uma conta em [https://ocr.space/](https://ocr.space/)
2. Pegue sua API Key.
3. No arquivo `app.py`, substitua:

```python
ocr_apikey = 'SUA_CHAVE_API_AQUI'
```

---

## ▶️ Execução

Com o ambiente ativado, rode:

```bash
python app.py
```

A aplicação estará acessível em:  
[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🔗 Endpoints da API

### 1. **/hackaton/get_excel** (GET)  
Extrai e limpa dados de um Excel do SharePoint.

**Resposta:**
```json
{
  "data": "[{\"Coluna1\":\"Valor1\", \"Valor parcela\":150.75, ...}]"
}
```

---

### 2. **/hackaton/get_sheets** (GET)  
Extrai e trata abas 'Receita', 'Despesas' e 'PLR' de uma planilha do Google Sheets.

**Resposta:**
```json
{
  "receita": [...],
  "despesa": [...],
  "plr": [...],
  "metas": [...],
  "metas_historico": [...]
}
```

---

### 3. **/hackaton/read_screenshot** (POST)  
Recebe imagem base64, extrai metas da campanha via OCR.

**Payload:**
```json
{
  "screenshot": "data:image/png;base64,iVBORw0KGgoAAAANS..."
}
```

**Sucesso:**
```json
{
  "success": true,
  "message": "Screenshot saved as temp.png"
}
```

**Erro:**
```json
{
  "success": false,
  "message": "Meta not found in screenshot"
}
```

---

## 📁 Estrutura do Projeto

```plaintext
.
├── app.py                 # Endpoints Flask
├── sheets.py              # Integração com Google Sheets
├── sheets_cleaner.py      # Tratamento dos dados das planilhas
├── sharepoint.py          # Download de arquivo Excel do SharePoint
├── config.py              # Configurações gerais
├── credentials_sheets.json # Credenciais Google (local)
└── requirements.txt       # Dependências do projeto
```

---

## 💡 Contribuição

Sinta-se livre para abrir **issues** ou enviar **pull requests** com melhorias e correções!

---

## 📄 Licença

Este projeto é open-source, desenvolvido apenas para fins educacionais durante a Hackathon.

---