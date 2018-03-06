using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
namespace assign
{
    class retrieveData
    {

        public void id(StreamReader srObj, string str)
        {
            string line = null;
            while (!srObj.EndOfStream)
            {
                line = srObj.ReadLine();

               
                 string subSt = line.Substring(0,5);
                 string refineSt = subSt.Trim();
                if (refineSt == str)
                 {
                    Console.WriteLine("student record is:" + line);
                     Console.ReadKey();
                    break;
                 }
                 
                   
            }
        }

        public void name (StreamReader srObj, string str)
        {
            string line = null;
            while (!srObj.EndOfStream)
            {
                line = srObj.ReadLine();


                string subSt = line.Substring(4, 9);
                string refineSt = subSt.Trim();
                if (refineSt == str)
                {
                    Console.WriteLine("Student record is:" + line);
                    Console.ReadKey();
                    //break;
                }


            }
        }
        public void semester (StreamReader srObj, string str)
        {
            string line = null;
            while (!srObj.EndOfStream)
            {
                line = srObj.ReadLine();


                string subSt = line.Substring(20, 3);
                string refineSt = subSt.Trim();
                if (refineSt == str)
                {
                    Console.WriteLine("Student record is: " + line);
                    Console.ReadKey();
                    
                }


            }
        }
        }
        
        

    }
