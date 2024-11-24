import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from logica_calculadora import CalculadoraLogica


class CalculadoraApp:
    def __init__(self, root):
        self.logica = CalculadoraLogica()
        self.root = root
        self.root.title("Calculadora Avanzada")
        self.root.geometry("1100x800")
        self.root.configure(bg="#2C3333")

        # Marco principal
        marco_principal = tk.Frame(self.root, bg="#2C3333")
        marco_principal.pack(fill="both", expand=True, padx=5, pady=5)

        # Marco calculadora
        marco_calculadora = tk.Frame(marco_principal, bg="#395B64", padx=15, pady=15)
        marco_calculadora.pack(side="left", fill="y", padx=5)

        # Encabezado
        etiqueta_encabezado = tk.Label(
            marco_calculadora,
            text="Calculadora Avanzada",
            font=("Roboto", 24, "bold"),
            bg="#395B64",
            fg="#E7F6F2",
        )
        etiqueta_encabezado.pack(pady=15)

        # Entrada de texto
        self.entrada_var = tk.StringVar()
        self.entrada_texto = tk.Entry(
            marco_calculadora,
            textvariable=self.entrada_var,
            font=("Roboto Mono", 20),
            width=20,
            bg="#A5C9CA",
            fg="#2C3333",
            bd=0,
            relief="flat",
            justify="right",
            insertbackground="#2C3333",
        )
        self.entrada_texto.pack(pady=15, ipady=10)

        # Resultado
        self.resultado_var = tk.StringVar()
        etiqueta_resultado = tk.Label(
            marco_calculadora,
            textvariable=self.resultado_var,
            font=("Roboto Mono", 28, "bold"),
            bg="#395B64",
            fg="#E7F6F2",
            height=2,
        )
        etiqueta_resultado.pack(pady=15)

        # Marco de botones
        marco_botones = tk.Frame(marco_calculadora, bg="#395B64")
        marco_botones.pack(pady=15, expand=True, fill="both")

        # Configurar el grid para que se expanda
        for i in range(5):  # 5 filas
            marco_botones.grid_rowconfigure(i, weight=1)
        for i in range(4):  # 4 columnas
            marco_botones.grid_columnconfigure(i, weight=1)

        # Botones
        botones = [
            ("C", 0, 0, "#E7F6F2", "#2C3333"), ("(", 0, 1), (")", 0, 2), ("/", 0, 3, "#A5C9CA", "#2C3333"),
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("*", 1, 3, "#A5C9CA", "#2C3333"),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("-", 2, 3, "#A5C9CA", "#2C3333"),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("+", 3, 3, "#A5C9CA", "#2C3333"),
            ("0", 4, 0, None, None, 2), (".", 4, 2), ("=", 4, 3, "#E7F6F2", "#2C3333"),
        ]

        for boton in botones:
            if len(boton) >= 5:
                texto, fila, columna, bg_color, fg_color = boton[:5]
                colspan = boton[5] if len(boton) > 5 else 1
            else:
                texto, fila, columna = boton
                bg_color, fg_color = "#395B64", "#E7F6F2"
                colspan = 1

            tk.Button(
                marco_botones,
                text=texto,
                font=("Roboto", 16, "bold"),
                width=4,
                height=1,
                bg=bg_color,
                fg=fg_color,
                bd=0,
                relief="flat",
                activebackground="#A5C9CA",
                activeforeground="#2C3333",
                command=lambda t=texto: self.clic_boton(t),
            ).grid(row=fila, column=columna, columnspan=colspan, padx=3, pady=3, sticky="nsew")

        # Inicializar factor de zoom
        self.zoom_factor = 0.7
        
        # Marco para el árbol con controles de zoom
        marco_arbol = tk.Frame(marco_principal, bg="#395B64", padx=15, pady=15)
        marco_arbol.pack(side="left", fill="both", expand=True, padx=5)

        # Controles de zoom
        frame_zoom = tk.Frame(marco_arbol, bg="#395B64")
        frame_zoom.pack(fill="x", pady=5)

        tk.Button(
            frame_zoom,
            text="🔍+",
            font=("Roboto", 10, "bold"),
            bg="#A5C9CA",
            fg="#2C3333",
            command=self.zoom_in
        ).pack(side="left", padx=2)

        tk.Button(
            frame_zoom,
            text="🔍-",
            font=("Roboto", 10, "bold"),
            bg="#A5C9CA",
            fg="#2C3333",
            command=self.zoom_out
        ).pack(side="left", padx=2)

        # Canvas con scroll
        self.frame_canvas = tk.Frame(marco_arbol)
        self.frame_canvas.pack(fill="both", expand=True)

        # Scrollbars
        self.h_scrollbar = tk.Scrollbar(self.frame_canvas, orient="horizontal")
        self.h_scrollbar.pack(side="bottom", fill="x")
        
        self.v_scrollbar = tk.Scrollbar(self.frame_canvas)
        self.v_scrollbar.pack(side="right", fill="y")

        # Canvas modificado
        self.lienzo_arbol = tk.Canvas(
            self.frame_canvas,
            width=600,
            height=500,
            bg="#A5C9CA",
            bd=0,
            highlightthickness=0,
            xscrollcommand=self.h_scrollbar.set,
            yscrollcommand=self.v_scrollbar.set
        )
        self.lienzo_arbol.pack(fill="both", expand=True)

        # Configurar scrollbars
        self.h_scrollbar.config(command=self.lienzo_arbol.xview)
        self.v_scrollbar.config(command=self.lienzo_arbol.yview)

        # Bind eventos de zoom
        self.lienzo_arbol.bind("<Control-MouseWheel>", self.zoom_wheel)
        self.lienzo_arbol.bind("<Control-Button-4>", self.zoom_wheel)  # Linux
        self.lienzo_arbol.bind("<Control-Button-5>", self.zoom_wheel)  # Linux

        # Agregar marco para la tabla de tokens
        marco_tokens = tk.Frame(marco_principal, bg="#395B64", padx=15, pady=15)
        marco_tokens.pack(side="left", fill="both", expand=True, padx=5)

        # Título de la tabla de tokens
        etiqueta_tokens = tk.Label(
            marco_tokens,
            text="Tabla de Tokens",
            font=("Roboto", 20, "bold"),
            bg="#395B64",
            fg="#E7F6F2",
        )
        etiqueta_tokens.pack(pady=15)

        # Frame para la tabla con scroll
        frame_tabla = tk.Frame(marco_tokens)
        frame_tabla.pack(fill="both", expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(frame_tabla)
        scrollbar.pack(side="right", fill="y")

        # Tabla de tokens (Treeview)
        self.tabla_tokens = ttk.Treeview(
            frame_tabla,
            columns=("Token", "Tipo"),
            show="headings",
            height=15
        )
        self.tabla_tokens.heading("Token", text="Token")
        self.tabla_tokens.heading("Tipo", text="Tipo")
        self.tabla_tokens.column("Token", width=100)
        self.tabla_tokens.column("Tipo", width=150)
        self.tabla_tokens.pack(fill="both", expand=True)

        # Configurar scrollbar
        self.tabla_tokens.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.tabla_tokens.yview)

        # Contador de tokens
        self.frame_contadores = tk.Frame(marco_tokens, bg="#395B64")
        self.frame_contadores.pack(fill="x", pady=10)

        self.label_total_numeros = tk.Label(
            self.frame_contadores,
            text="Total números: 0",
            font=("Roboto", 12),
            bg="#395B64",
            fg="#E7F6F2"
        )
        self.label_total_numeros.pack()

        self.label_total_operadores = tk.Label(
            self.frame_contadores,
            text="Total operadores: 0",
            font=("Roboto", 12),
            bg="#395B64",
            fg="#E7F6F2"
        )
        self.label_total_operadores.pack()

        # Botón de retroceso (←)
        tk.Button(
            marco_calculadora,
            text="←",
            font=("Roboto", 16, "bold"),
            bg="#A5C9CA",
            fg="#2C3333",
            command=self.borrar_ultimo
        ).pack(pady=5)

        # Marco para botones MS y MR juntos
        marco_memoria = tk.Frame(marco_calculadora, bg="#395B64")
        marco_memoria.pack(pady=5)
        
        tk.Button(
            marco_memoria,
            text="MS",
            font=("Roboto", 12, "bold"),
            bg="#A5C9CA",
            fg="#2C3333",
            command=self.guardar_en_memoria
        ).pack(side="left", padx=2)
        
        tk.Button(
            marco_memoria,
            text="MR",
            font=("Roboto", 12, "bold"),
            bg="#A5C9CA",
            fg="#2C3333",
            command=self.recuperar_de_memoria
        ).pack(side="left", padx=2)

    def actualizar_tabla_tokens(self):
        # Limpiar tabla
        for item in self.tabla_tokens.get_children():
            self.tabla_tokens.delete(item)
        
        # Obtener y mostrar tokens
        expresion = self.entrada_var.get()
        tokens = self.logica.analizar_tokens(expresion)
        
        for tipo, valor in tokens:
            self.tabla_tokens.insert("", "end", values=(valor, tipo))

        # Actualizar contadores
        conteo = self.logica.contar_tokens()
        self.label_total_numeros.config(text=f"Total números: {conteo['total_numeros']}")
        self.label_total_operadores.config(text=f"Total operadores: {conteo['total_operadores']}")

    def borrar_ultimo(self):
        texto_actual = self.entrada_var.get()
        if texto_actual:
            self.entrada_var.set(texto_actual[:-1])
            self.actualizar_tabla_tokens()

    def guardar_en_memoria(self):
        try:
            resultado = float(self.resultado_var.get())
            self.logica.guardar_en_memoria(resultado)
            messagebox.showinfo("Memoria", "Valor guardado en memoria")
        except:
            messagebox.showerror("Error", "No hay resultado para guardar")

    def clic_boton(self, caracter):
        if caracter == "=":
            try:
                expresion = self.entrada_var.get()
                if not self.parentesis_balanceados(expresion):
                    messagebox.showerror("Error", "Los paréntesis no están balanceados")
                    return
                resultado = self.logica.calcular_resultado(expresion)
                self.resultado_var.set(resultado)
                arbol = self.logica.generar_arbol(expresion)
                self.dibujar_arbol(arbol)
                self.actualizar_tabla_tokens()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        elif caracter == "C":
            self.limpiar()
        else:
            self.entrada_var.set(self.entrada_var.get() + caracter)
            self.actualizar_tabla_tokens()

    def parentesis_balanceados(self, expresion):
        """Verifica si los paréntesis están correctamente balanceados"""
        contador = 0
        for char in expresion:
            if char == '(':
                contador += 1
            elif char == ')':
                contador -= 1
            if contador < 0:
                return False
        return contador == 0

    def dibujar_arbol(self, arbol, x=300, y=30, coords_padre=None):
        """Dibuja el árbol de derivación en el lienzo."""
        self.arbol_actual = arbol  # Guardar el árbol actual
        self.redibujar_arbol()

    def redibujar_arbol(self):
        """Redibuja el árbol con el factor de zoom actual"""
        if not hasattr(self, 'arbol_actual'):
            return

        self.lienzo_arbol.delete("all")
        radio_nodo = 20 * self.zoom_factor

        def calcular_dimensiones(nodo):
            """Calcula las dimensiones totales necesarias para el árbol"""
            if isinstance(nodo, tuple):
                _, izq, der = nodo
                izq_w, izq_h = calcular_dimensiones(izq)
                der_w, der_h = calcular_dimensiones(der)
                return max(izq_w + der_w, 200), max(izq_h, der_h) + 100
            return 100, 100

        def dibujar_nodo(x, y, texto, coords_padre=None):
            x_scaled = x * self.zoom_factor
            y_scaled = y * self.zoom_factor

            self.lienzo_arbol.create_oval(
                x_scaled - radio_nodo,
                y_scaled - radio_nodo,
                x_scaled + radio_nodo,
                y_scaled + radio_nodo,
                fill="#E7F6F2",
                outline="#395B64",
                width=2
            )
            self.lienzo_arbol.create_text(
                x_scaled, y_scaled,
                text=texto,
                font=("Roboto", int(10 * self.zoom_factor), "bold"),
                fill="#2C3333"
            )
            if coords_padre:
                self.lienzo_arbol.create_line(
                    coords_padre[0] * self.zoom_factor,
                    (coords_padre[1] + radio_nodo/self.zoom_factor) * self.zoom_factor,
                    x_scaled,
                    y_scaled - radio_nodo,
                    width=2,
                    fill="#395B64"
                )

        def recorrer_arbol(nodo, x, y, coords_padre=None, nivel=0):
            if isinstance(nodo, tuple):
                texto, izq, der = nodo
                espaciado_horizontal = 150 / (nivel + 1)
                dibujar_nodo(x, y, texto, coords_padre)
                recorrer_arbol(izq, x - espaciado_horizontal, y + 60, (x, y), nivel + 1)
                recorrer_arbol(der, x + espaciado_horizontal, y + 60, (x, y), nivel + 1)
            else:
                dibujar_nodo(x, y, nodo, coords_padre)

        # Calcular dimensiones totales necesarias
        width, height = calcular_dimensiones(self.arbol_actual)
        scroll_region = (-width * self.zoom_factor, 0, 
                        width * self.zoom_factor, height * self.zoom_factor)
        self.lienzo_arbol.configure(scrollregion=scroll_region)
        
        # Comenzar el dibujo desde el centro
        recorrer_arbol(self.arbol_actual, 0, 30)

    def limpiar(self):
        """Limpia la entrada y el resultado."""
        self.entrada_var.set("")
        self.resultado_var.set("")
        self.lienzo_arbol.delete("all")

    def recuperar_de_memoria(self):
        """Recupera el valor guardado en memoria"""
        try:
            valor = self.logica.obtener_de_memoria()
            texto_actual = self.entrada_var.get()
            self.entrada_var.set(texto_actual + valor)
            self.actualizar_tabla_tokens()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def zoom_wheel(self, event):
        """Maneja el zoom con la rueda del mouse"""
        if event.delta > 0 or event.num == 4:
            self.zoom_in()
        elif event.delta < 0 or event.num == 5:
            self.zoom_out()

    def zoom_in(self):
        """Aumenta el zoom"""
        if self.zoom_factor < 2.0:
            self.zoom_factor *= 1.1
            self.redibujar_arbol()

    def zoom_out(self):
        """Reduce el zoom"""
        if self.zoom_factor > 0.3:
            self.zoom_factor *= 0.9
            self.redibujar_arbol()


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraApp(root)
    root.mainloop()
