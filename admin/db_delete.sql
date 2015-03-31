DELETE FROM MYSQL.USER WHERE USER = 'pushdb';
use piccolo;
DELETE FROM push_app;
DELETE FROM push_user;
DELETE FROM push_key;
DROP DATABASE piccolo;
