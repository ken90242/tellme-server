FROM centos
MAINTAINER ken-han ken90242@gmail.com

RUN yum -y update
RUN yum groupinstall -y "Development Tools"
RUN yum install -y gcc make python36 zlib-devel mysql-devel 
RUN yum install -y libffi-devel bzip2-devel openssl-devel python36-devel.x86_64 

WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
CMD ["uwsgi", "--ini", "uwsgi.ini"]

