
CREATE TABLE world (
  uuid CHAR(36) NOT NULL,
  map_id VARCHAR(8) NULL,
  size_x INT NOT NULL,
  size_y INT NOT NULL,
  PRIMARY KEY (uuid)
);

CREATE TABLE world_tile (
  id SERIAL,
  world_uuid  CHAR(36) NOT NULL,
  x INT NOT NULL,
  y INT NOT NULL,
  tile_id INT NOT NULL,
  FOREIGN KEY (world_uuid) REFERENCES world(uuid),
  PRIMARY KEY (id)
);
CREATE INDEX world_tile_x_idx ON world_tile (x);
CREATE INDEX world_tile_y_idx ON world_tile (y);

CREATE TABLE world_building (
  id SERIAL,
  world_uuid  CHAR(36) NOT NULL,
  x INT NOT NULL,
  y INT NOT NULL,
  building_id INT NOT NULL,
  owner_id VARCHAR(8) NULL,
  FOREIGN KEY (world_uuid) REFERENCES world(uuid),
  PRIMARY KEY (id)
);

ALTER TABLE game ADD COLUMN create_datetime BIGINT NOT NULL;
ALTER TABLE game ADD COLUMN is_lobby BOOLEAN NOT NULL;
ALTER TABLE game ADD COLUMN is_archived BOOLEAN NOT NULL;
ALTER TABLE game ADD COLUMN max_players INT NOT NULL;
ALTER TABLE game ADD COLUMN world_uuid CHAR(36) NOT NULL;
ALTER TABLE game DROP COLUMN maxplayers;
ALTER TABLE game DROP COLUMN mapid;
ALTER TABLE game DROP COLUMN state;
ALTER TABLE game ADD FOREIGN KEY (world_uuid) REFERENCES world(uuid);

