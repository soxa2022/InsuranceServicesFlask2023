# Flask Insurence Services

> This is a simple application for providing insurance services in REST API.

## Table of Contents

* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Setup](#setup)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)

<!-- * [License](#license) -->

## General Information

- Provide general information about your project here.
- What problem does it (intend to) solve?
- What is the purpose of your project?
- Why did you undertake it?

<!-- You don't have to answer all the questions - just the ones relevant to your project. -->

## Technologies Used

- Python - version 3.9
- Flask Framework
- PostgreSQL - version 15

## Features

List the ready features here:

- Create customer
- Create two types of insurences (vehicle and estate)
- Searching for employee
- Create stats for customers and profits
- Payment for created insurance
- Send marketing notification
- Send notification emails for expires insurences

## Setup

All project requirements/dependencies are in
`requirements.txt` in root directory.

`pip install -r requirements.txt`

# REST API

The REST API with endpoints information.

Create a new Customer  

POST /insurence/register  
http://127.0.0.1:5000/insurence/register

Response

HTTP/1.1 201 OK  
Status: 201 OK    
Content-Type: application/json   


Login custom   

Request  

POST /insurence/login   
http://127.0.0.1:5000/insurence/login 

Response 

HTTP/1.1 200 OK  
Status: 200 OK   
Content-Type: application/json 

Create a new Vehicle  

Request

POST /insurence/vehicle   
http://127.0.0.1:5000/insurence/vehicle

Response

HTTP/1.1 201 Created   
Status: 201 Created         
Content-Type: application/json

Create a new Estate 

Request

POST /insurence/estate   
http://127.0.0.1:5000/insurence/vehicle

Response

HTTP/1.1 201 Created   
Status: 201 Created         
Content-Type: application/json

Accept the input data from the customer for vehicle

Request

GET /insurence/vehicle/id/accept

http://127.0.0.1:5000/insurence/vehicle/2/accept

Response

HTTP/1.1 200 OK  
Status: 200 OK  
Content-Type: application/json  

Cancel the input data from the customer for vehicle

Request

GET /insurence/vehicle/id/accept

http://127.0.0.1:5000/insurence/vehicle/2/cancel

Response

HTTP/1.1 200 OK  
Status: 200 OK  
Content-Type: application/json

Delete vehicle

Request

DELETE /insurence/vehicle/3/delete

http://127.0.0.1:5000/insurence/vehicle/3/delete

Response

HTTP/1.1 200 OK  
Status: 200 OK  
Content-Type: application/json

Request

Customers make payments for their insurences

POST /insurence/payments/card

http://127.0.0.1:5000/insurence/payments/card

HTTP/1.1 200 OK  
Status: 200 OK  
Content-Type: application/json

Request

Employees looking for information about customers and vehicles

GET /insurence/search?email={customer`s id}&plate_number={vehicle's plate number}   

http://127.0.0.1:5000/insurence/search?email=test_flask@mail.bg&plate_number=CB8063BB

HTTP/1.1 200 OK  
Status: 200 OK  
Content-Type: application/json

Request

Employees can the stats for the customer`s name and email compared with paid sums

GET /insurence/stats

http://127.0.0.1:5000/insurence/stats

HTTP/1.1 200 OK  
Status: 200 OK  
Content-Type: application/json

## Project Status

Project is: _in progress_

## Room for Improvement

Room for improvement:
- Improve notification for the expired insurences
- Improve creating a new insurence
To do:
- 3rd party support for sms services


## Acknowledgements

- This project was inspired by myself
- This project was based on Softuni course
- Many thanks to Ines Ivanova

