-- Turn off foreign key constraints
SET session_replication_role = 'replica';

INSERT INTO "accounts" ("username","password","email","type") VALUES
	 ('student1','$2b$12$mJh72DNGJkxZHFKo2E0lCulJWQxxKgxyheegj5vJOrjsTsUoCe/cO','student1@exeter.ac.uk','student'),
	 ('student2','$2b$12$ICN.8TnWkE6Oo8GWfSHrweCjwvdFG2GukKIZTHYvK1lKWWe7v3DYe','student2@exeter.ac.uk','student'),
	 ('student3','$2b$12$qmkt/RPzuDD.J5G7cJvxQ.BsDiqWNNWPhXbSV44k0y5.HQi3nIuGq','student3@exeter.ac.uk','student'),
	 ('student4','$2b$12$Kw5d7e6vEzWpHsdYdAmNt.Dn7p3JbSYIXVukRM701hHCdu03k7vpm','student4@exeter.ac.uk','student'),
	 ('staffuser','$2b$12$cre2K9.CQ86mry4QYaqVCeVqfBgx4ZJY9K5lMg2fG53wl4ZX3ZfSu','staffuser@exeter.ac.uk','pending_staff'),
	 ('adminuser','$2b$12$Hi7kioO8dJxAJUBuudMlR.7CbajZX04HtJTv1xHc7woycBhDPVIfG','admin@exeter.ac.uk','admin'),
	 ('staffusertwo','$2b$12$97kyovttvyRDq3.gM8bSwuJgkg8PTcxcrlbJ566iQtoGvn1QD7ogy','staff2@exeter.ac.uk','staff'),
	 ('student5','$2b$12$.tIFU3dKsnf/uFgA.kClCeNZkBdLTF3QhilHt6b4YRKkUYvUcLtZy','student5@exeter.ac.uk','student'),
	 ('student6','$2b$12$z9RUKYHw9wzS9D8tLkWbfu6CqkRDkJnDa/39R5z/OsAHSbBae7gie','s6@exeter.ac.uk','student'),
	 ('student7','$2b$12$sQDKSr86cPDsd0ujmo7rCOh0oN2lmaBO6wnF8QveyhxyufSJdWYFa','s7@exeter.ac.uk','student');
INSERT INTO "accounts" ("username","password","email","type") VALUES
	 ('student8','$2b$12$eG3PxDKe4tbtFN5svIohh.HvMO127cgPHkrGnfrLlMFfjfTM0vuk.','s8@exeter.ac.uk','student'),
	 ('student1000','$2b$12$MjZ9GeTHG8azB5u2fQGCHerum3ZLLY79xR2rcbTMuJPBrEGWurTB2','student10@ox.ac.uk','student'),
	 ('student1001','$2b$12$wCPM0aov4lFDHxKsoZdIm.bNQtjFeqevOC.cTa4FdHlyGijwV7nMm','ic324@ox.ac.uk','student'),
	 ('student1002','$2b$12$2cu6/7Rer//FUbMMZ1Jy4e.uT2H8UaSMqfM5pQzZX4/K6VLTnOBY2','student1002@exeter.ac.uk','student');
INSERT INTO "achievements" ("achievement_id","achievement_name","description","xp_value","icon","rarity") VALUES
	 (1,'Look at you','Visit your profile page for the first time',25,'address card','bronze'),
	 (2,'Looking good','Visit someone else''s profile for the first time',25,'eye','bronze'),
	 (3,'Show it off','Open the achievements tab for the first time',25,'trophy','bronze'),
	 (4,'Connected','Add your first connection',50,'address book','silver'),
	 (5,'Popular','Add 10 connections',75,'address book','gold'),
	 (6,'Centre of attention','Add 100 connections',150,'address book','platinum'),
	 (7,'Express yourself','Post to your social feed for the first time',50,'file alternate','silver'),
	 (8,'5 posts','Post to your social feed 5 times',75,'file alternate','gold'),
	 (9,'20 posts','Post to your social feed 20 times',150,'file alternate','platinum'),
	 (10,'Commentary','Make your first comment on a post',50,'comment','silver');
INSERT INTO "achievements" ("achievement_id","achievement_name","description","xp_value","icon","rarity") VALUES
	 (11,'Describe yourself','Describe yourself by writing a bio',25,'tags','bronze'),
	 (12,'Friends','Add your first close connection',50,'users','silver'),
	 (13,'Friend group','Add 10 close connections',75,'users','gold'),
	 (14,'Reaching out','Connect with 1 person outside of your subject',50,'handshake','silver'),
	 (15,'Outside your bubble','Connect with 10 people outside of your subject',75,'handshake','gold'),
	 (16,'Shared intrests','Connect with someone who has a mutual intrest',50,'bowling ball','silver'),
	 (17,'Getting social','Send a connection request',25,'user plus','bronze'),
	 (18,'Show yourself','Add a profile picture',25,'user circle','bronze'),
	 (19,'Liking that','Like a post for the first time',25,'thumbs up','bronze'),
	 (20,'First like','Receive a like on a post',50,'heart','silver');
