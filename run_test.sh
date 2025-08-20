#!/bin/bash

# Script to run the test suite for the Soul Foods dashboard
# Returns exit code 0 if all tests pass, 1 if any test fails

# Function to display error messages
print_error() {
    echo -e "\033[0;31m$1\033[0m"
}

# Function to display success messages
print_success() {
    echo -e "\033[0;32m$1\033[0m"
}

# Navigate to the script directory (useful if running from elsewhere)
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "env" ]; then
    print_error "Virtual environment not found. Please set up your virtual environment first."
    exit 1
fi

# Activate the virtual environment
echo "Activating virtual environment..."
if [ -f "env/Scripts/activate" ]; then
    # Windows
    source env/Scripts/activate
else
    # Unix-like systems
    source env/bin/activate
fi

# Check if activation was successful
if [ $? -ne 0 ]; then
    print_error "Failed to activate virtual environment."
    exit 1
fi

echo "Running test suite..."

# Run the tests using pytest
python -m pytest test.py -v

# Capture the exit code of the test run
TEST_RESULT=$?

# Check the test result
if [ $TEST_RESULT -eq 0 ]; then
    print_success "All tests passed!"
    exit 0
else
    print_error "Some tests failed."
    exit 1
fi