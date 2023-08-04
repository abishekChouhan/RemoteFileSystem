CREATE TABLE folder (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    parent_folder_id INTEGER REFERENCES folder(id) ON DELETE CASCADE,
    CONSTRAINT folder_unique UNIQUE (name, parent_folder_id)
);

CREATE TABLE file (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    link VARCHAR(500),
    size BIGINT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    folder_id INTEGER REFERENCES folder(id) ON DELETE CASCADE,
    -- hash this will store hash of full file path. Would help in searching
    CONSTRAINT file_unique UNIQUE (name, folder_id)
);
