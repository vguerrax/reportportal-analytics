# reportportal-analytics:latest
FROM python:3

WORKDIR /usr/src

RUN svn checkout --username trc6014724 --password Vg*123321 --no-auth-cache https://svn.unimedbh.com.br/svn/Web/Testes/QAGeral/AmbienteDeTestes/tools/reportportal-analytics/app

WORKDIR /usr/src/app

RUN pip install --proxy http://serv_ggtitestes:cfDJ_2YQfN97zC@proxy2.unimedbh.com.br:8080 --no-cache-dir -r requirements.txt 

EXPOSE 5000

CMD ["python", "app.py", "-p 5000"]
