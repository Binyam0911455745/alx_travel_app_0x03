# ALX Travel App (0x03)

This project is a continuation of the ALX Travel App, a Django-based web application for managing travel listings and bookings. This version, `0x03`, focuses on implementing background task management using **Celery** and **RabbitMQ** to handle asynchronous operations, specifically **email notifications**.

## Features

- **Asynchronous Task Processing**: Uses Celery to offload time-consuming tasks to the background.
- **Email Notifications**: Sends booking confirmation emails asynchronously to avoid blocking the web server.
- **RabbitMQ Integration**: Configured as the message broker for Celery to manage task queues.

## Setup and Installation

### 1. Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.8 or higher
- Git
- RabbitMQ server

### 2. Clone the Repository

Clone this repository to your local machine:

```bash
git clone [https://github.com/Binyam0911455745/alx_travel_app_0x03.git](https://github.com/Binyam0911455745/alx_travel_app_0x03.git)
cd alx_travel_app_0x03