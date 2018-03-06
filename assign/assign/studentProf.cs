using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace assign
{
    class studentProf
    {
        public string ID()
        {
            string a="".PadRight(5);
            Console.WriteLine("Entr student Id");
            a = Console.ReadLine();
            
            return a;

        }
        public string name()
        {
            string a = "".PadRight(15);
            Console.WriteLine("Entr student Name");
            a = Console.ReadLine();
            string x = a.ToLower();
            return x;
        }
        public string cgpa()
        {
            string a = "".PadRight(4);
            Console.WriteLine("Entr student CGPA, CGPA should between 0-4");
            a = Console.ReadLine();
            return a;
        }
        public string semester()

        {
            string a = "".PadRight(3);
            Console.WriteLine("Entr student Semester");
            a = Console.ReadLine();
            return a;
        }

        public string dept()
        {
            string a = "".PadRight(10);
            Console.WriteLine("Entr student Department");
            a = Console.ReadLine();
            return a;
        }
        public string uni()
        {
            string a = "".PadRight(15);
            Console.WriteLine("Entr student University");
            a = Console.ReadLine();
            return a;
        }

    }
}
