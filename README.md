# Coffee Shop Full Stack

## Full Stack Nano - IAM Final Project

Coffee Shop is the 3rd project out of 5 projects of Udacity Full Stack Web Developer Nanodegree.

Main focus of the project is:
-   Implementing authentication and authorization in Flask
-   Designing against key security principals
-   Implementing role-based control design patterns
-   Securing a REST API
-   Applying software system risk and compliance principles

Besides public users web app defines 2 roles (shop baristas and shop managers) with different permissions to the API.
The App.

1) Displays graphics representing the ratios of ingredients in each drink.
2) Allows public users to view drink names and graphics.
3) Allows the shop baristas to see the recipe information.
4) Allows the shop managers to create new drinks and edit existing drinks.



### Backend

The `./backend` directory contains a Flask server with an SQLAlchemy module to satisfy the application's data needs. Backend defines the required endpoints, Flask server configuration, and Auth0 integratation for authentication.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server.

[View the README.md within ./frontend for more details.](./frontend/README.md)
