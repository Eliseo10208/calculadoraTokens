class CalculadoraLogica:
    def __init__(self):
        self.tokens = []
        self.memoria = None

    def calcular_resultado(self, expresion):
        """Calcula el resultado de la expresión ingresada."""
        try:
            resultado = eval(expresion)  # Evalúa la operación matemática
            return resultado
        except Exception as e:
            raise ValueError("Error en la operación: " + str(e))

    def generar_arbol(self, expresion):
        """Genera una representación estructurada del árbol de derivación."""
        arbol = []

        def analizar_expresion(expr):
            if '+' in expr:
                izq, der = expr.split('+', 1)
                return ('Suma', analizar_expresion(izq.strip()), analizar_expresion(der.strip()))
            elif '-' in expr:
                izq, der = expr.split('-', 1)
                return ('Resta', analizar_expresion(izq.strip()), analizar_expresion(der.strip()))
            elif '*' in expr:
                izq, der = expr.split('*', 1)
                return ('Multiplicación', analizar_expresion(izq.strip()), analizar_expresion(der.strip()))
            elif '/' in expr:
                izq, der = expr.split('/', 1)
                return ('División', analizar_expresion(izq.strip()), analizar_expresion(der.strip()))
            else:
                return expr

        arbol = analizar_expresion(expresion)
        return arbol

    def analizar_tokens(self, expresion):
        self.tokens = []
        numero_actual = ''
        
        for char in expresion:
            if char.isdigit() or char == '.':
                numero_actual += char
            else:
                if numero_actual:
                    # Determinar si es entero o decimal
                    tipo = 'Número decimal' if '.' in numero_actual else 'Número entero'
                    self.tokens.append((tipo, numero_actual))
                    numero_actual = ''
                if char in '+-*/':
                    tipo = {
                        '+': 'Operador suma',
                        '-': 'Operador resta',
                        '*': 'Operador multiplicación',
                        '/': 'Operador división'
                    }[char]
                    self.tokens.append((tipo, char))
                elif char in '()':
                    self.tokens.append(('Paréntesis', char))
                    
        if numero_actual:
            # Determinar si es entero o decimal para el último número
            tipo = 'Número decimal' if '.' in numero_actual else 'Número entero'
            self.tokens.append((tipo, numero_actual))
            
        return self.tokens

    def contar_tokens(self):
        numeros = sum(1 for tipo, _ in self.tokens if tipo in ['Número entero', 'Número decimal'])
        operadores = sum(1 for tipo, _ in self.tokens if 'Operador' in tipo)
        return {
            'total_numeros': numeros,
            'total_operadores': operadores
        }

    def guardar_en_memoria(self, valor):
        self.memoria = valor

    def obtener_de_memoria(self):
        if self.memoria is not None:
            # Convertir a entero si es un número sin decimales
            if self.memoria == int(self.memoria):
                return str(int(self.memoria))
            return str(self.memoria)
        raise ValueError("No hay valor guardado en memoria")
