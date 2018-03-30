namespace vpAssign2
{
    partial class addStudent
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.sID = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.sName = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.sSemester = new System.Windows.Forms.TextBox();
            this.label4 = new System.Windows.Forms.Label();
            this.cgpa = new System.Windows.Forms.TextBox();
            this.label5 = new System.Windows.Forms.Label();
            this.sDept = new System.Windows.Forms.TextBox();
            this.label6 = new System.Windows.Forms.Label();
            this.sUni = new System.Windows.Forms.TextBox();
            this.Submit = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // sID
            // 
            this.sID.Location = new System.Drawing.Point(241, 35);
            this.sID.Name = "sID";
            this.sID.Size = new System.Drawing.Size(100, 20);
            this.sID.TabIndex = 0;
            this.sID.TextChanged += new System.EventHandler(this.textBox1_TextChanged);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(80, 42);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(58, 13);
            this.label1.TabIndex = 1;
            this.label1.Text = "Student ID";
            this.label1.Click += new System.EventHandler(this.label1_Click);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(80, 90);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(75, 13);
            this.label2.TabIndex = 3;
            this.label2.Text = "Student Name";
            // 
            // sName
            // 
            this.sName.Location = new System.Drawing.Point(241, 83);
            this.sName.Name = "sName";
            this.sName.Size = new System.Drawing.Size(100, 20);
            this.sName.TabIndex = 2;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(80, 138);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(91, 13);
            this.label3.TabIndex = 5;
            this.label3.Text = "Student Semester";
            // 
            // sSemester
            // 
            this.sSemester.Location = new System.Drawing.Point(241, 131);
            this.sSemester.Name = "sSemester";
            this.sSemester.Size = new System.Drawing.Size(100, 20);
            this.sSemester.TabIndex = 4;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(80, 185);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(36, 13);
            this.label4.TabIndex = 7;
            this.label4.Text = "CGPA";
            // 
            // cgpa
            // 
            this.cgpa.Location = new System.Drawing.Point(241, 182);
            this.cgpa.Name = "cgpa";
            this.cgpa.Size = new System.Drawing.Size(100, 20);
            this.cgpa.TabIndex = 6;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(80, 232);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(62, 13);
            this.label5.TabIndex = 9;
            this.label5.Text = "Department";
            // 
            // sDept
            // 
            this.sDept.Location = new System.Drawing.Point(241, 225);
            this.sDept.Name = "sDept";
            this.sDept.Size = new System.Drawing.Size(100, 20);
            this.sDept.TabIndex = 8;
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(80, 275);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(53, 13);
            this.label6.TabIndex = 11;
            this.label6.Text = "University";
            // 
            // sUni
            // 
            this.sUni.Location = new System.Drawing.Point(241, 268);
            this.sUni.Name = "sUni";
            this.sUni.Size = new System.Drawing.Size(100, 20);
            this.sUni.TabIndex = 10;
            // 
            // Submit
            // 
            this.Submit.Location = new System.Drawing.Point(164, 308);
            this.Submit.Name = "Submit";
            this.Submit.Size = new System.Drawing.Size(75, 23);
            this.Submit.TabIndex = 12;
            this.Submit.Text = "Submit";
            this.Submit.UseVisualStyleBackColor = true;
            this.Submit.Click += new System.EventHandler(this.button1_Click);
            // 
            // addStudent
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(455, 343);
            this.Controls.Add(this.Submit);
            this.Controls.Add(this.label6);
            this.Controls.Add(this.sUni);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.sDept);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.cgpa);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.sSemester);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.sName);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.sID);
            this.Name = "addStudent";
            this.Text = "Add Student";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox sID;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox sName;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox sSemester;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.TextBox cgpa;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.TextBox sDept;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.TextBox sUni;
        private System.Windows.Forms.Button Submit;

    }
}