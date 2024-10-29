# Banking System with Concurrency Control

A simple banking system implementation in Python using SQLite with optimistic concurrency control to handle concurrent transactions.

## Features

- Account creation and management
- Secure fund transfers between accounts
- Concurrency control using version numbers
- Transaction rollback on conflicts
- Simulation of concurrent updates for testing

## Prerequisites

- Python 3.x
- SQLite3 (included in Python standard library)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/banking-system.git
cd banking-system
```

2. No additional package installation is required as the project uses only standard library modules.

## Usage

Run the application:
```bash
python bank.py
```

The program will:
1. Create a new database with sample accounts
2. Perform test transfers
3. Demonstrate concurrency handling

## Sample Operations

The system demonstrates several transfer scenarios:
- Normal transfer between accounts
- Transfer with insufficient funds
- Transfer to/from non-existent accounts
- Transfer with concurrent updates

## Technical Implementation

- Uses SQLite for data persistence
- Implements optimistic concurrency control using version numbers
- Automatic rollback on concurrent update conflicts
- Transaction isolation using SQLite's built-in transaction support

## Security Note

This is a demonstration project. For production use, consider:
- Adding proper authentication
- Implementing secure password handling
- Using environment variables for sensitive data
- Adding comprehensive error handling
- Implementing logging
