import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QDialog, QHBoxLayout, QListWidget, QInputDialog

class Library:
    def __init__(self, filename):
        self.filename = filename
        self.usersFileName = "üyeler.txt"
        self.file = open(self.filename, "a+")
        self.usersFile = open(self.usersFileName, "a+")

    def returnBook(self, bookTitle):
        with open(self.filename, "r+") as f:
            lines = f.readlines()
            f.seek(0)
            for i, line in enumerate(lines):
                if bookTitle in line:
                    if "Kiralandı" in line:
                        lines[i] = line.replace("Kiralandı", "Kiralabilir")
                        break
            f.writelines(lines)
            f.truncate()

    def ListAllBooks(self):
        available_books = []
        with open(self.filename, "r") as file:
            for line in file:
                book_info = line.strip().split(',')
                if len(book_info) == 4 and "Kiralandı" not in book_info:  # Only consider books that are available
                    available_books.append(f"Title: {book_info[0]}, Author: {book_info[1]}")
        return available_books

    def __del__(self):
        self.file.close()

    def listBooks(self):
        self.file.seek(0)
        bookList = self.file.readlines()
        for book in bookList:
            bookInfo = book.strip().split(',')
            print(f"Title {bookInfo[0]}, Author: {bookInfo[1]}")

    def addBook(self, title, author, release_year, num_pages):
        self.file.write(f"{title},{author},{release_year},{num_pages}\n")

    def removeBook(self, title):
        self.file.seek(0)
        lines = self.file.readlines()
        self.file.seek(0)
        self.file.truncate()
        for line in lines:
            if title not in line:
                self.file.write(line)

    def registerUser(self, name, surname, email, password):
        with open(self.usersFileName, "a") as f:
            f.write(f"{name},{surname},{email},{password}\n")

    def userLogin(self, email, password):
        with open(self.usersFileName, "r") as f:
            users = f.readlines()
            for user in users:
                user_data = user.strip().split(',')
                if user_data[2] == email and user_data[3] == password:
                    return True
        return False

    def authenticateUser(self, email, password):
        with open(self.usersFileName, "r") as f:
            users = f.readlines()
            for user in users:
                user_data = user.strip().split(',')
                if user_data[2] == email and user_data[3] == password:
                    return user_data[0] + " " + user_data[1]
        return False

    def rentBook(self, book_title):
        with open(self.filename, "r+") as f:
            lines = f.readlines()
            f.seek(0)
            for i, line in enumerate(lines):
                if book_title in line:
                    if "Kiralandı" not in line:
                        lines[i] = line.strip() + ", Kiralandı\n"
                        break
            f.seek(0)
            f.writelines(lines)
            f.truncate()

    def availableBooks(self):
        available_books = []
        with open(self.filename, "r") as f:
            lines = f.readlines()
            for line in lines:
                book_info = line.strip().split(',')
                if len(book_info) == 4 and "Kiralandı" not in book_info:
                    available_books.append(book_info[0])
        return available_books

class UserPanel(QWidget):
    def __init__(self, library):
        super().__init__()
        self.library = library
        self.setWindowTitle("Kullanıcı Girişi")
        self.setGeometry(100,100,400,400)

        self.layout = QVBoxLayout()
        self.liste = QListWidget()
        self.layout.addWidget(self.liste)

        self.listele_button = QPushButton("Tüm Kitapları Görüntüle")
        self.listele_button.clicked.connect(self.kitaplari_listele)
        self.layout.addWidget(self.listele_button)

        self.kirala_button = QPushButton("Kitap Kirala")
        self.kirala_button.clicked.connect(self.kitap_kirala)
        self.layout.addWidget(self.kirala_button)

        self.geri_ver_button = QPushButton("Kitabı Geri Ver")
        self.geri_ver_button.clicked.connect(self.kitabi_geri_ver)
        self.layout.addWidget(self.geri_ver_button)

        self.cikis_button = QPushButton("Çıkış")
        self.cikis_button.clicked.connect(self.close)
        self.layout.addWidget(self.cikis_button)

        self.setLayout(self.layout)

    def kitaplari_listele(self):
        self.liste.clear()
        with open("kitaplar.txt", "r") as f:
            kitaplar = f.readlines()
            for kitap in kitaplar:
                kitap_bilgisi = kitap.strip().split(',')
                if len(kitap_bilgisi) == 4:  # Sadece mevcut kitapları ekleyin
                    self.liste.addItem(kitap.strip())

    def kitap_kirala(self):
        kitap_adi, ok = QInputDialog.getText(self, "Kitap Kirala", "Kitap Adı:")
        if ok:
            with open("kitaplar.txt", "r+") as file:
                kitaplar = file.readlines()
                file.seek(0)
                for kitap in kitaplar:
                    if kitap.strip() == kitap_adi:
                        continue
                    file.write(kitap)
                file.truncate()
            self.kitaplari_listele()

    def kitabi_geri_ver(self):
        kitap_adi, ok = QInputDialog.getText(self, "Kitap Geri Ver", "Kitap Adı:")
        if ok:
            with open("kitaplar.txt", "a") as file:
                file.write(kitap_adi + "\n")
            self.kitaplari_listele()

