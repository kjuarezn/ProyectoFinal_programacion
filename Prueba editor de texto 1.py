import tkinter as tk
from tkinter import *
from tkinter import messagebox as ms
from tkinter import filedialog as fd
from tkinter import scrolledtext as st
import tkinter as tk
import re



class LineNumbers(tk.Text):
    def __init__(self, master, text_widget, **kwargs):
        super().__init__(master, **kwargs)

        self.text_widget = text_widget
        self.text_widget.bind('<KeyPress>', self.on_key_press)

        self.insert(1.0, '1')
        self.configure(state='disabled')

    def on_key_press(self, event=None):
        final_index = str(self.text_widget.index(tk.END))
        num_of_lines = final_index.split('.')[0]
        line_numbers_string = "\n".join(str(no + 1) for no in range(int(num_of_lines)-1))
        width = len(str(num_of_lines))

        self.configure(state='normal', width=width)
        self.delete(1.0, tk.END)
        self.insert(1.0, line_numbers_string)
        self.configure(state='disabled')



def configure_tags(text_widget, tags):
    for tag, color in tags.items():
        text_widget.tag_delete(tag)
        text_widget.tag_config(tag, foreground=color)   

def on_key_release(text_widget):
    lines = text_widget.get(1.0, tk.END).splitlines()
    regex = re.compile(
        r"(^\s*"
        r"(?P<if><if>)" + "|"  
        r"(?P<htmlc></html>)" + "|"  
        r"(?P<html><html>)" +"|"
        r"(?P<h1><h1>)" +"|"
        r"(?P<h1c></h1>)" +"|"
        r"(?P<h2><h2>)" +"|"
        r"(?P<h2c></h2>)" +"|"
        r"(?P<DOCTYPE><!DOCTYPE html>)" +"|"
        r"(?P<head><head>)" +"|"
        r"(?P<headc></head)" +"|"
        r"(?P<body><body>)" +"|"
        r"(?P<bodyc></body>)" +"|"
        r"(?P<title><title>)" +"|"
        r"(?P<titlec></title>)" +"|"

         
        r"[\s\(]+)"
    )
    for idx, line in enumerate(lines):
        html_tag = f"html_{idx}"
        htmlc_tag = f"htmlc_{idx}"
        if_tag = f"if_{idx}"
        h1_tag = f"h1_{idx}"
        h1c_tag = f"h1c_{idx}"
        h2_tag = f"h2_{idx}"
        h2c_tag = f"h2c_{idx}"
        DOCTYPE_tag = f"DOCTYPE_{idx}"
        head_tag = f"head_{idx}"
        headc_tag = f"headc_{idx}"
        body_tag = f"body_{idx}"
        bodyc_tag = f"bodyc_{idx}"
        title_tag = f"title_{idx}"
        titlec_tag = f"titlec_{idx}"
        
        tags = {
            html_tag: "blue",
            htmlc_tag: "blue",
            if_tag: "blue",
            h1_tag: "blue",
            h1c_tag: "blue",
            h2_tag: "blue",
            h2c_tag: "blue",
            DOCTYPE_tag: "blue",
            head_tag: "blue",
            headc_tag: "blue",
            body_tag: "blue",
            bodyc_tag: "blue",
            title_tag: "blue",
            titlec_tag: "blue",
            
            # add new tag here
        }
        configure_tags(text_widget, tags)

        for match in regex.finditer(line):
            for tag in tags:
                group_name = tag.split("_")[0]
                if -1 != match.start(group_name):
                    text_widget.tag_add(
                        tag,
                        "{0}.{1}".format(idx+1, match.start(group_name)),
                        "{0}.{1}".format(idx+1, match.end(group_name))
                    )


