
-- Account Table
CREATE TABLE account (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    user_fullname VARCHAR(255) NOT NULL,
    department VARCHAR(255),
    phone_num VARCHAR(255),
    email VARCHAR(255) NOT NULL
);

-- Project Table
CREATE TABLE project (
    project_id SERIAL PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    project_start_date DATE,
    project_end_date DATE,
    project_team TEXT,
    project_status VARCHAR(255),
    project_owner INT,
    CONSTRAINT fk_project_owner FOREIGN KEY (project_owner) REFERENCES account(id)
);

-- Release Table
CREATE TABLE release (
    release_id SERIAL PRIMARY KEY,
    release_name VARCHAR(255) NOT NULL,
    project_id INT,
    CONSTRAINT fk_release_project FOREIGN KEY (project_id) REFERENCES project(project_id)
);

-- Design Table
CREATE TABLE design (
    design_id SERIAL PRIMARY KEY,
    design_name VARCHAR(255) NOT NULL,
    release_id INT,
    CONSTRAINT fk_design_release FOREIGN KEY (release_id) REFERENCES release(release_id)
);

-- Stage Table
CREATE TABLE stage (
    stage_id SERIAL PRIMARY KEY,
    stage_name VARCHAR(255) NOT NULL,
    design_id INT,
    CONSTRAINT fk_stage_design FOREIGN KEY (design_id) REFERENCES design(design_id)
);

-- Version Table
CREATE TABLE version (
    version_id SERIAL PRIMARY KEY,
    version_name VARCHAR(255) NOT NULL,
    stage_id INT,
    script TEXT,
    CONSTRAINT fk_version_stage FOREIGN KEY (stage_id) REFERENCES stage(stage_id)
);

-- Output Table
CREATE TABLE output (
    output_id SERIAL PRIMARY KEY,
    output_type VARCHAR(255) NOT NULL,
    output_content TEXT,
    version_id INT,
    CONSTRAINT fk_output_version FOREIGN KEY (version_id) REFERENCES version(version_id)
);