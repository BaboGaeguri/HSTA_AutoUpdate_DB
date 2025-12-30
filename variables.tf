variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-northeast-2"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "ami_id" {
  description = "AMI ID for EC2 instance (Amazon Linux 2023)"
  type        = string
  default     = "ami-0c9c942bd7bf113a2" # Amazon Linux 2023 in ap-northeast-2
}

variable "key_pair_name" {
  description = "EC2 key pair name"
  type        = string
}
