# TrendinessProject
UW-Madison GB760 Twitter Trendiness Project
Group Members: Matt Plantz, Keith Hines, Hao Tran, Chelsi Gondalia, Logan Butson, Daniel Waller, Xinyuan Zhang

Milestone 2 Part A - HT
Create database 
Assuming host is 'gb760', run the following commands in terminal 
1) psql
2) create database trendy;
3) \q
4) cd to the directory where 'schema_postgres.sql' is located
5) psql trendy < schema_postgres.sql
6) psql
7) \c trendy <-- go to trendy database
8) \dt  <-- This should show your tables
9) select * from base <-- You should get 0 rows 
