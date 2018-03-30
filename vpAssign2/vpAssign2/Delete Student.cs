using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;

namespace vpAssign2
{
    public partial class Delete_Student : Form
    {
        public Delete_Student()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            string path = @"textFile.txt";
            string id=deleteID.Text;

            
                string[] line = File.ReadAllLines(path);
                string[] student = new string[line.Length - 1];
                int count = 0;
                for (int i = 0; i < line.Length; i++)
                {

                    string subSt = line[i].Substring(0, 3);
                    string refineSt = subSt.Trim();
                    ///MessageBox.Show(Convert.ToString( count));
                    

                    if (refineSt == id)
                    {
                        
                        i = i + 1;
                        
                    }

                    student[count] = line[i];
                    count++;
                }

                File.WriteAllLines(path, student);
                MessageBox.Show("Student Deleted");
                deleteID.ResetText();

           

            
        }

        private void deleteID_TextChanged(object sender, EventArgs e)
        {

        }
    }
}
