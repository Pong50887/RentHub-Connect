import logging
import os
import platform
import signal
import subprocess
import time
from enum import Enum
from io import BytesIO

import boto3
from PIL import Image
from botocore.exceptions import ClientError
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from promptpay import qrcode
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from mysite import settings
from mysite.settings import ADMIN_USERNAME, ADMIN_PASSWORD
from renthub.models import RoomType

logger = logging.getLogger('renthub')


def get_s3_client():
    """Get S3 client for authentication to access S3 storage."""
    return boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )


s3_client = get_s3_client()
BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME


def generate_qr_code(price, room_number):
    """Generate Promptpay QR payment with fixed price."""
    try:
        logger.info(f"Generating QR code for room {room_number} with price {price}")
        phone_number = settings.PROMPTPAY_PHONE_NUMBER
        payload_with_amount = qrcode.generate_payload(phone_number, price)
        qr_code_path = f"media/qr_code_images/{room_number}.png"
        qrcode.to_file(payload_with_amount, qr_code_path)
        logger.info(f"QR code generated successfully for room {room_number}.")

        s3_client.upload_file(qr_code_path, BUCKET_NAME, f"qr_code_images/{room_number}.png")
        logger.info(f"QR code generated and uploaded successfully for room {room_number}.")
    except ClientError as e:
        logger.error(f"Failed to upload QR code to S3: {e}")
    except Exception as e:
        logger.error(f"Failed to generate QR code: {e}")


def delete_qr_code(room_number):
    """Delete the QR code file for a specific room after receipt submission."""
    qr_code_path = f"media/qr_code_images/{room_number}.png"

    if os.path.exists(qr_code_path):
        os.remove(qr_code_path)
        logger.info(f"QR code for room {room_number} deleted successfully.")
    else:
        logger.debug(f"QR code for room {room_number} not found.")

    s3_key = f"qr_code_images/{room_number}.png"
    try:
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=s3_key)
        logger.info(f"QR code for room {room_number} deleted from S3 successfully.")
    except ClientError as e:
        logger.error(f"Failed to delete QR code from S3: {e}")


class Status(Enum):
    """Status Enum to ensure a consistant status value across all implementation throughout the project."""

    approve = 'approve'
    reject = 'reject'
    wait = 'wait'

    def __str__(self):
        return self.value

    @classmethod
    def choices(cls):
        """Returns the choices as a list of tuples."""
        return [(status.name, status.value) for status in cls]


def get_rental_progress_data(status):
    """Return milestones information regarding rental request approval status."""
    milestones = [
        {"step": 1, "description": "Payment Slip", "status": "Pending", "symbol": ""},
        {"step": 2, "description": "Rent Approval", "status": "Pending", "symbol": ""},
    ]

    if status == str(Status.wait):
        milestones[0]["status"] = "Submitted"
        milestones[0]["symbol"] = "o"
    elif status == str(Status.approve):
        milestones[0]["status"] = "Submitted"
        milestones[0]["symbol"] = "o"

        milestones[1]["status"] = "Approved"
        milestones[1]["symbol"] = "o"

    elif status == str(Status.reject):
        milestones[0]["status"] = "Submitted"
        milestones[0]["symbol"] = "o"

        milestones[1]["status"] = "Rejected"
        milestones[1]["symbol"] = "x"

    return milestones


def get_room_images(room_type: RoomType):
    """Return list of room type's image urls"""
    image_url_list = []
    image_folder_path = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/room_images/{room_type.id}/'
    image_url_list.append(f"{image_folder_path}bedroom.jpg")
    image_url_list.append(f"{image_folder_path}bathroom.jpg")
    image_url_list.append(f"{image_folder_path}kitchen.jpg")
    return image_url_list


def start_django_server():
    """Start the Django server using the test database."""
    server_command = ['python3', 'manage.py', 'runserver', '127.0.0.1:8000']
    server_process = subprocess.Popen(server_command)
    time.sleep(5)
    return server_process


