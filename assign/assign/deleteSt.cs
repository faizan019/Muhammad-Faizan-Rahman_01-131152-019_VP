using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace assign
{
    class deleteSt
    {
        public void delete(string path, string id)
        {
            string [] line = File.ReadAllLines(path);
            string [] student=new  string[line.Length-1];
            int count = 0; 
            for(int i=0; i<line.Length; i++)
            {
                
                string subSt = line[i].Substring(0, 5);
                string refineSt = subSt.Trim();
                
                if (refineSt == id)
                {
                    i = i + 1;
                }
                
                student[count] = line[i];
                count++;
            }
            
            File.WriteAllLines(path,student);
           
            }
        }
    }
