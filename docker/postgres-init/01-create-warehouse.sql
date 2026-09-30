CREATE DATABASE warehouse;

\connect warehouse
-- Created up front: DAGs that start at the same time (e.g. the three bronze loads at 09:00)
-- would otherwise race to create the same schema.
CREATE SCHEMA bronze;
CREATE SCHEMA silver;
CREATE SCHEMA gold;
