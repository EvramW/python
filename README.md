# Odoo Auto Reconciliation

Odoo Auto Reconciliation is a Python application that automates the process of reconciling invoices in Odoo. This tool logs into Odoo, navigates through invoices, and performs reconciliation actions based on specified criteria.

## Features

- Automatic login to Odoo using provided credentials
- Navigation through invoices
- Automatic clicking of buttons to reconcile invoices
- Retry mechanism with user prompts for error handling
- Error notification through beeps
- User-friendly GUI built with Tkinter
- Credential saving and loading from a JSON file

## Requirements

- Python 3.7 or higher
- `selenium` library
- `webdriver-manager` library
- `tkinter` library (usually included with Python)
- `json` library (included with Python)
- `winsound` library (included with Python on Windows)

## Installation

1. Clone the repository:

```sh
git clone https://github.com/yourusername/odoo-auto-reconciliation.git
cd odoo-auto-reconciliation
```

2. Install the required Python libraries:

```sh
pip install selenium webdriver-manager
```

## Usage

1. Run the `odoo_auto_reconciliation.py` script:

```sh
python odoo_auto_reconciliation.py
```

2. Fill in the Username, Password, Max Clicks, and URL fields in the GUI.
3. Click the "Login" button to start the process.
4. Follow the instructions provided in the "Instructions" menu.

## Error Handling

If an error occurs during the process:

- The application will retry the action up to three times with a 10-second pause between retries.
- If the maximum number of retries is reached, a message box will prompt you to either retry the login or stop the process.
- A beep sound will notify you of each error.

## GUI Elements

- **Username**: Your Odoo username
- **Password**: Your Odoo password
- **Max Clicks**: Maximum number of clicks for navigation (default is 80)
- **URL**: The URL of your Odoo instance
- **Login Button**: Starts the login and reconciliation process
- **Log Text**: Displays the log output

## Instructions

Detailed instructions are available in the "Instructions" menu within the application.

## About Us

We are a team dedicated to developing software solutions to streamline business processes. For more information, check the "About Us" menu within the application.

Design by Evram Wadeeh
- Phone: +201007899697
- Email: acc.evram@gmail.com

## License

This project is licensed under the MIT License.
```

You can save this content into a `README.md` file in your project directory. It provides an overview of the project, installation steps, usage instructions, and other relevant information.