INSERT INTO "achievements" ("achievement_id","achievement_name","description","xp_value","icon","rarity") VALUES
	 (21,'Hot topic','Have a post reach 10 comments',100,'comments','gold'),
	 (22,'Everyone loves you','Have a post reach 50 likes',100,'heart','gold'),
	 (23,'Secret meeting','Login during a special event',300,'user secret','diamond'),
	 (24,'Show the love','Like 50 posts',75,'thumbs up','gold'),
	 (25,'Loving everything','Like 500 posts',150,'thumbs up','platinum'),
	 (26,'Shared hobbies','Connect with someone who has a mutual hobby',50,'paint brush','silver'),
	 (27,'Boffin','Complete a quiz',25,'question','bronze'),
	 (28,'Brainiac','Complete a quiz with a perfect score',75,'question','gold'),
	 (29,'Secret Agent','Find a serious bug on this website and report it',1000,'desktop','black'),
	 (30,'Trivia writer','Have someone play one of your quizzes for the first time',50,'question','silver');
INSERT INTO "achievements" ("achievement_id","achievement_name","description","xp_value","icon","rarity") VALUES
	 (31,'Learning','Play a flashcard set for the first time',25,'clone','bronze'),
	 (32,'Teacher','Have someone play one of your flashcard sets for the first time',50,'clone','silver'),
	 (33,'Professor','Have a flashcard set you made reach 50 plays',100,'clone','gold');
INSERT INTO "all_user_likes" ("username","post_id") VALUES
	 ('student1',1),
	 ('staffuser',1),
	 ('student2',5),
	 ('student1',6),
	 ('student3',6),
	 ('student2',8),
	 ('student1',5),
	 ('student1',11);
INSERT INTO "close_friend" ("user1","user2") VALUES
	 ('student1','student2'),
	 ('student4','student1');
INSERT INTO "comments" ("comment_id","username","body","date","post_id") VALUES
	 (4,'staffuser','So cool!','2021-03-11 11:21:05',1),
	 (5,'staffuser','When should I go?','2021-03-11 11:21:24',1),
	 (6,'student1','I recommend you go near Christmas for the Christmas market','2021-03-11 11:22:16',1),
	 (8,'student2','wow','2021-05-21 02:16:42',8),
	 (10,'student2','dude stop spamming okay?','2021-05-21 02:19:22',8),
	 (11,'student2','wtf did you just say','2021-05-21 02:21:03',1),
	 (12,'student1','bro','2021-05-27 09:53:31',11);
INSERT INTO "complete_achievements" ("username","achievement_id","date_completed") VALUES
	 ('student1',1,'2021-03-11'),
	 ('student1',3,'2021-03-11'),
	 ('student2',1,'2021-03-11'),
	 ('student3',1,'2021-03-11'),
	 ('student4',1,'2021-03-11'),
	 ('staffuser',1,'2021-03-11'),
	 ('adminuser',1,'2021-03-11'),
	 ('staffusertwo',1,'2021-03-11'),
	 ('student1',7,'2021-03-11'),
	 ('student2',2,'2021-03-11');
INSERT INTO "complete_achievements" ("username","achievement_id","date_completed") VALUES
	 ('student2',17,'2021-03-11'),
	 ('student1',4,'2021-03-11'),
	 ('student2',4,'2021-03-11'),
	 ('student1',14,'2021-03-11'),
	 ('student2',14,'2021-03-11'),
	 ('student1',2,'2021-03-11'),
	 ('student1',17,'2021-03-11'),
	 ('student4',2,'2021-03-11'),
	 ('student4',17,'2021-03-11'),
	 ('staffusertwo',4,'2021-03-11');
INSERT INTO "complete_achievements" ("username","achievement_id","date_completed") VALUES
	 ('student4',4,'2021-03-11'),
	 ('student4',14,'2021-03-11'),
	 ('staffuser',2,'2021-03-11'),
	 ('staffuser',17,'2021-03-11'),
	 ('student1',20,'2021-03-11'),
	 ('student1',19,'2021-03-11'),
	 ('student1',10,'2021-03-11'),
	 ('student1',27,'2021-03-11'),
	 ('student1',28,'2021-03-11'),
	 ('staffuser',19,'2021-03-11');
