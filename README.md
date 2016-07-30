# The Hills FC
### 悉尼山区华人球队报名管理系统

#### Intro
The purpose of this system is to simplify the game signup and sign in flow, make it easier for the team mates to know where, when the match is, and using QR code to seamlessly track the signin status, on time, being late, or absent.

The site is running on Google App Engine, thanks to Google, it is $0 cost!

#### Prerequisite
The easiest way to setup the dev environment is to use docker, so get docker.
Alternatively you can have a Google App Engine env setup.

#### Get Started
Inside the project folder, run

```shell
docker-compose up -d
```

The first time run will build the container so it will take a few mins, after it's up running, you should be able to see the site at localhost and the App Engine console localhost:8000

**The container will map your machine's 80 and 8000 port, so be aware to leave these ports free**
