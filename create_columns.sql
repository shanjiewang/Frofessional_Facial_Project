# 建立資料庫
CREATE DATABASE faceTest;

# 新增使用者，設定密碼
create user 'faceTest'@'localhost' identified by 'P@ssw0rd';

show databases;

Use faceTest;

create TABLE faceTest.faceTest (
    Name VARCHAR(255) NULL,
    Sex VARCHAR(255) NULL,
    Country VARCHAR(255) NULL,
    Label VARCHAR(255) NULL,
    Eye_R_B_W VARCHAR(255) NULL,
    Eye_L_B_W VARCHAR(255) NULL,
    Eye_R_H4_L VARCHAR(255) NULL,
    Eye_L_H4_L VARCHAR(255) NULL,
    Eye_dis_B_W VARCHAR(255) NULL,
    Eyebrow_dis_W VARCHAR(255) NULL,
    Nose_H_L VARCHAR(255) NULL,
    Nose_W_M_W VARCHAR(255) NULL,
    philtrum_length_L VARCHAR(255) NULL,
    Lip_beads_L VARCHAR(255) NULL,
    Lip_width_W VARCHAR(255) NULL,
    Lip_height_L VARCHAR(255) NULL,
    face_up_L VARCHAR(255) NULL,
    face_middle_L VARCHAR(255) NULL,
    face_down_L VARCHAR(255) NULL,
    nose_area VARCHAR(255) NULL,
    eye_R_area VARCHAR(255) NULL,
    eye_L_area VARCHAR(255) NULL,
    Nosehead_W  VARCHAR(255) NULL,
    Forehead_w_W VARCHAR(255) NULL
);

alter table testdb.FaceFeatures add Lip_beads_W VARCHAR(255);
select * from faceTest.faceTest;

set sql_mode='';

LOAD DATA INFILE 'C:/Users/USER/git-repos/python3-junior-nogithub/Frofessional_Facial_Project/Csvs/all_clear_rate_db.csv'
INTO TABLE faceTest.faceTest FIELDS TERMINATED BY ',' IGNORE 1 ROWS ;

select * from faceTest.faceTest;