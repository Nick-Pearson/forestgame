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
  user_agent_type VARCHAR(64) NULL,
  user_agent_family VARCHAR(64) NULL,
  user_agent_name VARCHAR(64) NULL,
  PRIMARY KEY(uuid)
);

CREATE TABLE game (
  uuid CHAR(36) NOT NULL,
  host_uuid CHAR(36) NOT NULL,
  invite_code CHAR(4) NOT NULL,
  state CHAR(5) NOT NULL,
  maxPlayers INT NOT NULL,
  mapId INT NOT NULL,
  FOREIGN KEY (host_uuid) REFERENCES client(uuid),
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