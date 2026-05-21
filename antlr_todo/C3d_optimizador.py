import re

class C3DOptimizador:

    def __init__(self, codigo: list, tabla_simbolos: dict):
        self.codigo = [l.strip() for l in codigo if l.strip()]
        self.tabla = tabla_simbolos

    def optimizar(self):
        code = list(self.codigo)
        for _ in range(10):
            prev = list(code)
            code = self._propagar_constantes(code)
            code = self._propagar_copias(code)
            code = self._simplificar_temporales(code)
            code = self._eliminar_muertos(code)
            code = self._reducir_saltos(code)
            code = self._eliminar_goto_siguiente(code)
            code = self._reutilizar_temporales(code)
            if code == prev:
                break
        return code

    # ========== UTILS ==========
    @staticmethod
    def _es_temp(n):
        return re.match(r'^t\d+$', n) is not None

    @staticmethod
    def _es_num(t):
        try:
            float(t)
            return True
        except:
            return False

    @staticmethod
    def _es_str(t):
        return t.startswith('"') and t.endswith('"')

    @staticmethod
    def _invertir(cond):
        if ' minog ' in cond:
            return cond.replace(' minog ', ' aye ')
        if ' aye ' in cond:
            return cond.replace(' aye ', ' minog ')
        return None

    # ========== PASES ==========
    def _propagar_constantes(self, code):
        const = {}
        out = []
        for line in code:
            if '=' not in line or line.startswith('if ') or line.endswith(':'):
                out.append(line)
                continue
            dst, expr = line.split('=', 1)
            dst = dst.strip()
            expr = expr.strip()
            for t, v in const.items():
                expr = re.sub(r'\b' + re.escape(t) + r'\b', v, expr)
            new = f"{dst} = {expr}"
            out.append(new)
            if self._es_temp(dst) and (self._es_num(expr) or self._es_str(expr)):
                const[dst] = expr
            else:
                const.pop(dst, None)
        return out

    def _propagar_copias(self, code):
        copies = {}
        out = []
        for line in code:
            if '=' not in line or line.startswith('if ') or line.endswith(':'):
                out.append(line)
                continue
            dst, expr = line.split('=', 1)
            dst = dst.strip()
            expr = expr.strip()
            for t, orig in copies.items():
                expr = re.sub(r'\b' + re.escape(t) + r'\b', orig, expr)
            new = f"{dst} = {expr}"
            out.append(new)
            if self._es_temp(dst) and re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', expr):
                copies[dst] = expr
            else:
                copies.pop(dst, None)
            for t, orig in list(copies.items()):
                if orig == dst:
                    del copies[t]
        return out

    def _simplificar_temporales(self, code):
        out = []
        i = 0
        while i < len(code):
            cur = code[i].strip()
            if i + 1 < len(code):
                nxt = code[i+1].strip()
                m1 = re.match(r'^(t\d+)\s*=\s*(.+)$', cur)
                m2 = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(t\d+)$', nxt)
                if m1 and m2 and m1.group(1) == m2.group(2):
                    out.append(f"{m2.group(1)} = {m1.group(2)}")
                    i += 2
                    continue
            out.append(cur)
            i += 1
        return out

    def _eliminar_muertos(self, code):
        used = set()
        for line in code:
            if '=' in line:
                rhs = line.split('=', 1)[1]
                used.update(re.findall(r'\bt\d+\b', rhs))
            else:
                used.update(re.findall(r'\bt\d+\b', line))
        out = []
        for line in code:
            if '=' in line and not line.startswith('if ') and not line.endswith(':'):
                dst = line.split('=', 1)[0].strip()
                if self._es_temp(dst) and dst not in used:
                    continue
            out.append(line)
        return out

    def _reducir_saltos(self, code):
        res = list(code)
        i = 0
        while i < len(res) - 2:
            l1 = res[i].strip()
            l2 = res[i+1].strip()
            l3 = res[i+2].strip()
            if (l1.startswith('if ') and ' goto ' in l1 and
                l2.startswith('goto ') and l3.endswith(':')):
                true_label = l1.split()[-1]
                false_label = l2.split()[-1]
                next_label = l3[:-1]
                if true_label == next_label:
                    idx = l1.rfind(' goto ')
                    cond = l1[3:idx].strip()
                    inv = self._invertir(cond)
                    if inv:
                        res[i] = f"if {inv} goto {false_label}"
                        res.pop(i+1)
                        continue
            i += 1
        return res

    def _eliminar_goto_siguiente(self, code):
        out = []
        i = 0
        while i < len(code):
            cur = code[i].strip()
            if cur.startswith('goto ') and i+1 < len(code):
                label = cur.split()[1]
                nxt = code[i+1].strip()
                if nxt == f"{label}:":
                    i += 1
                    continue
            out.append(cur)
            i += 1
        return out

    def _reutilizar_temporales(self, code):
        mapping = {}
        next_t = 1
        out = []
        for line in code:
            def repl(m):
                nonlocal next_t
                t = m.group(0)
                if t not in mapping:
                    mapping[t] = f"t{next_t}"
                    next_t += 1
                return mapping[t]
            new_line = re.sub(r'\bt\d+\b', repl, line)
            out.append(new_line)
        return out