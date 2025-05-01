docker exec -it postgres_container psql -U admin -d postgres -c "DROP DATABASE hsa_connect;"
docker exec -it postgres_container psql -U admin -d postgres -c "CREATE DATABASE hsa_connect;"
docker exec -i postgres_container psql -U admin -d hsa_connect < schema.sql
docker cp data.sql postgres_container:/data.sql
docker exec -i postgres_container psql -U admin -d hsa_connect -f data.sql