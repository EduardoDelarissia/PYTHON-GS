FIAP —  Computational Thinking With Python 
Aluno: Eduardo Antonio Delarissia — RM 563468
Link do video :https://youtube.com/watch?v=I57zzv8Skfs

Futuro do Trabalho — Console App (Python)

Aplicativo de linha de comando que apoia requalificação (reskilling/upskilling) e aprendizagem contínua.
Permite cadastrar pessoas, mapear habilidades, planejar estudos, registrar sessões e gerar relatórios por habilidade.
Persistência exclusiva em JSON e consumo de APIs públicas (dica motivacional e manchetes de tecnologia) com fallback offline.



🧭 Sumário

Funcionalidades

Arquitetura & Conformidade

Estrutura do Projeto

Requisitos

Instalação

Execução

Como Usar (passo a passo)

APIs Públicas

Solução de Problemas

Documentação (PDF)

Roteiro do Vídeo

Roadmap

Licença

🚀 Funcionalidades

Cadastro de usuários

Habilidades (nome + nível 0–100)

Plano de estudo (habilidade, recurso, horas)

Registro de sessões (data/hora automática, minutos, notas)

Relatório por usuário com somatório de minutos por habilidade

APIs públicas

Dica motivacional (ZenQuotes; fallback AdviceSlip)

Manchetes tech (Hacker News; fallback Algolia)

Robusto a falta de internet (o app não quebra; apenas não exibe dados da API naquele momento)

🧱 Arquitetura & Conformidade

Sem POO / Sem classes → somente funções, listas e dicionários

Persistência exclusiva em JSON (dados_futuro_trabalho.json)

Sem API própria e sem banco relacional

Sem bibliotecas avançadas (nada de pandas, numpy, etc.)

Sem list/dict comprehensions → loops explícitos while/for

Boas práticas: validações, try/except, if/elif/else, match/case, docstrings, type hints

APIs consumidas com requests; se ausente, fallback via urllib (stdlib)

🗂️ Estrutura do Projeto
.
├─ futuro_trabalho.py           # aplicação principal (console)
├─ dados_futuro_trabalho.json   # criado na primeira gravação (ex.: cadastrar usuário)
└─ README.md


Exemplo do JSON:

{
  "usuarios": [
    {
      "nome": "Ana",
      "habilidades": [{"nome": "Python", "nivel": 60}],
      "plano": [{"habilidade": "Python", "recurso": "Curso X", "horas": 20}],
      "sessoes": [
        {"data": "2025-11-12 10:20", "habilidade": "Python", "minutos": 45, "notas": "Listas e dicionários"}
      ]
    }
  ]
}

🧰 Requisitos

Python 3.10+

Internet para as opções de APIs (o app funciona sem internet; apenas não exibe resultados das APIs)

Opcional: requests (há fallback via urllib)

🛠️ Instalação
Via terminal
# (opcional) criar ambiente virtual
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# (opcional) instalar requests
python -m pip install --upgrade pip
python -m pip install requests

Via PyCharm

File › Settings › Project › Python Interpreter → selecione um venv.

(Opcional) + Add Package → instale requests.

Em Run › Edit Configurations…, confirme o Working directory (pasta do projeto).

▶️ Execução
python futuro_trabalho.py


O arquivo dados_futuro_trabalho.json é criado automaticamente na primeira operação que salva dados (ex.: Cadastrar usuário).

🧪 Como Usar (passo a passo)

[1] Cadastrar usuário

[2] Adicionar/Atualizar habilidade (ex.: “Python”, nível 60)

[3] Planejar estudo (habilidade, recurso, horas)

[4] Registrar sessão (minutos + notas)

[5] Relatório do usuário → mostra habilidades, plano e tempo total (min) por habilidade

[6] Dica motivacional (API) / [7] Manchetes tech (API)

🌐 APIs Públicas

ZenQuotes → frase motivacional

AdviceSlip → fallback de dica

Hacker News (Firebase) → IDs/títulos

Algolia HN → fallback de manchetes

Em redes com proxy/firewall, algumas chamadas podem falhar; o app segue estável.

🧯 Solução de Problemas

ModuleNotFoundError: No module named 'requests'

python -m pip install requests


(ou use o PyCharm + Add Package no mesmo interpretador do projeto)

Sem internet / Proxy corporativo

Configure proxy no PyCharm: Settings › HTTP Proxy

Ou use HTTP_PROXY/HTTPS_PROXY

JSON não aparece

Verifique o Working directory

Faça uma operação que salva (ex.: cadastrar usuário)