INSERT INTO "complete_achievements" ("username","achievement_id","date_completed") VALUES
	 ('staffuser',10,'2021-03-11'),
	 ('staffuser',4,'2021-03-11'),
	 ('staffuser',14,'2021-03-11'),
	 ('staffusertwo',2,'2021-03-11'),
	 ('staffusertwo',17,'2021-03-11'),
	 ('student1',12,'2021-03-11'),
	 ('student4',12,'2021-03-11'),
	 ('student4',7,'2021-03-11'),
	 ('adminuser',2,'2021-03-11'),
	 ('student1',23,'2021-03-18');
INSERT INTO "complete_achievements" ("username","achievement_id","date_completed") VALUES
	 ('student2',3,'2021-04-27'),
	 ('student2',19,'2021-04-27'),
	 ('student4',20,'2021-04-27'),
	 ('student3',2,'2021-04-27'),
	 ('student3',17,'2021-04-27'),
	 ('student3',4,'2021-04-27'),
	 ('student3',19,'2021-04-27'),
	 ('student3',3,'2021-04-27'),
	 ('student3',27,'2021-04-27'),
	 ('student5',1,'2021-05-05');
INSERT INTO "complete_achievements" ("username","achievement_id","date_completed") VALUES
	 ('student5',3,'2021-05-05'),
	 ('student5',2,'2021-05-05'),
	 ('student5',17,'2021-05-05'),
	 ('student1',8,'2021-05-21'),
	 ('student1',9,'2021-05-21'),
	 ('student2',10,'2021-05-21'),
	 ('student2',7,'2021-05-21'),
	 ('student1',29,'2021-05-21'),
	 ('student1',11,'2021-05-24'),
	 ('student1',18,'2021-05-24');
INSERT INTO "complete_achievements" ("username","achievement_id","date_completed") VALUES
	 ('student6',1,'2021-05-27'),
	 ('student6',23,'2021-05-27'),
	 ('student7',1,'2021-05-27'),
	 ('student7',23,'2021-05-27'),
	 ('student6',2,'2021-05-27'),
	 ('student2',23,'2021-05-27'),
	 ('student2',27,'2021-05-27'),
	 ('student8',1,'2021-05-29'),
	 ('student8',3,'2021-05-29'),
	 ('student2',31,'2021-05-29');
INSERT INTO "complete_achievements" ("username","achievement_id","date_completed") VALUES
	 ('student1',32,'2021-05-29'),
	 ('student1',31,'2021-05-30'),
	 ('student5',31,'2021-05-30'),
	 ('student2',32,'2021-05-30'),
	 ('student1000',1,'2021-08-06'),
	 ('student1001',1,'2021-08-06'),
	 ('student1002',1,'2021-08-06'),
	 ('staffuser',7,'2025-04-20'),
	 ('staffuser',3,'2025-04-20'),
	 ('staffuser',27,'2025-04-20');
INSERT INTO "connection" ("user1","user2","connection_type") VALUES
	 ('student2','student1','connected'),
	 ('student1','student3','request'),
	 ('student4','student1','connected'),
	 ('student4','staffusertwo','connected'),
	 ('staffuser','student1','connected'),
	 ('staffusertwo','student1','request'),
	 ('student3','student4','connected'),
	 ('student5','staffuser','request');
INSERT INTO "degree" ("degree_id","degree") VALUES
	 (1,'Not specified '),
	 (2,'Accounting and Business BSc'),
	 (3,'Accounting and Finance BSc'),
	 (4,'Ancient History BA'),
	 (5,'Ancient History and Archaeology BA'),
	 (6,'Animal Behaviour BSc'),
	 (7,'Animal Behaviour MSci'),
	 (8,'Anthropology BA'),
	 (9,'Applied Finance (Degree Apprenticeship) BSc'),
	 (10,'Applied Psychology (Clinical) MSci');
INSERT INTO "degree" ("degree_id","degree") VALUES
	 (11,'Arab and Islamic Studies MArabic'),
	 (12,'Arabic and Politics BA'),
	 (14,'Archaeological Science BSc'),
	 (15,'Archaeology BA'),
	 (16,'Archaeology and Anthropology BA'),
	 (18,'Archaeology with Forensic Science BSc'),
	 (19,'Art History & Visual Culture BA'),
	 (20,'Art History & Visual Culture and Classical Studies BA'),
	 (21,'Art History & Visual Culture and Drama BA'),
	 (22,'Art History & Visual Culture and English BA');
INSERT INTO "degree" ("degree_id","degree") VALUES
	 (23,'Art History & Visual Culture and Film & Television Studies BA'),
	 (24,'Art History & Visual Culture and History BA'),
	 (25,'Bachelor of Business and Laws BBL (Cornwall)'),
	 (26,'Biochemistry BSc'),
	 (27,'Biochemistry MSci'),
	 (28,'Biological Sciences BSc'),
	 (29,'Biological Sciences MSci'),
	 (30,'Biological and Medicinal Chemistry BSc'),
	 (31,'Biological and Medicinal Chemistry MSci'),
	 (32,'Business Analytics BSc');
