terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# --- NETWORK ---
resource "aws_vpc" "motopp_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = { Name = "motopp-vpc" }
}

resource "aws_subnet" "motopp_subnet" {
  vpc_id                  = aws_vpc.motopp_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true
  tags = { Name = "motopp-public-subnet" }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.motopp_vpc.id
  tags = { Name = "motopp-igw" }
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.motopp_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }
  tags = { Name = "motopp-public-rt" }
}

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.motopp_subnet.id
  route_table_id = aws_route_table.public_rt.id
}

# --- SECURITY GROUPS ---
resource "aws_security_group" "allow_traffic" {
  name        = "motopp-sg"
  description = "Allow SSH, HTTP, and K8s NodePorts"
  vpc_id      = aws_vpc.motopp_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  # Kubernetes NodePort Range
  ingress {
    from_port   = 30000
    to_port     = 32767
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# --- COMPUTE ---
data "aws_ami" "ubuntu" {
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  owners = ["099720109477"] # Canonical
}

resource "aws_instance" "k8s_node" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "m7i-flex.large" # 2 vCPU, 4GB RAM (Minikube Minimum)
  subnet_id     = aws_subnet.motopp_subnet.id
  vpc_security_group_ids = [aws_security_group.allow_traffic.id]
  key_name      = "motopp-lab-exam" 

  # --- FIX 1: Storage Config moved here ---
  root_block_device {
    volume_size = 20  # 20GB to prevent disk space errors
    volume_type = "gp3"
  }

  # --- FIX 2: Auto-Install Docker, Minikube & Kubectl ---
  user_data = <<-EOF
              #!/bin/bash
              # Update and Install Docker
              apt-get update -y
              apt-get install -y ca-certificates curl gnupg lsb-release docker.io
              
              # Add ubuntu user to docker group (so we don't need sudo for docker)
              usermod -aG docker ubuntu
              newgrp docker

              # Install Minikube
              curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
              install minikube-linux-amd64 /usr/local/bin/minikube

              # Install Kubectl
              curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
              install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

              # Start Minikube (as ubuntu user)
              # We use 'su' because user_data runs as root
              su - ubuntu -c "minikube start --driver=docker --memory=6000mb"
              EOF

  tags = {
    Name = "Motopp-K8s-Node"
  }
}

# --- STORAGE (S3) ---
resource "random_id" "bucket_id" {
  byte_length = 4
}

resource "aws_s3_bucket" "motopp_storage" {
  bucket        = "motopp-assets-${random_id.bucket_id.hex}"
  force_destroy = true 
  tags = {
    Name        = "Motopp Assets"
    Environment = "Lab"
  }
}

# --- OUTPUTS ---
output "ec2_public_ip" {
  value       = aws_instance.k8s_node.public_ip
  description = "Public IP of the K8s Node"
}

output "s3_bucket_name" {
  value       = aws_s3_bucket.motopp_storage.bucket
  description = "Created S3 Bucket Name"
}