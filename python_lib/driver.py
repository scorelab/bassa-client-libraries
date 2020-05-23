from bassa import Bassa

client = Bassa("http://localhost:5000/")
client.login(user_name="rand", password="pass")
#client.start_download()
client.add_download_request(download_link="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/MESS_MENU_2018.jpg/640px-MESS_MENU_2018.jpg")
res= client.get_downloads_request(limit=1)
print (res)

