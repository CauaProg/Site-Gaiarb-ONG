# ═══════════════════════════════════════════════
# GAIARB – DESKTOP ADMIN CLIENT (TKINTER & API)
# ═══════════════════════════════════════════════

import tkinter as tk
from tkinter import ttk, messagebox
import requests
import sys

API_URL = "http://127.0.0.1:8000"
TOKEN = None
ADMIN_NAME = ""

class GaiarbAdminApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GAIARB – Sistema de Gestão do Administrador")
        self.root.geometry("1000x650")
        self.root.configure(bg="#f3f4f6")
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Color Palette
        self.style.configure(".", background="#f3f4f6", foreground="#1f2937")
        self.style.configure("TLabel", background="#f3f4f6", font=("Segoe UI", 10))
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#4f46e5", background="#f3f4f6")
        self.style.configure("Sub.TLabel", font=("Segoe UI", 11, "italic"), foreground="#4b5563", background="#f3f4f6")
        
        # Treeview styling
        self.style.configure("Treeview", font=("Segoe UI", 9), rowheight=25, background="#ffffff", fieldbackground="#ffffff")
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#e5e7eb", foreground="#1f2937")
        self.style.map("Treeview", background=[("selected", "#6366f1")], foreground=[("selected", "#ffffff")])
        
        # Setup Login Screen first
        self.show_login_screen()

    # ── LOGIN SCREEN ──────────────────────────────────
    def show_login_screen(self):
        self.login_frame = tk.Frame(self.root, bg="#ffffff", bd=1, relief="solid")
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center", width=420, height=350)
        
        # Inner padding frame
        inner = tk.Frame(self.login_frame, bg="#ffffff")
        inner.pack(padx=30, pady=30, fill="both", expand=True)
        
        lbl_title = tk.Label(inner, text="GAIARB", font=("Outfit", 26, "bold"), fg="#4f46e5", bg="#ffffff")
        lbl_title.pack(pady=(0, 5))
        
        lbl_subtitle = tk.Label(inner, text="Painel de Controle Administrativo", font=("Segoe UI", 10, "italic"), fg="#6b7280", bg="#ffffff")
        lbl_subtitle.pack(pady=(0, 20))
        
        # Username
        lbl_user = tk.Label(inner, text="Usuário:", font=("Segoe UI", 10, "bold"), fg="#374151", bg="#ffffff")
        lbl_user.pack(anchor="w")
        self.ent_user = ttk.Entry(inner, font=("Segoe UI", 11))
        self.ent_user.pack(fill="x", pady=(2, 12))
        self.ent_user.insert(0, "admin")  # Default placeholder
        
        # Password
        lbl_pass = tk.Label(inner, text="Senha:", font=("Segoe UI", 10, "bold"), fg="#374151", bg="#ffffff")
        lbl_pass.pack(anchor="w")
        self.ent_pass = ttk.Entry(inner, show="*", font=("Segoe UI", 11))
        self.ent_pass.pack(fill="x", pady=(2, 20))
        self.ent_pass.insert(0, "admin123")  # Default placeholder
        self.ent_pass.bind("<Return>", lambda e: self.perform_login())
        
        # Login Button
        btn_login = tk.Button(
            inner, 
            text="Entrar no Painel", 
            font=("Segoe UI", 11, "bold"), 
            bg="#4f46e5", 
            fg="#ffffff", 
            activebackground="#4338ca", 
            activeforeground="#ffffff", 
            relief="flat", 
            command=self.perform_login
        )
        btn_login.pack(fill="x", ipady=5)

    def perform_login(self):
        global TOKEN, ADMIN_NAME
        user = self.ent_user.get().strip()
        pwd = self.ent_pass.get().strip()
        
        if not user or not pwd:
            messagebox.showwarning("Campos Vazios", "Por favor, preencha o usuário e a senha!")
            return
            
        try:
            payload = {"username": user, "password": pwd}
            r = requests.post(f"{API_URL}/api/admin/login", json=payload, timeout=5)
            data = r.json()
            
            if r.status_code == 200 and data.get("success"):
                TOKEN = data.get("token")
                ADMIN_NAME = data.get("admin", {}).get("nome", "Administrador")
                
                # Clear login screen and load dashboard
                self.login_frame.destroy()
                self.show_dashboard()
            else:
                messagebox.showerror("Erro de Login", data.get("error", "Credenciais incorretas!"))
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao servidor backend em {API_URL}.\nCertifique-se de que o backend (server.py) esteja rodando!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    # ── MAIN DASHBOARD ────────────────────────────────
    def show_dashboard(self):
        # Header banner
        self.header_frame = tk.Frame(self.root, bg="#ffffff", height=60, bd=1, relief="ridge")
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)
        
        lbl_welcome = tk.Label(self.header_frame, text=f"Olá, {ADMIN_NAME} 👋", font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1f2937")
        lbl_welcome.pack(side="left", padx=20, pady=15)
        
        btn_logout = tk.Button(
            self.header_frame, 
            text="Sair", 
            font=("Segoe UI", 9, "bold"), 
            bg="#ef4444", 
            fg="#ffffff", 
            activebackground="#dc2626", 
            activeforeground="#ffffff", 
            relief="flat", 
            command=self.perform_logout
        )
        btn_logout.pack(side="right", padx=20, pady=12)
        
        # Tabs container (Notebook)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Build Tabs
        self.build_voluntarios_tab()
        self.build_equipe_tab()
        self.build_financeiro_tab()
        
        # Load initial data
        self.load_voluntarios()
        self.load_equipe()
        self.load_doacoes()

    def perform_logout(self):
        global TOKEN, ADMIN_NAME
        TOKEN = None
        ADMIN_NAME = ""
        # Remove widgets
        self.header_frame.destroy()
        self.notebook.destroy()
        # Relaunch login
        self.show_login_screen()

    # ── TAB 1: VOLUNTÁRIOS ────────────────────────────
    def build_voluntarios_tab(self):
        self.tab_vol = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_vol, text="Voluntários Inscritos")
        
        # Top tools frame
        tools = tk.Frame(self.tab_vol, bg="#f3f4f6")
        tools.pack(fill="x", padx=10, pady=10)
        
        lbl_title = ttk.Label(tools, text="Inscrições de Voluntários", style="Header.TLabel")
        lbl_title.pack(side="left", pady=5)
        
        btn_del = tk.Button(tools, text="🗑 Excluir Selecionado", font=("Segoe UI", 9, "bold"), bg="#ef4444", fg="#ffffff", relief="flat", command=self.delete_voluntario)
        btn_del.pack(side="right", padx=5)
        
        btn_ref = tk.Button(tools, text="🔄 Atualizar Lista", font=("Segoe UI", 9, "bold"), bg="#4f46e5", fg="#ffffff", relief="flat", command=self.load_voluntarios)
        btn_ref.pack(side="right", padx=5)
        
        # Table list
        cols = ("id", "nome", "email", "whatsapp", "area", "disponibilidade", "mensagem")
        self.tree_vol = ttk.Treeview(self.tab_vol, columns=cols, show="headings")
        
        self.tree_vol.heading("id", text="ID")
        self.tree_vol.heading("nome", text="Nome")
        self.tree_vol.heading("email", text="E-mail")
        self.tree_vol.heading("whatsapp", text="WhatsApp/Celular")
        self.tree_vol.heading("area", text="Área de Interesse")
        self.tree_vol.heading("disponibilidade", text="Disponibilidade")
        self.tree_vol.heading("mensagem", text="Mensagem / Observação")
        
        self.tree_vol.column("id", width=50, minwidth=40, anchor="center")
        self.tree_vol.column("nome", width=180, minwidth=120)
        self.tree_vol.column("email", width=180, minwidth=120)
        self.tree_vol.column("whatsapp", width=110, minwidth=90, anchor="center")
        self.tree_vol.column("area", width=150, minwidth=100)
        self.tree_vol.column("disponibilidade", width=130, minwidth=100)
        self.tree_vol.column("mensagem", width=200, minwidth=150)
        
        # Scrollbars
        sc_y = ttk.Scrollbar(self.tab_vol, orient="vertical", command=self.tree_vol.yview)
        sc_x = ttk.Scrollbar(self.tab_vol, orient="horizontal", command=self.tree_vol.xview)
        self.tree_vol.configure(yscrollcommand=sc_y.set, xscrollcommand=sc_x.set)
        
        self.tree_vol.pack(fill="both", expand=True, padx=10, pady=(0, 5))
        sc_y.pack(fill="y", side="right")
        sc_x.pack(fill="x", side="bottom")
        
        # Bind double-click to view message details
        self.tree_vol.bind("<Double-1>", self.view_volunteer_details)

    def load_voluntarios(self):
        self.tree_vol.delete(*self.tree_vol.get_children())
        try:
            h = {"Authorization": f"Bearer {TOKEN}"}
            r = requests.get(f"{API_URL}/api/admin/voluntarios", headers=h, timeout=5)
            if r.status_code == 200:
                data = r.json()
                for v in data:
                    self.tree_vol.insert("", "end", values=(
                        v.get("id"),
                        v.get("nome"),
                        v.get("email"),
                        v.get("whatsapp"),
                        v.get("area"),
                        v.get("disponibilidade"),
                        v.get("mensagem", "")
                    ))
            else:
                messagebox.showerror("Erro", "Não foi possível carregar os voluntários.")
        except Exception as e:
            messagebox.showerror("Erro de Conexão", str(e))

    def view_volunteer_details(self, event):
        sel = self.tree_vol.selection()
        if not sel:
            return
        item = self.tree_vol.item(sel[0])
        val = item["values"]
        
        # Popup detailing volunteer info
        detail_win = tk.Toplevel(self.root)
        detail_win.title(f"Ficha do Voluntário: {val[1]}")
        detail_win.geometry("500x380")
        detail_win.configure(bg="#ffffff")
        
        tk.Label(detail_win, text=f"Ficha Cadastral #{val[0]}", font=("Segoe UI", 14, "bold"), fg="#4f46e5", bg="#ffffff").pack(anchor="w", padx=20, pady=(20, 10))
        
        info = [
            ("Nome Completo:", val[1]),
            ("E-mail:", val[2]),
            ("WhatsApp:", val[3]),
            ("Área de Interesse:", val[4]),
            ("Disponibilidade:", val[5]),
        ]
        
        for label, content in info:
            row = tk.Frame(detail_win, bg="#ffffff")
            row.pack(fill="x", padx=20, pady=2)
            tk.Label(row, text=label, font=("Segoe UI", 9, "bold"), fg="#4b5563", width=18, anchor="w", bg="#ffffff").pack(side="left")
            tk.Label(row, text=content, font=("Segoe UI", 9), fg="#1f2937", bg="#ffffff").pack(side="left")
            
        tk.Label(detail_win, text="Mensagem de Apresentação:", font=("Segoe UI", 9, "bold"), fg="#4b5563", bg="#ffffff").pack(anchor="w", padx=20, pady=(15, 2))
        
        txt_msg = tk.Text(detail_win, font=("Segoe UI", 9), height=5, wrap="word", bg="#f9fafb", bd=1, relief="solid")
        txt_msg.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        txt_msg.insert("1.0", val[6])
        txt_msg.configure(state="disabled")

    def delete_voluntario(self):
        sel = self.tree_vol.selection()
        if not sel:
            messagebox.showwarning("Nenhum Item Selecionado", "Por favor, selecione um voluntário na tabela primeiro!")
            return
        item = self.tree_vol.item(sel[0])
        val = item["values"]
        
        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o cadastro do voluntário '{val[1]}'?"):
            try:
                r = requests.delete(f"{API_URL}/api/voluntarios/{val[0]}", timeout=5)
                if r.status_code == 200:
                    messagebox.showinfo("Sucesso", "Cadastro de voluntário excluído com sucesso!")
                    self.load_voluntarios()
                else:
                    messagebox.showerror("Erro", "Erro ao tentar deletar o voluntário.")
            except Exception as e:
                messagebox.showerror("Erro de Conexão", str(e))

    # ── TAB 2: EQUIPE (MEMBROS) ───────────────────────
    def build_equipe_tab(self):
        self.tab_eq = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_eq, text="Membros da Equipe")
        
        # Split layout: Form left, Table list right
        self.tab_eq.columnconfigure(0, weight=2)
        self.tab_eq.columnconfigure(1, weight=3)
        self.tab_eq.rowconfigure(0, weight=1)
        
        # Left Panel (Add Form)
        form_frame = tk.Frame(self.tab_eq, bg="#ffffff", bd=1, relief="solid")
        form_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Pad frame
        form_inner = tk.Frame(form_frame, bg="#ffffff")
        form_inner.pack(fill="both", expand=True, padx=15, pady=15)
        
        tk.Label(form_inner, text="Cadastrar Membro", font=("Segoe UI", 12, "bold"), fg="#4f46e5", bg="#ffffff").pack(anchor="w", pady=(0, 10))
        
        # Form inputs
        tk.Label(form_inner, text="Número da Tag (Ex: 01, 02):", font=("Segoe UI", 9, "bold"), fg="#4b5563", bg="#ffffff").pack(anchor="w")
        self.ent_eq_num = ttk.Entry(form_inner)
        self.ent_eq_num.pack(fill="x", pady=(2, 10))
        
        tk.Label(form_inner, text="Nome Completo:", font=("Segoe UI", 9, "bold"), fg="#4b5563", bg="#ffffff").pack(anchor="w")
        self.ent_eq_nome = ttk.Entry(form_inner)
        self.ent_eq_nome.pack(fill="x", pady=(2, 10))
        
        tk.Label(form_inner, text="Cargo/Função:", font=("Segoe UI", 9, "bold"), fg="#4b5563", bg="#ffffff").pack(anchor="w")
        self.ent_eq_cargo = ttk.Entry(form_inner)
        self.ent_eq_cargo.pack(fill="x", pady=(2, 10))
        
        tk.Label(form_inner, text="Ordem de Exibição (Número):", font=("Segoe UI", 9, "bold"), fg="#4b5563", bg="#ffffff").pack(anchor="w")
        self.ent_eq_ordem = ttk.Entry(form_inner)
        self.ent_eq_ordem.pack(fill="x", pady=(2, 10))
        self.ent_eq_ordem.insert(0, "0")
        
        tk.Label(form_inner, text="Biografia / Breve Descrição:", font=("Segoe UI", 9, "bold"), fg="#4b5563", bg="#ffffff").pack(anchor="w")
        self.txt_eq_bio = tk.Text(form_inner, font=("Segoe UI", 9), height=5, wrap="word", bd=1, relief="solid")
        self.txt_eq_bio.pack(fill="both", expand=True, pady=(2, 15))
        
        btn_add_eq = tk.Button(
            form_inner, 
            text="➕ Adicionar Membro à Equipe", 
            font=("Segoe UI", 10, "bold"), 
            bg="#10b981", 
            fg="#ffffff", 
            activebackground="#059669", 
            activeforeground="#ffffff", 
            relief="flat", 
            command=self.add_team_member
        )
        btn_add_eq.pack(fill="x", ipady=3)

        # Right Panel (List and delete)
        list_frame = tk.Frame(self.tab_eq)
        list_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        
        list_tools = tk.Frame(list_frame, bg="#f3f4f6")
        list_tools.pack(fill="x", pady=(0, 5))
        
        lbl_list_title = ttk.Label(list_tools, text="Membros Cadastrados", style="Header.TLabel")
        lbl_list_title.pack(side="left")
        
        btn_del_eq = tk.Button(list_tools, text="🗑 Excluir", font=("Segoe UI", 8, "bold"), bg="#ef4444", fg="#ffffff", relief="flat", command=self.delete_team_member)
        btn_del_eq.pack(side="right", padx=5)
        
        btn_ref_eq = tk.Button(list_tools, text="🔄 Atualizar", font=("Segoe UI", 8, "bold"), bg="#4f46e5", fg="#ffffff", relief="flat", command=self.load_equipe)
        btn_ref_eq.pack(side="right", padx=5)
        
        cols = ("id", "numero", "nome", "cargo", "bio", "ordem")
        self.tree_eq = ttk.Treeview(list_frame, columns=cols, show="headings")
        
        self.tree_eq.heading("id", text="ID")
        self.tree_eq.heading("numero", text="Tag")
        self.tree_eq.heading("nome", text="Nome")
        self.tree_eq.heading("cargo", text="Cargo")
        self.tree_eq.heading("bio", text="Bio")
        self.tree_eq.heading("ordem", text="Ordem")
        
        self.tree_eq.column("id", width=40, anchor="center")
        self.tree_eq.column("numero", width=50, anchor="center")
        self.tree_eq.column("nome", width=160)
        self.tree_eq.column("cargo", width=120)
        self.tree_eq.column("bio", width=150)
        self.tree_eq.column("ordem", width=55, anchor="center")
        
        sc_eq_y = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree_eq.yview)
        self.tree_eq.configure(yscrollcommand=sc_eq_y.set)
        
        self.tree_eq.pack(fill="both", expand=True, side="left")
        sc_eq_y.pack(fill="y", side="right")

    def load_equipe(self):
        self.tree_eq.delete(*self.tree_eq.get_children())
        try:
            r = requests.get(f"{API_URL}/api/equipe", timeout=5)
            if r.status_code == 200:
                data = r.json()
                for m in data:
                    self.tree_eq.insert("", "end", values=(
                        m.get("id"),
                        m.get("numero", ""),
                        m.get("nome"),
                        m.get("cargo"),
                        m.get("bio", ""),
                        m.get("ordem", 0)
                    ))
            else:
                messagebox.showerror("Erro", "Não foi possível carregar os membros da equipe.")
        except Exception as e:
            messagebox.showerror("Erro de Conexão", str(e))

    def add_team_member(self):
        num = self.ent_eq_num.get().strip()
        nome = self.ent_eq_nome.get().strip()
        cargo = self.ent_eq_cargo.get().strip()
        bio = self.txt_eq_bio.get("1.0", "end").strip()
        ordem_val = self.ent_eq_ordem.get().strip()
        
        if not nome or not cargo:
            messagebox.showwarning("Erro de Validação", "Nome e Cargo são campos obrigatórios!")
            return
            
        try:
            ordem = int(ordem_val)
        except ValueError:
            messagebox.showwarning("Erro de Validação", "A ordem de exibição deve ser um número inteiro!")
            return
            
        try:
            payload = {"numero": num, "nome": nome, "cargo": cargo, "bio": bio, "ordem": ordem}
            r = requests.post(f"{API_URL}/api/equipe", json=payload, timeout=5)
            if r.status_code == 200:
                messagebox.showinfo("Sucesso", "Novo membro adicionado com sucesso!")
                # Reset inputs
                self.ent_eq_num.delete(0, "end")
                self.ent_eq_nome.delete(0, "end")
                self.ent_eq_cargo.delete(0, "end")
                self.ent_eq_ordem.delete(0, "end")
                self.ent_eq_ordem.insert(0, "0")
                self.txt_eq_bio.delete("1.0", "end")
                # Reload table
                self.load_equipe()
            else:
                messagebox.showerror("Erro", "Erro ao tentar registrar o membro.")
        except Exception as e:
            messagebox.showerror("Erro de Conexão", str(e))

    def delete_team_member(self):
        sel = self.tree_eq.selection()
        if not sel:
            messagebox.showwarning("Nenhum Item Selecionado", "Por favor, selecione um membro na lista primeiro!")
            return
        item = self.tree_eq.item(sel[0])
        val = item["values"]
        
        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o membro '{val[2]}'?"):
            try:
                r = requests.delete(f"{API_URL}/api/equipe/{val[0]}", timeout=5)
                if r.status_code == 200:
                    messagebox.showinfo("Sucesso", "Membro excluído da equipe com sucesso!")
                    self.load_equipe()
                else:
                    messagebox.showerror("Erro", "Erro ao tentar excluir membro da equipe.")
            except Exception as e:
                messagebox.showerror("Erro de Conexão", str(e))

    # ── TAB 3: FINANCEIRO (DOAÇÕES) ───────────────────
    def build_financeiro_tab(self):
        self.tab_fin = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_fin, text="Registro Financeiro / Doações")
        
        # Split layout: Form left, Table list right
        self.tab_fin.columnconfigure(0, weight=2)
        self.tab_fin.columnconfigure(1, weight=3)
        self.tab_fin.rowconfigure(0, weight=1)
        
        # Left Panel (Add Form)
        form_frame = tk.Frame(self.tab_fin, bg="#ffffff", bd=1, relief="solid")
        form_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        form_inner = tk.Frame(form_frame, bg="#ffffff")
        form_inner.pack(fill="both", expand=True, padx=15, pady=15)
        
        tk.Label(form_inner, text="Registrar Doação / Lançamento", font=("Segoe UI", 12, "bold"), fg="#4f46e5", bg="#ffffff").pack(anchor="w", pady=(0, 15))
        
        # Form inputs
        tk.Label(form_inner, text="Valor do Lançamento (R$):", font=("Segoe UI", 9, "bold"), fg="#4b5563", bg="#ffffff").pack(anchor="w")
        self.ent_fin_valor = ttk.Entry(form_inner)
        self.ent_fin_valor.pack(fill="x", pady=(2, 12))
        self.ent_fin_valor.insert(0, "50.00")
        
        tk.Label(form_inner, text="Canal de Recebimento:", font=("Segoe UI", 9, "bold"), fg="#4b5563", bg="#ffffff").pack(anchor="w")
        self.cb_fin_tipo = ttk.Combobox(form_inner, values=["PIX", "Dinheiro", "Transferência Bancária", "Cartão de Crédito", "Outro"])
        self.cb_fin_tipo.pack(fill="x", pady=(2, 12))
        self.cb_fin_tipo.current(0)
        
        tk.Label(form_inner, text="Status do Lançamento:", font=("Segoe UI", 9, "bold"), fg="#4b5563", bg="#ffffff").pack(anchor="w")
        self.cb_fin_status = ttk.Combobox(form_inner, values=["Confirmado", "Pendente", "Cancelado"])
        self.cb_fin_status.pack(fill="x", pady=(2, 20))
        self.cb_fin_status.current(0)
        
        btn_add_fin = tk.Button(
            form_inner, 
            text="💵 Registrar Transação", 
            font=("Segoe UI", 10, "bold"), 
            bg="#10b981", 
            fg="#ffffff", 
            activebackground="#059669", 
            activeforeground="#ffffff", 
            relief="flat", 
            command=self.add_donation_log
        )
        btn_add_fin.pack(fill="x", ipady=3)

        # Right Panel (List and delete)
        list_frame = tk.Frame(self.tab_fin)
        list_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        
        list_tools = tk.Frame(list_frame, bg="#f3f4f6")
        list_tools.pack(fill="x", pady=(0, 5))
        
        lbl_list_title = ttk.Label(list_tools, text="Doações Registradas", style="Header.TLabel")
        lbl_list_title.pack(side="left")
        
        btn_del_fin = tk.Button(list_tools, text="🗑 Excluir", font=("Segoe UI", 8, "bold"), bg="#ef4444", fg="#ffffff", relief="flat", command=self.delete_donation_log)
        btn_del_fin.pack(side="right", padx=5)
        
        btn_ref_fin = tk.Button(list_tools, text="🔄 Atualizar", font=("Segoe UI", 8, "bold"), bg="#4f46e5", fg="#ffffff", relief="flat", command=self.load_doacoes)
        btn_ref_fin.pack(side="right", padx=5)
        
        cols = ("id", "valor", "data_doacao", "tipo", "status")
        self.tree_fin = ttk.Treeview(list_frame, columns=cols, show="headings")
        
        self.tree_fin.heading("id", text="ID")
        self.tree_fin.heading("valor", text="Valor")
        self.tree_fin.heading("data_doacao", text="Data do Lançamento")
        self.tree_fin.heading("tipo", text="Tipo")
        self.tree_fin.heading("status", text="Status")
        
        self.tree_fin.column("id", width=40, anchor="center")
        self.tree_fin.column("valor", width=90, anchor="center")
        self.tree_fin.column("data_doacao", width=170, anchor="center")
        self.tree_fin.column("tipo", width=120)
        self.tree_fin.column("status", width=95, anchor="center")
        
        sc_fin_y = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree_fin.yview)
        self.tree_fin.configure(yscrollcommand=sc_fin_y.set)
        
        self.tree_fin.pack(fill="both", expand=True, side="left")
        sc_fin_y.pack(fill="y", side="right")

    def load_doacoes(self):
        self.tree_fin.delete(*self.tree_fin.get_children())
        try:
            h = {"Authorization": f"Bearer {TOKEN}"}
            r = requests.get(f"{API_URL}/api/admin/doacoes", headers=h, timeout=5)
            if r.status_code == 200:
                data = r.json()
                for d in data:
                    val = d.get("valor", 0.0)
                    formatted_val = f"R$ {float(val):.2f}"
                    
                    # Convert date to standard friendly view
                    raw_date = d.get("data_doacao", "")
                    friendly_date = raw_date.replace("T", " ")[:19]
                    
                    self.tree_fin.insert("", "end", values=(
                        d.get("id"),
                        formatted_val,
                        friendly_date,
                        d.get("tipo"),
                        d.get("status")
                    ))
            else:
                messagebox.showerror("Erro", "Não foi possível carregar o log de transações.")
        except Exception as e:
            messagebox.showerror("Erro de Conexão", str(e))

    def add_donation_log(self):
        val_str = self.ent_fin_valor.get().strip()
        tipo = self.cb_fin_tipo.get().strip()
        status = self.cb_fin_status.get().strip()
        
        if not val_str:
            messagebox.showwarning("Erro de Validação", "O Valor do Lançamento é obrigatório!")
            return
            
        try:
            valor = float(val_str)
        except ValueError:
            messagebox.showwarning("Erro de Validação", "Por favor, digite um valor numérico válido (ex: 50.00)!")
            return
            
        try:
            payload = {"valor": valor, "tipo": tipo, "status": status}
            r = requests.post(f"{API_URL}/api/doacoes", json=payload, timeout=5)
            if r.status_code == 200:
                messagebox.showinfo("Sucesso", "Doação registrada com sucesso!")
                self.ent_fin_valor.delete(0, "end")
                self.ent_fin_valor.insert(0, "50.00")
                self.load_doacoes()
            else:
                messagebox.showerror("Erro", "Erro ao tentar registrar o lançamento.")
        except Exception as e:
            messagebox.showerror("Erro de Conexão", str(e))

    def delete_donation_log(self):
        sel = self.tree_fin.selection()
        if not sel:
            messagebox.showwarning("Nenhum Item Selecionado", "Por favor, selecione um lançamento financeiro na lista primeiro!")
            return
        item = self.tree_fin.item(sel[0])
        val = item["values"]
        
        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir a doação ID #{val[0]} de {val[1]}?"):
            try:
                r = requests.delete(f"{API_URL}/api/doacoes/{val[0]}", timeout=5)
                if r.status_code == 200:
                    messagebox.showinfo("Sucesso", "Lançamento de doação excluído com sucesso!")
                    self.load_doacoes()
                else:
                    messagebox.showerror("Erro", "Erro ao tentar excluir a doação.")
            except Exception as e:
                messagebox.showerror("Erro de Conexão", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = GaiarbAdminApp(root)
    root.mainloop()
