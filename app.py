from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask_session import Session

# initializations
app = Flask(__name__)

# Konfigurasi MySQL
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'polibatamkw'
app.config['SESSION_PERMANENT'] = False
app.config["SESSION_TYPE"] = "filesystem"
mysql = MySQL(app)
Session(app)

# APP secret key (bebas)
app.secret_key = "4cc645e832bc2ed0869da6d3a9bdc0ea"

# routes
@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(id) FROM mahasiswa")
    countMahasiswa = cursor.fetchone()
    cursor.execute("SELECT COUNT(id) FROM mata_kuliah")
    countMataKuliah = cursor.fetchone()
    cursor.execute("SELECT COUNT(id) FROM kelas")
    countKelas = cursor.fetchone()
    cursor.execute("SELECT COUNT(id) FROM jurusan")
    countJurusan = cursor.fetchone()
    cursor.execute("SELECT COUNT(id) FROM dosen")
    countDosen = cursor.fetchone()
    return render_template('home.html', mahasiswa = countMahasiswa[0], matakuliah = countMataKuliah[0], kelas = countKelas[0], jurusan = countJurusan[0], dosen = countDosen[0])

# login
@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT username FROM users WHERE username = '{username}' AND password = '{password}'")
        user = cursor.fetchone()
        # userSorted = user.sort()
        # userName = userSorted[0]
        if user != False:
            session['authenticated'] = True
            session['username'] = user
            return redirect('/')
        else:
            flash('Username / Password Kamu Salah!')

    return render_template('login/login.html')

# logout
@app.route("/logout")
def logout():
    session["username"] = None
    return redirect("/login")

# Mahasiswa
@app.route('/mahasiswa')
def data_mahasiswa():
    cur = mysql.connection.cursor()
    cur.execute('SELECT s.id, s.nim, s.nama_lengkap, s.alamat, s.tanggal_lahir, s.jenis_kelamin, j.nama, k.nama FROM mahasiswa as s LEFT OUTER JOIN jurusan as j ON s.jurusan_id = j.id LEFT OUTER JOIN kelas as k ON s.kelas_id = k.id ORDER BY id')
    data = cur.fetchall()
    cur.close()
    return render_template('mahasiswa/data-mahasiswa.html', mahasiswa = data)

@app.route('/mahasiswa/tambah', methods = ['GET'])
def tambah_mahasiswa():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nama FROM jurusan")
    dataJurusan = cursor.fetchall()
    cursor.execute("SELECT id, nama FROM kelas")
    dataKelas = cursor.fetchall()
    cursor.close()
    return render_template('mahasiswa/tambah-mahasiswa.html', jurusan = dataJurusan, kelas = dataKelas)

@app.route('/mahasiswa/insert', methods=['POST'])
def add_mahasiswa():
    if request.method == 'POST':
        nim = request.form['nim']
        nama_lengkap = request.form['nama_lengkap']
        alamat = request.form['alamat']
        jenisKelamin = request.form['jenis_kelamin']
        kelasId = request.form['kelas_id']
        jurusanId = request.form['jurusan_id']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO mahasiswa (nim, nama_lengkap, alamat, jenis_kelamin, jurusan_id, kelas_id) VALUES (%s,%s,%s,%s,%s,%s)", 
        (nim, nama_lengkap, alamat, jenisKelamin, jurusanId, kelasId))
        mysql.connection.commit()
        flash('Data mahasiswa berhasil ditambahkan!')
        return redirect(url_for('data_mahasiswa'))

@app.route('/mahasiswa/edit/<int:id>', methods = ['GET'])
def get_mahasiswa(id):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT id, nama_lengkap, nim, alamat, tanggal_lahir, jenis_kelamin, jurusan_id, kelas_id FROM mahasiswa WHERE id = {id}")
    data = cur.fetchall()
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nama FROM jurusan")
    dataJurusan = cursor.fetchall()
    cursor.execute("SELECT id, nama FROM kelas")
    dataKelas = cursor.fetchall()
    cursor.close()
    cur.close()
    print(data[0])
    return render_template('mahasiswa/ubah-mahasiswa.html', mahasiswa = data[0], jurusan = dataJurusan, kelas = dataKelas)

