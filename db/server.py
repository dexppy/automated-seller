import os

def start_server():
    try:
        os.startfile("C:/xampp/apache_start.bat")
        os.startfile("C:/xampp/mysql_start.bat")
        print("Server is running")
    except Exception as  e:
        print(f"Could't run server: {e}")


def stop_server():
    try:
        os.startfile("C:/xampp/apache_stop.bat")
        os.startfile("C:/xampp/mysql_stop.bat")
        print("Server is stopped")
    except Exception as  e:
        print(f"Could't stop server: {e}")