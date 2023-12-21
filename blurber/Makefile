
DOCKER_BUILD_FILES_PATH=image/
DOCKER_IMAGE=seervision/scipy-notebook
CONTAINER_NAME=sv-jupyter

# Customizeable via, e.g., `WORKSPACE_PATH=custom_path make launch`
DEFAULT_WORKSPACE_PATH=$$(pwd)
USED_WORKSPACE_PATH=$${WORKSPACE_PATH:-${DEFAULT_WORKSPACE_PATH}}

# Customizeable via, e.g., `DOCKER_TAG=custom_tag make launch`
DEFAULT_DOCKER_TAG=latest
USED_DOCKER_TAG=$${DOCKER_TAG:-${DEFAULT_DOCKER_TAG}}

launch:
	docker run --rm -it \
	-p 8888:8888 \
	--mount type=bind,source=${USED_WORKSPACE_PATH},target=/home/jovyan/work \
	--name ${CONTAINER_NAME} \
	${DOCKER_IMAGE}:${USED_DOCKER_TAG}

debug:
	docker run --rm -it \
	-p 8888:8888 \
	--mount type=bind,source=${USED_WORKSPACE_PATH},target=/home/jovyan/work \
	--name ${CONTAINER_NAME} \
	${DOCKER_IMAGE}:${USED_DOCKER_TAG} \
	bash

## Build an image
# Customizable via `DOCKER_TAG=custom_tag make build`, where
#   DOCKER_TAG is a docker tag, i.e., the built image will be tagged as seervision/scipy-notebook:custom_tag
build:
	DOCKER_BUILDKIT=1 docker build --rm --force-rm --tag ${DOCKER_IMAGE}:${USED_DOCKER_TAG} ${DOCKER_BUILD_FILES_PATH}

check_git_unstaged:
	@if [ "$(shell git status --porcelain=v1 2>/dev/null | wc -l)" -ne 0 ]; then \
		echo >&2 "Make sure you do not have any unstaged (or untracked) changes)"; \
		false; \
	fi

## Build and push an image
# Customizable via `DOCKER_TAG=custom_tag make build_and_push`, where
#   DOCKER_TAG is a docker tag, i.e., the built and pushed image will be seervision/scipy-notebook:custom_tag
#
# In addition, an image tagged with the git commit hash will be pushed, i.e., seervision/scipy-notebook:git_commit_hash
build_and_push: build check_git_unstaged
	GIT_COMMIT_REF="$(shell git rev-parse --verify HEAD)"; docker tag ${DOCKER_IMAGE}:${USED_DOCKER_TAG} ${DOCKER_IMAGE}:$${GIT_COMMIT_REF}; docker push ${DOCKER_IMAGE}:$${GIT_COMMIT_REF}
	docker push ${DOCKER_IMAGE}:${USED_DOCKER_TAG}
