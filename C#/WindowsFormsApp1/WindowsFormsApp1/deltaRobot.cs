using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


namespace WindowsFormsApp1
{
    class deltaRobot
    {
        float f = 100;
        float La = 165;
        float Lb = 340;
        float e = 50;

        public double x;
        public double y;
        public double z;

        public double theta1;
        public double theta2;
        public double theta3;

        public bool isAngle = false;

        public deltaRobot(double x, double y, double z)
        {
            this.x = x;
            this.y = y;
            this.z = z;
        }

        public deltaRobot(bool isAngle, double theta1, double theta2, double theta3)
        {
            if (isAngle)
            {
                this.theta1 = theta1;
                this.theta2 = theta2;
                this.theta3 = theta3;
            }
        } 

        public void forward()
        {

        }

        public void reverse()
        {
            try
            {
                double cos120 = Math.Cos(2 * Math.PI / 3);
                double sin120 = Math.Sin(2 * Math.PI / 3);
                double cos240 = Math.Cos(4 * Math.PI / 3);
                double sin240 = Math.Sin(4 * Math.PI / 3);
                this.theta1 = calcAngle(this.x, this.y, this.z);
                this.theta2 = calcAngle(this.x * cos120 - this.y * sin120, this.x * sin120 + this.y * cos120, this.z);
                this.theta3 = calcAngle(this.x * cos240 - this.y * sin240, this.x * sin240 + this.y * cos240, this.z);
                this.theta1 += 40;
                this.theta2 += 40;
                this.theta3 += 40;
            }
            catch (Exception ex)
            {
                throw ex;
            }
            
        }

        public double calcAngle(double x0, double y0, double z0)
        {
            double T = f + x0 - e;
            double K = Lb * Lb - y0 * y0 - T * T - z0 * z0 - La * La;

            double e1 = 2 * T * La + K;
            double e2 = -4 * z0 * La;
            double e3 = -2 * T * La + K;

            double theta = 2 * Math.Atan((-e2 + Math.Sqrt(e2 * e2 - 4*e1 * e3)) / (2 * e1));
            theta = theta * 180 / Math.PI;
            double thetamax = theta + 180;
            double thetamin = theta - 180;
            if(thetamax > -60 && thetamax < 90)
            {
                return thetamax;
            }else if(thetamin > -60 && thetamin < 90)
            {
                return thetamin;
            }else if(theta > -60 && theta < 90)
            {
                return theta;
            }
            else
            {
                throw new ArgumentException("position failed");
            }
            
        }
    }
}
