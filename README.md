TM TEST TASK - WAREHOUSES
================

## Configure dev environment variables:

copy ```.envs/env.example```  to ```.envs/.local```

build:

```
docker compose build
```

apply migrations:

```
docker compose run django python3 manage.py migrate
```

Load warehouse dump data:

```
docker compose run django python3 manage.py loaddata dump.json
```

run:

```
docker compose up
```

## API docs (swagger):

```
http://127.0.0.1:8000/api/docs/
```