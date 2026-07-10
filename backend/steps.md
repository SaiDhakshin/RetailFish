cd backend

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

<!-- To run app -->

uvicorn app.main:app --reload

source .venv/bin/activate
pip freeze > requirements.txt
docker compose exec backend sh

## connect to db

docker exec -it retailfish-postgres psql -U postgres -d retailfish
