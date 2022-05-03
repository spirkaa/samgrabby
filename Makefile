.POSIX:

export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

default: build

IMAGE_FULLNAME=git.devmem.ru/cr/soft
build:
	@docker build \
		--tag ${IMAGE_FULLNAME} \
		-f .docker/django/ci.Dockerfile .

prod:
	@docker-compose up -d --build
	@docker-compose logs -f

prod-down:
	@docker-compose down

local:
	@docker-compose -f docker-compose.local.yml up -d --build
	@docker exec samgrabby_django-local_1 python /app/samgrabby/manage.py migrate
	@docker exec samgrabby_django-local_1 python /app/samgrabby/manage.py runjobs daily
	@docker-compose -f docker-compose.local.yml logs -f

local-down:
	@docker-compose -f docker-compose.local.yml down

cleanup-images:
	@docker rmi -f \
		samgrabby_django-local \
		samgrabby_django \
		samgrabby_nginx
