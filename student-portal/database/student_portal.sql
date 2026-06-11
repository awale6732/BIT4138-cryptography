CREATE DATABASE IF NOT EXISTS student_portal;
USE student_portal;

CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    admission_number VARCHAR(50) UNIQUE NOT NULL,
    course_class VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    lecturer_name VARCHAR(100),
    semester VARCHAR(50),
    academic_year VARCHAR(20),
    project_title VARCHAR(255),
    technologies VARCHAR(255),
    portfolio_link VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO students (name, admission_number, course_class, email, password, lecturer_name, semester, academic_year, project_title, technologies)
VALUES ('Michael Student', 'BIT/2024/001', 'BIT 3.2', 'student@example.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Dr. John Kamau', 'Semester 2', '2024/2025', 'Smart E-Commerce Web Application', 'PHP + MySQL');

CREATE TABLE logbook_entries (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    week_number INT NOT NULL,
    week_title VARCHAR(255),
    reflection TEXT,
    status ENUM('draft', 'submitted', 'reviewed') DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

CREATE TABLE logbook_screenshots (
    id INT PRIMARY KEY AUTO_INCREMENT,
    entry_id INT NOT NULL,
    figure_number VARCHAR(20),
    caption TEXT,
    image_path VARCHAR(255),
    FOREIGN KEY (entry_id) REFERENCES logbook_entries(id) ON DELETE CASCADE
);

CREATE TABLE courses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    unit_code VARCHAR(20) UNIQUE NOT NULL,
    unit_name VARCHAR(255) NOT NULL,
    lecturer VARCHAR(100),
    description TEXT
);

INSERT INTO courses (unit_code, unit_name, lecturer, description) VALUES
('BIT3208', 'Advanced Web Design and Development', 'Dr. John Kamau', 'Covers frontend and backend web development including PHP, MySQL, JavaScript, and modern frameworks.'),
('BIT3101', 'Database Systems', 'Prof. Jane Wanjiku', 'Relational database design, SQL, normalization, and database administration.'),
('BIT3201', 'Software Engineering', 'Mr. Peter Ochieng', 'Software development lifecycle, UML modeling, and project management methodologies.');

CREATE TABLE assessments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    assessment_name VARCHAR(100),
    marks DECIMAL(5,2),
    total_marks DECIMAL(5,2) DEFAULT 15.00,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);
