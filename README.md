# MOTOPP – Flask + MySQL + Redis DevOps Project

## Overview
**MOTOPP** is a containerized web application built with **Flask**, **MySQL**, and **Redis**.  
It demonstrates a full **DevOps lifecycle** including Infrastructure as Code (Terraform), Container Orchestration (Kubernetes), and CI/CD Automation (GitHub Actions).

---

## Tech Stack
- **Backend:** Flask (Python 3.9)
- **Database:** MySQL 8
- **Cache:** Redis (Alpine)
- **Infrastructure:** AWS (EC2, VPC, S3) via Terraform
- **Orchestration:** Kubernetes (Minikube) & Docker Compose
- **CI/CD:** GitHub Actions
- **Monitoring:** Prometheus & Grafana

---

## How to Run

### 1. Run via Docker Compose (Local)
This starts the full stack (App + Database + Redis) locally for development and testing.

```bash
touch .env
echo "MYSQL_PASSWORD=root_password_123" >> .env
echo "SECRET_KEY=my_secret_key_123" >> .env
echo "MYSQL_ROOT_PASSWORD=root_123" >> .env
docker compose up --build
```

**Access App:** http://localhost:5000

---

### 2. Run on AWS via Terraform
Terraform is used to provision AWS infrastructure such as **VPC** and **EC2** instances.

```bash
cd infra
terraform init
terraform apply -auto-approve
```

> **Note:** The `ec2_public_ip` output will be required for the Ansible step.

---

#### Configuration Management (Ansible)
Ansible installs **Docker**, **Minikube**, and **kubectl** on the EC2 instance.
> **Note:** Update inventory.ini with the`ec2_public_ip` as follow.
```
[webservers]
motopp_server ansible_host=<ec2_public_ip> ansible_user=ubuntu ansible_ssh_common_args='-o StrictHostKeyChecking=no'
```

Before running ansible switch to linux terminal (on Windows via WSL).
```bash
cd ansible

ansible-playbook -i inventory.ini playbook.yaml --private-key ~/motopp.pem
```
 .pem file is obtained by creating key pairs in EC2 instance. It should be in the main directory.


---


## CI/CD Pipeline
The project uses **GitHub Actions** for a fully automated CI/CD pipeline.

To run the workflow pipeline simply push to github repo:
```
git add .
git push commit -m "made changes"
git push -u origin main
```
---

If the CI/CD pipeline fails, check if SSH_Host is updated with the current `ec2_public_ip` from Step 2. 
##### OR
SSH into the server:
```
ssh -i "motopp-lab-exam.pem" ubuntu@<ec2_public_ip>
```
and use following commands:
```
kubectl get pods -n prod –watch
#to see status of pods, if they are failing or are showing error
```
```
minikube stop
minikube start --driver=docker --memory=6000mb
```

Then open **http://e2_public_ip:30001** in your browser to access the app.


## Monitoring
The monitoring stack includes **Prometheus** and **Grafana**.

- **Prometheus:** Collects metrics from the Kubernetes cluster
- **Grafana:** Visualizes metrics such as:
  - CPU usage
  - Memory usage
  - Network I/O

### Getting Grafana Password

#####  1. SSH into the server
```
ssh -i "motopp-lab-exam.pem" ubuntu@<ec2_public_ip>
#same folder as of *.pem file
```

#####  2. Print out password
```
kubectl get secret --namespace monitoring monitor-stack-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```
user: `admin`
password: `<text from above command>`

Then open **http://e2_public_ip:30002** in your browser to access grafana.

---

### 3️. Teardown (Cleanup)
To destroy all AWS resources:

```bash
cd infra
terraform destroy -auto-approve
```
> **Note:** This will destroy both EC2 & S3 instances, to run the pipeline again, change ec2_public_ip again after running terraform apply command in Step 2.
---