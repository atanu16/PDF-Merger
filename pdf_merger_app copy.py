import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfWriter
import threading
import time
import os

# ---------------- CREDIT SLIDE ----------------
def show_credit(root):
    credit = tk.Toplevel(root)
    credit.overrideredirect(True)
    credit.configure(bg="#1e1e1e")

    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()

    w, h = 300, 80
    x, y = -w, sh - h - 40
    credit.geometry(f"{w}x{h}+{x}+{y}")

    tk.Label(
        credit, text="Developed by Atanu",
        fg="white", bg="#1e1e1e",
        font=("Segoe UI", 12, "bold")
    ).pack(expand=True)

    for i in range(35):
        credit.geometry(f"{w}x{h}+{int(-w + i*12)}+{y}")
        credit.update()
        time.sleep(0.02)

    credit.after(4000, credit.destroy)

# ---------------- PDF LOGIC ----------------
def merge_pdfs(files, output):
    writer = PdfWriter()
    for f in files:
        writer.append(f)
    with open(output, "wb") as out:
        writer.write(out)

def threaded_merge(files, output, loading):
    try:
        loading.pack()
        merge_pdfs(files, output)
        loading.pack_forget()
        messagebox.showinfo("Success", "PDFs merged successfully!")
    except Exception as e:
        loading.pack_forget()
        messagebox.showerror("Error", str(e))

# ---------------- MAIN APP ----------------
def main_ui():
    root = tk.Tk()
    root.title("PDF Merger")
    root.geometry("520x350")
    root.configure(bg="#121212")
    root.resizable(False, False)

    show_credit(root)

    # ---------- Frames ----------
    menu = tk.Frame(root, bg="#121212")
    single = tk.Frame(root, bg="#121212")
    multiple = tk.Frame(root, bg="#121212")

    for f in (menu, single, multiple):
        f.place(x=0, y=0, width=520, height=350)

    def show(frame):
        frame.tkraise()

    # ---------- MENU ----------
    tk.Label(
        menu, text="PDF MERGER",
        fg="white", bg="#121212",
        font=("Segoe UI", 18, "bold")
    ).pack(pady=40)

    tk.Button(
        menu, text="Single PDF Merge",
        font=("Segoe UI", 12, "bold"),
        width=25, bg="#2d89ef", fg="white",
        command=lambda: show(single)
    ).pack(pady=10)

    tk.Button(
        menu, text="Multiple PDF Merge",
        font=("Segoe UI", 12, "bold"),
        width=25, bg="#00cc66", fg="black",
        command=lambda: show(multiple)
    ).pack(pady=10)

    # ---------- SINGLE MERGE ----------
    def browse(entry):
        path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)

    def save(entry):
        path = filedialog.asksaveasfilename(defaultextension=".pdf")
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)

    tk.Label(single, text="Single PDF Merge",
             fg="white", bg="#121212",
             font=("Segoe UI", 14, "bold")).pack(pady=10)

    sf = tk.Frame(single, bg="#121212")
    sf.pack(pady=10)

    e1 = tk.Entry(sf, width=42)
    e2 = tk.Entry(sf, width=42)
    eout = tk.Entry(sf, width=42)

    tk.Button(sf, text="PDF 1", command=lambda: browse(e1)).grid(row=0, column=0)
    e1.grid(row=0, column=1)

    tk.Button(sf, text="PDF 2", command=lambda: browse(e2)).grid(row=1, column=0)
    e2.grid(row=1, column=1)

    tk.Button(sf, text="Save As", command=lambda: save(eout)).grid(row=2, column=0)
    eout.grid(row=2, column=1)

    loading1 = tk.Label(single, text="Merging...", fg="yellow", bg="#121212")

    tk.Button(
        single, text="MERGE",
        bg="#00cc66", font=("Segoe UI", 11, "bold"),
        command=lambda: threading.Thread(
            target=threaded_merge,
            args=([e1.get(), e2.get()], eout.get(), loading1),
            daemon=True
        ).start()
    ).pack(pady=10)

    tk.Button(single, text="⬅ Back", command=lambda: show(menu)).pack()

    # ---------- MULTIPLE MERGE ----------
    tk.Label(multiple, text="Multiple PDF Merge",
             fg="white", bg="#121212",
             font=("Segoe UI", 14, "bold")).pack(pady=10)

    mf = tk.Frame(multiple, bg="#121212")
    mf.pack(pady=10)

    folder_entry = tk.Entry(mf, width=42)
    out_entry = tk.Entry(mf, width=42)

    def browse_folder():
        path = filedialog.askdirectory()
        if path:
            folder_entry.delete(0, tk.END)
            folder_entry.insert(0, path)

    tk.Button(mf, text="Select Folder", command=browse_folder).grid(row=0, column=0)
    folder_entry.grid(row=0, column=1)

    tk.Button(mf, text="Save As", command=lambda: save(out_entry)).grid(row=1, column=0)
    out_entry.grid(row=1, column=1)

    loading2 = tk.Label(multiple, text="Merging...", fg="yellow", bg="#121212")

    def merge_folder():
        folder = folder_entry.get()
        files = sorted([
            os.path.join(folder, f)
            for f in os.listdir(folder)
            if f.lower().endswith(".pdf")
        ])
        threading.Thread(
            target=threaded_merge,
            args=(files, out_entry.get(), loading2),
            daemon=True
        ).start()

    tk.Button(
        multiple, text="MERGE ALL PDFs",
        bg="#00cc66", font=("Segoe UI", 11, "bold"),
        command=merge_folder
    ).pack(pady=10)

    tk.Button(multiple, text="⬅ Back", command=lambda: show(menu)).pack()

    show(menu)
    root.mainloop()

if __name__ == "__main__":
    main_ui()
