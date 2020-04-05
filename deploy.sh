cd db
docker-compose up -d
cd ..
docker-compose build
docker-compose rm
docker-compose up -d
