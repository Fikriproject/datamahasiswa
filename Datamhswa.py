import sys
from PyQt5 import QtWidgets, uic
import mysql.connector as mc
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox

qtcreator_file = "mahasiswa.ui"  # Nama File UI dari QtDesigner
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Koneksi ke database
        self.mydb = self.connect()

        # mamasukan fungsi button
        self.btnCari.clicked.connect(self.search_data)
        self.btnSimpan.clicked.connect(self.save_data)
        self.txtNIM.returnPressed.connect(self.search_data)
        self.btnClear.clicked.connect(self.clear_entry)
        self.btnHapus.clicked.connect(self.delete_data)
        self.btnTambah.clicked.connect(self.add_data)
        self.txtthnmasuk = self.findChild(QtWidgets.QLineEdit, 'txtthnmasuk')

        # buka data di tabel
        self.select_data()

    def connect(self):
        return mc.connect(
            host="localhost",
            user="root",
            password="",
            database="mahasiswa"
        )

    def select_data(self):
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute("SELECT * FROM mahasiswa")
            result = mycursor.fetchall()

            self.gridMahasiswa.setHorizontalHeaderLabels(
                ['ID', 'Nama', 'NIM', 'Jenis Kelamin', 'Prodi', 'Tahun Masuk'])
            self.gridMahasiswa.setRowCount(0)

            for row_number, row_data in enumerate(result):
                self.gridMahasiswa.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.gridMahasiswa.setItem(
                        row_number, column_number, QTableWidgetItem(str(data)))

        except mc.Error as e:
            self.messagebox("ERROR", "Terjadi kesalahan koneksi data")

    def search_data(self):
        try:
            nim = self.txtNIM.text()
            mycursor = self.mydb.cursor()
            mycursor.execute("SELECT * FROM mahasiswa WHERE nim='" + nim + "'")

            result = mycursor.fetchone()
            if result:
                self.txtNama.setText(result[1])
                if result[3] == "L":
                    self.optLaki.setChecked(True)
                    self.optPerempuan.setChecked(False)
                else:
                    self.optLaki.setChecked(False)
                    self.optPerempuan.setChecked(True)
                self.txtprodi.setText(result[4])
                self.txtthnmasuk.setText(str(result[5]))
                self.btnSimpan.setText("Update")
                self.edit_mode = True
                self.btnHapus.setEnabled(True)
                self.btnHapus.setStyleSheet("background-color : red")

            else:
                self.messagebox("INFO", "Data tidak ditemukan")
                self.txtNama.setFocus()
                self.btnSimpan.setText("Simpan")
                self.edit_mode = False
                self.btnHapus.setEnabled(False)
                self.btnHapus.setStyleSheet("color:black;background-color : grey")

        except mc.Error as e:
            self.messagebox("ERROR", "Terjadi kesalahan koneksi data")

    def save_data(self):
        try:
            nim = self.txtNIM.text()
            nama = self.txtNama.text()
            jk = "L" if self.optLaki.isChecked() else "P"
            prodi = self.txtprodi.text()
            thnmasuk = self.txtthnmasuk.text()

            mycursor = self.mydb.cursor()
            if not self.edit_mode:
                val = (nim, nama, jk, prodi, thnmasuk)
                sql = "INSERT INTO mahasiswa (nim, nama, jk, prodi, thnmasuk) VALUES (%s, %s, %s, %s, %s)"
                mycursor.execute(sql, val)
                self.mydb.commit()
                if mycursor.rowcount > 0:
                    self.messagebox("SUKSES", "Data Mahasiswa Tersimpan")
                else:
                    self.messagebox("GAGAL", "Data Mahasiswa Gagal Tersimpan")

                self.clear_entry()
                self.select_data()
            else:
                sql = "UPDATE mahasiswa SET nama = %s, jk=%s, prodi=%s, thnmasuk=%s WHERE nim=%s"
                val = (nama, jk, prodi, thnmasuk, nim)
                mycursor.execute(sql, val)
                self.mydb.commit()
                if mycursor.rowcount > 0:
                    self.messagebox("SUKSES", "Data Mahasiswa Diperbarui")
                else:
                    self.messagebox("GAGAL", "Data Mahasiswa Gagal Diperbarui")

                self.clear_entry()
                self.select_data()

        except mc.Error as e:
            self.messagebox("ERROR", "Terjadi kesalahan koneksi data")

    def delete_data(self):
        try:
            nim = self.txtNIM.text()
            mycursor = self.mydb.cursor()

            if self.edit_mode:
                sql = "DELETE FROM mahasiswa WHERE nim='" + nim + "'"
                mycursor.execute(sql)
                self.mydb.commit()
                if mycursor.rowcount > 0:
                    self.messagebox("SUKSES", "Data Mahasiswa Dihapus")
                else:
                    self.messagebox("GAGAL", "Data Mahasiswa Gagal Dihapus")

                self.clear_entry()
                self.select_data()
            else:
                self.messagebox("ERROR", "Sebelum menghapus data harus ditemukan terlebih dahulu")

        except mc.Error as e:
            self.messagebox("ERROR", "Terjadi kesalahan koneksi data")

    def add_data(self):
        try:
            nim = self.txtNIM.text()
            nama = self.txtNama.text()
            jk = "L" if self.optLaki.isChecked() else "P"
            prodi = self.txtprodi.text()
            thnmasuk = self.txtthnmasuk.text()

            mycursor = self.mydb.cursor()

            sql = "INSERT INTO mahasiswa (nim, nama, jk, prodi, thnmasuk) VALUES (%s, %s, %s, %s, %s)"
            val = (nim, nama, jk, prodi, thnmasuk)

            mycursor.execute(sql, val)
            self.mydb.commit()

            if mycursor.rowcount > 0:
                self.messagebox("SUKSES", "Data Mahasiswa Tersimpan")
                self.clear_entry()
                self.select_data()
            else:
                self.messagebox("GAGAL", "Data Mahasiswa Gagal Tersimpan")

        except mc.Error as e:
            self.messagebox("ERROR", "Terjadi kesalahan koneksi data")

    def clear_entry(self):
        self.txtNIM.setText("")
        self.txtNama.setText("")
        self.optLaki.setChecked(False)
        self.optPerempuan.setChecked(False)
        self.txtprodi.setText("")
        self.txtthnmasuk.setText("")
        self.btnHapus.setEnabled(False)
        self.btnHapus.setStyleSheet("color:black;background-color : grey")

    def messagebox(self, title, message):
        mess = QMessageBox()
        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setStandardButtons(QMessageBox.Ok)
        mess.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