INSERT INTO "degree" ("degree_id","degree") VALUES
	 (33,'Business BSc (Cornwall)'),
	 (34,'Business Economics BSc'),
	 (35,'Business and Environment BSc (Cornwall)'),
	 (36,'Business and Management BSc'),
	 (37,'Civil Engineering BEng'),
	 (38,'Civil Engineering BEng degree apprenticeship'),
	 (39,'Civil Engineering MEng'),
	 (40,'Classical Studies BA'),
	 (41,'Classical Studies and English BA'),
	 (42,'Classical Studies and Modern Languages BA');
INSERT INTO "degree" ("degree_id","degree") VALUES
	 (43,'Classical Studies and Philosophy BA'),
	 (44,'Classical Studies and Theology BA'),
	 (45,'Classics BA'),
	 (46,'Communications BA'),
	 (47,'Communications and Modern Languages BA'),
	 (48,'Computer Science BSc'),
	 (49,'Data Science BSc'),
	 (50,'Data Science MSci'),
	 (51,'Diagnostic Radiography and Imaging (Degree Apprenticeship) BSc (Hons)'),
	 (52,'Digital and Technology Solutions degree apprenticeship');
INSERT INTO "degree" ("degree_id","degree") VALUES
	 (53,'Drama BA'),
	 (54,'Drama and Film & Television Studies BA'),
	 (55,'Dual LLB/JD with the Chinese University of Hong Kong'),
	 (56,'Economics BSc'),
	 (57,'Economics and Finance BSc'),
	 (58,'Economics and Politics BSc'),
	 (59,'Economics with Econometrics BSc'),
	 (60,'Electronic Engineering BEng'),
	 (61,'Engineering Geology and Geotechnics BSc'),
	 (62,'Engineering Geology and Geotechnics MSci');
INSERT INTO "degree" ("degree_id","degree") VALUES
	 (63,'Engineering MEng'),
	 (64,'Engineering and Entrepreneurship BEng'),
	 (65,'Engineering and Entrepreneurship MEng'),
	 (66,'Engineering and Management BEng'),
	 (67,'Engineering and Management MEng'),
	 (68,'English BA'),
	 (69,'English Law and French Law LLB'),
	 (70,'English and Communications BA'),
	 (71,'English and Creative Writing BA'),
	 (72,'English and Drama BA');
INSERT INTO "degree" ("degree_id","degree") VALUES
	 (73,'English and Film & Television Studies BA'),
	 (74,'English and Modern Languages BA'),
	 (75,'English with Study in North America BA'),
	 (76,'Environmental Geoscience BSc'),
	 (77,'Environmental Geoscience MSci'),
	 (78,'Environmental Science BSc'),
	 (79,'Film & Television Studies BA'),
	 (80,'Film & Television Studies and Communications BA'),
	 (81,'Film & Television Studies and Modern Languages BA'),
	 (82,'Flexible Combined Honours BA/BSc (Cornwall)');
INSERT INTO "degree" ("degree_id","degree") VALUES
	 (83,'Flexible Combined Honours BA/BSc (Exeter)'),
	 (84,'Foundation'),
	 (85,'Geography BA'),
	 (86,'Geography BA/BSc'),
	 (87,'Geography BSc'),
	 (88,'Geography and Geology BSc'),
	 (89,'Geography with Applied GIS BSc'),
	 (90,'Geography with Applied Geographical Information Systems (GIS) BSc'),
	 (91,'Geology BSc'),
	 (92,'Geology MSci');
INSERT INTO "degree" ("degree_id","degree") VALUES
	 (93,'Global Politics BA (Cornwall)'),
	 (94,'Graduate Law LLB'),
	 (95,'History BA (Cornwall)'),
	 (96,'History BA (Exeter)'),
	 (97,'History and Ancient History BA'),
	 (98,'History and Archaeology BA'),
	 (99,'History and International Relations BA (Cornwall)'),
	 (100,'History and Modern Languages BA'),
	 (101,'History and Politics BA (Cornwall)'),
	 (102,'Human Biosciences BSc');
INSERT INTO "degree" ("degree_id","degree") VALUES
	 (103,'Human Sciences BSc'),
	 (104,'International Business and Modern Languages BA'),
	 (105,'International Relations BA'),
	 (106,'International Relations and Modern Languages BA'),
	 (107,'International Year One'),
	 (108,'Law LLB'),
	 (109,'Law with Business LLB (Cornwall)'),
	 (110,'Law with European Study LLB'),
	 (111,'Liberal Arts BA'),
	 (112,'Marine Biology BSc');
