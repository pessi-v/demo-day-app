# Task Manager Infrastructure
# This configuration deploys to a high-carbon region (us-east-1)
# Carbonara will recommend migrating to eu-north-1 for ~89% CO2 reduction

terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Provider configuration - HIGH CARBON REGION
# us-east-1 (Virginia) has ~400 gCO2/kWh
# Alternative: eu-north-1 (Stockholm) has only ~45 gCO2/kWh
provider "aws" {
  region = "us-east-1"
}

# VPC for the application
resource "aws_vpc" "task_manager" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "task-manager-vpc"
    Environment = "demo"
    Project     = "carbonara-demo"
  }
}

# Public subnet
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.task_manager.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "task-manager-public-subnet"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.task_manager.id

  tags = {
    Name = "task-manager-igw"
  }
}

# Lambda execution role
resource "aws_iam_role" "lambda_role" {
  name = "task_manager_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })

  tags = {
    Name = "task-manager-lambda-role"
  }
}

# Attach basic Lambda execution policy
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Lambda function for the API
resource "aws_lambda_function" "api" {
  function_name = "task-manager-api"
  role          = aws_iam_role.lambda_role.arn
  handler       = "app.main.handler"
  runtime       = "python3.11"
  timeout       = 30
  memory_size   = 512

  # In a real deployment, this would point to your deployment package
  filename         = "lambda_function.zip"
  source_code_hash = filebase64sha256("lambda_function.zip")

  environment {
    variables = {
      ENVIRONMENT = "demo"
      DB_ENDPOINT = aws_db_instance.tasks_db.endpoint
    }
  }

  tags = {
    Name        = "task-manager-api"
    Environment = "demo"
  }
}

# RDS PostgreSQL Database
# Running continuously in a high-carbon region
resource "aws_db_instance" "tasks_db" {
  identifier           = "task-manager-db"
  engine               = "postgres"
  engine_version       = "15.3"
  instance_class       = "db.t3.micro"
  allocated_storage    = 20
  storage_type         = "gp2"
  storage_encrypted    = true

  db_name  = "taskmanager"
  username = "dbadmin"
  password = "changeme123" # In production, use AWS Secrets Manager

  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  skip_final_snapshot = true
  publicly_accessible = false

  tags = {
    Name        = "task-manager-database"
    Environment = "demo"
  }
}

# Private subnet for RDS
resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.task_manager.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "task-manager-private-subnet"
  }
}

# DB subnet group
resource "aws_db_subnet_group" "main" {
  name       = "task-manager-db-subnet"
  subnet_ids = [aws_subnet.public.id, aws_subnet.private.id]

  tags = {
    Name = "task-manager-db-subnet-group"
  }
}

# Security group for RDS
resource "aws_security_group" "rds" {
  name        = "task-manager-rds-sg"
  description = "Security group for RDS database"
  vpc_id      = aws_vpc.task_manager.id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "task-manager-rds-sg"
  }
}

# API Gateway (optional - for HTTP access to Lambda)
resource "aws_apigatewayv2_api" "main" {
  name          = "task-manager-api"
  protocol_type = "HTTP"

  tags = {
    Name = "task-manager-api-gateway"
  }
}

# Outputs
output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.api.function_name
}

output "database_endpoint" {
  description = "RDS database endpoint"
  value       = aws_db_instance.tasks_db.endpoint
  sensitive   = true
}

output "region" {
  description = "AWS region (high carbon intensity)"
  value       = "us-east-1"
}

output "carbon_recommendation" {
  description = "Carbon optimization recommendation"
  value       = "Consider migrating to eu-north-1 (Stockholm) for ~89% CO2 reduction (45 vs 400 gCO2/kWh)"
}
