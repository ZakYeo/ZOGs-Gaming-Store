# advanced-development-assignment-ZakYeo
Online GameStore built using Python's Flask library for a backend with HTML,CSS & JavaScript for the frontend. Pulls a list of games from a Database (MongoDB or Firebase RealtimeDB) to dynamically display on the webpage. The games' information is modifiable by administrator accounts marked in the databas. Administrators can also add or remove games entirely and view the "logs" of the website. 

The app interacts with the Cloudinary API to handle the saving of images in a database, and uses the Steam API to view the top achievements of the game selected.

## How To Run
- Setup a MongoDB & Firebase Authentication with Realtime DB
- Use the MongoDB and Firebase directories for exported JSON data of the data to use (or use your own, just ensure the same format is used)
- Pull repo in your Google Cloud directory<br>
- Setup Google Cloud Functions in the cloudfunctions directory by placing them in your Google Cloud Functions.<br>
- Some cloud functions will have redacted information such as firebase credentials or MongoDB URL + password. These need to be filled in with your own
- Run the app using gcloud app deploy in the Google Cloud console