class LibraryApp(QWidget):
    def __init__(self, kitaplar):
        super().__init__()
        self.setGeometry(50, 50, 400, 400)
        self.library = Library(kitaplar)
        self.initUi()

    def initUi(self):
        self.setWindowTitle("Library Management System")
        layout = QVBoxLayout()

        self.adminBtn = QPushButton("Yönetici Girişi")
        self.adminBtn.clicked.connect(self.adminLogin)
        layout.addWidget(self.adminBtn)

        self.userBtn = QPushButton("Kullanıcı Girişi")
        self.userBtn.clicked.connect(self.userLogin)
        layout.addWidget(self.userBtn)

        self.registerBtn = QPushButton("Kayıt Ol")
        self.registerBtn.clicked.connect(self.registerUser)
        layout.addWidget(self.registerBtn)

        self.ExitBtn = QPushButton("Çıkış")
        self.ExitBtn.clicked.connect(self.close)
        layout.addWidget(self.ExitBtn)

        self.setLayout(layout)
        self.show()

    def welcomeMessage(self, name, lastname):
        QMessageBox.information(self, "Hoşgeldiniz!", f"Hoşgeldiniz {name} {lastname}")

    def adminLogin(self):
        dialog = AdminLoginDialog()
        if dialog.exec_() == QDialog.Accepted:
            username = dialog.usernameEdit.text()
            password = dialog.passwordEdit.text()
            if username == "admin" and password == "1234":
                QMessageBox.information(self, "Yönetici Girişi", "Giriş Başarılı!")
                self.openAdminPanel()
            else:
                QMessageBox.warning(self, "Yönetici Girişi", "Kullanıcı adı veya şifre hatalı!")

    def openAdminPanel(self):
        self.adminPanel = AdminPanel("kitaplar.txt")
        self.adminPanel.show()

    def userLogin(self):
        dialog = UserLoginDialog()
        if dialog.exec_() == QDialog.Accepted:
            email = dialog.emailEdit.text()
            password = dialog.passwordEdit.text()
            firstname = self.library.authenticateUser(email, password)
            if firstname:
                QMessageBox.information(self, "Kullanıcı Girişi", f"Hoşgeldiniz, {firstname}!")
                self.openUserPanel()
            else:
                QMessageBox.warning(self, "Kullanıcı Girişi", "E-posta veya şifre hatalı!")

    def openUserPanel(self):
        self.userPanel = UserPanel(self.library)
        self.userPanel.show()

    def registerUser(self):
        dialog = RegisterDialog()
        if dialog.exec_() == QDialog.Accepted:
            name = dialog.nameEdit.text()
            surname = dialog.surnameEdit.text()
            email = dialog.emailEdit.text()
            password = dialog.passwordEdit.text()
            self.library.registerUser(name, surname, email, password)
            QMessageBox.information(self, "Kayıt Ol", "Kayıt işlemi başarıyla tamamlandı!")

class AdminLoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(50, 50, 400, 400)
        self.setWindowTitle("Admin Girişi")
        layout = QVBoxLayout()

        usernameLayout = QHBoxLayout()
        self.usernameLabel = QLabel("Kullanıcı Adı:")
        self.usernameEdit = QLineEdit()
        usernameLayout.addWidget(self.usernameLabel)
        usernameLayout.addWidget(self.usernameEdit)

        passwordLayout = QHBoxLayout()
        self.passwordLabel = QLabel("Şifre:")
        self.passwordEdit = QLineEdit()
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        passwordLayout.addWidget(self.passwordLabel)
        passwordLayout.addWidget(self.passwordEdit)

        layout.addLayout(usernameLayout)
        layout.addLayout(passwordLayout)

        self.login_btn = QPushButton("Giriş")
        self.login_btn.clicked.connect(self.accept)
        layout.addWidget(self.login_btn)

        self.setLayout(layout)

class UserLoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kullanıcı Girişi")
        self.setGeometry(50, 50, 400, 400)
        layout = QVBoxLayout()

        emailLayout = QHBoxLayout()
        self.emailLabel = QLabel("E-posta:")
        self.emailEdit = QLineEdit()
        emailLayout.addWidget(self.emailLabel)
        emailLayout.addWidget(self.emailEdit)

        passwordLayout = QHBoxLayout()
        self.passwordLabel = QLabel("Şifre:")
        self.passwordEdit = QLineEdit()
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        passwordLayout.addWidget(self.passwordLabel)
        passwordLayout.addWidget(self.passwordEdit)

        layout.addLayout(emailLayout)
        layout.addLayout(passwordLayout)

        self.login_btn = QPushButton("Giriş")
        self.login_btn.clicked.connect(self.accept)
        layout.addWidget(self.login_btn)

        self.setLayout(layout)

class RegisterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(50, 50, 400, 400)
        self.setWindowTitle("Kayıt Ol")
        layout = QVBoxLayout()

        nameLayout = QHBoxLayout()
        self.nameLabel = QLabel("İsim:")
        self.nameEdit = QLineEdit()
        nameLayout.addWidget(self.nameLabel)
        nameLayout.addWidget(self.nameEdit)

        surnameLayout = QHBoxLayout()
        self.surnameLabel = QLabel("Soyisim:")
        self.surnameEdit = QLineEdit()
        surnameLayout.addWidget(self.surnameLabel)
        surnameLayout.addWidget(self.surnameEdit)

        emailLayout = QHBoxLayout()
        self.emailLabel = QLabel("E-posta:")
        self.emailEdit = QLineEdit()
        emailLayout.addWidget(self.emailLabel)
        emailLayout.addWidget(self.emailEdit)

        passwordLayout = QHBoxLayout()
        self.passwordLabel = QLabel("Şifre:")
        self.passwordEdit = QLineEdit()
        passwordLayout.addWidget(self.passwordLabel)
        passwordLayout.addWidget(self.passwordEdit)

        layout.addLayout(nameLayout)
        layout.addLayout(surnameLayout)
        layout.addLayout(emailLayout)
        layout.addLayout(passwordLayout)

        self.register_btn = QPushButton("Kayıt Ol")
        self.register_btn.clicked.connect(self.accept)
        layout.addWidget(self.register_btn)

        self.setLayout(layout)