if __name__ == '__main__':
    path = ""
    root = tk.Tk()
    
    root.title("Editor de texto")
    frame = Frame()
    frame.pack()
    text = st.ScrolledText(frame, font=("Times New Roman", 11))
    #llamado a contador de lineas
    t = tk.Text(root)
    l = LineNumbers(root, t, width=1)
    l.pack(side=tk.LEFT)
    t.pack(side=tk.LEFT, expand=1)
    t.bind("<KeyRelease>", lambda event: on_key_release(t))
    t.bind("<Enter>", lambda event: on_key_release(t))
    

    #Barra de menu

    #Primer menu de la barra llamada archivo

    def abrirArchivo():
        global path
        archivo = fd.askopenfilename(title="Abrir",
                                    filetypes=(("Todos los archivos", "*.*"), ("Archivos html", "*.html"),
                                                ("Archivos de texto", "*.txt")))
        arch1 = open(archivo, "r", encoding="utf-8")
        path = arch1.name
        contenido = arch1.read()
        arch1.close()
        t.delete("1.0", END)
        t.insert("1.0", contenido)

    

    def guardarArchivoComo():
        global path
        archivo = fd.asksaveasfilename(title="Guardar Como",
                                    filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"),("Archivos html",".html")),
                                    defaultextension=".txt")
        arch1 = open(archivo, "w", encoding="utf-8")
        path = arch1.name
        arch1.write(t.get("1.0", END))
        arch1.close()
        ms.showinfo("Guardar Como", "El archivo se guardó con exito.")

    def guardarArchivo():
        global path
        archivo = fd.asksaveasfilename(title="Guardar ",
                                    filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"),("Archivos html",".html")),
                                    defaultextension=".txt")
        arch1 = open(archivo, "w", encoding="utf-8")
        path = arch1.name
        arch1.write(t.get("1.0", END))
        arch1.close()
        ms.showinfo("Guardar", "El archivo se guardó con exito.")

    def guardar():
        if path != "":
            contenido = t.get(1.0, 'end-1c')
            archivo = open(path, 'w+')
            archivo.write(contenido)
            archivo.close()
            ms.showinfo("Confirmación", "Archivo guardado correctamente")
        else:
            guardarArchivo()

    def salir():
        valor = ms.askquestion("Cerrar", "¿Seguro que quieres salir?")

        if valor == "yes":
            root.destroy()
        
    
    #Segundo menu de la barra tareas llamada edición

    def cortar():
        t.clipboard_clear()
        t.clipboard_append(t.selection_get())
        t.delete("sel.first", "sel.last")
    
    def copiar():
        text.clipboard_clear()
        text.clipboard_append(text.selection_get())

    def pegar():
        t.insert(INSERT, t.clipboard_get())

    #de la barra menu las funciones de buscar y reemplazar

    entry_find = Entry(frame)
    
    def find1():
        t.tag_remove('found', '1.0', END)
        s = entry_find.get()
        if (s):
            index = '1.0'
            while 1:
                index = t.search(s, index, nocase=1, stopindex=END)
                if not index:
                    break
                lastindex = '% s+% dc' % (index, len(s))
                t.tag_add('found', index, lastindex)
                index = lastindex
            t.tag_config('found', foreground='red')
        entry_find.focus_set()


    find_btn = Button(frame, text='Buscar', command=find1)


    def closeSearch():
        close_find.pack_forget()
        find_btn.pack_forget()
        entry_find.pack_forget()
        close_replace.pack_forget()
        entry_replace.pack_forget()
        replace_btn.pack_forget()


    close_find = Button(frame, text='x', command=closeSearch)


    def find():
        close_find.pack(side=LEFT)
        entry_find.pack(side=LEFT, fill=BOTH, expand=1)
        entry_find.focus_set()
        find_btn.pack(side=LEFT)


    entry_replace = Entry(frame)


    def replace1():
        t.tag_remove('found', '1.0', END)
        s = entry_find.get()
        r = entry_replace.get()

        if (s and r):
            index = '1.0'
            while 1:
                index = t.search(s, index, nocase=1, stopindex=END)
                if not index:
                    break
                lastindex = '% s+% dc' % (index, len(s))
                t.delete(index, lastindex)
                t.insert(index, r)
                lastindex = '% s+% dc' % (index, len(r))
                t.tag_add('found', index, lastindex)
                index = lastindex
            text.tag_config('found', foreground='green', background='yellow')
        entry_find.focus_set()


    replace_btn = Button(frame, text='Reemplazar', command=replace1)


    def closeReplace():
        close_replace.pack_forget()
        entry_replace.pack_forget()
        replace_btn.pack_forget()


    close_replace = Button(frame, text='x', command=closeReplace)


    def replace():
        find()
        close_replace.pack(side=LEFT)
        entry_replace.pack(side=LEFT, fill=BOTH, expand=1)
        entry_replace.focus_set()
        replace_btn.pack(side=LEFT)



    
    #Se establece la barra menu

    barraMenu = Menu()
    root.config(menu=barraMenu, width=300, height=300)
        
    files = Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Arhivo", menu=files)
    files.add_command(label="Abrir Archivo", command=abrirArchivo)
    files.add_separator()
    files.add_command(label="Guardar", command=guardar)
    files.add_command(label="Guardar Como", command=guardarArchivoComo)
    files.add_separator()

    files.add_command(label="Salir", command=salir)

    edit = Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Editar", menu=edit)
    edit.add_command(label="Cortar", command=cortar)
    edit.add_command(label="Copiar", command=copiar)
    edit.add_command(label="Pegar", command=pegar)
    edit.add_separator()
    edit.add_command(label="Buscar", command=find)
    edit.add_command(label="Reemplazar", command=replace)

    tools = Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Herramientas", menu=tools)
    tools.add_command(label="Configuración")
    tools.add_command(label="Preferencias")




    
    
   

    
    
    root.mainloop()