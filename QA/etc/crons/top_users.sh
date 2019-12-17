#!/bin/bash

cd Downloads/Prog/TechnoPark/Web/Q\&A/
source venv/bin/activate
cd TechnoPark-Web/QA/

./manage.py top_users

deactivate