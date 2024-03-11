provider "aws" {
  region = "ap-southeast-1"
}

resource "aws_security_group" "simple_flask_sg" {
  name        = "simpleflask-sg"
  description = "Allow web and custom TCP traffic"

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
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 6500
    to_port     = 6500
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
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

resource "aws_instance" "simpleflask_instance" {
  ami             = "ami-0123c9b6bfb7eb962"
  instance_type   = "t2.micro"
  key_name        = "deploy" # Ensure 'deploy' key pair exists in your AWS account
  security_groups = [aws_security_group.simple_flask_sg.name]

  root_block_device {
    volume_size = 20
  }

  tags = {
    Name = "simpleflask"
  }
}
