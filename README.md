Save My Ass
=========

Simple python script for work with remove servers

Install
-------
requirements:
  - fabric
  - PyYAML
  
  pip install -r requirements.txt

Use
---

Single config file

```python
python savemyass.py -i myserver.yaml -o backup/
```

Directory configs

```python
python savemyass.py -d servers -o backup/
```

Config
------

File in YAML syntax with .yaml extension.

```yaml
host: 127.0.0.1 # remote address
login: root
password: myg00dpassw0rd
port: 22
commands: # commands list
  - run ls  # execute command
  - get /var/log/nginx/errors.log # get file to output directory
```

Full Example
------------

```yaml
host: 123.123.123.123
login: root
password: myg00dpassw0rd
port: 22
commands:
    - run tar cfvz /tmp/backup.tar.gz /var/www/
    - get /tmp/backup.tar.gz
    - run mysqldump -u root --password 'mysqlpassw0rd' --all-databases > /tmp/all-database.sql; echo 'y'
    - run gzip /tmp/all-database.sql
    - get /tmp/all-database.sql.gz
    - run rm /tmp/all-database.sql.gz
    - run rm /tmp/backup.tar.gz
```
