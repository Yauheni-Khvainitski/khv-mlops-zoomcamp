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
    default     = "ride-events"
}

variable "output_stream_name" {
    description = "Output data stream name (consumer)"
    default     = "ride-predictions"
}

variable "model_bucket" {
  description = "Name of the S3 bucket"
  default     = "ride-predictions"
}