# Cloud-Computing Project

 ## Starting the 2 Initial Master and Slave Workers
 
 1. To send the request in postman   
    ```
    http://instanceIP:80/api/v1/worker/spawn
    ```
    
    ## Creating the Docker Network

1. Start the docker service.
2. Run the `build` command to start Orchestrator, RabbitMQ and Zookeeper servers

    ```shell
    $docker-compose build
    ```

3. Start the containers as daemon process

    ```shell
    $docker-compose up -d
    ```
 
