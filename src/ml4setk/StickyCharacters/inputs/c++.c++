#include <iostream>
#include <string>
#include <stdexcept>

class BankAccount {
private:
    std::string ownerName;
    double balance;

public:
    BankAccount(std::string name, double initialBalance) {
        ownerName = name;
        if (initialBalance < 0) {
            balance = 0;
        } else {
            balance = initialBalance;
        }
    }

    void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            std::cout << "Deposit of " << amount << " successful." << std::endl;
        } else {
            std::cout << "Deposit amount must be positive." << std::endl;
        }
    }

    void withdraw(double amount) {
        if (amount > balance) {
            throw std::runtime_error("Insufficient balance, cannot withdraw.");
        } else if (amount <= 0) {
            throw std::invalid_argument("Withdrawal amount must be positive.");
        } else {
            balance -= amount;
            std::cout << "Withdrawal of " << amount << " successful." << std::endl;
        }
    }

    void displayBalance() const {
        std::cout << "Account: " << ownerName << ", Current balance: " << balance << std::endl;
    }
};

int main() {
    BankAccount myAccount("John", 500.0);
    myAccount.displayBalance();

    myAccount.deposit(150.0);
    myAccount.displayBalance();

    try {
        myAccount.withdraw(200.0);
        myAccount.displayBalance();
        myAccount.withdraw(1000.0);

    } catch (const std::runtime_error& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        myAccount.displayBalance();
    } catch (const std::invalid_argument& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }

    return 0;
}