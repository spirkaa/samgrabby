.POSIX:

export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

default: build

IMAGE_FULLNAME=git.devmem.ru/projects/samgrabby
build:
	@docker build \
		--tag ${IMAGE_FULLNAME} \
		-f .docker/django/ci.Dockerfile .

prod:
	@docker compose up -d --build
	@docker compose logs -f

prod-down:
	@docker compose down

local:
	@docker compose -f docker-compose.local.yml up -d --build
	@docker exec samgrabby-django-local-1 python /app/samgrabby/manage.py migrate
	@docker exec samgrabby-django-local-1 python /app/samgrabby/manage.py runjobs daily
	@docker compose -f docker-compose.local.yml logs -f

local-down:
	@docker compose -f docker-compose.local.yml down

migrations:
	@docker exec samgrabby-django-local-1 python /app/samgrabby/manage.py makemigrations

migrate:
	@docker exec samgrabby-django-local-1 python /app/samgrabby/manage.py migrate

admin:
	@docker exec samgrabby-django-local-1 sh -c '\
	DJANGO_SUPERUSER_USERNAME=admin \
	DJANGO_SUPERUSER_PASSWORD=admin \
	DJANGO_SUPERUSER_EMAIL="admin@admin.com" \
	python /app/samgrabby/manage.py createsuperuser --noinput'

shell_plus:
	@docker exec -it samgrabby-django-local-1 python /app/samgrabby/manage.py shell_plus

cleanup-images:
	@docker rmi -f \
		samgrabby-django-local \
		samgrabby-django \
		samgrabby-nginx
