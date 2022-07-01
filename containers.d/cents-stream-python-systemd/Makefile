USER = ssato079
NAME = centos-stream-python-systemd
TAG ?= 8
IMAGE = $(USER)/$(NAME):$(TAG)

all: build

build:
	podman build -t $(IMAGE) .

# seealso: https://hub.docker.com/settings/security (access-token)
push:
	podman login -u $(USER) registry-1.docker.io
	podman push $(IMAGE)