INSERT INTO "degree" ("degree_id","degree") VALUES
	 (113,'Marine Biology MSci'),
	 (114,'Marine Science BSc'),
	 (115,'Marketing and Management BSc'),
	 (116,'Mathematics (Climate Science) MSci'),
	 (117,'Mathematics (Geophysical and Astrophysical Fluid Dynamics) MSci'),
	 (118,'Mathematics (Mathematical Biology) MSci'),
	 (119,'Mathematics BSc'),
	 (120,'Mathematics MMath'),
	 (121,'Mathematics and Data Science BSc'),
	 (122,'Mathematics and Data Science MSci');
INSERT INTO "degree" ("degree_id","degree") VALUES
	 (123,'Mathematics and Physics BSc'),
	 (124,'Mathematics with Accounting BSc'),
	 (125,'Mathematics with Accounting MSci'),
	 (126,'Mathematics with Economics BSc'),
	 (127,'Mathematics with Economics MSci'),
	 (128,'Mathematics with Finance BSc'),
	 (129,'Mathematics with Finance MSci'),
	 (130,'Mathematics with Management BSc'),
	 (131,'Mathematics with Management MSci'),
	 (132,'Mechanical Engineering BEng');
INSERT INTO "degree" ("degree_id","degree") VALUES
	 (133,'Mechanical Engineering MEng'),
	 (134,'Medical Imaging (Diagnostic Radiography) BSc'),
	 (135,'Medical Sciences (Human Genomics) MSci'),
	 (136,'Medical Sciences BSc'),
	 (137,'Medicine BMBS'),
	 (138,'Middle East Studies BA'),
	 (139,'Mining Engineering BEng'),
	 (140,'Mining Engineering MEng'),
	 (141,'Modern Languages BA'),
	 (142,'Modern Languages and Arabic BA');
INSERT INTO "degree" ("degree_id","degree") VALUES
	 (143,'Modern Languages and Latin BA'),
	 (144,'Natural Sciences BSc'),
	 (145,'Natural Sciences MSci'),
	 (146,'Neuroscience BSc'),
	 (147,'Nursing MSci'),
	 (148,'Nutrition BSc'),
	 (149,'Philosophy BA'),
	 (150,'Philosophy and History BA'),
	 (151,'Philosophy and Modern Languages BA'),
	 (152,'Philosophy and Politics BA');
INSERT INTO "degree" ("degree_id","degree") VALUES
	 (153,'Philosophy and Sociology BA'),
	 (154,'Philosophy and Theology BA'),
	 (155,'Physics BSc'),
	 (156,'Physics MPhys'),
	 (157,'Physics with Astrophysics BSc'),
	 (158,'Physics with Astrophysics MPhys'),
	 (159,'Politics BA'),
	 (160,'Politics Philosophy and Economics BA'),
	 (161,'Politics and Geography BA'),
	 (162,'Politics and Geography BA (Cornwall)');
INSERT INTO "degree" ("degree_id","degree") VALUES
	 (163,'Politics and International Relations BA (Cornwall)'),
	 (164,'Politics and International Relations BSc'),
	 (165,'Politics and Management BA (Cornwall)'),
	 (166,'Politics and Modern Languages BA'),
	 (167,'Politics and Sociology BA'),
	 (168,'Psychology BSc'),
	 (169,'Psychology with Sport and Exercise Science BSc'),
	 (170,'Renewable Energy BSc'),
	 (171,'Renewable Energy Engineering BEng'),
	 (172,'Renewable Energy Engineering MEng');
INSERT INTO "degree" ("degree_id","degree") VALUES
	 (173,'Resource and Exploration Geology BSc'),
	 (174,'Resource and Exploration Geology MSci'),
	 (175,'Sociology BA'),
	 (176,'Sociology BSc'),
	 (177,'Sociology and Anthropology BA'),
	 (178,'Sociology and Criminology BA'),
	 (179,'Sociology and Modern Languages BA'),
	 (180,'Sport and Exercise Medical Sciences BSc'),
	 (181,'Theology and Religion BA'),
	 (182,'Zoology BSc');
INSERT INTO "degree" ("degree_id","degree") VALUES
	 (183,'Zoology MSci');
INSERT INTO "inventory_backgrounds" ("id","url") VALUES
	 (5,'field');
INSERT INTO "inventory_items" ("id","name","description","rarity","type") VALUES
	 (1,'Comic Sans','All beloved Comic Sans font!',4,'font_pack'),
	 (2,'Open Sans','The best font there is.',4,'font_pack'),
	 (3,'Lato','A popular font.',4,'font_pack'),
	 (4,'Times New Roman','One of the most recognizable fonts in the world.',4,'font_pack'),
	 (5,'Field','Who doesn''t like fields?',1,'profile_background');
