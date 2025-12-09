# Database initialization script for river-access-mvp

CREATE TABLE IF NOT EXISTS rivers (
    river_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    state VARCHAR(20),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_river_name (name, state)
);

CREATE TABLE IF NOT EXISTS river_sections (
    section_id INT PRIMARY KEY AUTO_INCREMENT,
    river_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    difficulty_class VARCHAR(10),
    length_miles DECIMAL(5, 2),
    min_flow_cfs INT,
    max_flow_cfs INT,
    optimal_min_cfs INT,
    optimal_max_cfs INT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (river_id) REFERENCES rivers(river_id) ON DELETE CASCADE,
    INDEX idx_river (river_id)
);

CREATE TABLE IF NOT EXISTS usgs_gauges (
    gauge_id INT PRIMARY KEY AUTO_INCREMENT,
    river_id INT NOT NULL,
    section_id INT,
    site_number VARCHAR(20) UNIQUE NOT NULL,
    gauge_name VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    drainage_area_sqmi DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (river_id) REFERENCES rivers(river_id) ON DELETE CASCADE,
    FOREIGN KEY (section_id) REFERENCES river_sections(section_id) ON DELETE SET NULL,
    INDEX idx_river (river_id),
    INDEX idx_site_number (site_number)
);

CREATE TABLE IF NOT EXISTS current_conditions (
    condition_id INT PRIMARY KEY AUTO_INCREMENT,
    gauge_id INT NOT NULL,
    timestamp DATETIME NOT NULL,
    flow_cfs DECIMAL(10, 2),
    gauge_height_ft DECIMAL(6, 2),
    temperature_f DECIMAL(5, 2),
    data_quality VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (gauge_id) REFERENCES usgs_gauges(gauge_id) ON DELETE CASCADE,
    INDEX idx_gauge_time (gauge_id, timestamp),
    INDEX idx_timestamp (timestamp)
);

CREATE TABLE IF NOT EXISTS arima_predictions (
    prediction_id INT PRIMARY KEY AUTO_INCREMENT,
    gauge_id INT NOT NULL,
    prediction_date DATE NOT NULL,
    predicted_flow_cfs DECIMAL(10, 2),
    confidence_lower DECIMAL(10, 2),
    confidence_upper DECIMAL(10, 2),
    model_version VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (gauge_id) REFERENCES usgs_gauges(gauge_id) ON DELETE CASCADE,
    INDEX idx_gauge_date (gauge_id, prediction_date),
    UNIQUE KEY unique_prediction (gauge_id, prediction_date)
);

CREATE TABLE IF NOT EXISTS access_points (
    access_id INT PRIMARY KEY AUTO_INCREMENT,
    river_id INT NOT NULL,
    section_id INT,
    name VARCHAR(100) NOT NULL,
    type ENUM('put_in', 'takeout', 'both') DEFAULT 'both',
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    parking_type ENUM('roadside', 'small_lot', 'large_lot', 'fee_required') DEFAULT 'small_lot',
    parking_capacity ENUM('limited', 'moderate', 'ample') DEFAULT 'moderate',
    parking_fee DECIMAL(5, 2) DEFAULT 0,
    facilities TEXT,
    access_difficulty ENUM('easy', 'moderate', 'difficult') DEFAULT 'moderate',
    notes TEXT,
    last_verified DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (river_id) REFERENCES rivers(river_id) ON DELETE CASCADE,
    FOREIGN KEY (section_id) REFERENCES river_sections(section_id) ON DELETE SET NULL,
    INDEX idx_river (river_id),
    INDEX idx_section (section_id)
);

CREATE TABLE IF NOT EXISTS weather_conditions (
    weather_id INT PRIMARY KEY AUTO_INCREMENT,
    section_id INT NOT NULL,
    timestamp DATETIME NOT NULL,
    temperature_f DECIMAL(5, 2),
    feels_like_f DECIMAL(5, 2),
    humidity_percent INT,
    wind_speed_mph DECIMAL(5, 2),
    wind_gust_mph DECIMAL(5, 2),
    wind_direction_deg INT,
    wind_direction VARCHAR(3),
    precipitation_in DECIMAL(6, 3),
    precipitation_chance INT,
    visibility_miles DECIMAL(5, 2),
    uv_index INT,
    cloud_cover_percent INT,
    conditions VARCHAR(100),
    weather_code INT,
    data_source VARCHAR(50) DEFAULT 'OpenWeatherMap',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (section_id) REFERENCES river_sections(section_id) ON DELETE CASCADE,
    INDEX idx_section_time (section_id, timestamp),
    INDEX idx_timestamp (timestamp)
);

