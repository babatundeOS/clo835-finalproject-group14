         ___        ______     ____ _                 _  ___  
        / \ \      / / ___|   / ___| | ___  _   _  __| |/ _ \ 
       / _ \ \ /\ / /\___ \  | |   | |/ _ \| | | |/ _` | (_) |
      / ___ \ V  V /  ___) | | |___| | (_) | |_| | (_| |\__, |
     /_/   \_\_/\_/  |____/   \____|_|\___/ \__,_|\__,_|  /_/ 
 ----------------------------------------------------------------- 


Hi there! Welcome to AWS Cloud9!

To get started, create some files, play with the terminal,
or visit https://docs.aws.amazon.com/console/cloud9/ for our documentation.

Happy coding!
# clo835-finalproject-group14

## Babatunde Oyeyemi
## Dharmik Rana
## Soham Kandhare



To deploy the YAML files in the correct order for a smooth deployment in the "final" namespace, you generally want to follow this sequence:

secret.yaml
pvc.yaml
deployment.yaml
service.yaml
Here are the commands you can use:

From the msql folder:

1. Create secret:
`kubectl apply -f secret.yaml -n final`
2. Create PersistentVolumeClaim (PVC):
`kubectl apply -f pvc.yaml -n final`
3. Create deployment:
`kubectl apply -f deployment.yaml -n final`
4. Create service:
`kubectl apply -f service.yaml -n final`

From the Manifest folder:

`kubectl apply -f serviceAccount.yaml -n final`

`kubectl apply -f role.yaml -n final`

`kubectl apply -f rolebinding.yaml -n final`

`kubectl apply -f configmap.yaml -n final`

`kubectl apply -f deployment.yaml -n final`

`kubectl apply -f service.yaml -n final`

`kubectl apply -f hpa.yaml -n final`
