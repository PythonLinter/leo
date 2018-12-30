
Leo
=====

[![Gitter](https://img.shields.io/gitter/room/Carrene/NuemdCoder.svg)](https://gitter.im/Carrene/NuemdCoder)

![Leo](http://www.ub-cool.com/magazine/wp-content/uploads/2017/05/shutterstock_547175674.jpg)

## Branches

### master

[![Build Status](https://travis-ci.com/Carrene/leo.svg?token=HWnTqWuJD5Ap9uCZHQqx&branch=master)](https://travis-ci.com/Carrene/leo)
[![Coverage Status](https://coveralls.io/repos/github/Carrene/leo/badge.svg?branch=master&t=Cg7Krq)](https://coveralls.io/github/Carrene/leo?branch=master)

### develop

[![Build Status](https://travis-ci.com/Carrene/leo.svg?token=HWnTqWuJD5Ap9uCZHQqx&branch=develop)](https://travis-ci.com/Carrene/leo)
[![Coverage Status](https://coveralls.io/repos/github/Carrene/leo/badge.svg?branch=develop&t=Cg7Krq)](https://coveralls.io/github/Carrene/leo?branch=develop)


Setting up development Environment on Linux
----------------------------------

### Installing Dependencies

    $ sudo apt-get install libass-dev libpq-dev postgresql \
        build-essential redis-server redis-tools

### Setup Python environment

    $ sudo apt-get install python3-pip python3-dev
    $ sudo pip3.6 install virtualenvwrapper
    $ echo "export VIRTUALENVWRAPPER_PYTHON=`which python3.6`" >> ~/.bashrc
    $ echo "alias v.activate=\"source $(which virtualenvwrapper.sh)\"" >> ~/.bashrc
    $ source ~/.bashrc
    $ v.activate
    $ mkvirtualenv --python=$(which python3.6) --no-site-packages leo

#### Activating virtual environment
    
    $ workon leo

#### Upgrade pip, setuptools and wheel to the latest version

    $ pip install -U pip setuptools wheel
  
### Installing Project (edit mode)

So, your changes will affect instantly on the installed version

#### nanohttp

    $ cd /path/to/workspace
    $ git clone git@github.com:pylover/nanohttp.git
    $ cd nanohttp
    $ pip install -e .
    
#### restfulpy
    
    $ cd /path/to/workspace
    $ git clone git@github.com:pylover/restfulpy.git
    $ cd restfulpy
    $ pip install -e .

#### leo
    
    $ cd /path/to/workspace
    $ git clone git@git.carrene.com:web/leo.git
    $ cd leo
    $ pip install -e .
    
#### Enabling the bash autocompletion for leo

    $ echo "eval \"\$(register-python-argcomplete leo)\"" >> $VIRTUAL_ENV/bin/postactivate    
    $ deactivate && workon leo
    
### Setup Database

#### Configuration

Create a file named `~/.config/leo.yml`

```yaml

db:
  url: postgresql://postgres:postgres@localhost/leo_dev
  test_url: postgresql://postgres:postgres@localhost/leo_test
  administrative_url: postgresql://postgres:postgres@localhost/postgres

messaging:
  default_messenger: restfulpy.messaging.SmtpProvider

smtp:
  host: mail.carrene.com
  port: 587
  username: nc@carrene.com
  password: <smtp-password>
  local_hostname: carrene.com
   
```


#### Change postgres password

    $ echo "alter user postgres with password 'postgres'" | sudo -u postgres psql

#### Remove old abd create a new database **TAKE CARE ABOUT USING THAT**

    $ leo admin create-db --drop --mockup
    
And or

    $ leo admin create-db --drop --basedata 

#### Drop old database: **TAKE CARE ABOUT USING THAT**

    $ leo [-c path/to/config.yml] admin drop-db

#### Create database

    $ leo [-c path/to/config.yml] admin create-db

Or, you can add `--drop` to drop the previously created database: **TAKE CARE ABOUT USING THAT**

    $ leo [-c path/to/config.yml] admin create-db --drop
    
#### Create database object

    $ leo [-c path/to/config.yml] admin setup-db

#### Database migration (in leo path)

    $ leo migrate upgrade head

#### Insert Base data

    $ leo [-c path/to/config.yml] admin base-data
    
#### Insert Mockup data

    $ leo [-c path/to/config.yml] admin mockup-data

### Import icd code sets (for year 2018)
Importing icd code sets, consists 2 phases:
1. Normalizing Data: Print normalized icd10, icd9 and icd codes conversions in csv format on stdout.
2. Importing Data: Import icd10, icd9 and icd codes conversions from csv files collected from phase 1.



#### Normalizing Data
Data required for normalizing data:
- Normalizing icd10: 
    - *icd10cm_tabular_2018.xml* file from [here](https://www.cms.gov/Medicare/Coding/ICD10/Downloads/2018-ICD-10-Table-And-Index.zip)
    - *icd10cm_order_2018.txt* file from [here](https://www.cms.gov/Medicare/Coding/ICD10/Downloads/2018-ICD-10-Code-Descriptions.zip)
    - *common_codes* collection in mongodb
- Normalizing icd9:
    - *CMS32_DESC_LONG_DX.txt* file from [here](https://www.cms.gov/Medicare/Coding/ICD9ProviderDiagnosticCodes/Downloads/ICD-9-CM-v32-master-descriptions.zip)
    - *common_codes* collection in mongodb 
- Normalizing icd9 to icd10 conversion:
    - *2018_I9gem.txt* file from [here](https://www.cms.gov/Medicare/Coding/ICD10/Downloads/2018-ICD-10-CM-General-Equivalence-Mappings.zip)
- Normalizing icd10 to icd9 conversion:
    - *2018_I10gem.txt* file from [here](https://www.cms.gov/Medicare/Coding/ICD10/Downloads/2018-ICD-10-CM-General-Equivalence-Mappings.zip)

##### <a name="normalize-icd10">Normalize icd10</a>
    $ leo normalize icd10 -x icd10cm_tabular_2018.xml -t icd10cm_order_2018.txt -d icd-mongodb-name > icd10.csv
##### <a name="normalize-icd9">Normalize icd9</a>
    $ leo normalize icd9 CMS32_DESC_LONG_DX.txt -d icd-mongodb-name > icd9.csv
##### <a name="normalize-icd9-to-icd10">Normalize icd9 to icd10 conversions</a>
    $ leo normalize icd9-to-icd10 2018_I9gem.txt > icd9_to_icd10.csv
##### <a name="normalize-icd10-to-icd9">Normalize icd10 to icd9 conversions</a>
    $ leo normalize icd10-to-icd9 2018_I10gem.txt > icd10_to_icd9.csv
    
#### Importing Data
Data required for importing data:
- Importing icd10: 
    - csv file collected from [normalized icd10](#normalize-icd10)
- Importing icd9:
    - csv file collected from [normalized icd9](#normalize-icd9)
- Importing icd9 to icd10 and icd10 to icd9 conversions:
    - csv files collected from [normalized icd9 to icd10](normalize-icd9-to-10)
    - csv files collected from [normalized icd10 to icd9](normalize-icd10-to-icd9)
    
**Warning:** Run following commands in ordered sequences.

##### Cleaning database
    $ leo admin create-db --drop [--basedata or --schema]
##### Import icd10
    $ leo import icd10 icd10.csv
##### Import icd9
    $ leo import icd9 icd9.csv
##### Import icd code conversions
    $ leo import conversions -9 icd9_to_icd10.csv -10 icd10_to_icd9.csv
    
    
### Unittests

    $ nosetests
    
### Serving

- Using python builtin http server

```bash
$ leo [-c path/to/config.yml] serve
```    

- Gunicorn

```bash
$ ./gunicorn
```
 

Setting up development Environment on Windows (Tested for Windows 10)
----------------------------------

### Setup Python environment
- Install Python on Windows (https://www.python.org/downloads/) and make sure the Scripts subdirectory of Python is in your PATH.
   For example, if python is installed in C:\Python35-32\,
   you should make sure C:\Python35-32\Scripts is in your PATH in addition to C:\Python35-32\.

- Install related Microsoft Visual C++ Build Tools according to your python version mentioned on [WindowsCompilers](https://wiki.python.org/moin/WindowsCompilers)
- Run the following command on a Command Prompt to install Virtual Environment Wrapper for Windows:

```
    > pip install virtualenvwrapper-win
```


- Add WORKON_HOME variable as an Environment Variable and set the value %USERPROFILE%\Envs by default.

- Run the following command to make a Virtual Environment for "leo" :

```
    > mkvirtualenv leo
```

#### Activating virtual environment

    > workon leo

#### Upgrade pip, setuptools and wheel to the latest version

    (leo) > pip install -U pip setuptools wheel

### Installing Project in Virtual Environment(edit mode)

So, your changes will affect instantly on the installed version

#### restfulpy

    (leo) > cd path/to/leo/..
    (leo) > git clone git@github.com:pylover/restfulpy.git
    (leo) > cd restfulpy
    (leo) > pip install -e .

    (leo) > cd path/to/leo/..
    (leo) > git clone git@github.com:pylover/nanohttp.git
    (leo) > cd nanohttp
    (leo) > pip install -e .

    (leo) > cd /path/to/leo
    (leo) > pip install -e .

### Setup PostgreSQL
You can find the windows installer on https://www.postgresql.org/download/windows/

### Setup Database

- Create the leo.yml file in %USERPROFILE%\AppData\Local
- Add the following lines to this file
```
    db:
      url: postgresql://postgres:postgres@localhost/leo_dev
      administrative_url: postgresql://postgres:postgres@localhost/postgres
      test_url: postgresql://postgres:postgres@localhost/leo_test
      echo: true
```

#### create database **TAKE CARE ABOUT USING THAT**

    (leo) /path/to/leo > leo admin create-db --drop --basedata

#### Drop old database: **TAKE CARE ABOUT USING THAT**

    (leo) /path/to/leo > leo -c path/to/leo.yml admin drop-db

#### Create database

    (leo) /path/to/leo > -c path/to/leo.yml admin create-db

Or, you can add `--drop` to drop the previously created database: **TAKE CARE ABOUT USING THAT**

    (leo) /path/to/leo > leo -c path/to/leo.yml admin create-db --drop

#### Create database object

    (leo) /path/to/leo > leo -c path/to/leo.yml admin setup-db

#### Database migration

    (leo) /path/to/leo > leo migrate upgrade head

#### Insert Base data

    (leo) /path/to/leo > leo -c path/to/leo.yml admin base-data

#### Insert Mockup data

    (leo) /path/to/leo > leo -c path/to/leo.yml dev mockup-data

### Unittests
This command will generate the Mark-Down documents which are needed for Front-end developers :

    (leo) /path/to/leo > nosetests

### Serving

- Using nanohttp server

```
    (leo) /path/to/leo > leo serve
```

### Importing from mongodb

Restoring the mongo db:
```bash
service mongodb stop
mongorestore --dbpath /var/lib/mongodb/ dump/
chown -R mongodb:mongodb /var/lib/mongodb
service mongodb start
leo import-mongo --db-name icd2017
```


```bash
leo import-mongo -h
```

```bash
usage: leo import-mongo [-h] [-a {HOST:}PORT] [-d DB_NAME]

optional arguments:
  -h, --help            show this help message and exit
  -a {HOST:}PORT, --address {HOST:}PORT
                        Bind Address. default: localhost:27017
  -d DB_NAME, --db-name DB_NAME
                        MongoDB database name to import from. default is:
                        "icd"

```

### Exporting to SQLite

#### Compile sqlite with `fts5` support. and install.

##### Installing dependencies:

```bash
sudo apt-get install -y build-essential bzip2 libbz2-dev libncursesw5-dev \
    lzma-dev liblz-dev liblzma-dev tk8.5-dev libreadline6 libreadline6-dev \
    libssl-dev libgdbm-dev libc6-dev tk-dev
```

##### Download the sqlite source code from: https://sqlite.org/download.html


```bash
tar -xvf sqlite-autoconf-*.tar.gz
cd sqlite-autoconf-*
make clean
./configure --prefix=/opt/sqlite3-fts5 --disable-static --enable-fts5 \
    CFLAGS="-g -O2 -DSQLITE_ENABLE_FTS3=1 -DSQLITE_ENABLE_FTS4=1 -DSQLITE_ENABLE_RTREE=1"
make
sudo make install
```

##### Link from /usr/local/bin (Optional)

```bash
sudo ln -s /opt/sqlite3-fts5/bin/sqlite3 /usr/local/bin/sqlite
```

##### Download and compile python

```bash
wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tar.xz
tar -xvf Python-3.6.1.tar.xz
cd Python-3.6.1
LD_RUN_PATH=/opt/sqlite3-fts5/lib ./configure --prefix=/opt/python3.6 LDFLAGS="-L/opt/sqlite3-fts5/lib" CPPFLAGS="-I /opt/sqlite3-fts5/include"
LD_RUN_PATH=/opt/sqlite3-fts5/lib make -j $(cat /proc/cpuinfo | grep -P '^processor' | wc -l)   
LD_RUN_PATH=/opt/sqlite3-fts5/lib make test
sudo LD_RUN_PATH=/opt/sqlite3-fts5/lib make install
```

#### Create the virtualenv using the newly built python

```bash
v.activate
rmvirtualenv leo
mkvirtualenv --python=/opt/python3.6/bin/python3.6 leo
cd /path/to/leo
pip install -e .
```

#### Finally you can export the sqlite database with fts5.

```bash
leo export-sqlite -h
```

```bash
usage: leo export-sqlite [-h] [-w] [dbname]

positional arguments:
  dbname           SQLite db filename

optional arguments:
  -h, --help       show this help message and exit
  -w, --overwrite  Overwrite the file if exists.

```

## Change Log

##### 1.0.0-a22

- Code conversion: [#82](/../../issues/82)

##### 1.0.0-a21

- Refactoring the project and use id for handling codes, because there are 
some redundant codes in both Icd9 and Icd10 databases: [#88](/../../issues/88)
- CLI launcher to exporting data as sqlite using FTS5: [#91](/../../issues/91) 
- Filtering codes by speciality: [#85](/../../issues/85)
- CLI launcher to import data from mongoDB: [#81](/../../issues/81) [#77](/../../issues/77)
- Recreating mockup data using semantic data: [#87](/../../issues/87)
- Refactoring the collection system: [#90](/../../issues/90) [#89](/../../issues/89) [#92](/../../issues/92)


##### 1.0.0-a18

- Write launcher for choose one icd type.

##### 1.0.0-a17

- Add launcher to project : read data from Mongodb database and make csv files and insert into postgres database

##### 1.0.0-a16

- BUGFIX: Different Result For Search Codes. [#73](/../../issues/73)

##### 1.0.0-a15

-  Add JSON patch to project  [#72](/../../issues/72)

##### 1.0.0-a13

-  Add Refresh Token [#68](/../../issues/68)
-  Show list of icd codes for each user login  [#70](/../../issues/70)
-  Increase code coverage

##### 1.0.0-a12

-  Change savedcode Api name to collections, [#56](/../../issues/56)
-  Saved Codes Are Not Required Soft Delete , [#64](/../../issues/64)
-  Search (pagination, filtering and sorting on icds), [#69](/../../issues/69)
-  GET icd code API, [#62](/../../issues/62)

##### 1.0.0-a11

-  change saved code models and change mockup data
-  Patch/Delete for savedcodes API [#47](/../../issues/57)

##### 1.0.0-a10


-  Saved code api with title and show icd codes information [#47](/../../issues/47)
-  Saved code Api with title and count [#46](/../../issues/46)
-  Add a new saved code list for a user [#44](/../../issues/44)


##### 1.0.0-a9

- Show savedcode list for authorized user  [#42](/../../issues/42)
- Change Icd tables, remove section and chapter from icd9 [#41](/../../issues/41)

##### 1.0.0-a8

- Bundle Icd10 into savedcodes JSON result [#40](/../../issues/40)

##### 1.0.0-a7

- Modified models on database
- Mockup data for user code table [#13](/../../issues/13)
- Reset password template [#33](/../../issues/33)
- Welcome email template [#34](/../../issues/34)
- CRUD Api for saved codes  [#12](/../../issues/12)

##### 1.0.0-a6

- Disallow login, if user not activate [#28](/../../issues/28)

##### 1.0.0-a5

- Change Password wrong old password  [#24](/../../issues/24)
- Confirmation Email on Signup [#17](/../../issues/17)
- Email Validation Error. [#23](/../../issues/23)
- Password Character Limitation  [#22](/../../issues/22)
- Duplicated Name  [#21](/../../issues/21)

##### 1.0.0-a3

- Name instead of firstName,lastName  [#16](/../../issues/16)

##### 1.0.0-a2

- Speciality omitted authorization  [#15](/../../issues/15)