-- Insert sample data for Little Falls
INSERT INTO rivers (name, state, description) VALUES
('Potomac River', 'MD/VA', 'Major river in the DMV region with excellent kayaking and paddling opportunities');

INSERT INTO river_sections (river_id, name, difficulty_class, length_miles, min_flow_cfs, max_flow_cfs, optimal_min_cfs, optimal_max_cfs, description) VALUES
(1, 'Little Falls', 'II', 1.5, 2000, 15000, 4000, 8000, 'Class II whitewater section at Little Falls with consistent flow and popular put-ins'),
(1, 'Mathers Gorge', 'III', 3.0, 3000, 12000, 5000, 9000, 'Class III technical section through scenic gorge with multiple small drops'),
(1, 'North Branch', 'II+', 2.5, 2500, 14000, 4500, 8500, 'Scenic North Branch section with moderate rapids and beautiful forest'),
(1, 'Shenandoah Staircase', 'III+', 4.0, 2000, 10000, 3500, 7000, 'Technical Class III+ section with series of drops creating a staircase effect');

INSERT INTO usgs_gauges (river_id, section_id, site_number, gauge_name, latitude, longitude, drainage_area_sqmi) VALUES
(1, 1, '01646500', 'Potomac River at Little Falls Lock near Bethesda MD', 39.0067, -77.2481, 9650),
(1, 2, '01646000', 'Potomac River at Mathers Gorge near Seneca MD', 39.0812, -77.3389, 9500),
(1, 3, '01645000', 'Potomac River North Branch near Westernport MD', 39.5234, -79.2876, 4200),
(1, 4, '01631500', 'Shenandoah River at Millville WV', 38.9234, -77.8901, 3000);

INSERT INTO access_points (river_id, section_id, name, type, latitude, longitude, parking_type, parking_capacity, parking_fee, facilities, access_difficulty, notes) VALUES
(1, 1, 'Great Falls Park', 'put_in', 39.0067, -77.2481, 'fee_required', 'ample', 10.00, 'Restrooms, Picnic area, Visitor center', 'easy', 'Popular starting point for Little Falls run'),
(1, 1, 'Violettes Lock', 'both', 39.0156, -77.2347, 'small_lot', 'moderate', 0.00, 'Restrooms available', 'moderate', 'Good access point, can be busy'),
(1, 1, 'Carderock Recreation Area', 'takeout', 38.9750, -77.2033, 'large_lot', 'moderate', 0.00, 'Picnic area', 'moderate', 'Main takeout for Little Falls'),
(1, 2, 'Seneca Creek', 'put_in', 39.0812, -77.3389, 'roadside', 'limited', 0.00, 'Street parking', 'moderate', 'Access to Mathers Gorge section'),
(1, 2, 'Mathers Gorge Take-Out', 'takeout', 39.0756, -77.3201, 'small_lot', 'moderate', 0.00, 'Basic parking', 'difficult', 'Technical takeout requiring portage'),
(1, 3, 'North Branch Put-In', 'put_in', 39.5234, -79.2876, 'large_lot', 'ample', 0.00, 'Picnic tables, Restrooms', 'easy', 'Scenic access point to North Branch'),
(1, 3, 'North Branch Take-Out', 'takeout', 39.4821, -79.1234, 'small_lot', 'moderate', 0.00, 'Limited facilities', 'moderate', 'Takeout after North Branch run'),
(1, 4, 'Shenandoah Staircase Put-In', 'put_in', 38.9234, -77.8901, 'large_lot', 'ample', 5.00, 'Restrooms, Picnic area', 'moderate', 'Gateway to technical Staircase section'),
(1, 4, 'Shenandoah Staircase Take-Out', 'takeout', 38.8945, -77.8456, 'small_lot', 'limited', 0.00, 'No facilities', 'difficult', 'Steep takeout after Staircase run');
