using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace vpAssign2
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button6_Click(object sender, EventArgs e)
        {
            this.Hide();
            Top_3_of_Class obj = new Top_3_of_Class();
            obj.Show();
            
        }

        private void button4_Click(object sender, EventArgs e)
        {
            this.Hide();
            View_Attendance obj = new View_Attendance();
            obj.Show();

        }

        private void addStudent_Click(object sender, EventArgs e)
        {
            this.Hide();
            addStudent obj = new addStudent();
            obj.Show();
           
        }

        private void searchStudent_Click(object sender, EventArgs e)
        {
            this.Hide();
            Search_Student obj = new Search_Student();
            obj.Show();
        }

        private void markAttend_Click(object sender, EventArgs e)
        {
            this.Hide();
            Mark_Student_Attendance obj = new Mark_Student_Attendance();
            obj.Show();
        }

        private void deleteStudent_Click(object sender, EventArgs e)
        {
            this.Hide();
            Delete_Student obj = new Delete_Student();
            obj.Show();
        }
    }
}
