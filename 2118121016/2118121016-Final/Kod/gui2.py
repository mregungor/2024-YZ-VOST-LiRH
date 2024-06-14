from tkinter import *
from tkinter import font
from tkinter import filedialog, messagebox
import tempfile
import os
from file_checker import checkFile



windowDesign = Tk()
IconPhoto = PhotoImage(master=windowDesign, file='C:/Users/Makbaba/Downloads/vir.png')
windowDesign.title('Virus Vigilante')
windowDesign.geometry('450x400')
windowDesign.resizable(width=True, height=True)
windowDesign.iconphoto(False, IconPhoto)
windowDesign.configure(bg='black')

selected_files = []
malware_files = []


def select_files():
    global selected_files
    filepaths = filedialog.askopenfilenames(
        title="Dosya Seçin",
        filetypes=(("Executable Files", "*.exe"), ("All Files", "*.*"))
    )

    if filepaths:
        selected_files = filepaths
        selected_files_text = "\n".join(filepaths)
        Label2.config(text=selected_files_text)


def analyze_files():
    global selected_files, malware_files
    malware_files = []  # Analiz her yapıldığında bu listeyi temizle

    if selected_files:
        for filepath in selected_files:
            with open(filepath, 'rb') as file:
                temp_file = tempfile.NamedTemporaryFile(delete=False)
                temp_file.write(file.read())

                legitimate = checkFile(temp_file.name)

                if legitimate:
                    messagebox.showinfo("Dosya Kontrolü", f"Dosya {os.path.basename(filepath)} İyi Huylu")
                else:
                    messagebox.showwarning("Dosya Kontrolü", f"Dosya {os.path.basename(filepath)} muhtemelen Malware")
                    malware_files.append(filepath)

        if malware_files:
            delete_button.config(state=NORMAL)
        else:
            delete_button.config(state=DISABLED)
    else:
        messagebox.showwarning("Dosya Seçilmedi", "Lütfen analiz etmek için önce dosya seçin.")


def delete_files():
    global malware_files
    for filepath in malware_files:
        try:
            os.remove(filepath)
            messagebox.showinfo("Dosya Silindi", f"Dosya {os.path.basename(filepath)} başarıyla silindi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya {os.path.basename(filepath)} silinirken bir hata oluştu: {e}")

    malware_files = []
    delete_button.config(state=DISABLED)
    clear_interface()


def clear_interface():
    global selected_files, malware_files
    selected_files = []
    malware_files = []
    Label2.config(text="")
    delete_button.config(state=DISABLED)


selectedFont4 = font.Font(name='font_4', family='Impact', size=12, weight='normal', slant='roman', underline=0,
                          overstrike=0)
selectedFont2 = font.Font(name='font_2', family='Berlin Sans FB', size=22, weight='normal', slant='roman', underline=0,
                          overstrike=0)
selectedFont5 = font.Font(name='font_5', family='Segoe UI', size=12, weight='normal', slant='roman', underline=0,
                          overstrike=0)

Button1 = Button(compound='bottom', font='font_4', image='', takefocus=True, text='Choose a PE File',
                 command=select_files,fg="red", bg="black")
Button1.place(x=160, y=107, height=45, width=131, anchor='nw')

analyze_button = Button(font='Impact', image='', takefocus=True, text='SCAN', command=analyze_files,fg="red", bg="black")
analyze_button.place(x=175, y=246, height=41, width=99, anchor='nw')

delete_button = Button(font='Impact', image='', takefocus=True, text='DELETE', command=delete_files,
                       state=DISABLED,fg="red", bg="black")
delete_button.place(x=175, y=300, height=41, width=99, anchor='nw')

clear_button = Button(font='Impact', image='', takefocus=True, text='CLEAR', command=clear_interface,fg="red", bg="black")
clear_button.place(x=175, y=350, height=41, width=99, anchor='nw')

Label1 = Label(font='font_2', image='', takefocus=True, text='Virus Vigilante',fg="red", bg="black")
Label1.place(x=134, y=43, height=30, width=185, anchor='nw')

Label2 = Label(font='font_5', image='', takefocus=True, text='', wraplength=400, justify=LEFT,fg="red", bg="black")
Label2.place(x=30, y=162, height=80, width=400, anchor='nw')



windowDesign.mainloop()