Save My Ass
=========

Simple python script for work with remove servers

Install
-------
requirements:
  - fabric
  - PyYAML
  - easywebdav
  
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
  - local ls # local execure command
  - set errors.log # upload localfile to webdav
```

WebDav
------

Script support upload backup files to any WebDav.
In yaml confid need set params in "webdav" section.

example
```yaml
webdav:
  host: webdav.your-domain.com
  username: mylogin
  password: 'passw0rd'
```

Full Example
------------

```yaml
host: 123.123.123.123
login: root
password: myg00dpassw0rd
port: 22
webdav:
  host: dav.box.com
  path: '/dav/backup'
  protocol: https
  username: admin@test.com
  password: 'myg00dpassw0rd'
commands:
    - run tar cfvz /tmp/backup.tar.gz /var/www/
    - get /tmp/backup.tar.gz
    - run mysqldump -u root --password=mysqlpassw0rd --all-databases > /tmp/all-database.sql; echo 'y'
    - run gzip /tmp/all-database.sql
    - get /tmp/all-database.sql.gz
    - run rm /tmp/all-database.sql.gz
    - run rm /tmp/backup.tar.gz
    - set backup.tar.gz
```

Changelog
---------
0.2
  - add support upload to webdav
  - fixes `getopt`
  - check file size and delete not changed files
0.1
  - first release
  