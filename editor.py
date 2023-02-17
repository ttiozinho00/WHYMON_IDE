from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess
import re

compiler = Tk()
compiler.title('WHYMON IDE')
file_path = ''

def set_file_path(path):
    global file_path
    file_path = path

def update_editor_tags():
    editor.event_generate("<<Idle>>")
    
def on_idle(arg):
    editor.after(500, update_editor_tags)
        
def open_file():
    global file_path
    path = askopenfilename(filetypes=[('Python Files', '*.py'),('Java Files', '*.java'),('C++ Files', '*.cpp'),('C Files', '*.c')])
    if not path:
        return
    
    file_type = path.split('.')[-1]  
    language = None

    if file_type == 'py':
        language = 'python'
    elif file_type == 'java':
        language = 'java'
    elif file_type == 'cpp':
        language = 'c++'
    elif file_type == 'c':
        language = 'c'    
    else:
        return

    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        set_file_path(path)

    update_editor_tags() # chama a função para atualizar as tags
        
def save_as():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Python Files', '*.py'),('Java Files', '*.java'),('C++ Files', '*.cpp'),('C Files', '*.c')])
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        set_file_path(path)
        
def run():
    if file_path == '':
        save_prompt = Toplevel()
        text = Label(save_prompt, text='Salve seu código')
        text.pack()
        return
    
    extension = file_path.split('.')[-1]
    
    if extension == 'py':
        command = f'python "{file_path}" -o "{file_path.split(".")[0]}.exe" && "{file_path.split(".")[0]}.exe"'
    elif extension == 'java':
        command = f'javac "{file_path}" -o "{file_path.split(".")[0]}.exe" && "{file_path.split(".")[0]}.exe"'
    elif extension == 'c':
        command = f'gcc "{file_path}" -o "{file_path.split(".")[0]}.exe" && "{file_path.split(".")[0]}.exe"'
    elif extension == 'cpp':
        command = f'g++ "{file_path}" -o "{file_path.split(".")[0]}.exe" && "{file_path.split(".")[0]}.exe"'
    else:
        code_output.insert('1.0', f'Extensão {extension} não suportada.\n')
        return
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    code_output.insert('1.0', output.decode('utf-8'))
    code_output.insert('1.0', error.decode('utf-8'))

def on_text_changed(event):
    editor.tag_configure("keyword", foreground="blue")
    editor.tag_configure("string", foreground="red")
    editor.tag_configure("comment", foreground="gray")
    
    editor.mark_set("range_start", "1.0")
    data = editor.get("1.0", "end-1c")
    
    pattern = r"\b(for|while|if|elif|else|def|class|print|return)\b"
    for tag, idx, *_ in re.findall(pattern, data):
        editor.tag_configure(tag, foreground="blue")
        editor.tag_add(tag, f"{idx} linestart", f"{idx} lineend +1c")
    
    pattern = r"(['\"].*?['\"])"
    for tag, idx, *_ in re.findall(pattern, data):
        editor.tag_configure("string", foreground="red")
        editor.tag_add("string", f"{idx}", f"{idx}.end")
    
    pattern = r"(#.*?)$"
    for tag, idx in re.findall(pattern, data, re.MULTILINE):
        editor.tag_configure("comment", foreground="gray")
        editor.tag_add("comment", f"{idx} linestart", f"{idx} lineend")

menu_bar = Menu(compiler)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Abrir', command=open_file)
file_menu.add_command(label='Salvar', command=save_as)
file_menu.add_command(label='Salvar como', command=save_as)
file_menu.add_command(label='Sair', command=exit)
menu_bar.add_cascade(label='Arquivo', menu=file_menu)

run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Rodar', command=run)
menu_bar.add_cascade(label='Rodar', menu=run_bar)

compiler.config(menu=menu_bar)
editor = Text(compiler)
editor.pack()
editor.bind("<<Idle>>", on_idle)
editor.bind("<<Modified>>", on_text_changed)
code_output = Text(height=10)
code_output.pack()
compiler.mainloop()