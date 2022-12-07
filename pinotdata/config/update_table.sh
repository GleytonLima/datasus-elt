curl -X POST "http://localhost:9000/schemas" \
-H "accept: application/json" \
-H "Content-Type: application/json" \
-d @schema.json

curl -X POST "http://localhost:9000/tables" \
-H "accept: application/json" \
-H "Content-Type: application/json" \
-d @table.json


curl -X PUT "http://localhost:9000/tables/events" \
-H "accept: application/json" \
-H "Content-Type: application/json" \
-d @table.json


