# Gardenia: Community Garden Management System

## Overview

**Gardenia** is a program designed to support local gardens by simplifying and organizing key aspects of garden management. The program includes functionalities such as volunteer management, scheduling, plant care tracking, inventory management, and harvest distribution. This application aims to streamline garden operations, making it easier for volunteers and administrators to collaborate effectively.

### Key Features
- **Volunteer Management**: Store and access volunteer information (e.g., name, specialization).
- **Schedule Management**: Organize and assign tasks (e.g., planting, watering, pruning, harvesting).
- **Plant Care Tracking**: Monitor crop status based on environmental factors and volunteer logs.
- **Inventory Management**: Track gardening tools, seeds, compost, and other resources.
- **Harvest Distribution**: Efficiently divide harvested crops among beneficiaries.

> :warning: **Note!!**: Currently, the program ONLY includes a **Login System** that authenticates users and displays basic volunteer information upon successful login.

---

## Login Functionality

The login system is the first step to accessing Gardenia. It includes the following features:

- **User Authentication**:
  - Users can log in using their username and password.
  - The system validates credentials against a MongoDB database.
- **Volunteer Information**:
  - Upon successful login, the system retrieves and displays the volunteer's name and specialization.
- **Restricted Access**:
  - Only authenticated users (admins or volunteers) can access the system.

---

## How to Run the Program on Ubuntu WSL

Follow these steps to set up and run the Gardenia login system on Ubuntu WSL.

### Prerequisites

1. **Ubuntu WSL**: Ensure you have Ubuntu installed on Windows Subsystem for Linux (WSL).
2. **Python**: Install Python 3.x on your Ubuntu terminal:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```
3. **Dependencies**: Install the dependencies, pymongo and flet.
   ```bash
   pip install pymongo flet
   ```

### Running the Program

1. Start the application:
   ```bash
   python main.py
   ```
2. Use the following credentials to test the login:
  - username: Mikz
  - password: 1234
3. After successful login, the application will display the volunteer's name and specialization.

Expected output:
Welcome, Mikz Lugtu!
Specialization: Floriculture


---

## Roadmap of functions:
- Implement admin and volunteer roles with distinct functionalities.
- Add additional features like task scheduling, inventory management, and harvest distribution.
