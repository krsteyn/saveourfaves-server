#cd db
#docker-compose up -d
#cd ..
docker-compose build
docker-compose stop
docker-compose rm -f
docker-compose up -d