INSERT INTO "notification" ("username","body","date","url") VALUES
	 ('student2','You have been tagged by student1 in a post!','2021-05-21 03:20:50','/post_page/1'),
	 ('student1','student2 has commented on your post!','2021-05-21 03:21:03','/post_page/1'),
	 ('student1','You have been tagged by student2 in a post!','2021-05-21 03:21:17','/post_page/2'),
	 ('student2','You have received an achievement badge!','2021-05-21 03:21:18','/achievements'),
	 ('student2','You have been tagged by student1 in a post!','2021-05-21 03:56:23','/post_page/3'),
	 ('student2','You have been tagged by student1 in a post!','2021-05-21 04:00:23','/post_page/4'),
	 ('student1','You have received an achievement badge!','2021-05-24 21:53:01','/achievements'),
	 ('student1','You have received an achievement badge!','2021-05-24 21:53:01','/achievements'),
	 ('student2','You have been tagged by student1 in a post!','2021-05-24 23:56:08','/post_page/5'),
	 ('student6','You have received an achievement badge!','2021-05-27 01:44:37','/achievements');
INSERT INTO "notification" ("username","body","date","url") VALUES
	 ('student6','You have received an achievement badge!','2021-05-27 01:44:38','/achievements'),
	 ('student6','You have received an achievement badge!','2021-05-27 01:44:53','/achievements'),
	 ('student7','You have received an achievement badge!','2021-05-27 01:46:17','/achievements'),
	 ('student7','You have received an achievement badge!','2021-05-27 01:46:17','/achievements'),
	 ('student7','You have received an achievement badge!','2021-05-27 01:46:33','/achievements'),
	 ('student6','You have received an achievement badge!','2021-05-27 01:46:56','/achievements'),
	 ('student2','You have received an achievement badge!','2021-05-27 10:45:14','/achievements'),
	 ('student2','You have received an achievement badge!','2021-05-27 10:47:08','/achievements'),
	 ('student8','You have received an achievement badge!','2021-05-29 00:29:09','/achievements'),
	 ('student8','You have received an achievement badge!','2021-05-29 00:29:14','/achievements');
INSERT INTO "notification" ("username","body","date","url") VALUES
	 ('student1','You have received an achievement badge!','2021-05-29 00:58:38','/achievements'),
	 ('student1','You have received an achievement badge!','2021-05-29 00:58:38','/achievements'),
	 ('student2','You have received an achievement badge!','2021-05-29 00:59:18','/achievements'),
	 ('student2','You have received an achievement badge!','2021-05-29 00:59:18','/achievements'),
	 ('student2','You have received an achievement badge!','2021-05-29 01:00:38','/achievements'),
	 ('student2','You have received an achievement badge!','2021-05-29 01:00:38','/achievements'),
	 ('student1','You have received an achievement badge!','2021-05-30 18:14:20','/achievements'),
	 ('student5','You have received an achievement badge!','2021-05-30 18:15:10','/achievements'),
	 ('student5','You have received an achievement badge!','2021-05-30 18:15:10','/achievements'),
	 ('student5','You have received an achievement badge!','2021-05-30 18:19:55','/achievements');
INSERT INTO "notification" ("username","body","date","url") VALUES
	 ('student5','You have received an achievement badge!','2021-05-30 18:21:00','/achievements'),
	 ('student2','You have been tagged by student1 in a post!','2021-05-31 00:24:29','/post_page/12'),
	 ('student1000','You have received an achievement badge!','2021-08-06 23:22:57','/achievements'),
	 ('student1001','You have received an achievement badge!','2021-08-06 23:29:52','/achievements'),
	 ('student1002','You have received an achievement badge!','2021-08-06 23:31:45','/achievements'),
	 ('staffuser','You have received an achievement badge!','2025-04-20 20:09:56','/achievements'),
	 ('staffuser','You have received an achievement badge!','2025-04-20 20:10:19','/achievements'),
	 ('staffuser','You have received an achievement badge!','2025-04-20 20:10:54','/achievements');
INSERT INTO "post_content" ("post_id","content_url") VALUES
	 (5,'6c994a3b-c67f-45f5-8729-72ff53f1c819'),
	 (5,'6ef9495b-25dc-4804-ba35-9634056ec64a'),
	 (5,'15825820-ef68-4c0c-bb9e-6661c4f482f5'),
	 (5,'6adf052d-050c-4a2a-a6b3-c0507cf21133'),
	 (5,'11fdb98a-fb9b-4e58-914a-0b04ea33eb0a'),
	 (5,'db10fe8b-ef32-4cbe-af7a-c7e9a305e40b'),
	 (5,'99c0b2e8-668b-4b66-aef1-73eb3fd3a5f0');
