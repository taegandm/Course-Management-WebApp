SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Enrolled;
DROP TABLE IF EXISTS student;
SET FOREIGN_KEY_CHECKS=1;

-- Create the student table if it doesn't exist
CREATE TABLE IF NOT EXISTS Student (
    sid INT AUTO_INCREMENT PRIMARY KEY,
    sname VARCHAR(255) NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    pnum CHAR(10) UNIQUE NOT NULL,
    dob DATE NOT NULL,
    gpa DECIMAL(3, 2) NOT NULL,
    pword VARCHAR(50) NOT NULL,
    CONSTRAINT GPARange
    CHECK (gpa >= 0 AND gpa <= 4)
);

DELETE from Student;

-- Insert 5 fake student records
INSERT INTO Student (sname, username, email, pnum, dob, gpa, pword) VALUES ('John Doe', 'doej1', 'john@example.com', '9735556677', STR_TO_DATE('16 December 2001', '%d %M %Y'), 3.65, 'password');
INSERT INTO Student (sname, username, email, pnum, dob, gpa, pword) VALUES ('Jane Smith', 'smithj1', 'jane@example.com', '9661114444', STR_TO_DATE('8 July 2003', '%d %M %Y'), 3.2, 'password');
INSERT INTO Student (sname, username, email, pnum, dob, gpa, pword) VALUES ('Alice Johnson', 'johnsona1', 'alice@example.com', '9080006789', STR_TO_DATE('23 February 2002', '%d %M %Y'), 4.0, 'password');
INSERT INTO Student (sname, username, email, pnum, dob, gpa, pword) VALUES ('Bob Brown', 'brownb1', 'bob@example.com', '2170104765', STR_TO_DATE('2 May 1999', '%d %M %Y'), 2.9, 'password');
INSERT INTO Student (sname, username, email, pnum, dob, gpa, pword) VALUES ('Eve Davis', 'davise1', 'eve@example.com', '9012324567', STR_TO_DATE('16 September 2001', '%d %M %Y'), 3.43, 'password');
INSERT INTO Student (sname, username, email, pnum, dob, gpa, pword) VALUES ('David Bri', 'brid1', 'bri@example.com', '9012901567', STR_TO_DATE('15 June 2003', '%d %M %Y'), 3.90, 'password');
INSERT INTO Student (sname, username, email, pnum, dob, gpa, pword) VALUES ('Joe Shmoo', 'shmooj1', 'joe@example.com', '9014444567', STR_TO_DATE('1 July 2003', '%d %M %Y'), 2.90, 'password');
INSERT INTO Student (sname, username, email, pnum, dob, gpa, pword) VALUES ('Xavier Smith', 'smithx1', 'xavier@example.com', '998764567', STR_TO_DATE('20 May 2005', '%d %M %Y'), 3.70, 'password');
INSERT INTO Student (sname, username, email, pnum, dob, gpa, pword) VALUES ('Sam Grey', 'greys1', 'sam@example.com', '9011234567', STR_TO_DATE('3 February 2002', '%d %M %Y'), 3.90, 'password');
INSERT INTO Student (sname, username, email, pnum, dob, gpa, pword) VALUES ('Don Mark', 'markd1', 'don@example.com', '9012328907', STR_TO_DATE('6 August 2000', '%d %M %Y'), 3.90, 'password');


-- Create the course table if it doesn't exist
CREATE TABLE IF NOT EXISTS Course (
    cid INT AUTO_INCREMENT PRIMARY KEY,
    cname VARCHAR(255) NOT NULL,
    description VARCHAR(1024) NOT NULL,
    credits INT NOT NULL,
    capacity INT NOT NULL,
    CONSTRAINT CapacityMax
    CHECK (capacity >= 0 AND capacity <= 25)
);

DELETE from Course;

-- Insert 5 fake student records
INSERT INTO Course (cname, description, credits, capacity) VALUES ('Computer Science Theory', 'Formal languages, theory, automata, Turing Machines. computability, the Church-Turing thesis, decidability, time and space complexity, and NP-completeness.', 3, 20);
INSERT INTO Course (cname, description, credits, capacity) VALUES ('Operating Systems', 'Process Management. Process synchronization and deadlock prevention. Memory Management. Interrupts processing. I/O Control.', 3, 20);
INSERT INTO Course (cname, description, credits, capacity) VALUES ('System Analysis and Design', 'A major project includes forms design, sequential files, files, merge, sort, and editing programs. Equivalent course CMPT 382 effective through Summer 2019.', 3, 25);
INSERT INTO Course (cname, description, credits, capacity) VALUES ('Data Structures', 'Design and analysis of data structures, pointers, linked representations, linear lists, trees, storage systems and structures, database design.', 4, 15);
INSERT INTO Course (cname, description, credits, capacity) VALUES ('Python Programming I', 'Introduction to basic computational concepts; legal and ethical issues in computing and information technology. Main focus- introduction to the Python programming language; syntax and semantics of the Python programming language, basic algorithms and problem-solving skills using Python.', 3, 25);


-- Create the course table if it doesn't exist
CREATE TABLE IF NOT EXISTS Enrolled (
    sid INT NOT NULL,
    cid INT NOT NULL,
    grade CHAR(2),
    PRIMARY KEY(sid, cid),
    FOREIGN KEY (sid) REFERENCES Student(sid) ON DELETE CASCADE,
    FOREIGN KEY (cid) REFERENCES Course(cid) ON DELETE CASCADE
);

DELETE from Enrolled;

-- Insert 5 fake student records
INSERT INTO Enrolled (sid, cid, grade) VALUES (1, 3, 'A-');
INSERT INTO Enrolled (sid, cid, grade) VALUES (2, 1, 'A');
INSERT INTO Enrolled (sid, cid, grade) VALUES (4, 1, 'B');
INSERT INTO Enrolled (sid, cid, grade) VALUES (2, 2, 'C+');
INSERT INTO Enrolled (sid, cid, grade) VALUES (5, 5, 'C');
INSERT INTO Enrolled (sid, cid, grade) VALUES (10, 2, 'B');
INSERT INTO Enrolled (sid, cid, grade) VALUES (9, 1, 'C');
INSERT INTO Enrolled (sid, cid, grade) VALUES (3, 4, 'A-');
INSERT INTO Enrolled (sid, cid, grade) VALUES (8, 3, 'D+');
INSERT INTO Enrolled (sid, cid, grade) VALUES (7, 5, 'B+');






