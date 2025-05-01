docker exec -it postgres psql -U admin -d postgres -c "DROP DATABASE hsa_connect;"
docker exec -it postgres psql -U admin -d postgres -c "CREATE DATABASE hsa_connect;"
docker exec -i postgres psql -U admin -d hsa_connect < schema.sql
docker cp data.sql postgres:/data.sql
docker exec -i postgres psql -U admin -d hsa_connect -f data.sql