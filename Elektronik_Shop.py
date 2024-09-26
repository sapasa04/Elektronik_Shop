import mysql.connector

def hubungkan_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        database="elektronik_shop"  
    )
    
def tambah_produk():
    mydb = hubungkan_database()
    mycursor = mydb.cursor()
    
    nama_produk = input("Masukkan nama produk baru: ")
    harga = int(input("Masukkan harga produk: "))

    query_tambah_produk = "INSERT INTO products (name, price) VALUES (%s, %s)"
    data_produk = (nama_produk, harga)
    mycursor.execute(query_tambah_produk, data_produk)
    mydb.commit()
    print("Produk berhasil ditambahkan.")

    mydb.close()


def lihat_produk():
    mydb = hubungkan_database()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM products")
    products = mycursor.fetchall()

    print("=== List Produk ===")
    for product in products:
        print(f"ID: {product[0]}\tNama: {product[1]}\tHarga: {product[2]}")

    mydb.close()

def edit_produk():
    mydb = hubungkan_database()
    mycursor = mydb.cursor()

    lihat_produk()

    produk_id = int(input("Masukkan ID produk yang akan diubah: "))
    new_nama = input("Masukkan nama baru: ")
    new_harga = int(input("Masukkan harga baru: "))

    query_edit_produk = "UPDATE products SET name = %s, price = %s WHERE id = %s"
    data_edit_produk = (new_nama, new_harga, produk_id)
    mycursor.execute(query_edit_produk, data_edit_produk)
    mydb.commit()
    print("Produk berhasil diubah.")

    mydb.close()


def hapus_produk():
    mydb = hubungkan_database()
    mycursor = mydb.cursor()

    lihat_produk()

    produk_id = int(input("Masukkan ID produk yang akan dihapus: "))

    query_hapus_produk = "DELETE FROM products WHERE id = %s"
    data_hapus_produk = (produk_id,)
    mycursor.execute(query_hapus_produk, data_hapus_produk)
    mydb.commit()
    print("Produk berhasil dihapus.")
    mydb.close()
    
def lihat_transaksi():
    mydb = hubungkan_database()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM transactions")
    transactions = mycursor.fetchall()

    print("=== Histori Transaksi ===")
    for transaction in transactions:
        print(f"ID Transaksi: {transaction[0]}\tProduk ID: {transaction[1]}\tNama Penerima: {transaction[2]}\tAlamat Penerima: {transaction[3]}\tTotal Harga: {transaction[7]}")

    mydb.close()

def menu_utama_admin():
    while True:
        print("=== Menu Utama Admin ===")
        print("1. Tambah Produk")
        print("2. Lihat Produk")
        print("3. Edit Produk")
        print("4. Hapus Produk")
        print("5. Lihat Histori Transaksi") 
        print("6. Keluar")

        pilihan = input("Pilih menu (1-6): ")

        if pilihan == "1":
            tambah_produk()
        elif pilihan == "2":
            lihat_produk()
        elif pilihan == "3":
            edit_produk()
        elif pilihan == "4":
            hapus_produk()
        elif pilihan == "5":
            lihat_transaksi()  
        elif pilihan == "6":
            print("Terima kasih.")
            break
        else:
            print("Pilihan tidak valid. Silakan pilih lagi.")

    
def admin_interface():
    while True:
        print("=== Admin Interface ===")
        print("1. Kelola Produk")
        print("2. Keluar")

        admin_pilihan = input("Pilih menu (1/2): ")

        if admin_pilihan == "1":
            menu_utama_admin()
        elif admin_pilihan == "2":
            print("Terima kasih, Anda keluar dari Admin Interface.")
            break
        else:
            print("Pilihan tidak valid. Silakan pilih lagi.")
            


def lihat_produk():
    mydb = hubungkan_database()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM products")
    products = mycursor.fetchall()

    print("=== List Produk ===")
    for product in products:
        print(f"ID: {product[0]}\tNama: {product[1]}\tHarga: {product[2]}")

    mydb.close()

def user_interface():
    while True:
        print("=== User Interface ===")
        print("1. Lihat Produk")
        print("2. Melakukan Transaksi")
        print("3. Keluar")

        user_pilihan = input("Pilih menu (1-3): ")

        if user_pilihan == "1":
            lihat_produk()
        elif user_pilihan == "2":
            transaksi()
        elif user_pilihan == "3":
            print("Terima kasih, Telah mengunjungi Toko Kami.")
            break
        else:
            print("Pilihan tidak valid. Silakan pilih lagi.")
            