@app.route('/mahasiswa/update/<int:id>', methods=['POST'])
def update_mahasiswa(id):
    if request.method == 'POST':
        nim = request.form['nim']
        nama_lengkap = request.form['nama_lengkap']
        alamat = request.form['alamat']
        jenis_kelamin = request.form['jenis_kelamin']
        jurusan_id = request.form['jurusan_id']
        kelas_id = request.form['kelas_id']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE mahasiswa
            SET nim = %s, nama_lengkap = %s, alamat = %s, jenis_kelamin = %s, jurusan_id = %s, kelas_id = %s
            WHERE id = %s
        """, (nim,nama_lengkap, alamat, jenis_kelamin, jurusan_id, kelas_id, id))
        flash('Data mahasiswa berhasil diubah!')
        mysql.connection.commit()
        return redirect(url_for('data_mahasiswa'))

@app.route('/mahasiswa/delete/<int:id>', methods = ['POST','GET'])
def delete_mahasiswa(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM mahasiswa WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Data mahasiswa berhasil dihapus!')
    return redirect(url_for('data_mahasiswa'))
    return render_template('mahasiswa/data-mahasiswa.html', mahasiswa = data)


# Kelas
@app.route('/kelas')
def data_kelas():
    cur = mysql.connection.cursor()
    cur.execute('SELECT k.id, k.nama, d.nama_lengkap, j.nama FROM kelas as k LEFT OUTER JOIN jurusan as j ON k.jurusan_id = j.id LEFT OUTER JOIN dosen as d ON k.dosen_id = d.id ORDER BY id')
    data = cur.fetchall()
    cur.close()
    return render_template('kelas/data-kelas.html', kelas = data)

@app.route('/kelas/tambah', methods = ['GET'])
def tambah_kelas():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nama FROM jurusan")
    dataJurusan = cursor.fetchall()
    cursor.execute("SELECT id, nama_lengkap FROM dosen")
    dataDosen = cursor.fetchall()
    cursor.close()
    return render_template('kelas/tambah-kelas.html', jurusan = dataJurusan, dosen = dataDosen)

@app.route('/kelas/insert', methods=['POST'])
def add_kelas():
    if request.method == 'POST':
        nama = request.form['nama']
        dosen_id = request.form['dosen_id']
        jurusan_id = request.form['jurusan_id']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO kelas (nama, dosen_id, jurusan_id) VALUES (%s,%s,%s)", 
        (nama, dosen_id, jurusan_id))
        mysql.connection.commit()
        flash('Data kelas berhasil ditambahkan!')
        return redirect(url_for('data_kelas'))

@app.route('/kelas/edit/<int:id>', methods = ['GET'])
def get_kelas(id):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM kelas WHERE id = {id}")
    data = cur.fetchall()
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nama FROM jurusan")
    dataJurusan = cursor.fetchall()
    cursor.execute("SELECT id, nama_lengkap FROM dosen")
    dataDosen = cursor.fetchall()
    cursor.close()
    cur.close()
    print(data[0])
    return render_template('kelas/ubah-kelas.html', kelas = data[0], jurusan = dataJurusan, dosen = dataDosen)

@app.route('/kelas/update/<int:id>', methods=['POST'])
def update_kelas(id):
    if request.method == 'POST':
        nama = request.form['nama']
        dosen_id = request.form['dosen_id']
        jurusan_id = request.form['jurusan_id']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE kelas
            SET nama = %s, dosen_id = %s, jurusan_id = %s WHERE id = %s
        """, (nama, dosen_id, jurusan_id, id))
        flash('Data kelas berhasil diubah!')
        mysql.connection.commit()
        return redirect(url_for('data_kelas'))

