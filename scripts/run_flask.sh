echo ">>> start server ---------------------"
gunicorn --bind 0.0.0.0:5000 --timeout 90 "app:create_app()" > /home/ubuntu/gunicorn.log 2>&1 &