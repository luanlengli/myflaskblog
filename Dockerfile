FROM python:3.6.7-alpine3.8
RUN apk add --no-cache --virtual=build-dependencies gcc g++ build-base libffi-dev libffi findutils gcc libc-dev libressl-dev make git coreutils && \
    mkdir -p /data && \
    cd /data/ && \
    git clone https://github.com/luanlengli/myflaskblog.git && \
    pip install -r /data/myflaskblog/requirements.txt && \
    pip install gunicorn gevent eventlet && \
    apk del --purge build-dependencies gcc g++ build-base libffi-dev findutils libc-dev libressl-dev make git coreutils 
COPY secret.py /data/myflaskblog/
CMD ["/usr/local/bin/gunicorn", "-b", "0.0.0.0:2001", "--chdir", "/data/myflaskblog/", "-k", "eventlet", "wsgi"]