using System;
using System.Collections.Generic;
using System.Text;

namespace prova_cs
{
    public class MyClass
    {
        public string ReturnMessage()
        {
            return "Happy coding!";
        }

        public int AddFive(int numberInput)
        {
            return numberInput + 5;
        }
    }

    public class BankAccount
    {
        public string Number { get; }
        public string Owner { get; set; }
        public decimal Balance 
        { 
            get
            {
                decimal balance = 0;
                foreach (var item in allTransactions)
                {
                    balance += item.Amount;
                }
                return balance;
            }
        }

        private static int accountNumberSeed = 1234567890;

        private List<Transaction> allTransactions = new List<Transaction>();

        public BankAccount(string name, decimal initialBalance)
        {
            this.Owner = name;
            MakeDeposit(initialBalance, DateTime.Now, "Initial Deposit");
            
            this.Number = accountNumberSeed.ToString();
            accountNumberSeed++;
        }

        public void MakeDeposit(decimal amount, DateTime date, string note)
        {
            if (amount <= 0)
            {
                throw new ArgumentOutOfRangeException(nameof(amount), "Amount of deposit must be positive");
            }
            var deposit = new Transaction(amount, date, note);
            allTransactions.Add(deposit);
        }

        public void MakeWithdrawal(decimal amount, DateTime date, string note)
        {
            if (amount <= 0)
            {
                throw new ArgumentOutOfRangeException(nameof(amount), "Amount of withdrawal must be positive");
            }
            if (Balance - amount < 0)
            {
                throw new InvalidOperationException("Not sufficient funds for this withdrawal");
            }
            var withdrawal = new Transaction(-amount, date, note);
            allTransactions.Add(withdrawal);
        }

        public string getAccountHistory()
        {
            var report = new StringBuilder();
            // Header
            report.AppendLine("Date\t\tAmount\t\tNote");
            foreach (var item in allTransactions)
            {
                // Rows
                report.AppendLine($"{item.Date.ToShortDateString()}\t{item.Amount}\t\t{item.Notes}");
            }
            return report.ToString();
        }
    }

    public class Transaction
    {
        public decimal Amount {get;}
        public DateTime Date {get;}
        public string Notes {get;}

        public Transaction(decimal amount, DateTime date, string note)
        {
            this.Amount = amount;
            this.Date = date;
            this.Notes = note;
        }
    }
}