def stop_django_server(server_process):
    """Stop the Django development server."""
    server_process.terminate()


def log_in(driver, username, password):
    """Log in with username and password."""
    try:
        driver.get(f"{settings.BASE_URL}/accounts/login/?next=/")
        username_field = driver.find_element(By.XPATH, '//td//input[@name="username"]')
        password_field = driver.find_element(By.XPATH, '//td//input[@name="password"]')
        login_button = driver.find_element(By.XPATH, '//form//button[@type="submit"]')

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()

        WebDriverWait(driver, 10).until(EC.url_to_be(f"{settings.BASE_URL}{reverse('renthub:home')}"))

    except Exception as e:
        raise RuntimeError(f"An error occurred during login: {e}")


def kill_port():
    # Specify the port to check
    port = 8000

    try:
        if platform.system() == "Windows":
            # For Windows, use netstat to find the process
            result = subprocess.run(
                ["netstat", "-ano", "|", "findstr", f":{port}"],
                capture_output=True, text=True, shell=True
            )
            lines = result.stdout.splitlines()

            # Parse the output to get the PID (Process ID)
            if lines:
                pid = int(lines[0].split()[-1])  # Get the last column (PID)
                print(f"Terminating process on port {port} with PID {pid}")

                # Kill the process using taskkill
                subprocess.run(["taskkill", "/PID", str(pid), "/F"])
        else:
            # Find the process using the port
            result = subprocess.run(
                ["lsof", "-i", f":{port}"], capture_output=True, text=True
            )
            lines = result.stdout.splitlines()

            # Parse the output to get the PID (Process ID)
            if len(lines) > 1:  # First line is the header, skip it
                pid = int(lines[1].split()[1])  # Extract PID from the output
                print(f"Terminating process on port {port} with PID {pid}")

                # Kill the process
                os.kill(pid, signal.SIGTERM)
    except Exception as e:
        print(f"Failed to free port {port}: {e}")


def admin_login(browser):
    browser.get(f"{settings.BASE_URL}/admin/login/")
    browser.find_element(By.NAME, 'username').send_keys(ADMIN_USERNAME)
    browser.find_element(By.NAME, 'password').send_keys(ADMIN_PASSWORD)
    browser.find_element(By.XPATH, '//input[@type="submit"]').click()


def create_temp_image_file():
    """
    Creates a temporary image file to simulate an upload for testing.
    Returns a SimpleUploadedFile object that can be assigned to an ImageField.
    """
    # Create an image using Pillow
    temp_file = BytesIO()
    image = Image.new('RGB', (100, 100), color='blue')
    image.save(temp_file, format='PNG')
    temp_file.seek(0)  # Rewind the BytesIO object to the start

    # Wrap the BytesIO content in a SimpleUploadedFile, simulating a real file upload
    return SimpleUploadedFile('temp_image.png', temp_file.read(), content_type='image/png')


class Browser:
    """Provide access to an instance of a Selenium web driver."""

    @classmethod
    def get_browser(cls):
        """Class method to initialize a headless Chrome WebDriver."""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        return driver

    @classmethod
    def get_logged_in_browser(cls, username, password):
        """Class method to initialize a headless driver and log in."""
        driver = cls.get_browser()
        log_in(driver, username, password)
        return driver


def checksum_thai_national_id(value):
    """Validate the checksum of a Thai National ID."""
    if len(value) != 13 or not value.isdigit():
        raise ValidationError("Thai National ID must be exactly 13 digits.")

    # Calculate checksum
    weights = range(13, 1, -1)  # Weights from 13 down to 2
    checksum = sum(int(value[i]) * weights[i] for i in range(12)) % 11
    checksum = (11 - checksum) % 10  # Adjust checksum: if 10 -> 0, if 11 -> 1

    # Compare with the last digit
    if checksum != int(value[12]):
        raise ValidationError("Invalid Thai National ID checksum.")
