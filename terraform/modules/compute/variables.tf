variable "environment" { type = string }
variable "vpc_id" { type = string }
variable "subnet_ids" { type = list(string) }
variable "key_name" { type = string }

variable "eks_instance_type" {
  type    = string
  default = "m7i-flex.large"
}