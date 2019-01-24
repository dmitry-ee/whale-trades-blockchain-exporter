.EXPORT_ALL_VARIABLES:
APP_VERSION			= $(shell git describe --abbrev=0 --tags)
APP_NAME				= $(notdir $(shell pwd))
DOCKER_ID_USER	= dmi7ry

.ONESHELL:

all: build

build:
	docker build --squash -t $(DOCKER_ID_USER)/$(APP_NAME):$(APP_VERSION) .

push:
	docker push $(DOCKER_ID_USER)/$(APP_NAME):$(APP_VERSION)

debug:
	docker run -e LOG_LEVEL=DEBUG --rm --name $(APP_NAME) $(DOCKER_ID_USER)/$(APP_NAME):$(APP_VERSION)
info:
	docker run -e LOG_LEVEL=INFO --rm --name $(APP_NAME) $(DOCKER_ID_USER)/$(APP_NAME):$(APP_VERSION)
run:
	docker run --rm --name $(APP_NAME) $(DOCKER_ID_USER)/$(APP_NAME):$(APP_VERSION)

bash:
	docker run -it --rm --name $(APP_NAME) $(DOCKER_ID_USER)/$(APP_NAME):$(APP_VERSION) bash

publish: build
