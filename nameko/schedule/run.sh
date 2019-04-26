#!/bin/sh

echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo " Nairobi Tecch Week schedule service  "
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

echo "Checking if rabbitmq server is up!"

while ! nc -z "${RABBIT_HOST:localhost}" 5672; do sleep 3; done
echo "RabbitMQ server: ✓"

# Run Service
nameko run --config config.yml service --backdoor 3000