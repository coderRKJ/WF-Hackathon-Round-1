# WF-Hackathon-Round-1
This repo contains the solution for Problem Statement-1: Generic notification system to send bulk text email.

## Introduction
The repo contains two parts:
1. An API Backend that uses FastAPI
1. A Vue3 Single Page Application (SPA) Frontend

The Backend and Frontend are combined in this Monorepo.

## Instructions to Run
- Requires Python 3.11 installed in a Linux system
1. Clone this repo and `cd` into the cloned folder
1. Run `bash local_setup.sh` to setup venv and python libraries
1. Run `bash local_run.sh` to start SMTP email server and FastAPI backend on uvicorn.
1. Open `localhost:8000` to access the client website
1. `localhost:8000/docs` shows API endpoints
1. *Ctrl*+*C* to Stop both servers