@app.route('/kelas/delete/<int:id>', methods = ['POST','GET'])
def delete_kelas(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM kelas WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Data kelas berhasil dihapus!')
    return redirect(url_for('data_kelas'))
    return render_template('kelas/data-kelas.html', kelas = data)


# Mata Kuliah
@app.route('/mata-kuliah')
def data_matakuliah():
    cur = mysql.connection.cursor()
    cur.execute('SELECT m.id, m.nama, m.jumlah_sks, d.nama_lengkap, m.semester FROM mata_kuliah as m LEFT OUTER JOIN dosen as d ON m.dosen_id = d.id ORDER BY id')
    data = cur.fetchall()
    cur.close()
    return render_template('matakuliah/data-matakuliah.html', matakuliah = data)

@app.route('/mata-kuliah/tambah', methods = ['GET'])
def tambah_matakuliah():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nama_lengkap FROM dosen")
    dataDosen = cursor.fetchall()
    cursor.close()
    return render_template('matakuliah/tambah-matakuliah.html', dosen = dataDosen)

@app.route('/mata-kuliah/insert', methods=['POST'])
def add_matakuliah():
    if request.method == 'POST':
        nama = request.form['nama']
        jumlah_sks = request.form['jumlah_sks']
        dosen_id = request.form['dosen_id']
        semester = request.form['semester']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO mata_kuliah (nama, jumlah_sks, dosen_id, semester) VALUES (%s, %s, %s, %s)", 
        (nama, jumlah_sks, dosen_id, semester))
        mysql.connection.commit()
        flash('Data matakuliah berhasil ditambahkan!')
        return redirect(url_for('data_matakuliah'))

@app.route('/mata-kuliah/edit/<int:id>', methods = ['GET'])
def get_matakuliah(id):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT id, nama, jumlah_sks, semester, dosen_id FROM mata_kuliah WHERE id = {id}")
    matakuliah = cur.fetchall()
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nama_lengkap FROM dosen")
    dataDosen = cursor.fetchall()
    cursor.close()
    cur.close()
    return render_template('matakuliah/ubah-matakuliah.html', matakuliah = matakuliah[0], dosen = dataDosen)

@app.route('/mata-kuliah/update/<int:id>', methods=['POST'])
def update_matakuliah(id):
    if request.method == 'POST':
        nama = request.form['nama']
        jumlah_sks = request.form['jumlah_sks']
        dosen_id = request.form['dosen_id']
        semester = request.form['semester']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE mata_kuliah
            SET nama = %s, jumlah_sks = %s, dosen_id = %s, semester = %s WHERE id = %s
        """, (nama, jumlah_sks, dosen_id, semester, id))
        flash('Data matakuliah berhasil diubah!')
        mysql.connection.commit()
        return redirect(url_for('data_matakuliah'))

@app.route('/mata-kuliah/delete/<int:id>', methods = ['POST','GET'])
def delete_matakuliah(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM mata_kuliah WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Data matakuliah berhasil dihapus!')
    return redirect(url_for('data_matakuliah'))
    return render_template('matakuliah/data-matakuliah.html', matakuliah = data)


# Jurusan
@app.route('/jurusan')
def data_jurusan():
    cur = mysql.connection.cursor()
    cur.execute('SELECT j.id, j.nama, d.nama_lengkap FROM jurusan as j LEFT OUTER JOIN dosen as d ON j.dosen_id = d.id ORDER BY id')
    data = cur.fetchall()
    cur.close()
    return render_template('jurusan/data-jurusan.html', jurusan = data)

@app.route('/jurusan/tambah', methods = ['GET'])
def tambah_jurusan():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nama_lengkap FROM dosen")
    dataDosen = cursor.fetchall()
    cursor.close()
    return render_template('jurusan/tambah-jurusan.html', dosen = dataDosen)

@app.route('/jurusan/insert', methods=['POST'])
def add_jurusan():
    if request.method == 'POST':
        nama = request.form['nama']
        dosen_id = request.form['dosen_id']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO jurusan (nama, dosen_id) VALUES (%s, %s)", 
        (nama, dosen_id))
        mysql.connection.commit()
        flash('Data jurusan berhasil ditambahkan!')
        return redirect(url_for('data_jurusan'))

@app.route('/jurusan/edit/<int:id>', methods = ['GET'])
def get_jurusan(id):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM jurusan WHERE id = {id}")
    jurusan = cur.fetchall()
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nama_lengkap FROM dosen")
    dataDosen = cursor.fetchall()
    cursor.close()
    cur.close()
    print(jurusan[0])
    return render_template('jurusan/ubah-jurusan.html', jurusan = jurusan[0], dosen = dataDosen)

@app.route('/jurusan/update/<int:id>', methods=['POST'])
def update_jurusan(id):
    if request.method == 'POST':
        nama = request.form['nama']
        dosen_id = request.form['dosen_id']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE jurusan
            SET nama = %s, dosen_id = %s WHERE id = %s
        """, (nama, dosen_id, id))
        flash('Data jurusan berhasil diubah!')
        mysql.connection.commit()
        return redirect(url_for('data_jurusan'))

