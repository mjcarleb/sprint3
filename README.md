# To run ngrok: 
(base) markcarlebach@Marks-MBP Downloads % ./ngrok http 127.0.0.1:5000              

# To run rabbitMQ
docker run -d -p 5672:5672 rabbitmq

# To run celery:  
$celery -A celery_tasks worker --loglevel=INF
