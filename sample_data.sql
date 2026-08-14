-- 1. USERS TABLE
INSERT INTO users (name, email, password, phone_no, is_admin, created_at) VALUES 
('Rahul Sharma', 'rahul@gmail.com', '$2b$12$scSk6KAkDvVvzrEsY6Rv5.QFhxcTzHvbCdysjdbnGD/1NZXOPz7pi', '9876543210', 0, NOW()),
('Priya Patil', 'priya@gmail.com', '$2b$12$scSk6KAkDvVvzrEsY6Rv5.QFhxcTzHvbCdysjdbnGD/1NZXOPz7pi', '9876543211', 0, NOW()),
('Amit Kulkarni', 'amit@gmail.com', '$2b$12$scSk6KAkDvVvzrEsY6Rv5.QFhxcTzHvbCdysjdbnGD/1NZXOPz7pi', '9876543212', 0, NOW()),
('Sneha Joshi', 'sneha@gmail.com', '$2b$12$scSk6KAkDvVvzrEsY6Rv5.QFhxcTzHvbCdysjdbnGD/1NZXOPz7pi', '9876543213', 0, NOW()),
('Rohan Deshmukh', 'rohan@gmail.com', '$2b$12$scSk6KAkDvVvzrEsY6Rv5.QFhxcTzHvbCdysjdbnGD/1NZXOPz7pi', '9876543214', 0, NOW()),
('Anjali Singh', 'anjali@gmail.com', '$2b$12$scSk6KAkDvVvzrEsY6Rv5.QFhxcTzHvbCdysjdbnGD/1NZXOPz7pi', '9876543215', 0, NOW()),
('Vikram Kumar', 'vikram@gmail.com', '$2b$12$scSk6KAkDvVvzrEsY6Rv5.QFhxcTzHvbCdysjdbnGD/1NZXOPz7pi', '9876543216', 0, NOW()),
('Pooja Patel', 'pooja@gmail.com', '$2b$12$scSk6KAkDvVvzrEsY6Rv5.QFhxcTzHvbCdysjdbnGD/1NZXOPz7pi', '9876543217', 0, NOW()),
('Aditya Verma', 'aditya@gmail.com', '$2b$12$scSk6KAkDvVvzrEsY6Rv5.QFhxcTzHvbCdysjdbnGD/1NZXOPz7pi', '9876543218', 0, NOW()),
('Riya Gupta', 'riya@gmail.com', '$2b$12$scSk6KAkDvVvzrEsY6Rv5.QFhxcTzHvbCdysjdbnGD/1NZXOPz7pi', '9876543219', 0, NOW());

-- 2. SUBJECTS TABLE
INSERT INTO subjects (user_id, subject_name, description, created_at) VALUES 
(1, 'Database Management Systems', 'Core concepts of SQL, Normalization, and Transactions.', NOW()),
(1, 'Java Programming', 'Object-Oriented Programming and advanced Java concepts.', NOW()),
(2, 'Operating Systems', 'Processes, Memory Management, and Concurrency.', NOW()),
(2, 'Computer Networks', 'OSI model, TCP/IP protocols, and network security.', NOW()),
(3, 'Artificial Intelligence', 'Search algorithms, machine learning basics, and neural networks.', NOW()),
(4, 'Python Programming', 'Data structures, APIs, and scripting using Python.', NOW()),
(5, 'Web Development', 'HTML, CSS, JavaScript, and backend frameworks.', NOW()),
(6, 'Software Engineering', 'SDLC, Agile methodologies, and project planning.', NOW()),
(7, 'Machine Learning', 'Supervised vs unsupervised learning models.', NOW()),
(8, 'Data Structures', 'Arrays, Linked Lists, Trees, and Graphs theory.', NOW()),
(9, 'Cloud Computing', 'AWS, Azure, and Google Cloud services overview.', NOW()),
(10, 'Cyber Security', 'Network vulnerabilities, cryptography, and ethical hacking.', NOW());

