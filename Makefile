COMPOSE_FILE = docker-compose.yml

up:
	@echo "Starting Docker containers..."
	docker-compose -f $(COMPOSE_FILE) up -d

down:
	@echo "Stopping Docker containers..."
	docker-compose -f $(COMPOSE_FILE) down

test:
	@echo "Running tests..."
	pytest --disable-warnings

logs:
	@echo "Displaying logs..."
	docker-compose -f $(COMPOSE_FILE) logs -f

restart:
	@echo "Rebuilding and restarting containers..."
	docker-compose -f $(COMPOSE_FILE) down
	docker-compose -f $(COMPOSE_FILE) up --build -d

clean:
	@echo "Cleaning up dangling images and containers..."
	docker system prune -f
