# Install the required MySQL package

sudo apt-get update -y
sudo apt-get install mysql-client -y

# Running application locally
pip3 install -r requirements.txt
sudo python3 app.py
# Building and running 2 tier web application locally
### Building mysql docker image 
```docker build -t my_db -f Dockerfile_mysql . ```

### Building application docker image 
```docker build -t my_app -f Dockerfile . ```

### Running mysql
```docker run -d -e MYSQL_ROOT_PASSWORD=pw  my_db```


### Get the IP of the database and export it as DBHOST variable
```docker inspect <container_id>```


### Example when running DB runs as a docker container and app is running locally
```
export DBHOST=127.0.0.1
export DBPORT=3307
```
### Example when running DB runs as a docker container and app is running locally
```
export DBHOST=172.17.0.2
export DBPORT=3306
```
```
export DBUSER=root
export DATABASE=employees
export DBPWD=pw
export APP_COLOR=blue
```
### Run the application, make sure it is visible in the browser
```docker run -p 80:81  -e DBHOST=$DBHOST -e DBPORT=$DBPORT -e  DBUSER=$DBUSER -e DBPWD=$DBPWD  my_app```





k delete deployment.apps/my-deployment -n final
k delete service/app-service -n final

kubectl get all -n final

kubectl config set-context --current --namespace final

aws eks update-kubeconfig --region us-east-1 --name clo835
kubectl config set-context --current --namespace final
k apply -f pvc.yaml
k apply -f sqldb-pod-deployment.yaml
