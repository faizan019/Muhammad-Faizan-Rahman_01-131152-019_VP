using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace assign
{
    class Program
    {
        static void Main(string[] args)
        {
            
            string path = args[0];
            string choice = null;
            string opt, info;
            Console.WriteLine("press 1 to creat ID\n Press 2 to Search Student\n Press 3 to delete Student Record\n Press 4 to List top3 Students\n Press 5 to mark attendance\n Press 6 to view Attendance ");
            choice= Console.ReadLine();
            studentProf obj = new studentProf();
            retrieveData obj1 = new retrieveData();
            deleteSt obj2 = new deleteSt();

            FileStream fileW = new FileStream(path, FileMode.Append, FileAccess.Write, FileShare.Read); 
            StreamWriter sw = new StreamWriter(fileW);

            FileStream fileR = new FileStream(path, FileMode.Open, FileAccess.Read, FileShare.ReadWrite);             
            StreamReader sr = new StreamReader(fileR);
            sw.AutoFlush = true;

            if(choice=="1")
            {
                do
                {
                    sw.WriteLine(obj.ID() + "   " + obj.name() + "   " + obj.cgpa() + "   " + obj.semester() + "   " + obj.dept() + "   " + obj.uni());
                    //sw.WriteLine(obj.ID());
                    //sw.WriteLine(obj.name());
                    //sw.WriteLine(obj.cgpa());
                    //sw.WriteLine(obj.semester());
                    //sw.WriteLine(obj.dept());
                    //sw.WriteLine(obj.uni());

                    Console.WriteLine("Do u want to create another student profile \nPress Y for Yes \nPress N for NO  ");
                    opt = Console.ReadLine();
                } while (opt == "y" || opt == "Y");
            }


            else if(choice=="2")
            {
                Console.WriteLine("press 1 to search by ID\n Press 2 to Search by Name\n Press 3 to search By Semester\n");
                 choice = Console.ReadLine();
                if(choice=="1")
                {
                    Console.WriteLine("Enter ID to Search student");
                    info = Console.ReadLine();
                    obj1.id(sr, info);

                }
                else if (choice=="2")
                {
                    Console.WriteLine("Enter Name to Search student");
                    info = Console.ReadLine();
                    string information = info.ToLower();

                    obj1.name(sr, information);

                }
                else if (choice == "3")
                {
                    Console.WriteLine("Enter Semester to Search student");
                    info = Console.ReadLine();
                    obj1.semester(sr, info);


                }
                else { };

            }
            else if (choice =="3")
            {
                sw.Close();
                Console.WriteLine("Enter ID to delete");
                info = Console.ReadLine();
                obj2.delete(path, info);
            }

        }
    }
}
