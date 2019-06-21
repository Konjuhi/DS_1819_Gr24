import socket, tkinter, Crypto, base64, json, jwt
from tkinter import *
from tkinter import messagebox
from Crypto import Random
from Crypto.Cipher import DES, PKCS1_OAEP
from Crypto.PublicKey import RSA

class ClientTk(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.display = True
        self.title("Client")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.onClose)
        self.geometry("240x320")
        self.dataSent = False

        client = Client()

        loginFrame = LoginFrame(self)
        signupFrame = SignupFrame(self)
        mainFrame = MainFrame(self)

        publicKeyFile = open("C:\\Users\\albin\\source\\repos\\DS_1819_Gr24\\Projekti2\\Public Key.pem", "r")
        self.publicKey = publicKeyFile.read()
        publicKeyFile.close()
        iv = Random.get_random_bytes(8)
        key = Random.get_random_bytes(8)
        message = ""

        jsonData = {
            "iv": base64.b64encode(iv).decode(),
            "key": base64.b64encode(PKCS1_OAEP.new(RSA.importKey(self.publicKey)).encrypt(key)).decode(),
            "message": base64.b64encode(DES.new(key, DES.MODE_CBC, iv).encrypt(multipleOf8(message).encode())).decode()
        }

        loginFrame.loginButton.configure(command = lambda: self.login(client, jsonData, iv, key, message, loginFrame))
        loginFrame.signupButton.configure(command = lambda: signupFrame.lift())
        signupFrame.signupButton.configure(command = lambda: self.signup(client, jsonData, iv, key, message, signupFrame))
        signupFrame.backButton.configure(command = lambda: loginFrame.lift())
        mainFrame.logoutButton.configure(command = lambda: self.logout(mainFrame, loginFrame))

        loginFrame.lift()

        while self.display:
            self.update_idletasks()
            self.update()

            if self.dataSent:
                (data, address) = client.receiveData()

                jsonReceivedData = json.loads(data.decode())

                iv1 = base64.b64decode(jsonReceivedData["iv"].encode())
                message1 = DES.new(key, DES.MODE_CBC, iv1).decrypt(base64.b64decode(jsonReceivedData["message"].encode("utf-8")))
                message1 = jwt.decode(removeDots(message1.decode()), self.publicKey, algorithms = ["RS512", "RS256"])
                if any("errorType" in r for r in message1):
                    if message1["errorType"] == "1":
                        messagebox.showerror("Sign up error", "Username is not available.")
                    elif message1["errorType"] == "2":
                        messagebox.showerror("Sign in error", "Wrong username.")
                    elif message1["errorType"] == "3":
                        messagebox.showerror("Sign in error", "Wrong password.")
                else:
                    mainFrame.setStudentData(message1)
                    mainFrame.lift()

                self.dataSent = False

    def onClose(self):
        self.display = False
        self.destroy()

    def login(self, client, jsonData, iv, key, message, loginFrame):
        if(loginFrame.usernameEntry.get() == "" or loginFrame.passwordEntry.get() == ""):
            messagebox.showerror("Sign in error", "Please fill all fields.")
        else:
            message += "login" + ' ' + loginFrame.usernameEntry.get() + ' ' + loginFrame.passwordEntry.get()
            jsonData["message"] = base64.b64encode(DES.new(key, DES.MODE_CBC, iv).encrypt(multipleOf8(message).encode())).decode()
            client.sendData(json.dumps(jsonData).encode())
            self.dataSent = True

    def signup(self, client, jsonData, iv, key, message, signupFrame):
        if(signupFrame.firstNameEntry.get() == "" or signupFrame.lastNameEntry.get() == "" or str(signupFrame.gender.get()) == "" or signupFrame.facultyEntry.get() == "" or signupFrame.idEntry.get() == "" or signupFrame.averageGradeEntry.get() == "" or signupFrame.usernameEntry.get() == "" or signupFrame.passwordEntry.get() == ""):
            messagebox.showerror("Sign up error", "Please fill all fields.")
        else:
            message += "register" + ' ' + signupFrame.firstNameEntry.get() + ' ' + signupFrame.lastNameEntry.get() + ' ' + str(signupFrame.gender.get()) + ' ' + signupFrame.facultyEntry.get() + ' ' + signupFrame.idEntry.get() + ' ' + signupFrame.averageGradeEntry.get() + ' ' + signupFrame.usernameEntry.get() + ' ' + signupFrame.passwordEntry.get()
            jsonData["message"] = base64.b64encode(DES.new(key, DES.MODE_CBC, iv).encrypt(multipleOf8(message).encode())).decode()
            client.sendData(json.dumps(jsonData).encode())
            self.dataSent = True

    def logout(self, mainFrame, loginFrame):
        mainFrame.clearStudentData()
        loginFrame.lift()
        loginFrame.passwordEntry.delete(0, END)

    def showFrame(self, frameName):
        frame = self.frames[frameName]
        frame.tkraise()

class LoginFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.place(in_ = parent, x = 0, y = 0, relwidth = 1, relheight = 1)
        self.configure(padx = 20, pady = 20)
        self.grid_rowconfigure(0, pad = 60)
        for i in range(1, 3):
            self.grid_columnconfigure(i, pad = 5)
        for i in range(1, 4):
            self.grid_rowconfigure(i, pad = 5)
        self.grid_rowconfigure(4, pad = 60)

        Label(self, text = "Welcome", font = ('Helvetica', 20)).grid(column = 0, row = 0, columnspan = 3)

        Label(self, text = "Username: ").grid(column = 0, row = 1)

        self.usernameEntry = Entry(self, width = 20)
        self.usernameEntry.grid(column = 1, row = 1, columnspan = 2)

        Label(self, text = "Password: ").grid(column = 0, row = 2)

        self.passwordEntry = Entry(self, show = "*", width = 20)
        self.passwordEntry.grid(column = 1, row = 2, columnspan = 2)

        self.loginButton = Button(self, text = "Log In")
        self.loginButton.grid(column = 2, row = 3)

        Label(self, text = "Don't have an account? ").grid(column = 0, row = 4, columnspan = 2)

        self.signupButton = Button(self, text = "Sign Up")
        self.signupButton.grid(column = 2, row = 4)

class SignupFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.place(in_ = parent, x = 0, y = 0, relwidth = 1, relheight = 1)
        self.configure(padx = 20, pady = 10)
        self.grid_rowconfigure(0, pad = 15)
        for i in range(1, 3):
            self.grid_columnconfigure(i, pad = 5)
        for i in range(1, 10):
            self.grid_rowconfigure(i, pad = 5)

        Label(self, text = "Create your account", font = ('Helvetica', 14)).grid(column = 0, row = 0, columnspan = 3)

        Label(self, text = "First name: ").grid(column = 0, row = 1)

        self.firstNameEntry = Entry(self, width = 20)
        self.firstNameEntry.grid(column = 1, row = 1, columnspan = 2)

        Label(self, text = "Last name: ").grid(column = 0, row = 2)

        self.lastNameEntry = Entry(self, width = 20)
        self.lastNameEntry.grid(column = 1, row = 2, columnspan = 2)

        self.gender = IntVar(self, value = 1)

        Label(self, text = "Gender: ").grid(column = 0, row = 3)

        Radiobutton(self, text = "Female", variable = self.gender, value = 1).grid(column = 1, row = 3)
        Radiobutton(self, text = "Male", variable = self.gender, value = 2).grid(column = 2, row = 3)

        Label(self, text = "Faculty: ").grid(column = 0, row = 4)

        self.facultyEntry = Entry(self, width = 20)
        self.facultyEntry.grid(column = 1, row = 4, columnspan = 2)

        Label(self, text = "ID: ").grid(column = 0, row = 5)

        self.idEntry = Entry(self, width = 20)
        self.idEntry.grid(column = 1, row = 5, columnspan = 2)

        Label(self, text = "Avg. grade: ").grid(column = 0, row = 6)

        self.averageGradeEntry = Entry(self, width = 20)
        self.averageGradeEntry.grid(column = 1, row = 6, columnspan = 2)

        Label(self, text = "Username: ").grid(column = 0, row = 7)

        self.usernameEntry = Entry(self, width = 20)
        self.usernameEntry.grid(column = 1, row = 7, columnspan = 2)

        Label(self, text = "Password").grid(column = 0, row = 8)

        self.passwordEntry = Entry(self, width = 20, show = "*")
        self.passwordEntry.grid(column = 1, row = 8, columnspan = 2)

        self.backButton = Button(self, text = "Back")
        self.backButton.grid(column = 0, row = 9)

        self.signupButton = Button(self, text = "Sign up")
        self.signupButton.grid(column = 2, row = 9)