# 1. vs-code-tips-tricks
Visual Studio Code Tips &amp; Tricks

- [1. vs-code-tips-tricks](#1-vs-code-tips-tricks)
- [2. Understanding Visual Studio Code settings](#2-understanding-visual-studio-code-settings)
- [3. CONTEXT](#3-context)
- [4. ENVIRONMENT CONFIGURATION](#4-environment-configuration)
  - [4.1. settings.json](#41-settingsjson)
  - [4.2. launch.json](#42-launchjson)
  - [4.3. tasks.json](#43-tasksjson)
- [5. Run in Docker and Debug](#5-run-in-docker-and-debug)
- [6. View code coverage](#6-view-code-coverage)
- [7. Troubleshooting](#7-troubleshooting)

Do you know how to debug your code while it's running inside a container? Do you know how to inject environment variables to Docker? Do you know how to measure the coverage of your unit tests? In this article I want to present you with a series of tricks to improve your skills and abilities developing applications and microservices with Python, Docker and Visual Studio Code. Are you interested? Read on.


# 2. Understanding Visual Studio Code settings


The .vscode folder is where our development environment is set up. It contains all the necessary configuration files to customize our experience with VS Code. In my opinion, this folder should be included in our source code repository so that all members of the development team contribute and share their experience about the work environment



# 3. CONTEXT
For this example I have prepared a very simple API developed with Fast API that has the following characteristics:

- Exposes the documentation with Swagger (Open API)
- Exposes a [GET] /version method that returns the version of the APP 
- Uses environment variables, defined in a local .env file 
- It contains a Dockerfile that will allow us to deploy it wherever we want 
- We also want to cover our code with Unit Tests 
- EXTRA: we want to visualize areas of the code not covered by unit tests

# 4. ENVIRONMENT CONFIGURATION
The three most important files are:

## 4.1. settings.json
This file contains the environment settings. In another article I will talk in depth about what we can do with it and I will leave several examples. We are going to configure two actions that we can then execute from VS Code, one to execute our application in Docker and another to execute the unit tests.

## 4.2. launch.json
This file contains the settings for how and where our applications will be launched.</p>

## 4.3. tasks.json
This file defines the settings for certain commands such as compile and run tasks, including certain arguments to pass. Here we define two tasks, one to compile the application and one to launch it, which will then be used by the configuration that we have defined in launch.json previously. These two tasks, docker-build and docker-run, are part of the Docker plugin, if you don't have it installed it will give you errors when trying to launch the application.


Having this well defined we should be able to see these two launch options in the dropdown that is seen in the RUN AND DEBUG section.

# 5. Run in Docker and Debug
Similarly, in the RUN AND DEBUG section, we must select the option that compiles and launches the application. When we hit play to launch it, we will see how the entire process is orchestrated. 

As a result, if all went well, we'll see two things. On the one hand, a notification will open from our Windows firewall informing us that Docker is requesting access to the Interne and on the other we will see a browser with the web that has been generated with the documentation of our API, which as we can see is very simple.

We have achieved this with just 35 lines of code as you can see in main.py

# 6. View code coverage

I've tried several ways and the easiest for me is to install a Visual Studio Code extension called Coverage Gutters. Once this extension is installed, using the files generated by pytest-cov, it marks in our code which areas are covered and which are not, with green and red respectively. To show and hide this visual "hint", just check the "Watch" option that we have in the bottom bar of VS Code. It is a Toggle button that will show us the percentage of coverage and the colors in the bar. 

# 7. Troubleshooting

There are many problems that we can find in this context. The one that has caused me the most headaches and the one that I have seen the most times on Stack Overflow is that we mark some breakpoints and VS Code tells us that it cannot find that file in the container.

This may be due to an inconsistency in the remote file system, ie the file path in the container does not match what VS Code expects. 

To clarify what we have deployed in the container, what is the path of the working directory, that is, the root of the Python process, we must take a look at our Dockerfile and the a launch.json file. 

In our Dockerfile we have: 
<pre class="EnlighterJSRAW" data-enlighter-language="dockerfile" data-enlighter-theme="" data-enlighter-highlight="" data-enlighter-linenumbers="" data-enlighter-lineoffset="" data- enlighter-title="" data-enlighter-group="">FROM python:3.10-slim

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

WORKDIR /app/src

ARG PORT=8080
EXPOSE $PORT</pre>

As you can see, the working directory (Working Directory) in the container is /app/src... Now take a look at the Python configuration we had for the container in launch.json:

<pre class="EnlighterJSRAW" data-enlighter-language="json" data-enlighter-theme="" data-enlighter-highlight="" data-enlighter-linenumbers="" data-enlighter-lineoffset="" data- enlighter-title="" data-enlighter-group="">"python": {
        "args": [
          "-m ",
          "simple_api"
        ],
        "pathMappings": [
          {
            "localRoot": "${workspaceFolder}",
            "remoteRoot": "/app"
          }
        ],
        "projectType": "fastapi"
      },</pre>

We need to adjust the path mapping so that the local root (${workspaceRoot }/simple-api/src) matches the remote root (/app/src) so that the debugging engine can set and use breakpoints in the container. We're also going to configure We're going to change several Python things to run our code as a module with "module": "simple_api". The Python section in the launch.json would look like this:
<pre class="EnlighterJSRAW" data-enlighter-language="json" data-enlighter-theme="" data-enlighter-highlight="" data-enlighter-linenumbers="" data-enlighter-lineoffset="" data- enlighter-title="" data-enlighter-group="">"python": {
        "module": "simple_api",
        "pathMappings": [
          {
            "localRoot": "${workspaceRoot}/simple-api/src",
            "remoteRoot": "/app/src"
          }
        ],
        "projectType": "fastapi"
      },</pre>

Once these changes have been made, we can debug as I explained above.