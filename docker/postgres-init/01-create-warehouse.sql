CREATE DATABASE warehouse;

\connect warehouse
-- Created up front: parallel Cosmos tasks would otherwise race to create it on the first run.
CREATE SCHEMA analytics;