-- 3. STUDY SESSIONS TABLE
INSERT INTO sessions (user_id, subject_id, start_time, end_time, duration_minutes, status) VALUES 
(1, 1, '2026-03-20 10:00:00', '2026-03-20 12:00:00', 120, 'completed'),
(1, 2, '2026-03-21 14:00:00', '2026-03-21 16:30:00', 150, 'completed'),
(2, 3, '2026-03-22 09:00:00', '2026-03-22 11:00:00', 120, 'completed'),
(2, 4, '2026-03-23 15:00:00', '2026-03-23 18:00:00', 180, 'completed'),
(3, 5, '2026-03-24 10:00:00', '2026-03-24 11:30:00', 90, 'completed'),
(4, 6, '2026-03-25 18:00:00', '2026-03-25 20:00:00', 120, 'completed'),
(5, 7, '2026-03-26 13:00:00', '2026-03-26 16:00:00', 180, 'completed'),
(6, 8, '2026-03-27 08:00:00', '2026-03-27 10:00:00', 120, 'completed'),
(7, 9, '2026-03-27 19:00:00', '2026-03-27 21:00:00', 120, 'completed'),
(8, 10, '2026-03-28 11:00:00', '2026-03-28 13:00:00', 120, 'completed');

-- 4. GOALS TABLE
INSERT INTO goals (user_id, goal_type, target_hours, status, created_at) VALUES 
(1, 'Daily', 4.0, 'pending', NOW()),
(2, 'Weekly', 20.0, 'active', NOW()),
(3, 'Monthly', 80.0, 'completed', NOW()),
(4, 'Daily', 3.5, 'active', NOW()),
(5, 'Weekly', 25.0, 'pending', NOW()),
(6, 'Monthly', 100.0, 'completed', NOW()),
(7, 'Daily', 5.0, 'active', NOW()),
(8, 'Weekly', 15.0, 'pending', NOW()),
(9, 'Daily', 2.0, 'active', NOW()),
(10, 'Weekly', 30.0, 'active', NOW());

-- 5. FRIENDS TABLE
INSERT INTO friends (sender_id, receiver_id, status, created_at) VALUES 
(1, 2, 'accepted', NOW()),
(2, 3, 'accepted', NOW()),
(3, 4, 'pending', NOW()),
(4, 5, 'accepted', NOW()),
(1, 5, 'accepted', NOW()),
(6, 7, 'pending', NOW()),
(7, 8, 'accepted', NOW()),
(8, 9, 'accepted', NOW()),
(9, 10, 'pending', NOW()),
(1, 10, 'accepted', NOW());

-- 6. REMINDERS TABLE
INSERT INTO reminders (user_id, message, time, status, created_at) VALUES 
(1, 'Revise DBMS normal forms', '2026-04-01 10:00:00', 'pending', NOW()),
(2, 'Complete OS assignment', '2026-04-02 18:00:00', 'pending', NOW()),
(3, 'Prepare for AI presentation', '2026-04-03 09:00:00', 'pending', NOW()),
(4, 'Review Python dictionaries', '2026-04-04 20:00:00', 'pending', NOW()),
(5, 'Practice Web Dev CSS grids', '2026-04-05 15:00:00', 'pending', NOW()),
(6, 'Read Software Engg chapter 3', '2026-04-06 14:00:00', 'pending', NOW()),
(7, 'Implement ML linear regression', '2026-04-07 16:00:00', 'pending', NOW()),
(8, 'Solve Data Structures graph problems', '2026-04-08 11:00:00', 'pending', NOW()),
(9, 'Watch Cloud Computing tutorial', '2026-04-09 21:00:00', 'pending', NOW()),
(10, 'Study Cyber Security policies', '2026-04-10 13:00:00', 'pending', NOW());

-- 7. RATINGS TABLE
INSERT INTO ratings (user_id, rating, feedback, created_at) VALUES 
(1, 5, 'Very useful app for tracking study sessions.', NOW()),
(2, 4, 'Great interface and easy to use.', NOW()),
(3, 5, 'The analytics dashboard is amazing!', NOW()),
(4, 4, 'Helped me stay consistent with my goals.', NOW()),
(5, 5, 'Highly recommended for students.', NOW()),
(6, 5, 'Best study tracker out there.', NOW()),
(7, 4, 'Good app but could add more graph features.', NOW()),
(8, 5, 'Love the friend feature, makes studying fun.', NOW()),
(9, 4, 'Reminders always keep me on track.', NOW()),
(10, 5, 'A must-have app for final year projects!', NOW());

-- 8. ADMIN TABLE
INSERT INTO admin (email, password) VALUES 
('admin@study.com', '$2b$12$scSk6KAkDvVvzrEsY6Rv5.QFhxcTzHvbCdysjdbnGD/1NZXOPz7pi');
