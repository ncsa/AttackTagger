PROJECT_NAME=bootstrap

# make c m="first commit"
c:
	git add -A
	git commit -m "$m"
	git push

# docker
docker_build:
	docker build -t $(PROJECT_NAME) .

# TODO: pass env via this command, remove .env file from Docker container
docker_run:
	-docker rm $(PROJECT_NAME)
	@docker run -P \
	--name $(PROJECT_NAME) $(PROJECT_NAME)

docker_shell:
	-docker rm $(PROJECT_NAME)
	@docker run -ti -P \
	--name $(PROJECT_NAME) $(PROJECT_NAME) \
	/bin/bash