class AdminPanel(QWidget):
    def __init__(self, kitaplar):
        super().__init__()
        self.setWindowTitle("Admin Paneli")
        self.setGeometry(50, 50, 400, 400)
        self.kitaplar = kitaplar

        layout = QVBoxLayout()

        self.kitapEkleBtn = QPushButton("Kitap Ekle")
        self.kitapEkleBtn.clicked.connect(self.openAddBookDialog)
        layout.addWidget(self.kitapEkleBtn)

        self.kitapSilBtn = QPushButton("Kitap Sil")
        self.kitapSilBtn.clicked.connect(self.kitapSil)
        layout.addWidget(self.kitapSilBtn)

        self.kitapListeBtn = QPushButton("Kitapları Listele")
        self.kitapListeBtn.clicked.connect(self.kitapListesi)
        layout.addWidget(self.kitapListeBtn)

        self.CikisBtn = QPushButton("Çıkış")
        self.CikisBtn.clicked.connect(self.close)
        layout.addWidget(self.CikisBtn)

        self.setLayout(layout)

    def openAddBookDialog(self):
        dialog = AddBookDialog(self)
        if dialog.exec_():
            kitapAdi, yazar, cikisTarihi, sayfaSayisi = dialog.getBookInfo()
            with open(self.kitaplar, "a") as dosya:
                dosya.write(f"{kitapAdi}, {yazar}, {cikisTarihi}, {sayfaSayisi} sayfa\n")
            QMessageBox.information(self, "Kitap Ekle", "Kitap başarıyla eklendi.")

    def KitapEkle(self):
        dialog = AddBookDialog(self)
        if dialog.exec_():
            kitapAdı, yazar, cikisTarihi, sayfaSayısı = dialog.getBookInfo()
            with open(self.kitaplar, "a") as dosya:
                dosya.write(f"{kitapAdı}, {yazar}, {cikisTarihi}, {sayfaSayısı} sayfa \n")
            QMessageBox.information(self, "Kitap Ekle", "Kitap Başarıyla Eklendi.")

    def kitapSil(self):
        kitapAdi, okPressed = QInputDialog.getText(self, "Kitap Sil", "Silinecek Kitap Adı: ")
        if okPressed and kitapAdi.strip():
            with open(self.kitaplar, "r") as dosya:
                kitaplar = dosya.readlines()
            with open(self.kitaplar, "w") as dosya:
                kitap_silindi = False
                for kitap in kitaplar:
                    if kitapAdi.strip() not in kitap:
                        dosya.write(kitap)
                    else:
                        kitap_silindi = True
                if kitap_silindi:
                    QMessageBox.information(self, "Kitap Sil", f"{kitapAdi} kitabı silindi.")
                else:
                    QMessageBox.warning(self, "Kitap Sil", f"{kitapAdi} kitabı bulunamadı.")

    def kitapListesi(self):
        with open(self.kitaplar, "r") as dosya:
            kitaplar = dosya.readlines()
        kitapListesi = "".join(kitaplar)
        QMessageBox.information(self, "Kitap Listesi", kitapListesi)

class AddBookDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kitap Ekle")
        self.setLayout(QVBoxLayout())

        self.kitap_adı_edit = QLineEdit()
        self.layout().addWidget(QLabel("Kitap Adı:"))
        self.layout().addWidget(self.kitap_adı_edit)

        self.yazar_edit = QLineEdit()
        self.layout().addWidget(QLabel("Yazarı:"))
        self.layout().addWidget(self.yazar_edit)

        self.çıkış_tarihi_edit = QLineEdit()
        self.layout().addWidget(QLabel("Çıkış Tarihi:"))
        self.layout().addWidget(self.çıkış_tarihi_edit)

        self.sayfa_sayısı_edit = QLineEdit()
        self.layout().addWidget(QLabel("Sayfa Sayısı:"))
        self.layout().addWidget(self.sayfa_sayısı_edit)

        self.kitapEkleBtn = QPushButton("Kitap Ekle")
        self.kitapEkleBtn.clicked.connect(self.checkAndAddBook)
        self.layout().addWidget(self.kitapEkleBtn)

    def checkAndAddBook(self):
        kitap_adı = self.kitap_adı_edit.text().strip()
        yazar = self.yazar_edit.text().strip()
        çıkış_tarihi = self.çıkış_tarihi_edit.text().strip()
        sayfa_sayısı = self.sayfa_sayısı_edit.text().strip()

        if not kitap_adı or not yazar or not çıkış_tarihi or not sayfa_sayısı:
            QMessageBox.warning(self, "Boş Alanlar", "Tüm alanları doldurunuz.")
        else:
            self.accept()

    def getBookInfo(self):
        kitap_adı = self.kitap_adı_edit.text().strip()
        yazar = self.yazar_edit.text().strip()
        çıkış_tarihi = self.çıkış_tarihi_edit.text().strip()
        sayfa_sayısı = self.sayfa_sayısı_edit.text().strip()
        return kitap_adı, yazar, çıkış_tarihi, sayfa_sayısı

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dosya = "kitaplar.txt"
    win = LibraryApp(dosya)
    win.show()
    sys.exit(app.exec_())
