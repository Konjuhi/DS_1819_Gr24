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
                textBox5.Text = Caesar.encrypt(textBox1.Text, Convert.ToInt32(textBox3.Text));
            } catch(Exception ex) {
                MessageBox.Show("Ju lutemi mbushini te gjithe hapesirat per tekst.");
            }
        }

        private void button2_Click(object sender, EventArgs e) {
            try {
                textBox6.Text = Caesar.decrypt(textBox2.Text, Convert.ToInt32(textBox4.Text));
            }
            catch(Exception ex) {
                MessageBox.Show("Ju lutemi mbushini te gjithe hapesirat per tekst.");
            }
        }

        private void label1_Click(object sender, EventArgs e) {

        }

        private void textBox1_TextChanged(object sender, EventArgs e) {

        }

        private void label2_Click(object sender, EventArgs e) {

        }
    }

    static class Caesar {
        public static string encrypt(string str, int shift) {
            string encryptedString = "";
            for (int i = 0; i < str.Length; i++) {
                encryptedString += (char)((int)str[i]+shift);
            }
            return encryptedString;
        }

        public static string decrypt(string str, int shift) {
            string decryptedString = "";
            for (int i = 0; i < str.Length; i++)
                decryptedString += (char)((int)str[i]-shift);
            return decryptedString;
        }
    }
}
