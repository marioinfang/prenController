# PREN Controller

# How to Start the project

## Prerequisites

Before starting the project, make sure you have the following installed:

- **Python** (Recommended: 3.9+)

## 1. Create Virtual Environment 
```sh
python -m venv venv
source venv/bin/activate #macos
venv\Scripts\activate  # Windows

```
## 2. Install dependencies
```sh
pip install -r requirements.txt
```
## 3. Run tests
```sh
 python -m unittest tests.<your_test_file>
(e.g python -m unittest tests.test_uart_handler)
```

## 3. RPi Setup
```sh
sudo apt-get update
sudo apt-get upgrade
sudo apt install python3-gpiozero
```