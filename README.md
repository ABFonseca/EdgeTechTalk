# EdgeTechTalk
Repositório para conteudo da Live Tech Talk Edge sobre Python


# Set-Up machines (postgres and PgAdmin)
You can set up with docker or install directly on the machine.

### With Docker
All the commands below are for a Windows machine. If using Mac or Linux machine adapt the commands

```
docker run --name pg-docker -e POSTGRES_PASSWORD=docker -d -p 5432:5432 postgres 
docker exec -it pg-docker /bin/bash 
    psql -h localhost -U postgres 
        create database api_example; 
        \q 
    exit

if PgAdmin needed: 
docker run -p 80:80 -e "PGADMIN_DEFAULT_EMAIL=user@domain.com" -e "PGADMIN_DEFAULT_PASSWORD=root" -d dpage/pgadmin4 

```

### In Windows Server 2016
Install Grafana: [Instructions here](https://grafana.com/docs/grafana/latest/installation/windows/)

Install Postgres: [Instructions here](https://www.postgresql.org/download/windows/)

Install InfluxDB: [Instructions here](https://portal.influxdata.com/downloads/)


# Executing the code
on the directory of the code (same folder as this README.md file) do:
```
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python api.py
```
