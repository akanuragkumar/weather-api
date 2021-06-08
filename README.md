# Weather forecasting API
This app gives weather forecast of 30 citites and also generates report and send them as mail.
## Quickstart

To work in a sandboxed Python environment it is recommended to install the app in a Python [virtualenv](https://pypi.python.org/pypi/virtualenv).

1. Clone and install dependencies

    ```bash
    $ git clone https://github.com/akanuragkumar/weather-api.git
    $ cd weather_api
    $ pip install -r requirements.txt
    ```
2. Install and run Redis and Celery

   If not installed then follow these steps to install [Redis](https://medium.com/@petehouston/install-and-config-redis-on-mac-os-x-via-homebrew-eb8df9a4f298)
   and [Celery](https://medium.com/@petehouston/install-and-config-redis-on-mac-os-x-via-homebrew-eb8df9a4f298).  
   To lean more about redis and celery rate limitting refer this [article](https://callhub.io/distributed-rate-limiting-with-redis-and-celery/).
   
   
3. Exporting environment variables
 ```bash
   $ export email_id='your email id'
   $ export password='Your password'
   $ export api_key='Your open weather API key'
   $ export main_url='http://api.openweathermap.org/data/2.5/weather?'
   ``` 

4. Running app

   ```bash
   $ manage.py makemigrations 
   $ python manage.py migrate
   $ python manage.py runserver
   ``` 
   
## API Documentation 

### `This Endpoint takes username and password and registers and gives the access token` 

1. `POST /user/register/` 

```json
 application/json - {
    "username": "username:,
    "password": "password"
}
```
##### `response`

```json
{
   "access_token": "access token"
}   
```
2. `POST /user/login/` 

```json
 application/json - {
    "username": "username:,
    "password": "password"
}
```
##### `response`

```json
{
   "access_token": "access token"
}
    
```
##### `For all the requests we would use this access token for authentication and permission in headers request`
```json
   Authorization: Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9
    
```
    

### `This Endpoint gives the list cities with their corresponding tempreture with pagination support ` 

1. `GET /api/current_weather/?page=1` 

##### `response`

```json
 application/json - {
 “count”: "total number of cities",
 “next”: "link for next page, if present",
 “previous”: "link for previous page",
 “data”: [
 {
 “city”: "city name",
 “current_temp”: "current tempreture of the city",
 “feels_like_temp”: "feels like tempreture of the city",
 “modified_on”: "last updated datetime for this city"
 },
 ...
 ]
}
```

### `This Endpoint takes city name and stores it in CityWeatherCollection so that celery scheduled job would populate weather details.` 

2. `POST /api/current_weather/` 

```json
 application/json - {"city": "mumbai"}
```
##### `response`

```json
{
    "status": "New city added to the weather list."
}   
```


### `This Endpoint takes email ids in a list, validates them, store them in MailingTask model with status as pending, calls celery task to generate excel report for 30 citites and send them mail with attachment.`

3. `POST /api/mailing_list/` 

```json
 application/json - {"emails":["anuragk@onefin.in", "bkss@one.in"]}
```
##### `response`

```json
{
    "status": "Task Initiated. Please wait for sometime for mail."
}
    
```
