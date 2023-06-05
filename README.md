# ZOGS Gaming Store: An Online Game Store

ZOGS Gaming Store is an online gaming platform built with a dynamic and interactive frontend and a robust backend. It was designed as part of my final year project at University and scored 94 out of 100 points. 

## Overview

The application is built using Python's Flask library for the backend and HTML, CSS & JavaScript for the frontend. It interfaces with either a MongoDB or Firebase Realtime Database to fetch and dynamically display a list of games on the webpage. 

The information pertaining to each game is modifiable by administrators who are granted permissions in the database. In addition to editing game information, administrators have the ability to add or remove games, and to view the website's "logs".

ZOGS Gaming Store also interacts with two APIs:
- The Cloudinary API: Handles the saving of images in the database.
- The Steam API: Allows the viewing of the top achievements for the selected game.

## Running the App

To get ZOGS Gaming Store up and running, follow the steps below:

1. **Database Setup**: Set up a MongoDB and Firebase Authentication with a Realtime Database. The necessary data to use (exported as JSON) is found in the MongoDB and Firebase directories. You can also use your own data, but ensure it's in the same format.

2. **Repository Setup**: Clone this repository into your Google Cloud directory.

3. **Google Cloud Functions Setup**: Set up Google Cloud Functions using the scripts provided in the `cloudfunctions` directory. Note: Some cloud functions have redacted information such as Firebase credentials or MongoDB URL and password. Fill in these fields with your own details.

4. **Deploy the App**: Finally, run the app by executing the `gcloud app deploy` command in the Google Cloud console.

That's it! Now you should have your instance of the ZOGS Gaming Store up and running. Enjoy!


## Application Screenshots
<img
  src="/screenshots/login.png"
  alt="Login Page Screenshot"
  title="Login Page"
  style="display: inline-block; margin: 0 auto;">
  <img
  src="/screenshots/main-page.png"
  alt="Main Page Screenshot"
  title="Main Page"
  style="display: inline-block; margin: 0 auto;">
   <img
  src="/screenshots/list-of-games.png"
  alt="List Of Games Screenshot"
  title="List Of Games"
  style="display: inline-block; margin: 0 auto;">
  <img
  src="/screenshots/game-page.png"
  alt="Game Page Screenshot"
  title="Game Page"
  style="display: inline-block; margin: 0 auto;">
For more screenshots and a video demonstration, see the screenshots folder.
