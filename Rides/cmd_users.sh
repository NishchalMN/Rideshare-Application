sudo docker cp AreaNameEnum.csv users:/assign2/AreaNameEnum.csv
sudo docker cp second.sql users:/assign2/second.sql
sudo docker exec -it users /bin/bash
/etc/init.d/mysql start
mysql
create database cloud;
exit;
mysql -u root -p cloud < second.sql
mysql;
\r cloud;
create table calls( req INT );
insert into calls value(0);
exit;
exit;



sudo docker cp AreaNameEnum.csv users:/assign2/AreaNameEnum.csv && sudo docker cp second.sql users:/assign2/second.sql && sudo docker exec -it users /bin/bash
/etc/init.d/mysql start
create database cloud;
mysql -u root -p cloud < second.sql
create table calls( req INT );
insert into calls value(0);


sudo docker cp AreaNameEnum.csv rides:/assign2/AreaNameEnum.csv && sudo docker cp second.sql rides:/assign2/second.sql && sudo docker exec -it rides /bin/bash

from flask_cors import cors


# old
ssh -i "Project.pem" ubuntu@ec2-34-231-57-195.compute-1.amazonaws.com

# new
ssh -i "New_Project.pem" ubuntu@ec2-52-71-151-42.compute-1.amazonaws.com

