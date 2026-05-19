import re


class C3DOptimizador:
    """
    Optimizador de Codigo de Tres Direcciones.
    Aplica las siguientes pasadas en orden:
      1. Propagacion de constantes
      2. Propagacion de copias
      3. Eliminacion de codigo muerto (variables temporales no usadas)
      4. Reduccion de saltos redundantes
      5. Eliminacion de goto seguido de su propia etiqueta
    """

    def __init__(self, codigo: list, tabla_simbolos: dict):
        self.codigo  = [l for l in codigo if l.strip()]
        self.tabla   = tabla_simbolos

    #  punto de entrada 

    def optimizar(self):
        codigo = self.codigo

        # pasadas iterativas hasta que no haya cambios
        for _ in range(10):
            anterior = list(codigo)
            codigo = self._propagar_constantes(codigo)
            codigo = self._propagar_copias(codigo)
            codigo = self._eliminar_muertos(codigo)
            codigo = self._reducir_saltos(codigo)
            codigo = self._eliminar_goto_siguiente(codigo)
            if codigo == anterior:
                break

        return codigo

    #  helper: detectar si un token es constante numerica 

    @staticmethod
    def _es_numero(val):
        try:
            float(val)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def _es_string_lit(val):
        return isinstance(val, str) and val.startswith('"')

    @staticmethod
    def _es_temp(nombre):
        return re.match(r'^t\d+$', nombre) is not None

    #  1. PROPAGACION DE CONSTANTES 
    # Si t1 = 5 y luego se usa t1, reemplaza t1 por 5
    # Solo para temporales con valor constante

    def _propagar_constantes(self, codigo):
        constantes = {}

        # primer recorrido: recolectar temporales con valor constante
        for linea in codigo:
            l = linea.strip()
            if '=' in l and not l.startswith('if') and not l.endswith(':'):
                dest, expr = l.split('=', 1)
                dest = dest.strip()
                expr = expr.strip()
                if self._es_temp(dest) and self._es_numero(expr):
                    constantes[dest] = expr
                elif self._es_temp(dest) and self._es_string_lit(expr):
                    constantes[dest] = expr

        if not constantes:
            return codigo

        # segundo recorrido: reemplazar usos
        resultado = []
        for linea in codigo:
            l = linea.strip()
            nueva = l
            for temp, val in constantes.items():
                # reemplazar solo como token completo (no parte de otro nombre)
                nueva = re.sub(r'\b' + re.escape(temp) + r'\b', val, nueva)
            resultado.append(nueva)

        return resultado

    #  2. PROPAGACION DE COPIAS 
    # Si t1 = x y luego usa t1, reemplaza t1 por x
    # Solo si x no cambia entre la asignacion y el uso

    def _propagar_copias(self, codigo):
        copias = {}

        for linea in codigo:
            l = linea.strip()
            if '=' in l and not l.startswith('if') and not l.endswith(':'):
                dest, expr = l.split('=', 1)
                dest = dest.strip()
                expr = expr.strip()
                # copia pura: dest = var (sin operadores)
                if (self._es_temp(dest)
                        and re.match(r'^[a-zA-Z_][a-zA-Z_0-9]*$', expr)
                        and expr not in ('call',)):
                    copias[dest] = expr
                # si el origen se reasigna, invalidar copias que lo usen
                if not self._es_temp(dest):
                    invalidos = [k for k, v in copias.items() if v == dest]
                    for k in invalidos:
                        del copias[k]

        if not copias:
            return codigo

        resultado = []
        for linea in codigo:
            l = linea.strip()
            nueva = l
            for temp, var in copias.items():
                nueva = re.sub(r'\b' + re.escape(temp) + r'\b', var, nueva)
            resultado.append(nueva)

        return resultado

    #  3. ELIMINACION DE CODIGO MUERTO 
    # Elimina temporales que se asignan pero nunca se usan

    def _eliminar_muertos(self, codigo):
        # contar usos de cada temporal
        usos = {}
        for linea in codigo:
            l = linea.strip()
            # en el lado derecho / condiciones buscar temporales
            tokens = re.findall(r'\bt\d+\b', l)
            for t in tokens:
                usos[t] = usos.get(t, 0)

        # marcar definiciones
        definidos = {}
        for i, linea in enumerate(codigo):
            l = linea.strip()
            if '=' in l and not l.startswith('if') and not l.endswith(':'):
                dest = l.split('=')[0].strip()
                if self._es_temp(dest):
                    definidos[dest] = i

        # contar usos en el lado derecho
        for linea in codigo:
            l = linea.strip()
            # separar lado derecho
            if '=' in l and not l.startswith('if') and not l.endswith(':'):
                rhs = l.split('=', 1)[1]
            else:
                rhs = l
            tokens = re.findall(r'\bt\d+\b', rhs)
            for t in tokens:
                usos[t] = usos.get(t, 0) + 1

        # eliminar lineas donde el temporal nunca se usa fuera de su definicion
        lineas_eliminar = set()
        for temp, idx in definidos.items():
            if usos.get(temp, 0) == 0:
                lineas_eliminar.add(idx)

        return [l for i, l in enumerate(codigo) if i not in lineas_eliminar]

    #  4. REDUCCION DE SALTOS REDUNDANTES 
    # Patron:
    #   if cond goto L1
    #   goto L2
    #   L1:
    # Se puede transformar a:
    #   if !cond goto L2
    #   L1:
    # (elimina el goto L2 intermedio)

    @staticmethod
    def _invertir_op(cond):
        inversiones = {
            ' minog ': ' aye ',
            ' aye ':   ' minog ',
            ' compag ': ' compag ',
        }
        for op, inv in inversiones.items():
            if op in cond:
                return cond.replace(op, inv, 1)
        return None

    def _reducir_saltos(self, codigo):
        resultado = list(codigo)
        i = 0
        while i < len(resultado) - 2:
            l0 = resultado[i].strip()
            l1 = resultado[i + 1].strip()
            l2 = resultado[i + 2].strip() if i + 2 < len(resultado) else ''

            # patron: if cond goto LA / goto LB / LA:
            if (l0.startswith('if ') and ' goto ' in l0
                    and l1.startswith('goto ')
                    and l2.endswith(':') and ' ' not in l2):

                label_true = l0.split()[-1]
                label_false = l1.split()[-1]
                label_next = l2[:-1]

                if label_true == label_next:
                    # invertir condicion
                    idx_goto = l0.rfind(' goto ')
                    cond_original = l0[3:idx_goto].strip()
                    inv = self._invertir_op(cond_original)
                    if inv:
                        resultado[i]     = f"if {inv} goto {label_false}"
                        resultado[i + 1] = l2          # LA:
                        resultado.pop(i + 2)
                        continue
            i += 1

        return resultado

    #  5. ELIMINAR goto SEGUIDO DE SU PROPIA ETIQUETA 
    # goto L1 seguido inmediatamente de L1: es inutil

    def _eliminar_goto_siguiente(self, codigo):
        resultado = []
        i = 0
        while i < len(codigo):
            l = codigo[i].strip()
            if l.startswith('goto ') and i + 1 < len(codigo):
                label = l.split()[1]
                siguiente = codigo[i + 1].strip()
                if siguiente == f"{label}:":
                    i += 1
                    continue
            resultado.append(codigo[i])
            i += 1
        return resultado


#  integracion con generar_c3d.py 
# Uso:
#   from antlr_todo.C3D_optimizador import C3DOptimizador
#   opt = C3DOptimizador(generador.codigo, semantico.tabla_simbolos)
#   codigo_optimizado = opt.optimizar()