def transaksi():
    mydb = hubungkan_database()
    mycursor = mydb.cursor()

    keranjang = []  

    try:
        while True:
            lihat_produk()  

            produk_id = int(input("Masukkan ID produk yang ingin Anda beli (atau 0 untuk selesai): "))
            
            if produk_id == 0:
                break 

            jumlah = int(input("Masukkan jumlah produk yang ingin Anda beli: "))

            query_produk = "SELECT * FROM products WHERE id = %s"
            mycursor.execute(query_produk, (produk_id,))
            product = mycursor.fetchone()

            if not product:
                print("Produk tidak ditemukan.")
                continue

            total_harga = jumlah * product[2]

            is_product_in_cart = any(item['produk_id'] == produk_id for item in keranjang)
            if is_product_in_cart:
                index = next((index for index, item in enumerate(keranjang) if item['produk_id'] == produk_id), None)
                if index is not None:
                    update_item = lambda item: {'jumlah': item['jumlah'] + jumlah, 'total_harga': item['total_harga'] + (jumlah * item['harga'])}
                    keranjang[index].update(update_item(keranjang[index]))
                    print("Jumlah produk dalam keranjang berhasil diperbarui.")
            else:
                keranjang.append({
                    'produk_id': produk_id,
                    'jumlah': jumlah,
                    'harga': product[2],
                    'total_harga': total_harga
                })
                print("Produk berhasil dimasukkan ke keranjang.")

            batalkan_produk = input("Apakah ada barang yang tidak jadi dibeli? (ya/tidak): ")
            if batalkan_produk.lower() == "ya":
                batalkan_id = int(input("Masukkan ID produk yang ingin dibatalkan: "))
                keranjang = [item for item in keranjang if item['produk_id'] != batalkan_id]
                print("Produk berhasil dibatalkan dari keranjang.")
            
            tambah_lagi = input("Apakah Anda ingin menambah produk lain ke keranjang? (ya/tidak): ")
            if tambah_lagi.lower() != "ya":
                break

        if not keranjang:
            print("Keranjang belanja kosong.")
            return

        nama_penerima = input("Masukkan nama penerima: ")
        alamat_penerima = input("Masukkan alamat penerima: ")
        telephone = input("Masukkan nomor telepon: ")

        print("Pilih kurir pengiriman:")
        print("1. JNE")
        print("2. TIKI")
        print("3. Pos Indonesia")
        kurir_pengiriman = input("Pilih kurir (JNE/TIKI/Pos Indonesia): ")

        kurir_pengiriman = kurir_pengiriman.lower()

        if kurir_pengiriman not in ['jne', 'tiki', 'pos indonesia']:
            print("Pilihan kurir tidak valid.")
            return

        for item in keranjang:
            produk_id = item['produk_id']
            jumlah = item['jumlah']
            total_harga = item['total_harga']

            insert_transaksi_query = "INSERT INTO transactions (product_id, nama_penerima, alamat_penerima, telephone, kurir_pengiriman, metode_pembayaran, harga) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            transaksi_data = (produk_id, nama_penerima, alamat_penerima, telephone, kurir_pengiriman, 'Cash', total_harga)
            mycursor.execute(insert_transaksi_query, transaksi_data)

        mydb.commit()
        print("Transaki Berhasil.")
        print("Terima kasih atas pembelian Anda.")
        
    except Exception as e:
        print("Terjadi kesalahan:", e)
    finally:
        mydb.close()




import re

def is_valid_password(password):
    # Pola ekspresi reguler untuk validasi format password:
    # - Setidaknya 8 karakter
    # - Minimal satu huruf besar, satu huruf kecil, dan satu angka
    # - Dapat berisi karakter khusus seperti !@#$%^&*()-_+=
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d!@#$%^&*()-_+=]{8,}$'
    return re.match(pattern, password) is not None

def register():
    mydb = hubungkan_database()
    mycursor = mydb.cursor()

    print("Pilih role untuk registrasi:")
    print("1. Admin")
    print("2. User")
    role_choice = input("Pilih role (1/2): ")

    if role_choice == "1":
        role = "admin"
    elif role_choice == "2":
        role = "user"
    else:
        print("Pilihan tidak valid.")
        return

    username = input("Masukkan Username baru: ")
    password = input("Masukkan Password baru: ")

    # Validasi format password menggunakan ekspresi reguler
    if not is_valid_password(password):
        print("Format password tidak valid.")
        return

    # Lanjutkan proses registrasi
    check_existing_user_query = "SELECT * FROM users WHERE username = %s"
    mycursor.execute(check_existing_user_query, (username,))
    existing_user = mycursor.fetchone()

    if existing_user:
        print("----- Username sudah terdaftar! Silahkan masukkan username lain. -----")
    else:
        insert_user_query = (
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
        )
        user_data = (username, password, role)
        mycursor.execute(insert_user_query, user_data)
        mydb.commit()
        print("----- Registrasi berhasil sebagai", role, "-----")

    mydb.close()


def login():
    mydb = hubungkan_database()
    mycursor = mydb.cursor()

    username = input("Masukan Username: ")
    password = input("Masukan Password: ")

    sql = "SELECT * FROM users WHERE username = %s AND password = %s"
    val = (username, password)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()

    mydb.close()

    if result:
        print("----- Selamat Anda Berhasil Login -----")
        if result[3] == "admin":
            print("Anda berhasil login sebagai Admin.")
            admin_interface()  
        else:
            user_interface()  
    else:
        print("----- Akun yang Anda masukkan tidak terdaftar -----")
        

def login_or_register():
    while True:
        print("=== Selamat Datang  Di Toko Elektronik Shop ===")
        print("1. Login")
        print("2. Register")
        print("3. Keluar")

        choice = input("Pilih menu (1-3): ")

        if choice == "1":
            login()
            break
        elif choice == "2":
            register()
        elif choice == "3":
            print("Terima kasih, Telah mengunjungi Toko Kami.")
            break
        else:
            print("Pilihan tidak valid. Silakan pilih lagi.")

if __name__ == "__main__":
    login_or_register()