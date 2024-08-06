# Simple Microservice Project

This is a small microservice project designed to demonstrate the use of FastAPI and RabbitMQ. The service performs OCR on PDF files. The project is containerized and can be easily started using Docker Compose.

## Features
- **FastAPI** for the backend.
- **RabbitMQ** as the message queue.
- **Docker Compose** for container orchestration.

## Requirements
- Docker
- Docker Compose

## Getting Started
1. Clone the repository:
   ```bash
   git clone https://github.com/Nurshot/ocr-pdf-microservice-demo.git
   cd ocr-pdf-microservice-demo
2. Start the services using Docker Compose:
   ```bash
   docker-compose up

## Usage
Once the services are up, you can interact with the FastAPI backend to upload PDF files and perform OCR.
RabbitMQ handles the message queue to process the OCR tasks.
