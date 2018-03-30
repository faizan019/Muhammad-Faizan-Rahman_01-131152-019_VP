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
    public partial class addStudent : Form
    {
        public addStudent()
        {
            InitializeComponent();
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            string ID=null;
            string name=null;
            string semester=null;
            string CGPA=null;
            string dept=null;
            string uni=null;
            
            using (StreamWriter sw = new StreamWriter("textFile.txt",true))
            {   

                for (int i = 0; i < (15 - sID.TextLength);i++ )
                {
                    ID += " ";
                }

                for (int i = 0; i < (15 - sName.TextLength); i++)
                {
                    name += " ";
                }

                for (int i = 0; i < (15 - sSemester.TextLength); i++)
                {
                    semester += " ";
                }

                for (int i = 0; i < (15 - cgpa.TextLength); i++)
                {
                    CGPA += " ";
                }

                for (int i = 0; i < (15 - sDept.TextLength); i++)
                {
                    dept += " ";
                }

                for (int i = 0; i < (15 - sUni.TextLength); i++)
                {
                    uni += " ";
                }
                sw.WriteLine(sID.Text + ID + sName.Text + name + sSemester.Text + semester + cgpa.Text + CGPA + sDept.Text + dept + sUni.Text +uni);
                
                //sw.WriteLine(sName.Text);
                //sw.WriteLine(sSemester.Text);
                //sw.WriteLine(cgpa.Text);
                //sw.WriteLine(sDept.Text);
                //sw.WriteLine(sUni.Text);

            }
            sID.ResetText();
            sName.ResetText();
            sSemester.ResetText();
            cgpa.ResetText();
            sDept.ResetText();
            sUni.ResetText();
            MessageBox.Show("Student Added");
        }
    }
}
