# Install

1. python3 -m venv .venv 
2. source .venv/bin/activate
3. pip install -r ./requirements.txt
4. copy .env.example .env
5. docker-compose up -d
6. python .\manage.py makemigrations
7. python .\manage.py migrate