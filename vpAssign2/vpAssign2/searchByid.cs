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
    public partial class searchByid : Form
    {
        public searchByid()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            string path = @"textFile.txt";
            using (StreamReader srObj = new StreamReader(path))
             {
                 string line = null;
                 ///string str;
                 while (!srObj.EndOfStream)
                 {
                     line = srObj.ReadLine();


                     string subSt = line.Substring(0, 15);
                     string refineSt = subSt.Trim();
                     //richTextBox1.Text = line;
                     if (refineSt == id_Box.Text)
                     {
                         richTextBox1.Text = line;
                         break;
                     }
                     else
                         richTextBox1.Text = "Not Exist";
                    
                     
                 }
                 id_Box.ResetText();

             }

        }

        private void listView1_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void label7_Click(object sender, EventArgs e)
        {

        }
    }        
    
}