import re

class C3DOptimizador:

    def __init__(self, codigo: list, tabla_simbolos: dict):
        self.codigo = [l.strip() for l in codigo if l.strip()]
        self.tabla = tabla_simbolos

    def optimizar(self):
        codigo = list(self.codigo)
        for _ in range(10):
            anterior = list(codigo)
            codigo = self._propagar_constantes(codigo)
            codigo = self._propagar_copias(codigo)
            codigo = self._simplificar_temporales(codigo)
            codigo = self._eliminar_muertos(codigo)
            codigo = self._reducir_saltos(codigo)
            codigo = self._eliminar_goto_siguiente(codigo)
            codigo = self._reutilizar_temporales(codigo)
            if codigo == anterior:
                break
        return codigo

    # HELPERS
    @staticmethod
    def _es_temp(nombre):
        return re.match(r'^t\d+$', nombre) is not None

    @staticmethod
    def _es_numero(txt):
        try:
            float(txt)
            return True
        except:
            return False

    @staticmethod
    def _es_string(txt):
        return txt.startswith('"') and txt.endswith('"')

    @staticmethod
    def _invertir_operador(cond):
        if ' minog ' in cond:
            return cond.replace(' minog ', ' aye ')
        if ' aye ' in cond:
            return cond.replace(' aye ', ' minog ')
        # compag no se invierte fácilmente, se deja igual
        return None

    # 1. PROPAGACION CONSTANTES
    def _propagar_constantes(self, codigo):
        constantes = {}
        resultado = []
        for linea in codigo:
            l = linea.strip()
            if '=' not in l or l.startswith('if ') or l.endswith(':'):
                resultado.append(l)
                continue
            dest, expr = l.split('=', 1)
            dest = dest.strip()
            expr = expr.strip()
            for temp, valor in constantes.items():
                expr = re.sub(r'\b' + re.escape(temp) + r'\b', valor, expr)
            nueva = f"{dest} = {expr}"
            resultado.append(nueva)
            if self._es_temp(dest):
                if self._es_numero(expr) or self._es_string(expr):
                    constantes[dest] = expr
                else:
                    constantes.pop(dest, None)
        return resultado

    # 2. PROPAGACION COPIAS
    def _propagar_copias(self, codigo):
        copias = {}
        resultado = []
        for linea in codigo:
            l = linea.strip()
            if '=' not in l or l.startswith('if ') or l.endswith(':'):
                resultado.append(l)
                continue
            dest, expr = l.split('=', 1)
            dest = dest.strip()
            expr = expr.strip()
            for temp, original in copias.items():
                expr = re.sub(r'\b' + re.escape(temp) + r'\b', original, expr)
            nueva = f"{dest} = {expr}"
            resultado.append(nueva)
            if self._es_temp(dest):
                if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', expr):
                    copias[dest] = expr
                else:
                    copias.pop(dest, None)
            for t, orig in list(copias.items()):
                if orig == dest:
                    del copias[t]
        return resultado

    # 3. SIMPLIFICAR TEMPORALES (t1 = x; a = t1  -> a = x)
    def _simplificar_temporales(self, codigo):
        resultado = []
        i = 0
        while i < len(codigo):
            actual = codigo[i].strip()
            if i + 1 < len(codigo):
                siguiente = codigo[i + 1].strip()
                m1 = re.match(r'^(t\d+)\s*=\s*(.+)$', actual)
                m2 = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(t\d+)$', siguiente)
                if m1 and m2 and m1.group(1) == m2.group(2):
                    resultado.append(f"{m2.group(1)} = {m1.group(2)}")
                    i += 2
                    continue
            resultado.append(actual)
            i += 1
        return resultado

    # 4. ELIMINAR MUERTOS (temporales no usados)
    def _eliminar_muertos(self, codigo):
        usados = set()
        for linea in codigo:
            l = linea.strip()
            # Buscar usos en RHS
            if '=' in l:
                rhs = l.split('=', 1)[1]
                usados.update(re.findall(r'\bt\d+\b', rhs))
            else:
                usados.update(re.findall(r'\bt\d+\b', l))
        resultado = []
        for linea in codigo:
            l = linea.strip()
            if '=' in l and not l.startswith('if ') and not l.endswith(':'):
                dest = l.split('=', 1)[0].strip()
                if self._es_temp(dest) and dest not in usados:
                    continue
            resultado.append(l)
        return resultado

    # 5. REDUCCION DE SALTOS (if cond goto L1; goto L2; L1: ...  -> if !cond goto L2)
    def _reducir_saltos(self, codigo):
        resultado = list(codigo)
        i = 0
        while i < len(resultado) - 2:
            l1 = resultado[i].strip()
            l2 = resultado[i + 1].strip()
            l3 = resultado[i + 2].strip()
            if (l1.startswith('if ') and ' goto ' in l1 and
                l2.startswith('goto ') and l3.endswith(':')):
                label_true = l1.split()[-1]
                label_false = l2.split()[-1]
                label_next = l3[:-1]
                if label_true == label_next:
                    idx = l1.rfind(' goto ')
                    cond = l1[3:idx].strip()
                    invertida = self._invertir_operador(cond)
                    if invertida:
                        resultado[i] = f"if {invertida} goto {label_false}"
                        resultado.pop(i + 1)
                        continue
            i += 1
        return resultado

    # 6. ELIMINAR GOTO INUTIL (goto L; L: -> eliminar goto)
    def _eliminar_goto_siguiente(self, codigo):
        resultado = []
        i = 0
        while i < len(codigo):
            actual = codigo[i].strip()
            if actual.startswith('goto ') and i + 1 < len(codigo):
                label = actual.split()[1]
                siguiente = codigo[i + 1].strip()
                if siguiente == f"{label}:":
                    i += 1
                    continue
            resultado.append(actual)
            i += 1
        return resultado

    # 7. REUTILIZAR TEMPORALES (renumerar secuencialmente)
    def _reutilizar_temporales(self, codigo):
        temp_map = {}
        next_temp = 1
        nuevo_codigo = []
        for linea in codigo:
            l = linea.strip()
            def repl(m):
                nonlocal next_temp
                t = m.group(0)
                if t not in temp_map:
                    temp_map[t] = f"t{next_temp}"
                    next_temp += 1
                return temp_map[t]
            nueva = re.sub(r'\bt\d+\b', repl, l)
            nuevo_codigo.append(nueva)
        return nuevo_codigo