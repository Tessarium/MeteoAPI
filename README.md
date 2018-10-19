# MeteoAPI

This small project was created to demonstrate the current level of development and as a addition to the resume.
The main purpose is to show code examples and skills work with the frameworks.

## Requirements

```
pip3 install django
pip3 install djangorestframework
pip3 install coreapi
```

## Running the tests
In the words of Jacob Kaplan-Moss (founded the Django Software Foundation and was one of the core developer of django):
>"Code without tests is broken as designed"

```
python manage.py test (or python3 manage.py test)
```

## Documentation

```
https://localhost/docs/
```

| URL  | Method | Required parameters | Addition parameters | Description |
| :---         |     :---:      |     :---:      |     :---:      |     :---:      |
| /api/{version}/locations/ | GET | version | | Returns all locations. |
| /api/{version}/locations/ | POST | version | name | Creates a new location object. |
| /api/{version}/locations/{id} | GET | version, id | | Returns the location. |
| /api/{version}/locations/{id} | PUT | version, id, name | | Updates the location. |
| /api/{version}/locations/{id}| PATCH | version, id | name | Partial updates the location. |
| /api/{version}/locations/{id} | DELETE | version, id | | Deletes the location. |
| /api/{version}/temperatures/ | GET | version | date, date_start, date_end | Returns all temperatures. It returns all temperatures in a range of 3 days by adding parameter 'date' (ex. 2018-10-23). It returns all temperatures in the specified range by adding a 'date_start' and a 'date_end' parameters. |
| /api/{version}/temperatures/ | POST | version | | Creates a new temperature. |
| /api/{version}/temperatures/{id} | GET | version, id | scale | Returns the temperature. It returns converted value with specified scale, by adding parameter of the scale (allowed - 'K', 'U+2103', '0xE2 0x84 0x89'). |
| /api/{version}/temperatures/{id} | PUT | version, id, scale, value, location | date | Updates the temperature. |
| /api/{version}/temperatures/{id} | PATCH | version, id | scale, value, date, location | Partial updates the temperature. |
| /api/{version}/temperatures/{id} | DELETE | version, id | | Deletes the temperature. |
| /api/{version}/temperatures/location/{id}/ | GET | version, id | | Returns all temperatures in the location. |

## Commands

This command creates temperatures with randomly parameters in 6 hours increments since the date that you specified.

```
python manage.py fill_db YYYY-MM-DD (ex. 2018-10-10)
```

