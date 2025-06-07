import customtkinter as ctk
from tkinter import messagebox, Text, END
from PIL import Image
import os
import datetime # Import datetime here
from database import DatabaseManager # Import the DatabaseManager

class MarcenariaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager() # Initialize the DatabaseManager
        self.title('Marcenaria Pica Pau - Login')
        self.geometry('960x540')
        self.resizable(False, False)
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme("blue")
        self.configure(fg_color=self._get_appearance_mode_color())
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            bg_image_path = os.path.join(script_dir, "picapaupng.png")
            self.bg_image = ctk.CTkImage(Image.open(bg_image_path), size=(480, 540))
            self.background_label = ctk.CTkLabel(self, image=self.bg_image, text="")
            self.background_label.place(x=0, y=0)
        except FileNotFoundError:
            print("Aviso: Imagem 'picapaupng.png' não encontrada.")

        self.login_frame = ctk.CTkFrame(self, width=480, height=540, corner_radius=0, fg_color=self._get_appearance_mode_color())
        self.main_content_frame = ctk.CTkFrame(self, fg_color=self._get_appearance_mode_color())
        self.show_login_widgets()

    def on_closing(self):
        self.db.close()
        self.destroy()

    def _get_appearance_mode_color(self):
        return "#2b2b2b" if ctk.get_appearance_mode() == "Dark" else "#e6e6e6"

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def show_login_widgets(self):
        self.main_content_frame.place_forget()
        self.login_frame.place(relx=0.75, rely=0.5, anchor='center')
        self.clear_frame(self.login_frame)
        ctk.CTkLabel(self.login_frame, text="Marcenaria Pica Pau", font=ctk.CTkFont(size=30, weight="bold")).pack(pady=(50, 30))
        self.user_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Usuário", width=300, height=40)
        self.user_entry.pack(pady=10)
        self.pass_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Senha", show="*", width=300, height=40)
        self.pass_entry.pack(pady=10)
        ctk.CTkButton(self.login_frame, text="Login", command=self.login, width=300, height=40).pack(pady=20)
        ctk.CTkButton(self.login_frame, text="Cadastrar Novo Usuário", command=self.show_register_widgets, width=300, height=40).pack(pady=10)

    def show_register_widgets(self):
        self.clear_frame(self.login_frame)
        ctk.CTkLabel(self.login_frame, text="Cadastro de Usuário", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(50, 30))
        self.reg_user_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Novo Usuário", width=300, height=40)
        self.reg_user_entry.pack(pady=10)
        self.reg_pass_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Nova Senha", show="*", width=300, height=40)
        self.reg_pass_entry.pack(pady=10)
        self.reg_pass_confirm_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Confirmar Senha", show="*", width=300, height=40)
        self.reg_pass_confirm_entry.pack(pady=10)
        ctk.CTkButton(self.login_frame, text="Cadastrar", command=self.register_user, width=300, height=40).pack(pady=20)
        ctk.CTkButton(self.login_frame, text="Voltar para Login", command=self.show_login_widgets, width=200, fg_color="transparent", border_width=1).pack(pady=10)

    def register_user(self):
        username = self.reg_user_entry.get()
        password = self.reg_pass_entry.get()
        password_confirm = self.reg_pass_confirm_entry.get()
        if not username or not password:
            messagebox.showerror("Erro", "Usuário e senha não podem ser vazios.")
            return
        if password != password_confirm:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return
        if self.db.check_user_exists(username):
            messagebox.showerror("Erro", "Este nome de usuário já existe.")
            return
        if self.db.add_user(username, password):
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            self.show_login_widgets()
        else:
            messagebox.showerror("Erro", "Não foi possível cadastrar o usuário.")

    def login(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()
        user = self.db.verify_user(username, password)
        if user:
            self.username = username
            self.show_main_window()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

    def logout(self):
        self.clear_frame(self.main_content_frame)
        self.show_login_widgets()

    def show_main_window(self):
        self.login_frame.place_forget()
        self.main_content_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.clear_frame(self.main_content_frame)
        self._add_nav_bar()
        ctk.CTkLabel(self.main_content_frame, text=f"Bem-vindo(a), {self.username}!", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        ctk.CTkLabel(self.main_content_frame, text="Use a barra de navegação para gerenciar o sistema.", font=ctk.CTkFont(size=14)).pack(pady=10)

    def _add_nav_bar(self):
        nav_bar = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        nav_bar.pack(pady=10, fill="x", padx=20)
        ctk.CTkButton(nav_bar, text="Produtos", command=self.show_manage_products).pack(side="left", expand=True, padx=5)
        ctk.CTkButton(nav_bar, text="Nova Encomenda", command=self.show_create_order).pack(side="left", expand=True, padx=5)
        ctk.CTkButton(nav_bar, text="Atualizar Encomenda", command=self.show_update_order_status).pack(side="left", expand=True, padx=5)
        ctk.CTkButton(nav_bar, text="Relatórios", command=self.show_reports).pack(side="left", expand=True, padx=5)
        ctk.CTkButton(nav_bar, text="Logout", command=self.logout, fg_color="red").pack(side="right", padx=5)

    def show_manage_products(self):
        self.clear_frame(self.main_content_frame)
        self._add_nav_bar()
        ctk.CTkLabel(self.main_content_frame, text="Gerenciamento de Produtos", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        actions_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        actions_frame.pack(pady=10)
        ctk.CTkButton(actions_frame, text="Adicionar Novo Produto", command=self._show_add_product_form).pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text="Editar Produto Existente", command=self._show_edit_product_form).pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text="Remover Produto", command=self._show_delete_product_form).pack(side="left", padx=5)
        self.product_list_text = ctk.CTkTextbox(self.main_content_frame, width=780, height=300)
        self.product_list_text.pack(pady=10)
        self.refresh_product_list(self.product_list_text)

    def refresh_product_list(self, textbox):
        textbox.delete("1.0", END)
        products = self.db.get_all_products()
        if not products:
            textbox.insert(END, "Nenhum produto cadastrado.")
            return
        header = f"{'ID':<5}{'Nome':<30}{'Descrição':<40}{'Preço (R$)':>10}\n" + "-"*85 + "\n"
        textbox.insert(END, header)
        for p in products:
            line = f"{p[0]:<5}{p[1]:<30}{p[2] if p[2] else '':<40}{p[3]:>10.2f}\n"
            textbox.insert(END, line)

    def _show_add_product_form(self):
        self.clear_frame(self.main_content_frame)
        self._add_nav_bar()
        ctk.CTkLabel(self.main_content_frame, text="Adicionar Novo Produto", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        form_frame = ctk.CTkFrame(self.main_content_frame)
        form_frame.pack(pady=10)
        ctk.CTkLabel(form_frame, text="Nome:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        name_entry = ctk.CTkEntry(form_frame, width=250)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkLabel(form_frame, text="Descrição:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        desc_entry = ctk.CTkEntry(form_frame, width=250)
        desc_entry.grid(row=1, column=1, padx=10, pady=5)
        ctk.CTkLabel(form_frame, text="Preço:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        price_entry = ctk.CTkEntry(form_frame, width=250)
        price_entry.grid(row=2, column=1, padx=10, pady=5)
        def save():
            name, desc, price = name_entry.get(), desc_entry.get(), price_entry.get()
            if not name or not price:
                messagebox.showerror("Erro", "Nome e Preço são obrigatórios.")
                return
            if self.db.add_product(name, desc, price):
                messagebox.showinfo("Sucesso", "Produto adicionado.")
                self.show_manage_products()
            else:
                messagebox.showerror("Erro", "Preço inválido ou erro no banco de dados.")
        ctk.CTkButton(self.main_content_frame, text="Salvar Produto", command=save, width=150, height=40).pack(pady=20)
        ctk.CTkButton(self.main_content_frame, text="Voltar", command=self.show_manage_products, fg_color="transparent", border_width=1).pack(pady=5)

    def _show_edit_product_form(self):
        self.clear_frame(self.main_content_frame)
        self._add_nav_bar()
        ctk.CTkLabel(self.main_content_frame, text="Editar Produto Existente", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        edit_form_frame = ctk.CTkFrame(self.main_content_frame)
        edit_form_frame.pack(pady=10)
        ctk.CTkLabel(edit_form_frame, text="ID do Produto:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        id_entry = ctk.CTkEntry(edit_form_frame, width=250)
        id_entry.grid(row=0, column=1, padx=10, pady=5)
        name_entry = ctk.CTkEntry(edit_form_frame, width=250)
        desc_entry = ctk.CTkEntry(edit_form_frame, width=250)
        price_entry = ctk.CTkEntry(edit_form_frame, width=250)
        def load_product_data():
            try:
                prod_id = int(id_entry.get())
                product = self.db.get_product(prod_id)
                if product:
                    # Clear and re-pack existing widgets for dynamic update
                    for widget in [name_entry, desc_entry, price_entry]:
                        widget.grid_forget() # Hide if already visible
                    for label_text in ["Novo Nome:", "Nova Descrição:", "Novo Preço:"]:
                        for child in edit_form_frame.winfo_children():
                            if isinstance(child, ctk.CTkLabel) and child.cget("text") == label_text:
                                child.destroy()

                    ctk.CTkLabel(edit_form_frame, text="Novo Nome:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
                    name_entry.grid(row=1, column=1, padx=10, pady=5)
                    name_entry.delete(0, END); name_entry.insert(0, product[0])
                    ctk.CTkLabel(edit_form_frame, text="Nova Descrição:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
                    desc_entry.grid(row=2, column=1, padx=10, pady=5)
                    desc_entry.delete(0, END); desc_entry.insert(0, product[1])
                    ctk.CTkLabel(edit_form_frame, text="Novo Preço:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
                    price_entry.grid(row=3, column=1, padx=10, pady=5)
                    price_entry.delete(0, END); price_entry.insert(0, str(product[2]))
                    
                    # Ensure "Salvar Alterações" button is present and correctly linked
                    for widget in edit_form_frame.winfo_children():
                        if isinstance(widget, ctk.CTkButton) and widget.cget("text") == "Salvar Alterações":
                            widget.destroy() # Remove old button to prevent duplicates
                    ctk.CTkButton(edit_form_frame, text="Salvar Alterações", command=save_changes, width=150).grid(row=4, column=0, columnspan=2, pady=10)
                else:
                    messagebox.showerror("Erro", "Produto não encontrado.")
            except ValueError:
                messagebox.showerror("Erro", "ID inválido.")
        def save_changes():
            try:
                prod_id = int(id_entry.get())
                name, desc, price = name_entry.get(), desc_entry.get(), price_entry.get()
                if self.db.update_product(prod_id, name, desc, price):
                    messagebox.showinfo("Sucesso", "Produto atualizado.")
                    self.show_manage_products()
                else:
                    messagebox.showerror("Erro", "Não foi possível salvar.")
            except ValueError:
                messagebox.showerror("Erro", "Dados inválidos.")
        ctk.CTkButton(edit_form_frame, text="Carregar Produto", command=load_product_data, width=150).grid(row=0, column=2, padx=10, pady=5)
        ctk.CTkButton(self.main_content_frame, text="Voltar", command=self.show_manage_products, fg_color="transparent", border_width=1).pack(pady=5)

    def _show_delete_product_form(self):
        self.clear_frame(self.main_content_frame)
        self._add_nav_bar()
        ctk.CTkLabel(self.main_content_frame, text="Remover Produto", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        delete_form_frame = ctk.CTkFrame(self.main_content_frame)
        delete_form_frame.pack(pady=10)
        ctk.CTkLabel(delete_form_frame, text="ID do Produto para Remover:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        id_entry = ctk.CTkEntry(delete_form_frame, width=250)
        id_entry.grid(row=0, column=1, padx=10, pady=5)
        def delete():
            if not messagebox.askyesno("Confirmar", "Tem certeza?"):
                return
            try:
                prod_id = int(id_entry.get())
                if self.db.delete_product(prod_id):
                    messagebox.showinfo("Sucesso", "Produto removido.")
                    self.show_manage_products()
                else:
                    messagebox.showerror("Erro", "Produto não encontrado ou associado a uma encomenda.")
            except ValueError:
                messagebox.showerror("Erro", "ID inválido.")
        ctk.CTkButton(delete_form_frame, text="Remover", command=delete, fg_color="red", width=150).grid(row=0, column=2, padx=10, pady=5)
        ctk.CTkButton(self.main_content_frame, text="Voltar", command=self.show_manage_products, fg_color="transparent", border_width=1).pack(pady=5)

    def show_create_order(self):
        self.clear_frame(self.main_content_frame)
        self._add_nav_bar()
        ctk.CTkLabel(self.main_content_frame, text="Criar Nova Encomenda", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        client_info_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        client_info_frame.pack(pady=5)
        ctk.CTkLabel(client_info_frame, text="Nome do Cliente:").pack(side="left", padx=5)
        client_name_entry = ctk.CTkEntry(client_info_frame, width=400)
        client_name_entry.pack(side="left", padx=5)
        items_display_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        items_display_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.order_items_display = ctk.CTkTextbox(items_display_frame, width=600, height=200)
        self.order_items_display.pack(pady=5, fill="both", expand=True)
        self.order_items_display.insert(END, f"{'ID':<5}{'Produto':<30}{'Preço Uni.':<15}{'Qtd':<10}{'Subtotal':>15}\n" + "="*80 + "\n")
        self.products_in_current_order = []
        action_buttons_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        action_buttons_frame.pack(pady=10)
        total_label = ctk.CTkLabel(action_buttons_frame, text="Total: R$ 0.00", font=ctk.CTkFont(size=16, weight="bold"))
        total_label.pack(side="left", padx=10)
        def update_total():
            current_total = sum(item['subtotal'] for item in self.products_in_current_order)
            total_label.configure(text=f"Total: R$ {current_total:.2f}")
        def add_item_to_order_popup():
            select_prod_win = ctk.CTkToplevel(self)
            select_prod_win.title("Selecionar Produto")
            select_prod_win.geometry("500x400")
            select_prod_win.transient(self)
            select_prod_win.configure(fg_color=self._get_appearance_mode_color()) # Set background color

            products = self.db.get_all_products() # Get products from the database
            if not products:
                messagebox.showerror("Erro", "Nenhum produto cadastrado. Cadastre produtos antes de criar uma encomenda.", parent=select_prod_win)
                select_prod_win.destroy()
                return

            product_map = {f"{p[0]} - {p[1]} (R$ {p[3]:.2f})": {"id": p[0], "name": p[1], "price": p[3]} for p in products} # Corrected index for price (p[3])
            product_options = list(product_map.keys())

            ctk.CTkLabel(select_prod_win, text="Selecione um Produto:").pack(pady=10)
            product_combobox = ctk.CTkComboBox(select_prod_win, values=product_options, width=400)
            product_combobox.pack(pady=10)
            product_combobox.set(product_options[0] if product_options else "")

            ctk.CTkLabel(select_prod_win, text="Quantidade:").pack(pady=5)
            quantity_entry = ctk.CTkEntry(select_prod_win, width=100)
            quantity_entry.pack(pady=5)
            quantity_entry.insert(0, "1")

            def confirm_add():
                try:
                    selected_prod_text = product_combobox.get()
                    qty_str = quantity_entry.get()

                    if not selected_prod_text or not qty_str:
                        messagebox.showerror("Erro", "Selecione um produto e insira a quantidade.", parent=select_prod_win)
                        return

                    selected_info = product_map[selected_prod_text]
                    product_id = selected_info["id"]
                    product_name = selected_info["name"]
                    product_price = selected_info["price"]
                    quantity = int(qty_str)

                    if quantity <= 0:
                        messagebox.showerror("Erro", "A quantidade deve ser maior que zero.", parent=select_prod_win)
                        return

                    subtotal = product_price * quantity
                    self.products_in_current_order.append({"id": product_id, "name": product_name,
                                                            "price": product_price, "quantity": quantity,
                                                            "subtotal": subtotal})

                    self.order_items_display.insert(END, f"{product_id:<5}{product_name:<30}{product_price:<15.2f}{quantity:<10}{subtotal:>15.2f}\n")
                    update_total()
                    select_prod_win.destroy()

                except ValueError:
                    messagebox.showerror("Erro", "Quantidade inválida.", parent=select_prod_win)
                except KeyError:
                    messagebox.showerror("Erro", "Produto selecionado inválido.", parent=select_prod_win)

            ctk.CTkButton(select_prod_win, text="Adicionar Produto", command=confirm_add).pack(pady=20)

        def save_order():
            client_name = client_name_entry.get()
            if not client_name:
                messagebox.showerror("Erro", "Nome do cliente é obrigatório."); return
            if not self.products_in_current_order:
                messagebox.showerror("Erro", "Adicione pelo menos um item."); return
            order_total = sum(item['subtotal'] for item in self.products_in_current_order)
            order_id = self.db.create_order(client_name, order_total, self.products_in_current_order)
            if order_id:
                messagebox.showinfo("Sucesso", f"Encomenda #{order_id} criada com sucesso!")
                self.show_create_order()
            else:
                messagebox.showerror("Erro", "Não foi possível salvar a encomenda.")
        ctk.CTkButton(action_buttons_frame, text="Adicionar Item", command=add_item_to_order_popup, width=150).pack(side="left", padx=10)
        ctk.CTkButton(action_buttons_frame, text="Salvar Encomenda", command=save_order, width=150).pack(side="right", padx=10)

    def show_update_order_status(self):
        self.clear_frame(self.main_content_frame)
        self._add_nav_bar()
        ctk.CTkLabel(self.main_content_frame, text="Atualizar Status da Encomenda", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        ctk.CTkLabel(self.main_content_frame, text="ID da Encomenda:").pack(pady=10)
        order_id_entry = ctk.CTkEntry(self.main_content_frame, width=250)
        order_id_entry.pack(pady=5)
        current_status_label = ctk.CTkLabel(self.main_content_frame, text="Status Atual: N/A", font=ctk.CTkFont(size=14, weight="bold"))
        current_status_label.pack(pady=5)
        ctk.CTkLabel(self.main_content_frame, text="Novo Status:").pack(pady=5)
        status_options = ["Pendente", "Em Produção", "Concluído", "Entregue", "Cancelado"]
        status_combobox = ctk.CTkComboBox(self.main_content_frame, values=status_options, width=250)
        status_combobox.pack(pady=5)
        def load_order_status():
            try:
                order_id = int(order_id_entry.get())
                status = self.db.get_order_status(order_id)
                if status:
                    current_status_label.configure(text=f"Status Atual: {status}")
                    status_combobox.set(status)
                else:
                    messagebox.showerror("Erro", "Encomenda não encontrada.")
            except ValueError:
                messagebox.showerror("Erro", "ID inválido.")
        def save_new_status():
            try:
                order_id = int(order_id_entry.get())
                new_status = status_combobox.get()
                if not new_status:
                    messagebox.showerror("Erro", "Selecione um novo status."); return
                if self.db.update_order_status(order_id, new_status):
                    messagebox.showinfo("Sucesso", f"Status da Encomenda #{order_id} atualizado.")
                    self.show_update_order_status()
                else:
                    messagebox.showerror("Erro", "Encomenda não encontrada.")
            except ValueError:
                messagebox.showerror("Erro", "ID inválido.")
        button_group_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        button_group_frame.pack(pady=20)
        ctk.CTkButton(button_group_frame, text="Carregar Status", command=load_order_status, width=150).pack(side="left", padx=10)
        ctk.CTkButton(button_group_frame, text="Salvar Novo Status", command=save_new_status, fg_color="green", width=150).pack(side="left", padx=10)

    def show_reports(self):
        self.clear_frame(self.main_content_frame)
        self._add_nav_bar()
        ctk.CTkLabel(self.main_content_frame, text="Relatório de Encomendas", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        report_text = ctk.CTkTextbox(self.main_content_frame, width=780, height=400)
        report_text.pack(pady=10, padx=10)
        report_data = self.db.get_full_report()
        if not report_data:
            report_text.insert(END, "Nenhuma encomenda registrada.")
            return
        for data in report_data:
            order, items = data['order'], data['items']
            order_id, client, date, status, total = order
            report_text.insert(END, f"--- Encomenda ID: {order_id} | Cliente: {client} | Data: {date} ---\n")
            report_text.insert(END, f"    Status: {status}\n    Total: R$ {total:.2f}\n    Itens:\n")
            if not items:
                report_text.insert(END, "        (Nenhum item encontrado)\n")
            else:
                for item in items:
                    report_text.insert(END, f"        - {item[0]}: {item[1]} unidade(s)\n")
            report_text.insert(END, "-"*60 + "\n\n")

if __name__ == "__main__":
    app = MarcenariaApp()
    app.mainloop()