# Pipeline para extração de dados do datasus

## Pré-requisitos

docker-compose 1.28. Se possuir uma versão anterior no Ubuntu utilize o seguintes comandos caso tenha sido instalado com apt-get

```bash
sudo apt-get remove docker-compose
```

Em seguida instale seguindo as instruções, por exemplo, de <https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04>

## Subindo Airflow

Para subir a instancia do airflow siga as instruções em <https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html>

Mas, basicamente os comandos são:

```bash
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
docker-compose up airflow-init
```

E para iniciar

```bash
docker-compose up
```

ou

```bash
docker-compose --profile flower up
```

Acesse a página da UI do airflow em: localhost:8080, com as credenciais airflow, airflow

## Minio

Exemplo extraído de <https://github.com/startreedata/pinot-recipes/tree/main/recipes/minio-real-time>.

Acesse <http://localhost:9101> com as credenciais padrão minioadmin, minioadmin

```bash
compose -f docker-compose-minio.yml -p datasus-minio updocker-
```

## Apache Pinot

Para subir o container com Apache Pinot, execute o comando:

```bash
docker-compose -f docker-compose-pinot.yml --project-name datasus-pinot up
```

Abra o navegador em <http://localhost:9000>

Mais detalhes em <https://docs.pinot.apache.org/basics/getting-started/running-pinot-in-docker> e <https://dev.startree.ai/docs/pinot/recipes/real-time-offline-job-automatic-scheduling>

Ingestão de Dados

<https://medium.com/apache-pinot-developer-blog/leverage-plugins-to-ingest-parquet-files-from-s3-in-pinot-decb12e4d09d>
<https://docs.pinot.apache.org/basics/data-import/batch-ingestion/spark>
<https://docs.pinot.apache.org/users/tutorials/ingest-parquet-files-from-s3-using-spark>
<https://github.com/apache/pinot/blob/release-0.11.0/pinot-plugins/pinot-file-system/pinot-s3/src/main/java/org/apache/pinot/plugin/filesystem/S3PinotFS.java>
<https://www.youtube.com/watch?v=fXraQygBzxg>

## Apache Spark

```bash
docker-compose -f docker-compose-spark.yml --project-name datasus-spark up
```

## Exemplo de Ingestão de dados do Minio para o Apache Pinot

1. Executar o container do Minio
2. Criar dois buckets: "landing" e "curated"
3. Transformar o arquivo [events-sample.csv](events-sample.csv) em arquivo parquet com o script [testes_local.py](src/testes_local.py). É ncessário instalar as dependências de [requirements.txt](requirements.txt) e renomear o arquivo [src/.env.example](src/.env.example) para .env e atualizar os valores.
4. Criar o container do Apache Pinot
5. Criar o schema de exemplo:

   ```sh
   curl -X POST "http://localhost:9000/schemas" \
   -H "accept: application/json" \
   -H "Content-Type: application/json" \
   -d @pinotdata/config/schema.json
   ```

   ```sh
   curl -X POST "http://localhost:9000/schemas" \
   -H "accept: application/json" \
   -H "Content-Type: application/json" \
   -d @pinotdata/config/schema-cnes.json
   ```

   ```sh
   curl -X POST "http://localhost:9000/schemas" \
   -H "accept: application/json" \
   -H "Content-Type: application/json" \
   -d @pinotdata/config/schema-sia-pa.json
   ```

   ```sh
   curl -X POST "http://localhost:9000/schemas" \
   -H "accept: application/json" \
   -H "Content-Type: application/json" \
   -d @pinotdata/config/schema-cnes-auxiliar.json
   ```

6. Criar a tabela de exemplo:

   ```sh
   curl -X POST "http://localhost:9000/tables" \
   -H "accept: application/json" \
   -H "Content-Type: application/json" \
   -d @pinotdata/config/table.json
   ```

   ```sh
   curl -X POST "http://localhost:9000/tables" \
   -H "accept: application/json" \
   -H "Content-Type: application/json" \
   -d @pinotdata/config/table-cnes.json
   ```

   ```sh
   curl -X POST "http://localhost:9000/tables" \
   -H "accept: application/json" \
   -H "Content-Type: application/json" \
   -d @pinotdata/config/table-sia-pa.json
   ```
   
   ```sh
   curl -X POST "http://localhost:9000/tables" \
   -H "accept: application/json" \
   -H "Content-Type: application/json" \
   -d @pinotdata/config/table-cnes-auxiliar.json
   ```

   5.1. Se necessário atualizar a tabela:

   ```sh
   curl -X PUT "http://localhost:9000/tables/cnes_st" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d @pinotdata/config/table-cnes.json
   ```

7. Acompanhar em <http://localhost:9000> que o arquivo é populado no Apache Pinot

### Tabelas de Dimensão

Tabelas de Dimensão oferecem suporte a join para enriquecer dados. O arquivo [table-cnes-auxiliar-exemplo.json](pinotdata/config/table-cnes-auxiliar-exemplo.json) 
demonstra um exemplo. A [documentação](https://docs.pinot.apache.org/basics/data-import/batch-ingestion/dim-table) tem mais detalhes.

```sql
select sia_pa.*, lookup('cnes_st_auxiliar','FANTASIA','CNES', PA_CODUNI) as name from sia_pa limit 10
```

Um exemplo de dados para compor uma tabela de dados auxiliares pode ser visto no [projeto microdatasus](https://github.com/rfsaldanha/microdatasus/blob/32d2fd96f63a9d74a6294b2a5a9a387567b9ce04/data-raw/cadger.R).

## Apache Superset

Tutorial para instalar drivers <https://superset.apache.org/docs/databases/docker-add-drivers>

```sh
# From the repo root...
touch ./docker/requirements-local.txt
```

```sh
echo "pinotdb" >> ./docker/requirements-local.txt
```

Adicionando pinot:

<https://superset.apache.org/docs/databases/pinot>

Exemplo:
<pinot+http://host.docker.internal:8099/query?controller=http://host.docker.internal:9000/>

https://datasus.saude.gov.br/transferencia-de-arquivos/#
