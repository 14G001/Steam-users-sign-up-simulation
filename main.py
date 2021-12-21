import tkinter as tk
import sqlite3 # Guardo los datos que ingresan los usuarios en una base de datos SQLite para poder verlos con DB Browser for SQLite.



# --- --------- --- #
# --- funciones --- #
# --- --------- --- #

def signup(next_id_number):
	if e_name.get() != "" and e_password.get() != "":
		user = (next_id_number[0], e_name.get(), e_password.get())
	else:
		print("No puede haber usuario o contrasena vacios.")
		return

	users_cursor.execute("INSERT INTO users VALUES (?, ?, ?)", user)

	db_users.commit()
	next_id_number[0] += 1


def thereAreNoNews():
	t_noNewGaemes = tk.Label(text = "There are no new games")
	t_noNewGaemes.place(x = 155, y = 120)


def exit():
	db_users.commit()
	db_users.close()
	quit()




# --- ---- --- #
# --- main --- #
# --- ---- --- #


# Database init:
db_users = sqlite3.connect("Users.db")
users_cursor = db_users.cursor()

try:
	users_cursor.execute("CREATE TABLE users (id INT, name TEXT, password TEXT)")
except sqlite3.OperationalError:
	# Table alredy created
	pass

# SELECT * FROM users DESC LIMIT 1 # Con eso solo retorna el primero.
# Con la siguiente funcion de SQLite, se obtiene el ultimo registro por orden de la columna "id":
users_cursor.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1") # TOMAR SOLO EL ULTIMO REGISTRO (Para saber cual era la ultima ID) (Si tomaramos todos usariamos muchisima memoeia innecesariamente).

response_content = users_cursor.fetchall()
# Creo lo siguiente como lista en vez de como entero para que retorne el valor al pasar por la funcion "signup"
next_id_number = []

if len(response_content) > 0: # No habia registros en la base de datos.
	next_id_number.append(response_content[0][0] + 1) # response_content = [(<id mas alta en la base>, "nombre", "pass")]
else:
	next_id_number.append(0)

#print(next_id_number)




# Main window:
window = tk.Tk()
window.config(width = 300, heigh = 400)
window.title("Pruebas 1")


t_description = tk.Label(text = "Strem client sign up")
t_description.place(x = 80, y = 10)


# Steam logo:
logo = tk.PhotoImage(file = "Logo.png")
imagen = tk.Label(image = logo)
imagen.place(x = 10, y = 10)


# Username:
t_name = tk.Label(text = "Username:")
t_name.place(x = 20, y = 90)

e_name = tk.Entry()
e_name.place(x = 20, y = 120)


# Password:
t_password = tk.Label(text = "Password:")
t_password.place(x = 20, y = 160)

e_password = tk.Entry()
e_password.place(x = 20, y = 190)


# Login button:
b_login = tk.Button(text = "Sign up!", command = lambda:signup(next_id_number))
b_login.place(x = 220, y = 350)


# Exit button:
b_exit = tk.Button(text = "Exit", command = exit)
b_exit.place(x = 20, y = 350)


# News
t_news = tk.Label(text = "News:")
t_news.place(x = 200, y = 80)


try:
	with open("new_games.txt", "r") as file:
		textLines = file.readlines()
		length = len(textLines)
		
		if length > 0:
			l_games = tk.Listbox()
		
			for i in range(0, length):
				l_games.insert(i, textLines[i])

			del textLines
			l_games.place(x = 170, y = 120, width = 110, height = 16.5*length)
		else:
			thereAreNoNews()

except FileNotFoundError:
	thereAreNoNews()


# Main window loop:
window.mainloop()