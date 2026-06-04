up:
	docker compose up -d --build --force-recreate

down:
	docker compose down

scale:
	docker compose up -d --scale consumer=3

watch:
	watch docker ps -a

logs1:
	docker logs kafka-mvp-consumer-1

test:
	curl -X POST http://localhost:8000/order

test-more:
	@for i in $$(seq 1 100); do \
		curl -s -X POST http://localhost:8000/order > /dev/null; \
	done