terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "perfumeshop/terraform.tfstate"
    region = "eu-west-1"
  }
}

provider "aws" {
  region = "eu-west-1"
}

resource "aws_s3_bucket" "embeddings" {
  bucket = "perfumeshop-embeddings-${var.environment}"
}

variable "environment" {
  type    = string
  default = "dev"
}