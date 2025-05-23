# プロジェクト設定
IMAGE_NAME=kaitai-yuho-gpu
CONTAINER_NAME=kaitai-yuho-container
HOST_PORT=8888
CONTAINER_PORT=8888
WORKDIR=/app

# Build Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run container with GPU, Jupyter, and volume mount
run:
	docker run --gpus all -p $(HOST_PORT):$(CONTAINER_PORT) \
	-v $(PWD):$(WORKDIR) \
	--name $(CONTAINER_NAME) \
	$(IMAGE_NAME)

# Run in detached mode
run-detached:
	docker run -d --gpus all -p $(HOST_PORT):$(CONTAINER_PORT) \
	-v $(PWD):$(WORKDIR) \
	--name $(CONTAINER_NAME) \
	$(IMAGE_NAME)

# Stop container
stop:
	docker stop $(CONTAINER_NAME)

# Restart container
restart:
	docker start -a $(CONTAINER_NAME)

# Remove container
rm:
	docker rm $(CONTAINER_NAME)

# Remove image
rmi:
	docker rmi $(IMAGE_NAME)

# Show logs
logs:
	docker logs -f $(CONTAINER_NAME)

# Clean up everything
clean: stop rm rmi

# Check Python path inside container
which-python:
	docker exec -it $(CONTAINER_NAME) which python

# Jupyter token URL (optional debug)
url:
	@echo "Access Jupyter at: http://localhost:$(HOST_PORT)/lab"