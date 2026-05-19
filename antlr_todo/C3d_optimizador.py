import re


class C3DOptimizador:

    def __init__(self, codigo: list, tabla_simbolos: dict):
        self.codigo = [l.strip() for l in codigo if l.strip()]
        self.tabla = tabla_simbolos

    # ENTRADA PRINCIPAL

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

        inversiones = {
            ' minog ': ' aye ',
            ' aye ': ' minog ',
            ' compag ': ' compag '
        }

        for a, b in inversiones.items():
            if a in cond:
                return cond.replace(a, b, 1)

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

            # reemplazar SOLO RHS
            for temp, valor in constantes.items():
                expr = re.sub(r'\b' + re.escape(temp) + r'\b', valor, expr)

            nueva = f"{dest} = {expr}"
            resultado.append(nueva)

            # registrar constantes
            if self._es_temp(dest):

                if self._es_numero(expr) or self._es_string(expr):
                    constantes[dest] = expr
                else:
                    if dest in constantes:
                        del constantes[dest]

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

            # reemplazar RHS
            for temp, original in copias.items():
                expr = re.sub(r'\b' + re.escape(temp) + r'\b', original, expr)

            nueva = f"{dest} = {expr}"
            resultado.append(nueva)

            # detectar copia pura
            if self._es_temp(dest):

                if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', expr):
                    copias[dest] = expr
                else:
                    if dest in copias:
                        del copias[dest]

            # invalidar si cambia variable original
            invalidos = []

            for temp, original in copias.items():
                if original == dest:
                    invalidos.append(temp)

            for x in invalidos:
                del copias[x]

        return resultado

    # 3. SIMPLIFICAR TEMPORALES

    def _simplificar_temporales(self, codigo):

        resultado = []

        i = 0

        while i < len(codigo):

            actual = codigo[i].strip()

            if i + 1 < len(codigo):

                siguiente = codigo[i + 1].strip()

                # t1 = x + y
                # a = t1
                m1 = re.match(r'^(t\d+)\s*=\s*(.+)$', actual)
                m2 = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(t\d+)$', siguiente)

                if m1 and m2:

                    temp1 = m1.group(1)
                    expr = m1.group(2)

                    destino = m2.group(1)
                    temp2 = m2.group(2)

                    if temp1 == temp2:

                        resultado.append(f"{destino} = {expr}")

                        i += 2
                        continue

            resultado.append(actual)
            i += 1

        return resultado

    # 4. ELIMINAR MUERTOS

    def _eliminar_muertos(self, codigo):

        usados = set()

        # detectar usos
        for linea in codigo:

            l = linea.strip()

            if '=' in l:

                rhs = l.split('=', 1)[1]

                temps = re.findall(r'\bt\d+\b', rhs)

                for t in temps:
                    usados.add(t)

            else:

                temps = re.findall(r'\bt\d+\b', l)

                for t in temps:
                    usados.add(t)

        resultado = []

        for linea in codigo:

            l = linea.strip()

            if '=' in l and not l.startswith('if '):

                dest = l.split('=', 1)[0].strip()

                if self._es_temp(dest) and dest not in usados:
                    continue

            resultado.append(l)

        return resultado

    # 5. REDUCCION DE SALTOS

    def _reducir_saltos(self, codigo):

        resultado = list(codigo)

        i = 0

        while i < len(resultado) - 2:

            l1 = resultado[i].strip()
            l2 = resultado[i + 1].strip()
            l3 = resultado[i + 2].strip()

            if (
                l1.startswith('if ')
                and ' goto ' in l1
                and l2.startswith('goto ')
                and l3.endswith(':')
            ):

                label_true = l1.split()[-1]
                label_false = l2.split()[-1]
                label_next = l3[:-1]

                if label_true == label_next:

                    idx = l1.rfind(' goto ')

                    condicion = l1[3:idx].strip()

                    invertida = self._invertir_operador(condicion)

                    if invertida:

                        resultado[i] = f"if {invertida} goto {label_false}"
                        resultado.pop(i + 1)

                        continue

            i += 1

        return resultado

    # 6. ELIMINAR GOTO INUTIL

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