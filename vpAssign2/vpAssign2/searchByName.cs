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
    public partial class searchByName : Form
    {
        public searchByName()
        {
            InitializeComponent();
        }

        private void searchByName_Load(object sender, EventArgs e)
        {

        }

        private void Submit_Click(object sender, EventArgs e)
        {
            string path = @"textFile.txt";
            using (StreamReader srObj = new StreamReader(path))
             {
                 string line = null;
                 
            while (!srObj.EndOfStream)
            {
                line = srObj.ReadLine();

                
                string subSt = line.Substring(13, 15);
                string refineSt = subSt.Trim();
                
                if (refineSt == Name_Box.Text)
                {
                    richTextBox1.Text=line; 
                    break;
                }


            
                         richTextBox1.Text = "Not Exist";
                    
                     
                 }
                 
                 Name_Box.ResetText();

             }

        
        }

        private void label6_Click(object sender, EventArgs e)
        {

        }

        private void label2_Click(object sender, EventArgs e)
        {

        }
    }
}
