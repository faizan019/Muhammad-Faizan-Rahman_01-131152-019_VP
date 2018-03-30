namespace vpAssign2
{
    partial class Form1
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
            this.addStudent = new System.Windows.Forms.Button();
            this.searchStudent = new System.Windows.Forms.Button();
            this.deleteStudent = new System.Windows.Forms.Button();
            this.viewAtrend = new System.Windows.Forms.Button();
            this.markAttend = new System.Windows.Forms.Button();
            this.top3 = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // addStudent
            // 
            this.addStudent.Location = new System.Drawing.Point(43, 50);
            this.addStudent.Name = "addStudent";
            this.addStudent.Size = new System.Drawing.Size(108, 44);
            this.addStudent.TabIndex = 0;
            this.addStudent.Text = "Add Student";
            this.addStudent.UseVisualStyleBackColor = true;
            this.addStudent.Click += new System.EventHandler(this.addStudent_Click);
            // 
            // searchStudent
            // 
            this.searchStudent.Location = new System.Drawing.Point(43, 119);
            this.searchStudent.Name = "searchStudent";
            this.searchStudent.Size = new System.Drawing.Size(108, 43);
            this.searchStudent.TabIndex = 1;
            this.searchStudent.Text = "Search Student";
            this.searchStudent.UseVisualStyleBackColor = true;
            this.searchStudent.Click += new System.EventHandler(this.searchStudent_Click);
            // 
            // deleteStudent
            // 
            this.deleteStudent.Location = new System.Drawing.Point(43, 201);
            this.deleteStudent.Name = "deleteStudent";
            this.deleteStudent.Size = new System.Drawing.Size(108, 39);
            this.deleteStudent.TabIndex = 2;
            this.deleteStudent.Text = "Delete Student";
            this.deleteStudent.UseVisualStyleBackColor = true;
            this.deleteStudent.Click += new System.EventHandler(this.deleteStudent_Click);
            // 
            // viewAtrend
            // 
            this.viewAtrend.Location = new System.Drawing.Point(284, 201);
            this.viewAtrend.Name = "viewAtrend";
            this.viewAtrend.Size = new System.Drawing.Size(103, 39);
            this.viewAtrend.TabIndex = 5;
            this.viewAtrend.Text = "View Attendance";
            this.viewAtrend.UseVisualStyleBackColor = true;
            this.viewAtrend.Click += new System.EventHandler(this.button4_Click);
            // 
            // markAttend
            // 
            this.markAttend.Location = new System.Drawing.Point(284, 119);
            this.markAttend.Name = "markAttend";
            this.markAttend.Size = new System.Drawing.Size(103, 43);
            this.markAttend.TabIndex = 4;
            this.markAttend.Text = "Mark Attendance";
            this.markAttend.UseVisualStyleBackColor = true;
            this.markAttend.Click += new System.EventHandler(this.markAttend_Click);
            // 
            // top3
            // 
            this.top3.Location = new System.Drawing.Point(284, 50);
            this.top3.Name = "top3";
            this.top3.Size = new System.Drawing.Size(103, 44);
            this.top3.TabIndex = 3;
            this.top3.Text = "Top 3 of class";
            this.top3.UseVisualStyleBackColor = true;
            this.top3.Click += new System.EventHandler(this.button6_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(469, 306);
            this.Controls.Add(this.viewAtrend);
            this.Controls.Add(this.markAttend);
            this.Controls.Add(this.top3);
            this.Controls.Add(this.deleteStudent);
            this.Controls.Add(this.searchStudent);
            this.Controls.Add(this.addStudent);
            this.Name = "Form1";
            this.Text = "Student Profile System";
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Button addStudent;
        private System.Windows.Forms.Button searchStudent;
        private System.Windows.Forms.Button deleteStudent;
        private System.Windows.Forms.Button viewAtrend;
        private System.Windows.Forms.Button markAttend;
        private System.Windows.Forms.Button top3;
    }
}

