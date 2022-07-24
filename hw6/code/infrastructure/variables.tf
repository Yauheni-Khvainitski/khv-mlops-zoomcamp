variable "aws_region" {
    description = "AWS region to create resources"
    default     = "us-east-1"
}

variable "project_id" {
    description = "value"
    default     = "mlops-zoomcamp"
}

variable "source_stream_name" {
    description = "Input data stream name"
    default     = "ride_predictions"
}