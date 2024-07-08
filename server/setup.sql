CREATE DATABASE attendance;

USE attendance;

CREATE TABLE roommates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    status VARCHAR(255) NOT NULL,
    monday INT,
    tuesday INT,
    wednesday INT,
    thursday INT,
    friday INT,
    saturday INT,
    sunday INT,
    lastEnter VARCHAR(255),
    lastExit VARCHAR(255),
    avgTimeAway VARCHAR(255),
    avgTimeLeft INT,
    timeStamp VARCHAR(255)
);
