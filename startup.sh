#!/bin/bash

# Navigate to the directory where the file is located.
cd .\src\

# Run the Flask application
.\src\python app.py

# Open browser
xdg-open http://127.0.0.1:5000