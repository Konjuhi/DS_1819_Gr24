import socket, Crypto, base64, json, hashlib, binascii, os, tinydb, jwt
from Crypto import Random
from Crypto.Cipher import DES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from tinydb import TinyDB, Query

class Server:
    def __init__(self):

        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDP_HOST_SERVER = "localhost"
        self.UDP_PORT = 12000;
        self.serverSocket.bind((self.UDP_HOST_SERVER, self.UDP_PORT))

        self.keys = RSA.generate(1024, Random.new().read)
        self.privateKey = self.keys.exportKey("PEM")
        publicKeyFile = open("C:\\Users\\albin\\source\\repos\\DS_1819_Gr24\\Projekti2\\Public Key.pem", "wb")
        publicKeyFile.write(self.keys.publickey().exportKey("PEM"))
        publicKeyFile.close()

        print("Server is active...")
        print("")

    def loop(self):
        while True:
            (data, clientAddress) = self.receiveData()

            jsonReceivedData = json.loads(data.decode("utf-8"))

            iv = base64.b64decode(jsonReceivedData["iv"].encode())
            key = PKCS1_OAEP.new(RSA.importKey(self.privateKey)).decrypt(base64.b64decode(jsonReceivedData["key"].encode("utf-8")))
            message = DES.new(key, DES.MODE_CBC, iv).decrypt(base64.b64decode(jsonReceivedData["message"].encode("utf-8")))
            iv1 = Random.get_random_bytes(8)
            message1 = ""

            splitMessage = message.decode("utf-8").split(" ")

            jsonData = {
                "iv": base64.b64encode(iv1).decode("utf-8"),
                "message": base64.b64encode(DES.new(key, DES.MODE_CBC, iv1).encrypt(multipleOf8(message1).encode())).decode()
            }

            if("login" in splitMessage[0]):
                db = TinyDB("C:\\Users\\albin\\source\\repos\\DS_1819_Gr24\\Projekti2\\Server\\db.json")
                students = db.table("students")
                student = Query()
                if not students.search(student.username == splitMessage[1]):
                    message1 = jwt.encode({"errorType": "2"}, self.privateKey, "RS256").decode()
                    jsonData["message"] = base64.b64encode(DES.new(key, DES.MODE_CBC, iv1).encrypt(multipleOf8(message1).encode())).decode()
                    self.sendData(json.dumps(jsonData), clientAddress)
                else:
                    dbStudentInfo = students.search(student.username == splitMessage[1])[0]
                    if not checkPassword(dbStudentInfo["password"], splitMessage[2]):
                        message1 = jwt.encode({"errorType": "3"}, self.privateKey, "RS256").decode()
                        jsonData["message"] = base64.b64encode(DES.new(key, DES.MODE_CBC, iv1).encrypt(multipleOf8(message1).encode())).decode()
                        self.sendData(json.dumps(jsonData), clientAddress)
                    else:
                        studentInfo = {
                            "firstName": dbStudentInfo["firstName"],
                            "lastName": dbStudentInfo["lastName"],
                            "gender": "Female" if (dbStudentInfo["gender"] == "1") else "Male",
                            "faculty": dbStudentInfo["faculty"],
                            "id": dbStudentInfo["id"],
                            "averageGrade": dbStudentInfo["averageGrade"],
                            "username": dbStudentInfo["username"],
                            "password": dbStudentInfo["password"]
                        }
                        message1 = jwt.encode(studentInfo, self.privateKey, "RS256").decode()
                        jsonData["message"] = base64.b64encode(DES.new(key, DES.MODE_CBC, iv1).encrypt(multipleOf8(message1).encode())).decode()
                        self.sendData(json.dumps(jsonData), clientAddress)
                db.close()
            elif ("register" in splitMessage[0]):
                studentInfo = {
                    "firstName": splitMessage[1],
                    "lastName": splitMessage[2],
                    "gender": "Female" if (splitMessage[3] == "1") else "Male",
                    "faculty": splitMessage[4],
                    "id": splitMessage[5],
                    "averageGrade": splitMessage[6],
                    "username": splitMessage[7],
                    "password": hashPassword(splitMessage[8])
                }
                db = TinyDB("C:\\Users\\albin\\source\\repos\\DS_1819_Gr24\\Projekti2\\Server\\db.json")
                students = db.table("students")
                student = Query()
                if not students.search(student.username == studentInfo["username"]):
                    self.insertStudent(studentInfo)
                    message1 = jwt.encode(studentInfo, self.privateKey, "RS256").decode()
                    jsonData["message"] = base64.b64encode(DES.new(key, DES.MODE_CBC, iv1).encrypt(multipleOf8(message1).encode())).decode()
                    self.sendData(json.dumps(jsonData), clientAddress)
                else:
                    message1 = jwt.encode({"errorType": "1"}, self.privateKey, "RS256").decode()
                    jsonData["message"] = base64.b64encode(DES.new(key, DES.MODE_CBC, iv1).encrypt(multipleOf8(message1).encode())).decode()
                    self.sendData(json.dumps(jsonData), clientAddress)
                db.close()

    def receiveData(self):
        return self.serverSocket.recvfrom(4096)

    def sendData(self, data, clientAddress):
        self.serverSocket.sendto(data.encode("utf-8"), clientAddress)

    def insertStudent(self, studentInfo):
        dt = TinyDB("C:\\Users\\albin\\source\\repos\\DS_1819_Gr24\\Projekti2\\Server\\db.json")
        students = dt.table("students")
        students.insert({"firstName": studentInfo["firstName"], "lastName": studentInfo["lastName"], "gender": studentInfo["gender"], "faculty": studentInfo["faculty"], "id": studentInfo["id"], "averageGrade": studentInfo["averageGrade"], "username": studentInfo["username"], "password": studentInfo["password"]})
        dt.close()

def hashPassword(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    hashedPassword = binascii.hexlify(hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000))
    return (salt + hashedPassword).decode('ascii')

def checkPassword(storedPassword, providedPassword):
    salt = storedPassword[:64]
    storedPassword = storedPassword[64:]
    hashedPassword = hashlib.pbkdf2_hmac('sha512', providedPassword.encode('utf-8'), salt.encode('ascii'), 100000)
    hashedPassword = binascii.hexlify(hashedPassword).decode('ascii')
    return hashedPassword == storedPassword

def multipleOf8(str):
    addNumber = 8-len(str)%8
    addDots = ""
    for i in range(addNumber):
        addDots += '.'
    return addDots + str

if __name__ == "__main__":
    server = Server()
    server.loop()





























