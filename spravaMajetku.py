import sqlite3
from tkinter import font


def init_db():
    connection = sqlite3.connect("firemni_majetek.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS majetek (
        id INTEGER PRIMARY KEY,
        nazev TEXT NOT NULL,
        popis TEXT,
        datum_nakupu DATE,
        cena REAL,
        stav TEXT,
        umisteni TEXT
    )
    """)

    connection.commit()
    connection.close()


import tkinter as tk
from tkinter import ttk, messagebox




def search_majetek_by_nazev(nazev):
    connection = sqlite3.connect("firemni_majetek.db")
    cursor = connection.cursor()

    # Používám znaky % kolem názvu pro vyhledávání výskytu ve sloupci nazev
    cursor.execute("SELECT * FROM majetek WHERE nazev LIKE ?", ('%' + nazev + '%',))
    rows = cursor.fetchall()

    connection.close()

    return rows


def fetch_all_majetek():
    connection = sqlite3.connect("firemni_majetek.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM majetek")
    rows = cursor.fetchall()

    connection.close()

    return rows





def add_majetek(nazev, popis, datum, cena, stav, umisteni):
    connection = sqlite3.connect("firemni_majetek.db")
    cursor = connection.cursor()

    cursor.execute("INSERT INTO majetek (nazev, popis, datum_nakupu, cena, stav, umisteni) VALUES (?, ?, ?, ?, ?, ?)",
                   (nazev, popis, datum, cena, stav, umisteni))
    
    connection.commit()
    connection.close()

    messagebox.showinfo("Info", "Majetek byl přidán!")

def delete_majetek(id):
    connection = sqlite3.connect("firemni_majetek.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM majetek WHERE id=?", (id,))
    
    connection.commit()
    connection.close()

    messagebox.showinfo("Info", "Majetek byl odebrán!")

def main_gui():
    root = tk.Tk()
    root.title("Správa firemního majetku")
    button_font = font.Font(size=12, weight='bold')
    root.configure(bg='#90bcf2')

    

    

    ttk.Label(root, text="Vyhledat majetek podle názvu:").grid(row=10, column=0)
    search_entry = ttk.Entry(root)
    search_entry.grid(row=10, column=1)



    def handle_search():
        results = search_majetek_by_nazev(search_entry.get())
        
        # Aktualizujte seznam majetku podle výsledků vyhledávání
        for row in majetek_tree.get_children():
            majetek_tree.delete(row)
        for row in results:
            majetek_tree.insert("", "end", values=row)

    ttk.Button(root, text="Vyhledat", command=handle_search).grid(row=11, column=0, columnspan=2)

    ttk.Label(root, text="Název:").grid(row=0, column=0)
    nazev_entry = ttk.Entry(root)
    nazev_entry.grid(row=0, column=1)

    ttk.Label(root, text="Serial Number:").grid(row=1, column=0)
    popis_entry = ttk.Entry(root)
    popis_entry.grid(row=1, column=1)

    ttk.Label(root, text="Datum nákupu:").grid(row=2, column=0)
    datum_entry = ttk.Entry(root)
    datum_entry.grid(row=2, column=1)

    ttk.Label(root, text="Cena:").grid(row=3, column=0)
    cena_entry = ttk.Entry(root)
    cena_entry.grid(row=3, column=1)

    ttk.Label(root, text="Stav:").grid(row=4, column=0)
    stav_entry = ttk.Entry(root)
    stav_entry.grid(row=4, column=1)

    ttk.Label(root, text="Umístění:").grid(row=5, column=0)
    umisteni_entry = ttk.Entry(root)
    umisteni_entry.grid(row=5, column=1)

    def handle_add():
        add_majetek(
            nazev_entry.get(),
            popis_entry.get(),
            datum_entry.get(),
            cena_entry.get(),
            stav_entry.get(),
            umisteni_entry.get()
        )
        update_majetek_list()

    def handle_delete():
        try:
            id_majetku = int(id_entry.get())
            delete_majetek(id_majetku)
            update_majetek_list()
        except ValueError:
            messagebox.showerror("Chyba", "Prosím, zadejte platné ID majetku.")




    # Treeview pro zobrazení majetku
    columns = ("ID", "Název", "Popis", "Datum nákupu", "Cena", "Stav", "Umístění", "Akce")
    majetek_tree = ttk.Treeview(root, columns=columns, show="headings")

    for col in columns:
        majetek_tree.heading(col, text=col)
    majetek_tree.grid(row=9, column=0, columnspan=2, sticky="ew")


    for col in columns:
        majetek_tree.heading(col, text=col)
    majetek_tree.column("Akce", width=50)


    

    ttk.Button(root, text="Přidat majetek", command=handle_add).grid(row=6, column=0, columnspan=2)

    ttk.Label(root, text="ID majetku pro odebrání:").grid(row=7, column=0)
    id_entry = ttk.Entry(root)
    id_entry.grid(row=7, column=1)

    ttk.Button(root, text="Odebrat majetek", command=handle_delete).grid(row=8, column=0, columnspan=2)

    
    # Inicializace seznamu majetku při startu aplikace
    def update_majetek_list():
        for row in majetek_tree.get_children():
            majetek_tree.delete(row)

        for row in fetch_all_majetek():
            majetek_tree.insert("", "end", values=row + ("❌",))

    def on_majetek_tree_click(event):
        item = majetek_tree.identify('item', event.x, event.y)
        column = majetek_tree.identify('column', event.x, event.y)
        if column == "#8":
            id = majetek_tree.item(item, "values")[0]
            delete_majetek(id)
            update_majetek_list()

    majetek_tree.bind("<Button-1>", on_majetek_tree_click)
    update_majetek_list()


    root.mainloop()


if __name__ == "__main__":
    init_db()
    main_gui()
   


