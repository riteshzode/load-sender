import os
import time
import requests
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

# Load environment variables from .env file
load_dotenv()

# Get the ALB URL from the environment variables
alb_dns_name = os.getenv("URL")

if not alb_dns_name:
    print("ALB URL not found in the environment variables.")
    exit(1)

# Number of requests to send
num_requests = 100000

# Function to send a single request
def send_request(index):
    try:
        response = requests.get(alb_dns_name)
        print(f"Request {index}: Status Code = {response.status_code}")
    except requests.RequestException as e:
        print(f"Request {index}: Failed with error - {e}")

# Function to create and start threads using ThreadPoolExecutor
def main():
    index = 1

    # Create a ThreadPoolExecutor to manage concurrent requests
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        
        # Submit tasks to the executor for the desired number of requests
        for i in range(1, num_requests + 1):
            future = executor.submit(send_request, index)
            futures.append(future)
            index += 1

        # Wait for all futures to complete
        for future in futures:
            future.result()  # This will raise exceptions if any task fails

if __name__ == "__main__":
    main()
