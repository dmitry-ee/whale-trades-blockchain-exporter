### BASE IMAGE ###
FROM      dmi7ry/py-basic-exporter:0.6.0 as base
FROM      base                           as builder

RUN       mkdir /install
WORKDIR   /install

COPY      ${DOCKER_DIR}requirements.txt /requirements.txt
RUN       set -ex ;\
          pip install --no-cache-dir --install-option="--prefix=/install" -r /requirements.txt

### IMAGE ###
FROM      base

COPY      --from=builder /install /usr/local
COPY      src /app
