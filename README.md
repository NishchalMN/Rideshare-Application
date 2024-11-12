# RideShare Application

This repository contains the backend code for a scalable, cloud-based RideSharing application, developed using microservices architecture and deployed on AWS EC2. The project leverages Docker containers, RabbitMQ, Zookeeper, and PostgreSQL to ensure high availability, fault tolerance, and auto-scaling based on user demand.

## Features

- **Microservices Architecture**: Each core functionality (Users, Rides, Database) is deployed as a separate microservice on AWS EC2 instances.
- **Load Balancing**: Path-based routing with AWS Load Balancer, reducing response times by approximately 15%.
- **Database as a Service (DBaaS)**: Centralized, fault-tolerant DBaaS implemented with RabbitMQ and Zookeeper to manage read/write consistency and high availability.
- **Auto-Scaling**: Dynamic scaling of read containers based on incoming traffic, triggered at regular intervals.
- **Fault Tolerance**: Built-in leader election and failover mechanisms using Zookeeper, ensuring system resilience in case of node failure.
- **Comprehensive Testing**: Verified system reliability with Nginx and Postman, ensuring robustness across various traffic loads.

## Technologies

- **Flask** - for API development
- **Docker** - for containerization of services
- **AWS EC2** - for scalable cloud deployment
- **RabbitMQ** - for message queuing in remote procedure calls (RPC)
- **Zookeeper** - for leader election and node monitoring
- **PostgreSQL** - for database management
- **Nginx & Postman** - for load testing and API validation

## Architecture

The application uses a Load Balancer to direct requests to microservices, isolating the **Users**, **Rides**, and **Database** functionalities. A **Database as a Service (DBaaS)** setup ensures consistency across distributed databases with RabbitMQ for write/read operations and Zookeeper to manage node roles.

<img width="806" alt="Screenshot 2024-11-12 at 3 54 59 PM" src="https://github.com/user-attachments/assets/f03db5a2-ff6c-4248-be1f-8529d9de5e0b">

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

## Auto-Scaling Mechanism

The system scales read containers every two minutes based on the request count:
- 0–20 requests: 1 container
- 21–40 requests: 2 containers
- 41–60 requests: 3 containers

Each read operation triggers the orchestration layer to manage container count, optimizing cost and performance.