INSERT INTO "posts" ("post_id","body","likes","username","date","privacy") VALUES
	 (1,'@student2 you''re so dumb dude, stop it.',1,'student1','2021-05-21','public'),
	 (2,'why @student1 is dumb',0,'student2','2021-05-21','public'),
	 (3,'@student2',0,'student1','2021-05-21','public'),
	 (4,'@student2 is really cool, check him out please!',0,'student1','2021-05-21','public'),
	 (5,'# Hello

Heading level 1
===============

**Hello**

> Dorothy followed her through many of the beautiful rooms in her castle.

> #### The quarterly results look great!
>
> - Revenue was off the chart.
> - Profits were higher than ever.
>
>  *Everything* is going according to **plan**.


- First item
- Second item
- Third item
    - Indented item
    - Indented item
- Fourth item

![Tux, the Linux mascot](/assets/images/tux.png)

``Use `code` in your Markdown file.``

My favorite search engine is [Duck Duck Go](https://duckduckgo.com).

@student2

I love supporting the **[EFF](https://eff.org)**.
This is the *[Markdown Guide](https://www.markdownguide.org)*.
See the section on [`code`](#code).

https://www.youtube.com/watch?v=BDeDqJ8GQMY',0,'student1','2021-05-24','public'),
	 (6,'https://www.youtube.com/watch?v=BDeDqJ8GQMY',1,'student1','2021-05-24','public'),
	 (7,'hey',0,'student1','2021-05-24','public'),
	 (8,'hey',0,'student1','2021-05-24','public'),
	 (9,'hey',0,'student1','2021-05-24','public'),
	 (10,'hey',0,'student1','2021-05-24','public');
INSERT INTO "posts" ("post_id","body","likes","username","date","privacy") VALUES
	 (11,'hey',1,'student1','2021-05-24','public'),
	 (12,'@student2 meet me outside if we got beef',0,'student1','2021-05-30','public'),
	 (13,'SHITTT',0,'staffuser','2025-04-20','public');
INSERT INTO "private_messages" ("sender","receiver","message","date") VALUES
	 ('student1','student2','hello','2021-05-20 17:14:46'),
	 ('student1','student2','hey','2021-05-20 17:14:47');
INSERT INTO "question" ("question_id","quiz_id","question","answer_1","answer_2","answer_3","answer_4") VALUES
	 (11,12,'In what movie did Jack freeze to death while Rose floated safely nearby?','Titanic','Jack and the Beanstalk','Gladiator','The Wizard of Oz'),
	 (12,12,'What is the name of male bees, whose only function is to breed?','Drones','Queens','Buzzers','Kings'),
	 (13,12,'What common food product do vampires dislike?','Garlic','Steak','Baked Beans','Anchovies'),
	 (14,13,'What political party did Tony Blair lead?','Labour','Conservative','Democrat','Liberal Democrat'),
	 (15,13,'Who made Pinocchio?','Geppetto','Seven Smith','Jesus','Jiminy Cricket'),
	 (16,14,'What is my favourite colour','Blue','Green','Red','Pink'),
	 (17,14,'What did I have for breakfast','Bacon','Cereal','Toast','Fruit'),
	 (61,25,'What is this','22','333','xxx','444'),
	 (62,26,'sssss','22','xxxx','22222','xxxxx');
INSERT INTO "question_sets" ("set_id","set_name","date_created","author","questions","answers","cards_played") VALUES
	 (1,'test','2021-05-24','student2','q1|q2|q3|question 3|question 4|question 5|question 6','a1|a2|a3|answer 3|answer 4|answer 5|answer 6',25),
	 (8,'Unnamed','2021-05-25','student1','question1','answer1',1),
	 (11,'Unnamed','2021-05-26','student2','Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus nisi sapien, sagittis ut placerat nec, lacinia nec enim. Praesent facilisis tellus eget nibh sodales scelerisque. Fusce gravida aliquet tortor, sit amet sodales nulla blandit at. Nunc varius dignissim pretium. Donec blandit rhoncus urna eu dictum. Aliquam ac orci id mi pulvinar pellentesque eget in dui. Integer ac ante pharetra, sodales est nec, vulputate ante. Sed tristique tincidunt nibh at blandit. Maecenas tincidunt justo eu.','Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus nisi sapien, sagittis ut placerat nec, lacinia nec enim. Praesent facilisis tellus eget nibh sodales scelerisque. Fusce gravida aliquet tortor, sit amet sodales nulla blandit at. Nunc varius dignissim pretium. Donec blandit rhoncus urna eu dictum. Aliquam ac orci id mi pulvinar pellentesque eget in dui. Integer ac ante pharetra, sodales est nec, vulputate ante. Sed tristique tincidunt nibh at blandit. Maecenas tincidunt justo eu.',2),
	 (14,'prolog terms','2021-05-29','student1','Facts|yes|question 4|question 5','- Must start with a predicate (which is an atom) and end with a fullstop. - Syntax: father(john, peter). father(john, mary). mother(susan, peter).|sey|answer 4|answer 5',9),
	 (18,'Unnamed','2021-05-29','student1','question1','answer1',0);
INSERT INTO "quiz" ("quiz_id","quiz_name","date_created","author","plays") VALUES
	 (12,'General Knowledge!','2021-05-27','student1',4),
	 (13,'my favourite questions','2021-05-27','student2',1),
	 (14,'my quiz','2021-05-29','student1',1),
	 (25,'sssss','2025-04-20','staffuser',1),
	 (26,'xxxx','2025-04-20','staffuser',0);
INSERT INTO "user_inventory" ("username","id") VALUES
	 ('student1',1),
	 ('student1',2),
	 ('student1',1),
	 ('student1',1),
	 ('student1',3),
	 ('student1',4),
	 ('student1',5);
INSERT INTO "user_hobby" ("username","hobby") VALUES
	 ('student1','code'),
	 ('student1','coding'),
	 ('student1','programming'),
	 ('student1','swimming'),
	 ('student6','coding'),
	 ('student6','programming'),
	 ('student5','coding'),
	 ('student5','programming');
INSERT INTO "user_interests" ("username","interest") VALUES
	 ('student1','book'),
	 ('student1','reading'),
	 ('student1','swimming'),
	 ('student6','c'),
	 ('student5','book'),
	 ('student5','reading'),
	 ('student5','swimming');
INSERT INTO "user_level" ("username","experience") VALUES
	 ('adminuser',50),
	 ('staffuser',350),
	 ('staffusertwo',100),
	 ('student1',2361),
	 ('student1000',25),
	 ('student1001',25),
	 ('student1002',25),
	 ('student2',826),
	 ('student3',225),
	 ('student4',302);
INSERT INTO "user_level" ("username","experience") VALUES
	 ('student5',200),
	 ('student6',400),
	 ('student7',375),
	 ('student8',50);
INSERT INTO "user_likes" ("username","post_id") VALUES
	 ('student1',1),
	 ('staffuser',1),
	 ('student2',5),
	 ('student3',6),
	 ('student1',11),
	 ('student1',6);
INSERT INTO "user_profile" ("username","name","bio","gender","birthday","profilepicture","degree","privacy") VALUES
	 ('student1','First Student','                                                                                                                        Change your bio in the settings.','Female','2001-04-15','/static/images/default-pfp.jpg',48,'public'),
	 ('student2','Second Student','Change your bio in the settings.','Male','2021-03-11','/static/images/default-pfp.jpg',1,'public'),
	 ('student3','Third Student','Change your bio in the settings.','Male','2021-03-11','/static/images/default-pfp.jpg',1,'public'),
	 ('student4','Fourth Student','Change your bio in the settings.','Male','2021-03-11','/static/images/default-pfp.jpg',1,'public'),
	 ('staffuser','Staff User','Change your bio in the settings.','Male','2021-03-11','/static/images/default-pfp.jpg',1,'public'),
	 ('adminuser','Admin User','Change your bio in the settings.','Male','2021-03-11','/static/images/default-pfp.jpg',1,'public'),
	 ('staffusertwo','Second Staff','Change your bio in the settings.','Male','2021-03-11','/static/images/default-pfp.jpg',1,'public'),
	 ('student5','Student Five','Change your bio in the settings.','Male','2021-05-05','/static/images/default-pfp.jpg',69,'public'),
	 ('student6','Sixth Student','Change your bio in the settings.','Male','2021-05-27','/static/images/default-pfp.jpg',48,'public'),
	 ('student7','Seventh Student','Change your bio in the settings.','Male','2021-05-27','/static/images/default-pfp.jpg',48,'public');
INSERT INTO "user_profile" ("username","name","bio","gender","birthday","profilepicture","degree","privacy") VALUES
	 ('student8','Sstudent Numero Eight','Change your bio in the settings.','Male','2021-05-29','/static/images/default-pfp.jpg',1,'public'),
	 ('student1000','Test','Change your bio in the settings.','Male','2021-08-06','/static/images/default-pfp.jpg',1,'public'),
	 ('student1001','Test','Change your bio in the settings.','Male','2021-08-06','/static/images/default-pfp.jpg',1,'public'),
	 ('student1002','Test','Change your bio in the settings.','Male','2021-08-06','/static/images/default-pfp.jpg',1,'public');
INSERT INTO "user_social" ("username","social","link") VALUES
	 ('student1','facebook','sadasd');

SET session_replication_role = 'origin';


