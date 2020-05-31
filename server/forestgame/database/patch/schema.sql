CREATE TABLE db_patch (
  id SERIAL,
  apply_datetime BIGINT NOT NULL,
  patch_id INT NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE client (
  uuid VARCHAR(36),
  create_datetime BIGINT NOT NULL,
  last_datetime BIGINT NOT NULL,
  user_agent VARCHAR(255) NULL,
  user_os_name VARCHAR(64) NULL,
  user_os_version VARCHAR(64) NULL,
  user_browser_name VARCHAR(64) NULL,
  user_browser_version VARCHAR(64) NULL,
  bot BOOLEAN NULL,
  PRIMARY KEY(uuid)
);

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

CREATE TABLE game (
  uuid CHAR(36) NOT NULL,
  create_datetime BIGINT NOT NULL,
  host_uuid CHAR(36) NOT NULL,
  invite_code CHAR(4) NOT NULL,
  is_lobby BOOLEAN NOT NULL,
  is_archived BOOLEAN NOT NULL,
  max_players INT NOT NULL,
  world_uuid INT NOT NULL,
  FOREIGN KEY (host_uuid) REFERENCES client(uuid),
  FOREIGN KEY (world_uuid) REFERENCES world(uuid),
  PRIMARY KEY (uuid)
);

CREATE TABLE game_player (
  id SERIAL,
  game_uuid CHAR(36) NOT NULL,
  client_uuid CHAR(36) NOT NULL,
  player_idx INT NOT NULL,
  name VARCHAR(32) NOT NULL,
  colour_r SMALLINT NOT NULL,
  colour_g SMALLINT NOT NULL,
  colour_b SMALLINT NOT NULL,
  population INT NOT NULL,
  wood INT NOT NULL,
  coin INT NOT NULL,
  food INT NOT NULL,
  FOREIGN KEY (game_uuid) REFERENCES game(uuid),
  FOREIGN KEY (client_uuid) REFERENCES client(uuid),
  PRIMARY KEY (id)
);