#!/bin/bash


cd   /home/ubuntu/recipe_BE


echo ">>> pip install ----------------------"
pip install -r requirements.txt


echo ">>> remove template files ------------"
rm -rf appspec.yml requirements.txt


echo ">>> change owner to ubuntu -----------"
chown -R ubuntu /home/ubuntu/recipe_BE

# echo ">>> set env --------------------------"
# chmod +x /home/ubuntu/recipe_BE/scripts/env.sh
# cd /home/ubuntu/recipe_BE/scripts
# source ./env.sh

cd   /home/ubuntu/recipe_BE

# flask db init
# flask db migrate
# flask db upgrade

echo ">>> start server ---------------------"
gunicorn --bind 0.0.0.0:5000 --timeout 90 "app:create_app()" > /home/ubuntu/gunicorn.log 2>&1 &

