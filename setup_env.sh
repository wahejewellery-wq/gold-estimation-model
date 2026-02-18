#!/bin/bash

# Define the virtual environment directory
VENV_DIR="venv"

# Check for python3.11
PYTHON_CMD="python3.11"
if ! command -v $PYTHON_CMD &> /dev/null; then
    # Try looking in typical brew locations
    if [ -f "/opt/homebrew/bin/python3.11" ]; then
        PYTHON_CMD="/opt/homebrew/bin/python3.11"
    elif [ -f "/usr/local/bin/python3.11" ]; then
        PYTHON_CMD="/usr/local/bin/python3.11"
    else
        echo "Error: python3.11 could not be found. Please install it using 'brew install python@3.11'"
        exit 1
    fi
fi

echo "Using Python: $PYTHON_CMD"
echo "Creating virtual environment in $VENV_DIR..."
$PYTHON_CMD -m venv $VENV_DIR

echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing requirements from requirements.txt..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "Error: requirements.txt not found."
    exit 1
fi

echo "Registering kernel with Jupyter..."
$VENV_DIR/bin/python -m ipykernel install --user --name=gold_estimation_env --display-name "Python (Gold Estimation)"

echo "----------------------------------------------------------------"
echo "Setup Complete!"
echo "To run your notebook with this environment:"
echo "1. Restart Jupyter Notebook if it's already running."
echo "2. Open 'estimation_nodel.ipynb'."
echo "3. In the Jupyter menu, go to Kernel -> Change Kernel -> Python (Gold Estimation)."
echo "4. Run the cells again."
echo "----------------------------------------------------------------"
