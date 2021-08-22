CREATE TABLE sensors (
  id SERIAL PRIMARY KEY,
  type VARCHAR(50),
  name VARCHAR(50)
);

CREATE TABLE sensor_data (
  time TIMESTAMPTZ NOT NULL,
  sensor_id INTEGER,
  measurement DOUBLE PRECISION,
  FOREIGN KEY (sensor_id) REFERENCES sensors (id)
);

SELECT create_hypertable('sensor_data', 'time');

INSERT INTO sensors (type, name) VALUES
('electrical', 'current_solarPanel');



