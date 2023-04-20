notification-engine
Notification Engine

For this project I have used FastAPI with Django(ORM) to combine the strengths of both fastapi and django which builds a much powerfull application.
I decided to use django for the orm because that is much more handy, much better migration system than alembic, and ofcourse who dosen't wants to 
monitor the database with the django's built in admin.

For all of the functionalities I have used FastAPI, because its much more easier and faster way to develop the API.

I have also containerized the application with docker so that it can be run on multiple platforms easily.

To install the project:
1) Check out the docker-compose.yml file to change the database credentials. Also make sure to add those changes in core/settings.py under DATABASES.
2) Build the project (`docker-compose up --build`) This would run two services web and database (We are using postgresql for this project).
3) Now we need to run create the superuser for that we need to shell in the docker container `docker ps` to list all containers. Use the `ContainerID` to run this command to shell in the container `docker exec -it <container-id> sh` if sh doesnt works, you can try `bin/sh` or `bin/bash` depends on the users operating system.
4) After we are in the container shell for the web container, we can run the command `./manage.py createsuperuser` and follow the onscreen instructions to create an admin user.

Thats it, now we can access the notification engine.
Some of the routes are:
1) `http://127.0.0.1:8000/web/admin` Django Admin
2) `http://127.0.0.1:8000/docs` FastAPI Docs
3) `http://127.0.0.1:8000/api/v1/notifications/live/<user-id>` Watch the Live Notifications for any user

Other routes for the apis and the endpoints that were asked to built can we seen and used with the FastAPI docs. That makes things so much usefull.

Hope you liked the project.
Thanks.
