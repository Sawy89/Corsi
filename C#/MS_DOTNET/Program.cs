using System;
using System.Collections.Generic;


namespace prova_cs
{
    class Program
    {
        static void Main(string[] args)
        {
            // Prima parte
            // Program.Stringhe();

            // Numeri
            // Program.Numeri();

            // branches
            // Program.Branches();

            // List & index
            // Program.ListAndIndex();

            // Prova Banca
            // Program.BankMain();

            // Prova Hash
            // Program.provaPassword();
            
            // Prova Double Costructor
            Program.provaDoubleConstructor();

        }

        public static void Stringhe()
        {
            var c1 = new MyClass();
            string Hello = "    Hello World!";
            Hello = Hello.Replace("Hello","Good morning");
            Console.WriteLine($"{Hello.TrimStart().ToUpper()} {c1.ReturnMessage()}");
            Console.WriteLine(value: $"La variabile Hello ha {Hello.Length} caratteri, la variabile dopo ne ha {c1.ReturnMessage().Length}");
            System.Console.WriteLine(Hello.Contains("Good"));
        }

        public static void Numeri()
        {
            var c2 = 6;
            var c1 = new MyClass();
            System.Console.WriteLine($"Se sommo 5 a {c2} ottengo {c1.AddFive(c2)}");
            int a = 2;
            int b = 3;
            int c = 7;
            double d = (double) a * c / b;
            System.Console.WriteLine(d);

            // Nuova libreria
            double raggio = 3;
            double area = Math.Round(Math.PI * raggio * raggio,2);
            System.Console.WriteLine($"L'area di un cerchio con raggio {raggio} è {area}");
        }


        public static void Branches()
        {
            // Prova IF
            System.Console.WriteLine("Prova IF");
            string nome1 = "Denny";
            string nome2 = "denny";
            if (nome1.ToLower() == nome2.ToLower())
            {
                System.Console.WriteLine("Sono uguali");
            }
            else
                System.Console.WriteLine($"{nome1} e {nome2} sono diversi");
            
            // Prova WHILE
            System.Console.WriteLine("While Loop");
            int counter = 0;
            while (counter < 5)
            {
                System.Console.WriteLine($"Il contatore dice {counter}");
                counter++;
            }
            do
            {
                System.Console.WriteLine($"Il contatore dice {counter}");
                counter--;
            } while (counter>0);

            // Prova FOR
            System.Console.WriteLine("For Loop");
            for (int ind = 0; ind < 10; ind++)
            {
                System.Console.WriteLine($"Il contatore FOR dice {ind}");
            }

            // Prova FOREACH
            System.Console.WriteLine("Foreach loop");
            var ages = new List<int> {32, 33, 37}; // crea una lista di interi!
            ages.Add(12);
            ages.Remove(33);
            foreach (var age in ages)
            {
                System.Console.WriteLine($"L'età è {age} rispetto al primo {ages[0]}");
            }   
        }

        public static void ListAndIndex()
        {
            // Index nella lista
            var names = new List<string> {"Denny","Tullio","Luca"};
            names.Add("Daniele");
            foreach (var name in names)
            {
                System.Console.WriteLine(name);
            }
            if (names.Contains("Denny"))
            {
                System.Console.WriteLine("Denny c'è!");
            }
            int index = names.IndexOf("Danielee");
            System.Console.WriteLine($"Daniele c'è in posizione {index}");

            // Sort
            System.Console.WriteLine("Riorganizzo la lista");
            names.Sort();
            foreach (var name in names)
            {
                System.Console.WriteLine(name);
            }
            var numeri = new List<int> {2,5,1,4,2};
            
            System.Console.WriteLine("\nLista di numeri DA ORDINARE");
            foreach (var num in numeri)
            {
                System.Console.WriteLine(num);
            }
            System.Console.WriteLine("Lista di numeri ORDINATA!");
            numeri.Sort();
            foreach (var num in numeri)
            {
                System.Console.WriteLine(num);
            }

            // Fibonacci
            var fibonacciNumeri = new List<int> {1,1};

            for (int i = 0; i < 10; i++)
            {
                var prec1 = fibonacciNumeri[fibonacciNumeri.Count - 1];
                var prec2 = fibonacciNumeri[fibonacciNumeri.Count - 2];
                fibonacciNumeri.Add(prec1 + prec2);
            }
            System.Console.WriteLine("\nEcco la lista di Fibonacci");
            foreach (var num in fibonacciNumeri)
            {
                System.Console.WriteLine(num);
            }
        }

        public static void BankMain()
        {
            {
                var account = new BankAccount("Giavarra",1);
                account.MakeDeposit(100, DateTime.Now, "Primo caricamento");
                account.MakeWithdrawal(20, DateTime.Now, "Bolletta Eviso");

                var account2 = new BankAccount("Denny",100);
                account2.MakeDeposit(1002, DateTime.Now, "Primo Caricamento");

                System.Console.WriteLine($"Account {account.Number} was created for {account.Owner} with {account.Balance}€.");
                System.Console.WriteLine($"Account {account2.Number} was created for {account2.Owner} with {account2.Balance}€.");

                System.Console.WriteLine(account.getAccountHistory());
                System.Console.WriteLine(account2.getAccountHistory());
            }
        }

        public static void provaPassword()
        {
            // prova a creare l'hash di una password
            var password = "mettiquilatuapassword";
            var passwordHased = HashPass.hash(password);
            System.Console.WriteLine(passwordHased);
        }

        public static void provaDoubleConstructor()
        {
            var a = new DoubleCostructor("Prova con due input", "Ecco il secondo input");
            var b = new DoubleCostructor("Prova con un solo input");
        }
    }

}