@app.route('/jurusan/delete/<int:id>', methods = ['POST','GET'])
def delete_jurusan(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM jurusan WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Data jurusan berhasil dihapus!')
    return redirect(url_for('data_jurusan'))
    return render_template('jurusan/data-jurusan.html', jurusan = data)


# dosen
@app.route('/dosen')
def data_dosen():
    cur = mysql.connection.cursor()
    cur.execute('SELECT d.id, d.nama_lengkap, d.alamat, d.jenis_kelamin, d.tanggal_lahir FROM dosen as d ORDER BY id')
    data = cur.fetchall()
    cur.close()
    return render_template('dosen/data-dosen.html', dosen = data)

@app.route('/dosen/tambah', methods = ['GET'])
def tambah_dosen():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nama_lengkap, alamat, jenis_kelamin, tanggal_lahir FROM dosen")
    dataDosen = cursor.fetchall()
    cursor.close()
    return render_template('dosen/tambah-dosen.html', dosen = dataDosen)

@app.route('/dosen/insert', methods=['POST'])
def add_dosen():
    if request.method == 'POST':
        nama_lengkap = request.form['nama_lengkap']
        alamat = request.form['alamat']
        jenis_kelamin = request.form['jenis_kelamin']
        tanggal_lahir = request.form['tanggal_lahir']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO dosen (nama_lengkap, alamat, jenis_kelamin, tanggal_lahir) VALUES (%s,%s,%s,%s)", 
        (nama_lengkap, alamat, jenis_kelamin, tanggal_lahir))
        mysql.connection.commit()
        flash('Data dosen berhasil ditambahkan!')
        return redirect(url_for('data_dosen'))

@app.route('/dosen/edit/<int:id>', methods = ['GET'])
def get_dosen(id):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT id, nama_lengkap, alamat, jenis_kelamin, tanggal_lahir FROM dosen WHERE id = {id}")
    dosen = cur.fetchall()
    cur.close()
    cur.close()
    print(dosen[0])
    return render_template('dosen/ubah-dosen.html', dosen = dosen[0])

@app.route('/dosen/update/<int:id>', methods=['POST'])
def update_dosen(id):
    if request.method == 'POST':
        nama_lengkap = request.form['nama_lengkap']
        alamat = request.form['alamat']
        jenis_kelamin = request.form['jenis_kelamin']
        tanggal_lahir = request.form['tanggal_lahir']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE dosen
            SET nama_lengkap = %s, alamat = %s, jenis_kelamin = %s, tanggal_lahir = %s WHERE id = %s
        """, (nama_lengkap, alamat, jenis_kelamin, tanggal_lahir, id))
        flash('Data dosen berhasil diubah!')
        mysql.connection.commit()
        return redirect(url_for('data_dosen'))

@app.route('/dosen/delete/<int:id>', methods = ['POST','GET'])
def delete_dosen(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM dosen WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Data dosen berhasil dihapus!')
    return redirect(url_for('data_dosen'))
    return render_template('dosen/data-dosen.html', dosen = data)

# starting the app
if __name__ == "__main__":
    app.run(port=9999, debug=True)