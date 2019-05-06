using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace CaesarCipher {
    public partial class Form1: Form {
        public Form1() {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e) {

        }

        private void button1_Click(object sender, EventArgs e) {
            try {
                if(Convert.ToInt32(textBox3.Text) < 0)
                    throw new Exception();
                textBox5.Text = Caesar.encrypt(textBox1.Text, Convert.ToInt32(textBox3.Text));
            } catch(Exception ex) {
                MessageBox.Show("Ju lutemi mbushini te gjitha kutite.\nQelesi duhet te jete nje numer i plote.");
            }
        }

        private void button2_Click(object sender, EventArgs e) {
            try {
                if(Convert.ToInt32(textBox4.Text) < 0)
                    throw new Exception();
                textBox6.Text = Caesar.decrypt(textBox2.Text, Convert.ToInt32(textBox4.Text));
            }
            catch(Exception ex) {
                MessageBox.Show("Ju lutemi mbushini te gjitha kutite.\nQelesi duhet te jete nje numer i plote.");
            }
        }

        private void textBox1_TextChanged(object sender, EventArgs e) {

        }
    }

    static class Caesar {
        public static string encrypt(string str, int shift) {
            string encryptedString = "";
            for(int i = 0; i < str.Length; i++)
                if((int)str[i] >= 65 && (int)str[i] <= 90)
                    encryptedString += (char)((int)str[i] + shift - (int)((int)(str[i] - 65 + shift) / 26) * 26);
                else if((int)str[i] >= 97 && (int)str[i] <= 122)
                    encryptedString += (char)((int)str[i] + shift - (int)((int)(str[i] - 97 + shift) / 26) * 26);
                else
                    encryptedString += str[i];
            return encryptedString;
        }

        public static string decrypt(string str, int shift) {
            string decryptedString = "";
            for(int i = 0; i < str.Length; i++)
                if((int)str[i] >= 65 && (int)str[i] <= 90)
                    decryptedString += (char)((int)str[i] - shift + (int)((90 - (int)str[i] + shift) / 26) * 26);
                else if ((int)str[i] >= 97 && (int)str[i] <= 122)
                    decryptedString += (char)((int)str[i] - shift + (int)((122 - (int)str[i] + shift) / 26) * 26);
                else
                    decryptedString += str[i];
            return decryptedString;
        }
    }
}
