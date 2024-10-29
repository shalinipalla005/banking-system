import sqlite3

DB_FILE = "bank.db"
def create_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS accounts;')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        account_id INTEGER PRIMARY KEY,
        account_holder TEXT,
        balance REAL,
        version INTEGER DEFAULT 0
    )
    ''')

    cursor.execute("INSERT OR IGNORE INTO accounts (account_id, account_holder, balance) VALUES (?, ?, ?)", (1, 'Alice', 1000.0))
    cursor.execute("INSERT OR IGNORE INTO accounts (account_id, account_holder, balance) VALUES (?, ?, ?)", (2, 'Bob', 500.0))
    
    conn.commit()
    conn.close()

def fetch_from_account(conn, account_id):
    cursor = conn.cursor()
    cursor.execute("SELECT balance, version FROM accounts WHERE account_id = ?", (account_id,))
    account = cursor.fetchone()
    return account

def update_balance(conn, account_id, amount, version):
    cursor = conn.cursor()
    cursor.execute("""
                    UPDATE accounts 
                    SET balance = balance + ?, version = version + 1 
                    WHERE account_id = ? AND version = ?
    """, (amount, account_id, version))

    if cursor.rowcount == 0:
        raise ValueError("Concurrency conflict: Account was modified by another transaction.")
    
    print(f"Updated balance in account {account_id} with amount {amount}.")


def transfer_funds(src_account_id, dst_account_id, amount, 
                   test_for_concurrent=False):
    print(f"\nStarting transfer of {amount}/- from a/c {src_account_id} to {dst_account_id}")
    print("Balances before transfer:")
    show_balances()
    conn = sqlite3.connect(DB_FILE)
    try:
        src_account = fetch_from_account(conn, src_account_id)
        dst_account = fetch_from_account(conn, dst_account_id)

        if src_account is None or dst_account is None:
            print("One of the accounts does not exist. Transfer aborted!")
            conn.close()
            return

        src_balance, src_version = src_account
        _, dst_version = dst_account

        if src_balance < amount:
            print(f"A/c {src_account_id} has only {src_balance}/-. Transfer aborted due to insufficient funds!")
            conn.close()
            return
        update_balance(conn, src_account_id, -amount, src_version)  
        if test_for_concurrent:
            simulate_concurrent_account_update(conn, dst_account_id)
        update_balance(conn, dst_account_id, amount, dst_version)
        conn.commit()
        print("Tranfer successful!")

    except Exception as e:
        conn.rollback()
        print(f"Transfer failed: {e}")
    finally:
        conn.close()
        print("\nFinal balances:")
        show_balances()
        print("==============================")

def simulate_concurrent_account_update(conn, dst_account_id):
    print(f">>> Simulating concurrent update to a/c {dst_account_id}")
    try:
        cursor = conn.cursor()
        cursor.execute("""
                        UPDATE accounts SET balance = balance + 100, 
                        version = version + 1 WHERE account_id = ?
                        """, (dst_account_id,))
        print("... done.")
    except Exception as ex:
        print(f"Concurrent update failed: {ex}")


def main():
    create_database() 
    transfer_funds(1, 2, 50) 
    transfer_funds(3, 2, 50)
    transfer_funds(1, 2, 9999) 
    transfer_funds(1, 2, 150, True) 


def show_balances():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts")
    accounts = cursor.fetchall()
    for account in accounts:
        print(f"Account ID: {account[0]}, Holder: {account[1]}, Balance: {account[2]}, Version: {account[3]}")
    conn.close()

if __name__ == "__main__":
    main()