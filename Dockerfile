from python:3.6

ENV LANG C.UTF-8

ADD ./templates /server/templates
ADD ./configuration.py /server/configuration.py
ADD ./main.py /server/main.py

# TODO: move to requirements.txt
RUN pip install redis
RUN pip install flask==1.0.2
RUN pip install werkzeug==0.14.1  # fixes weird bug with flask not starting

EXPOSE 5000

WORKDIR /server

# ENV FLASK_APP=main.py
# CMD ["flask", "run"]

CMD ["python", "main.py"]
