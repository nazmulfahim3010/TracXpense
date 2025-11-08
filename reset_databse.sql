DROP TABLE user_pass;
DROP TABLE group_info;
DROP TABLE hasan_add;
DROP TABLE group_member;
DROP TABLE user_info;



------------------ ✅ DROP DONE ----------------------
CREATE TABLE user_info (
    u_id INT AUTO_INCREMENT,
    user_name VARCHAR(15) NOT NULL UNIQUE,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    date_of_birth DATETIME NOT NULL,
    contact VARCHAR(12) NOT NULL,
    email VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY (u_id)
);

CREATE TABLE user_pass (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    user_name VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user_info(u_id)
);

CREATE TABLE group_info(
    id INT AUTO_INCREMENT,
    grp_name VARCHAR(255) NOT NULL UNIQUE,
    created_by INT NOT NULL UNIQUE,
    PRIMARY KEY(id),
    FOREIGN KEY(created_by) REFERENCES user_info(u_id)
);

CREATE TABLE group_member(
    id INT AUTO_INCREMENT PRIMARY KEY,
    grp_id INT NOT NULL,
    member_id INT NOT NULL,
    FOREIGN KEY(grp_id) REFERENCES group_info(id),
    FOREIGN KEY(member_id) REFERENCES user_info(u_id)
);

DROP TABLE IF EXISTS {self.user_name}add;
/*            
CREATE TABLE {self.user_name}_add(
    id INT AUTO_INCREMENT PRIMARY KEY,
    date TIMESTAMP DEFAULT CURRENT_DATE,
    appended DECIMAL(8,2) ,
    total DECIMAL(8,2) ,
    expense DECIMAL(8,2),
    expense_comment TEXT,
    stat ENUM('Add','Expense') NOT NULL 
);
*/
-----------------✅ TABLE CREATION---------------------
