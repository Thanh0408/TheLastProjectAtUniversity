using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO.Ports;


namespace WindowsFormsApp1
{
  

    public partial class Form1 : Form
    {
        deltaRobot deltaRobot;
        SerialPort serialPort;
        int DeviceStatus = 1;
        public Form1()
        {
            InitializeComponent();
            serialPort = new SerialPort();
            serialPort.PortName = "COM5";
            serialPort.BaudRate = 9600;
            //serialPort.RtsEnable = true;
            serialPort.DataReceived += new SerialDataReceivedEventHandler(DataReceivedHandler);
            serialPort.Open();
        }

        private void DataReceivedHandler(
                        object sender,
                        SerialDataReceivedEventArgs e)
        {
            SerialPort sp = (SerialPort)sender;
            string indata = sp.ReadExisting();
            Console.WriteLine("Data Received:");
            Console.Write(indata);
            ShowData(indata);
            DeviceStatus = 1;
        }

        void ShowData(string data)
        {
            this.Invoke((MethodInvoker)delegate
            {
                ResultTxb.Text += data;
            });
        }

       
        /*private void SendBtn_Click(object sender, EventArgs e)
        {
            string s = LocalXTxb.Text;
            serialPort.Write(s);
            while (true)
            {
                string t = serialPort.ReadExisting();
                Console.WriteLine(t);
            }
        }*/


        private void LocalBtn_Click(object sender, EventArgs e)
        {
            try {
                float x = float.Parse(LocalXTxb.Text);
                float y = float.Parse(LocalYTxb.Text);
                float z = float.Parse(LocalZTxb.Text);
                deltaRobot = new deltaRobot(x, y, z);
                deltaRobot.reverse();
                string cmd = $"T {string.Format("{0:0.00}",deltaRobot.theta1)} {string.Format("{0:0.00}", deltaRobot.theta2)} {string.Format("{0:0.00}", deltaRobot.theta3)}\n";
                SendCmd(cmd);
                ResultTxb.Text = "";
            }catch(Exception eeee)
            {

            }
            
        }

        private void AngleBtn_Click(object sender, EventArgs e)
        {
            try { 
                float Theta1 = float.Parse(Theta1Txb.Text);
                float Theta2 = float.Parse(Theta2Txb.Text);
                float Theta3 = float.Parse(Theta3Txb.Text);
                string cmd = $"T {Theta1} {Theta2} {Theta3}\n";
                SendCmd(cmd);
                ResultTxb.Text = "";
            }catch(Exception aaaa)
            {

            }
            
        }
        void SendCmd(string cmd)
        {
            if(DeviceStatus == 1)
            {
                serialPort.Write(cmd);
                DeviceStatus = 0;
            }
            else
            {
                Console.WriteLine("Device Not Ready");
            }
        }

        
    }     
}
