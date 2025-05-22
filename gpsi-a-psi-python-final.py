import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

class Filme:
    def __init__(self, titulo, duracao, classificacao):
        self.titulo = titulo
        self.duracao = duracao
        self.classificacao = classificacao

    def __str__(self):
        return self.titulo + " (" + str(self.duracao) + " min) - " + self.classificacao

class Sessao:
    def __init__(self, filme, horario, assentos, preco=20.0):
        self.filme = filme
        self.horario = horario
        self.assentos = assentos
        self.preco = preco

    def __str__(self):
        return self.filme.titulo + " às " + self.horario + " - Lugares: " + str(self.assentos)

class Cliente:
    def __init__(self, nome, nif, estudante=False):
        self.nome = nome
        self.nif = nif
        self.estudante = estudante
        self.bilhetes = []

    def adicionar_bilhete(self, sessao):
        self.bilhetes.append(sessao)

    def ver_bilhetes(self):
        resultado = []
        for s in self.bilhetes:
            resultado.append(s.filme.titulo + " às " + s.horario)
        return resultado

class Cinema:
    def __init__(self):
        self.filmes = []
        self.sessoes = []
        self.clientes = []

    def adicionar_filme(self, filme):
        self.filmes.append(filme)

    def adicionar_sessao(self, sessao):
        self.sessoes.append(sessao)

    def adicionar_cliente(self, cliente):
        self.clientes.append(cliente)

    def quase_lotadas(self):
        quase = []
        for s in self.sessoes:
            if s.assentos < 5:
                quase.append(s)
        return quase

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Cinema - Sistema de Bilheteira")
        self.cinema = Cinema()

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)

        self.titulo = tk.Label(self.main_frame, text="Sistema de Bilhetes do Cinema", font=("Arial", 14, "bold"))
        self.titulo.pack(pady=10)

        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=10)

        button_style = {"width": 35}

        tk.Button(button_frame, text="Adicionar Filme", command=self.add_filme, **button_style).pack(pady=5)
        tk.Button(button_frame, text="Adicionar Sessão", command=self.add_sessao, **button_style).pack(pady=5)
        tk.Button(button_frame, text="Mostrar Sessões", command=self.mostrar_sessoes, **button_style).pack(pady=5)
        tk.Button(button_frame, text="Comprar Bilhetes", command=self.comprar_bilhete, **button_style).pack(pady=5)
        tk.Button(button_frame, text="Ver Bilhetes do Cliente", command=self.ver_bilhetes, **button_style).pack(pady=5)
        tk.Button(button_frame, text="Remover Sessão", command=self.remover_sessao, **button_style).pack(pady=5)

    def add_filme(self):
        titulo = simpledialog.askstring("Filme", "Digite o título do filme:")
        if titulo == None or titulo.strip() == "":
            messagebox.showerror("Erro", "Título inválido.")
            return

        duracao = simpledialog.askinteger("Duração", "Quantos minutos o filme tem?")
        if duracao == None or duracao <= 0:
            messagebox.showerror("Erro", "Duração inválida.")
            return

        classificacao = simpledialog.askstring("Classificação", "Digite a classificação:")
        if classificacao == None or classificacao.strip() == "":
            messagebox.showerror("Erro", "Classificação inválida.")
            return

        novo_filme = Filme(titulo.strip(), duracao, classificacao.strip())
        self.cinema.adicionar_filme(novo_filme)
        messagebox.showinfo("OK", "Filme adicionado!")

    def add_sessao(self):
        if len(self.cinema.filmes) == 0:
            messagebox.showwarning("Aviso", "Não há filmes cadastrados.")
            return

        filmes_lista = ""
        for i in range(len(self.cinema.filmes)):
            filmes_lista += str(i+1) + ". " + str(self.cinema.filmes[i]) + "\n"

        escolha = simpledialog.askinteger("Escolha", filmes_lista + "Digite o número do filme:")
        if escolha == None or escolha < 1 or escolha > len(self.cinema.filmes):
            messagebox.showerror("Erro", "Escolha inválida.")
            return

        horario = simpledialog.askstring("Horário", "Digite o horário (ex: 19:30):")
        if horario == None or horario.strip() == "":
            messagebox.showerror("Erro", "Horário inválido.")
            return

        lugares = simpledialog.askinteger("Lugares", "Quantos lugares disponíveis?")
        if lugares == None or lugares <= 0:
            messagebox.showerror("Erro", "Número inválido.")
            return

        preco = simpledialog.askfloat("Preço", "Preço do bilhete:", initialvalue=20.0)
        if preco == None or preco <= 0:
            preco = 20.0

        sessao = Sessao(self.cinema.filmes[escolha - 1], horario.strip(), lugares, preco)
        self.cinema.adicionar_sessao(sessao)
        messagebox.showinfo("OK", "Sessão adicionada!")

    def mostrar_sessoes(self):
        if len(self.cinema.sessoes) == 0:
            messagebox.showinfo("Sessões", "Não há sessões.")
            return

        lista = ""
        for i in range(len(self.cinema.sessoes)):
            lista += str(i+1) + ". " + str(self.cinema.sessoes[i]) + "\n"

        messagebox.showinfo("Sessões Disponíveis", lista)

    def comprar_bilhete(self):
        nome = simpledialog.askstring("Nome", "Digite o nome do cliente:")
        if nome == None or nome.strip() == "":
            messagebox.showerror("Erro", "Nome inválido.")
            return

        nif = simpledialog.askstring("NIF", "Digite o NIF:")
        if nif == None or nif.strip() == "":
            messagebox.showerror("Erro", "NIF inválido.")
            return

        estudante = messagebox.askyesno("Estudante", "O cliente é estudante?")

        cliente = None
        for c in self.cinema.clientes:
            if c.nome == nome.strip() and c.nif == nif.strip():
                cliente = c
                break

        if cliente == None:
            cliente = Cliente(nome.strip(), nif.strip(), estudante)
            self.cinema.adicionar_cliente(cliente)

        if len(self.cinema.sessoes) == 0:
            messagebox.showwarning("Aviso", "Nenhuma sessão disponível.")
            return

        opcoes = ""
        for i in range(len(self.cinema.sessoes)):
            opcoes += str(i+1) + ". " + str(self.cinema.sessoes[i]) + "\n"

        escolha = simpledialog.askinteger("Sessão", opcoes + "Escolha a sessão:")
        if escolha == None or escolha < 1 or escolha > len(self.cinema.sessoes):
            messagebox.showerror("Erro", "Escolha inválida.")
            return

        sessao_escolhida = self.cinema.sessoes[escolha - 1]
        if sessao_escolhida.assentos > 0:
            sessao_escolhida.assentos = sessao_escolhida.assentos - 1
            cliente.adicionar_bilhete(sessao_escolhida)
            valor = sessao_escolhida.preco
            if estudante:
                valor = valor * 0.5
            messagebox.showinfo("Compra feita", "Bilhete comprado para " + sessao_escolhida.filme.titulo + " às " + sessao_escolhida.horario + "\nPreço: €" + str(round(valor, 2)))
        else:
            messagebox.showerror("Erro", "Sessão lotada.")

    def ver_bilhetes(self):
        nome = simpledialog.askstring("Nome", "Digite o nome do cliente:")
        if nome == None or nome.strip() == "":
            messagebox.showerror("Erro", "Nome inválido.")
            return

        nif = simpledialog.askstring("NIF", "Digite o NIF:")
        if nif == None or nif.strip() == "":
            messagebox.showerror("Erro", "NIF inválido.")
            return

        cliente = None
        for c in self.cinema.clientes:
            if c.nome == nome.strip() and c.nif == nif.strip():
                cliente = c
                break

        if cliente != None:
            if len(cliente.bilhetes) > 0:
                lista = ""
                for b in cliente.ver_bilhetes():
                    lista += b + "\n"
                messagebox.showinfo("Bilhetes", lista)
            else:
                messagebox.showinfo("Bilhetes", "Nenhum bilhete comprado.")
        else:
            messagebox.showerror("Erro", "Cliente não encontrado.")

    def remover_sessao(self):
        if len(self.cinema.sessoes) == 0:
            messagebox.showinfo("Sessões", "Não há sessões cadastradas.")
            return

        lista = ""
        for i in range(len(self.cinema.sessoes)):
            lista += str(i+1) + ". " + str(self.cinema.sessoes[i]) + "\n"

        escolha = simpledialog.askinteger("Remover", lista + "Escolha a sessão para remover:")
        if escolha == None or escolha < 1 or escolha > len(self.cinema.sessoes):
            messagebox.showerror("Erro", "Escolha inválida.")
            return

        sessao_removida = self.cinema.sessoes.pop(escolha - 1)

        for cliente in self.cinema.clientes:
            nova_lista = []
            for s in cliente.bilhetes:
                if s != sessao_removida:
                    nova_lista.append(s)
            cliente.bilhetes = nova_lista

        messagebox.showinfo("OK", "Sessão removida: " + sessao_removida.filme.titulo + " às " + sessao_removida.horario)

janela = tk.Tk()
aplicacao = App(janela)
janela.mainloop()
