docker-compose down
docker-compose up -d
sleep 10
docker-compose run --rm runner nosetests
