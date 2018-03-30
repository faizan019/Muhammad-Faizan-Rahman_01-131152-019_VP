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
    public partial class Search_Student : Form
    {
        public Search_Student()
        {
            InitializeComponent();
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            this.Hide();
            searchByid obj = new searchByid();
            obj.Show();

        }

        private void button3_Click(object sender, EventArgs e)
        {
            this.Hide();
            Search_By_Semester obj = new Search_By_Semester();
            obj.Show();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            this.Hide();
            searchByName obj = new searchByName();
            obj.Show();
        }
    }
}
