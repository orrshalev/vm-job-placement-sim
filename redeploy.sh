docker build . -t flask-api
kubectl delete -f flask-deployment.yml
kubectl apply -f flask-deployment.yml
minikube service flask-service
