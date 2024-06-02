create database GuestBookingSystem2302021;
use GuestBookingSystem2302021;


-- Creating roomtype Table
create table Roomtype(
roomtypeid int primary key auto_increment,
roomtype_desc varchar(255)
);
insert into Roomtype values
(1,'SINGLE WITH AC'),
(2,'SINGLE WITHOUT AC'),
(3,'DOUBLE WITH AC'),
(4,'DOUBLE WITHOUT AC');
-- Creating Room Table

create table Rooms(
roomid int primary key auto_increment,
room_number varchar(255),
room_flor int(50),
roomtypeid int(100),
status varchar(255),
foreign key(roomtypeid) references Roomtype(roomtypeid)
);  

insert into Rooms
values 
(1,'100',1,1,'empty'),
(2,'101',1,1,'empty'),
(3,'102',1,1,'empty'),
(4,'103',1,1,'empty'),
(5,'104',1,1,'empty'),
(6,'200',2,2,'empty'),
(7,'201',2,2,'empty'),
(8,'202',2,2,'empty'),
(9,'203',2,2,'empty'),
(10,'204',2,2,'empty'),
(11,'300',3,3,'empty'),
(12,'301',3,3,'empty'),
(13,'302',3,3,'empty'),
(14,'303',3,3,'empty'),
(15,'304',3,3,'empty'),
(16,'400',4,4,'empty'),
(17,'401',4,4,'empty'),
(18,'402',4,4,'empty'),
(19,'403',4,4,'empty'),
(20,'404',4,4,'empty');



-- Creating Table Guest
drop table Guests;
create table Guests(
guestid int primary key auto_increment,
gname varchar(255),
gphone varchar(255),
gemail varchar(255));

-- Creating Table Bookings

create table Bookings(
bid int primary key auto_increment,
guestid int,
roomtypeid int(100),
from_ datetime,
to_ datetime,
roomid int,
status varchar(255),
Check_out datetime,
foreign key(roomtypeid) references Roomtype(roomtypeid),
foreign key (guestid) references Guests(guestid),
foreign key(roomid) references Rooms(roomid)
);

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    date_of_birth DATE NOT NULL,
    Type varchar(255) not null
);
