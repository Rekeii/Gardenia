# Gardenia: Community Garden Management System


## Overview

**Gardenia** is a program designed to support local gardens by simplifying and organizing key aspects of garden management. The program includes functionalities such as volunteer management, scheduling, plant care tracking, inventory management, and harvest distribution. This application aims to streamline garden operations, making it easier for volunteers and administrators to collaborate effectively.

### Key Features
- **Volunteer Management**: Store and access volunteer information (e.g., name, specialization).
- **Schedule Management**: Organize and assign tasks (e.g., planting, watering, pruning, harvesting).
- **Plant Care Tracking**: Monitor crop status based on environmental factors and volunteer logs.
- **Inventory Management**: Track gardening tools, seeds, compost, and other resources.
- **Harvest Distribution**: Efficiently divide harvested crops among beneficiaries.

> [!CAUTION] 
> **Note,** currently, the program ONLY includes a **Login System** that authenticates users and displays basic volunteer information upon successful login, AND a simple plant management system.

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

## Plant Management Functionality

The plant management can be accessed by both volunteers and admins.

- **Update Plant Health:**
  - Volunteers and administrators can update the health status of plants.
  - Health statuses include options like "Healthy," "Needs Water," "Pests Detected," and "Ready for Harvest."
- **Add New Plants:**
Volunteers can add new plants to the system with essential details including:
  - Plant name
  - Plant type (e.g., fruit, vegetable, flower, herb)
  - Planting date
  - Estimated harvest date
  - Location
  - Initial health status
- **Log Volunteer Observations:**
Volunteers can record observations about plant conditions.
  - Observations are stored with timestamps for tracking changes and monitoring progress.

---

## How to Run the Program on Ubuntu WSL

Follow these steps to set up and run the Gardenia login system on Ubuntu WSL.

### Prerequisites

1. **Ubuntu WSL**: Ensure you have Ubuntu installed on Windows Subsystem for Linux (WSL).
2. **Packages**: Install Essential Packages on your Ubuntu terminal:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   sudo apt install python3-venv
   sudo apt install git
   sudo apt install mpv
   ```
3. **Check Ubuntu Version**: Open the terminal. Check your Ubuntu Version:
   ```bash
    lsb_release -a
   ```
    **For Ubuntu 24.04**:
    - Install the following additional packages:
      ``` bash
      sudo apt install libmpv-dev libmpv2
      sudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so /usr/lib/libmpv.so.1
      ```
   
### Running the Program
1. Create a suitable directory for cloning the repository. Afterwards, clone the Gardenia Repository. In the Ubuntu Terminal, type the following:
   ```bash
   mkdir GardeniaProject
   cd GardeniaProject
   git clone https://github.com/Rekeii/gardenia.git
   ```
2. Navigate to the Cloned Repository. 
   ```bash
   cd gardenia
   ```
3. Create and Activate a Virtual Environment.
   ```bash
   python3 - m venv GardeniaProject
   source GardeniaProject/bin/activate
   ```
4. Install the dependencies, pymongo and flet within the actviated Virtual Environment.
   ```bash
   pip install pymongo flet
   ```
5. Start the application:
   ```bash
   python3 main.py
   ```
6. Use the following credentials to test the login:
  - username: Mikz
  - password: 1234
7. After successful login, the application will display the volunteer's name and specialization.

Expected output:
Welcome, Mikz Lugtu!
Specialization: Floriculture


> [!NOTE] For admin:
> username: admin
> password: admin



---

## Roadmap of functions:
- Implement admin and volunteer roles with distinct functionalities.
- Add additional features like task scheduling, inventory management, and harvest distribution.
