
namespace WindowsFormsApp1
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
            this.X = new System.Windows.Forms.Label();
            this.LocalXTxb = new System.Windows.Forms.TextBox();
            this.LocalZTxb = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.LocalYTxb = new System.Windows.Forms.TextBox();
            this.label2 = new System.Windows.Forms.Label();
            this.Theta2Txb = new System.Windows.Forms.TextBox();
            this.Theta1Txb = new System.Windows.Forms.TextBox();
            this.label4 = new System.Windows.Forms.Label();
            this.Theta3Txb = new System.Windows.Forms.TextBox();
            this.label5 = new System.Windows.Forms.Label();
            this.LocalBtn = new System.Windows.Forms.Button();
            this.AngleBtn = new System.Windows.Forms.Button();
            this.ResultTxb = new System.Windows.Forms.TextBox();
            this.SuspendLayout();
            // 
            // X
            // 
            this.X.AutoSize = true;
            this.X.Location = new System.Drawing.Point(68, 26);
            this.X.Name = "X";
            this.X.Size = new System.Drawing.Size(14, 13);
            this.X.TabIndex = 0;
            this.X.Text = "X";
            // 
            // LocalXTxb
            // 
            this.LocalXTxb.Location = new System.Drawing.Point(88, 19);
            this.LocalXTxb.Name = "LocalXTxb";
            this.LocalXTxb.Size = new System.Drawing.Size(64, 20);
            this.LocalXTxb.TabIndex = 1;
            // 
            // LocalZTxb
            // 
            this.LocalZTxb.Location = new System.Drawing.Point(88, 71);
            this.LocalZTxb.Name = "LocalZTxb";
            this.LocalZTxb.Size = new System.Drawing.Size(64, 20);
            this.LocalZTxb.TabIndex = 3;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(68, 78);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(14, 13);
            this.label1.TabIndex = 2;
            this.label1.Text = "Z";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(68, 52);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(14, 13);
            this.label3.TabIndex = 2;
            this.label3.Text = "Y";
            // 
            // LocalYTxb
            // 
            this.LocalYTxb.Location = new System.Drawing.Point(88, 45);
            this.LocalYTxb.Name = "LocalYTxb";
            this.LocalYTxb.Size = new System.Drawing.Size(64, 20);
            this.LocalYTxb.TabIndex = 3;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(41, 173);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(41, 13);
            this.label2.TabIndex = 2;
            this.label2.Text = "Theta2";
            // 
            // Theta2Txb
            // 
            this.Theta2Txb.Location = new System.Drawing.Point(88, 170);
            this.Theta2Txb.Name = "Theta2Txb";
            this.Theta2Txb.Size = new System.Drawing.Size(64, 20);
            this.Theta2Txb.TabIndex = 3;
            // 
            // Theta1Txb
            // 
            this.Theta1Txb.Location = new System.Drawing.Point(88, 144);
            this.Theta1Txb.Name = "Theta1Txb";
            this.Theta1Txb.Size = new System.Drawing.Size(64, 20);
            this.Theta1Txb.TabIndex = 5;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(41, 147);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(41, 13);
            this.label4.TabIndex = 4;
            this.label4.Text = "Theta1";
            // 
            // Theta3Txb
            // 
            this.Theta3Txb.Location = new System.Drawing.Point(88, 196);
            this.Theta3Txb.Name = "Theta3Txb";
            this.Theta3Txb.Size = new System.Drawing.Size(64, 20);
            this.Theta3Txb.TabIndex = 7;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(41, 199);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(41, 13);
            this.label5.TabIndex = 6;
            this.label5.Text = "Theta3";
            // 
            // LocalBtn
            // 
            this.LocalBtn.Location = new System.Drawing.Point(187, 42);
            this.LocalBtn.Name = "LocalBtn";
            this.LocalBtn.Size = new System.Drawing.Size(75, 23);
            this.LocalBtn.TabIndex = 8;
            this.LocalBtn.Text = "button1";
            this.LocalBtn.UseVisualStyleBackColor = true;
            this.LocalBtn.Click += new System.EventHandler(this.LocalBtn_Click);
            // 
            // AngleBtn
            // 
            this.AngleBtn.Location = new System.Drawing.Point(187, 163);
            this.AngleBtn.Name = "AngleBtn";
            this.AngleBtn.Size = new System.Drawing.Size(75, 23);
            this.AngleBtn.TabIndex = 8;
            this.AngleBtn.Text = "button2";
            this.AngleBtn.UseVisualStyleBackColor = true;
            this.AngleBtn.Click += new System.EventHandler(this.AngleBtn_Click);
            // 
            // ResultTxb
            // 
            this.ResultTxb.Location = new System.Drawing.Point(375, 26);
            this.ResultTxb.Multiline = true;
            this.ResultTxb.Name = "ResultTxb";
            this.ResultTxb.Size = new System.Drawing.Size(183, 252);
            this.ResultTxb.TabIndex = 9;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(583, 311);
            this.Controls.Add(this.ResultTxb);
            this.Controls.Add(this.AngleBtn);
            this.Controls.Add(this.LocalBtn);
            this.Controls.Add(this.Theta3Txb);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.Theta1Txb);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.LocalYTxb);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.Theta2Txb);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.LocalZTxb);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.LocalXTxb);
            this.Controls.Add(this.X);
            this.Name = "Form1";
            this.Text = "x";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label X;
        private System.Windows.Forms.TextBox LocalXTxb;
        private System.Windows.Forms.TextBox LocalZTxb;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox LocalYTxb;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox Theta2Txb;
        private System.Windows.Forms.TextBox Theta1Txb;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.TextBox Theta3Txb;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Button LocalBtn;
        private System.Windows.Forms.Button AngleBtn;
        private System.Windows.Forms.TextBox ResultTxb;
    }
}

