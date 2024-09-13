# file-managment-system


celery -A apps.taskapp beat -l info

celery -A apps.taskapp worker --loglevel=info --pool=threads --concurrency=100