# Property Opportunity Tracker

A Flask-based property opportunity tracker built for personal use.

The application allows a user to enter an area they want to scan and then searches property listings for opportunities such as price reductions.

## How it works

1. Open the Flask application.
2. Enter the area you want to scan into the **Add Area** box.
3. Start the scan.
4. The application collects relevant property listing information.
5. Property data is stored in a database.
6. Relevant opportunities can then be displayed to the user.

## Features

* Flask web interface
* Add an area to scan
* Automated property listing collection
* Property database
* Price-drop detection
* Property listing information and links
* Docker support

## Technologies

* Python
* Flask
* SQLite
* Playwright
* Docker

## Running the application

The application can be run locally using Python or using Docker.

### Local

Install the dependencies:

```bash
pip install -r requirements.txt
```

Start the Flask application:

```bash
python app.py
```

Then open the local address shown by Flask in your browser.

### Docker

Build the Docker image:

```bash
docker build -t property-opportunity-tracker .
```

Run the container:

```bash
docker run -p 5000:5000 property-opportunity-tracker
```

Then open:

```text
http://localhost:5000
```

## Purpose

This project was originally developed to solve a real problem for my dad: reducing the amount of manual searching required to find potentially interesting property opportunities.

It was developed as a private experimental project for personal use.
