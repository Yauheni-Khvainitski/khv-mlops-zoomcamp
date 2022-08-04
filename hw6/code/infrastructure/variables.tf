variable "aws_region" {
    description = "AWS region to create resources"
    default     = "us-east-1"
}

variable "env" {
  type        = string
  description = "environment prefix"
}

variable "project_id" {
    description = "value"
    default     = "mlops-zoomcamp"
}

variable "source_stream_name" {
    description = "Input data stream name (producer)"
}

variable "output_stream_name" {
    description = "Output data stream name (consumer)"
}

variable "model_bucket" {
  description = "Name of the S3 bucket"
}

variable "lambda_function_local_path" {
  description = "lambda local path for ecr image"
}

variable "docker_image_local_path" {
  description = "Dockerfile local path for dockerizing lambda"
}

variable "ecr_repo_name" {
  description = "ecr repo name"
}

variable "lambda_function_name" {
  description = "Name of the lambda function"
}