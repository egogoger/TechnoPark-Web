#!/bin/bash

cd Downloads/Prog/TechnoPark/Web/Q\&A/
source venv/bin/activate
cd TechnoPark-Web/QA/

./manage.py get_top --users 1
./manage.py get_top --tags 1

deactivate