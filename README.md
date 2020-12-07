# Pulse RH - Desafio SPE


## Linguagem, Frameworks e Bibliotecas usados(as)
* Python
* SQLite3 [db.sqlite3]
* Django
* Django REST Framework (API)


## Requisitos
* Python

## Configuração
	pip install -r requirements.txt # (instalar bibliotecas Python)
	python manage.py migrate # (criar banco de dados)
	python manage.py createsuperuser # (para criar um super-usuário, pois algumas rotas requerem autenticação)
	python manage.py runserver # (iniciar o servidor local na porta 8000 <http://127.0.0.1:8000>)

## Testes
	python manage.py test # (rodar testes unitários da API)

* Testar rotas da API manualmente
	- Swagger [https://app.swaggerhub.com/apis/sparttacus/ElecPoint/1.0.0]

## Rotas
