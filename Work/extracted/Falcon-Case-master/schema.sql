DROP TABLE if exists json_table;

CREATE TABLE json_table 
(
    json_id serial PRIMARY KEY,
    json_contents json
); 