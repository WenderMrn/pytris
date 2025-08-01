# Pytris

#### Video Demo: https://youtu.be/JVsDOCG1Kq0

#### Description

A simple python game that runs on the console

#### Main Dependencies

- python 3.13.5
- pysqlite 2.8.3
- blessed 1.21.0

#### Create ENV

```bash
python -m venv env
```

#### Active ENV

```bash
source env/bin/activate
```

#### Deactivate

```bash
deactivate
```

#### Create requiments.txt

pip freeze > requirements.txt

#### Run on watch mode

watchfiles 'python main.py' .

#### Keep console size

Keep the console at a minimum of 100x30

#### Sqlite schema

```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    score INTEGER NOT NULL
)

```

#### Screenshots

<img src="./assets/images/examples/1.png" alt="menu" width="550" height="400">
<img src="./assets/images/examples/2.png" alt="new game" width="550" height="400">
<img src="./assets/images/examples/3.png" alt="game play" width="550" height="400">
<img src="./assets/images/examples/5.png" alt="game play 2" width="550" height="400">
<img src="./assets/images/examples/6.png" alt="game over" width="550" height="400">
<img src="./assets/images/examples/4.png" alt="scores" width="550" height="400">
