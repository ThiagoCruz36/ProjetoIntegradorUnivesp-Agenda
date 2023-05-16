# Agenda Beauty - BackEnd

Utilização do Python-Flask para construção de um Web Server API Restful

Integração com as extensões Flask-SQLAlchemy, Flask-HTTPAuth

## Python

- PYTHON: [Python](https://www.python.org/downloads/)


## Databases

- PostgreSQL: [PostgreSQL](https://www.postgresql.org/)

## Download do projeto

- Acessar o repósitorio do projeto no GitHub: [Agenda Flask](https://bitbucket.org/seno-ti/)

Clicar em clone, e no terminal do seu sistema operacional, acessar a pasta que deseja salvar o projeto e colar o link gerado no GitHb.

## Instalação

### Criação e ativação do ambiente virtual:

Criação do ambiente virtual:

```
python3.8 -m venv venv  
```

Ativação do ambiente virtual:

```
source venv/bin/activate
```

### Instalação das extensões utlizadas:

Instalação com pip:

```
pip install -r requirements.txt
```

### Ativação Flask via CLI

Inicialização do Projeto Flask:

```
export FLASK_APP=agenda_beauty.py
export FLASK_DEBUG=1
```

Criação da DataBase através dos migrates Flask:

```
flask db upgrade
```

Para rodar o serviço:

```
flask run
```
