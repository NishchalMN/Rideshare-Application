FROM python 
ADD . /assign2
WORKDIR ./assign2
RUN apt update
RUN pip install -r requirements.txt
RUN apt install -y libpq-dev python-dev
RUN apt install -y default-libmysqlclient-dev
RUN apt install -y default-mysql-server
CMD ["python","users.py"]
ENV TEAM_NAME = CC_0055_1511_1523_1551
