# 🖥️ BuildItUp

Aplicação web para **montar setups de PC** escolhendo peças e validando a compatibilidade entre elas automaticamente.

## ✨ Funcionalidades

- Cadastro e login de usuários
- Catálogo de peças (CPU, placa-mãe, GPU, RAM, SSD, HD, fonte, cooler, gabinete e ventoinhas) com ordenação por preço
- Montagem, edição e exclusão de setups
- **Validação de compatibilidade:**
  - socket do processador × socket da placa-mãe
  - potência da fonte × TDP total do setup (com sugestão de fontes compatíveis)
- Cálculo automático do preço total e do consumo (TDP)

## 🛠️ Tecnologias

Python · Django 5 · PostgreSQL · HTML/CSS

## 🚀 Como rodar

```bash
git clone https://github.com/NagueAbiviolo/BuildItUp.git
cd BuildItUp
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env          # preencha com seus dados
set -a; source .env; set +a   # carrega as variáveis de ambiente

createdb builditup
psql builditup < builditup.sql   # opcional: carrega peças de exemplo
python manage.py migrate
python manage.py runserver
```

Acesse http://127.0.0.1:8000/
