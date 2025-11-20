import tkinter as tk
from tkinter import ttk
import calculos  
import simulacion

class MarkovApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modelo de Colas - Cadena de Markov")
        self.root.geometry("900x450")

        # ---------------- PANEL IZQUIERDO (FIJO) ----------------
        self.left_frame = ttk.Frame(self.root, padding=10)
        self.left_frame.pack(side="left", fill="y")

        self.create_left_panel()

        # ---------------- PANEL DERECHO ----------------
        self.right_frame = ttk.Frame(self.root, padding=10)
        self.right_frame.pack(side="right", fill="both", expand=True)

        # Notebook dentro del panel derecho
        self.notebook = ttk.Notebook(self.right_frame)
        self.notebook.pack(fill="both", expand=True)

        # ---- Crear pestañas ----
        self.tab_calculos = ttk.Frame(self.notebook)
        self.tab_simulacion = ttk.Frame(self.notebook)
        self.tab_analisis = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_calculos, text="Cálculos")
        self.notebook.add(self.tab_simulacion, text="Simulación")
        self.notebook.add(self.tab_analisis, text="Análisis")

        # ---------------- CONTENIDO DE CADA PESTAÑA ----------------

        # Pestaña cálculos → solo resultados
        self.result_label = ttk.Label(
            self.tab_calculos,
            text="",
            font=("Arial", 12, "bold"),
            anchor="center",
            justify="center"
        )
        self.result_label.pack(expand=True)

        # ---------- TABLA SIMULACIÓN ----------
        self.sim_frame = ttk.Frame(self.tab_simulacion)
        self.sim_frame.pack(fill="both", expand=True)

        self.sim_scroll = ttk.Scrollbar(self.sim_frame)
        self.sim_scroll.pack(side="right", fill="y")

        self.sim_table = ttk.Treeview(
            self.sim_frame,
            yscrollcommand=self.sim_scroll.set,
            columns=("t","N","Lq","estado","W","L","P0","Tinest"),
            show="headings",
            height=18
        )

        self.sim_scroll.config(command=self.sim_table.yview)

        # Encabezados
        encabezados = {
            "t": "Tiempo (min)",
            "N": "N(t)",
            "Lq": "Lq(t)",
            "estado": "Estado",
            "W": "W",
            "L": "L",
            "P0": "P0",
            "Tinest": "T inestable"
        }

        for col, nombre in encabezados.items():
            self.sim_table.heading(col, text=nombre)
            self.sim_table.column(col, width=90, anchor="center")

        self.sim_table.pack(fill="both", expand=True)

        # Pestaña análisis
        self.analisis_label = tk.Text(self.tab_analisis, width=70, height=22)
        self.analisis_label.pack(padx=10, pady=10)
        self.analisis_label.insert(tk.END,
        """
ANÁLISIS DEL MODELO

• d) Estabilidad del sistema
• e) Comparación entre cálculos y simulación
• Interpretación del tiempo en estado inestable
        """
        )


    # -----------------------------------------------------
    # PANEL IZQUIERDO
    # -----------------------------------------------------
    def create_left_panel(self):

        ttk.Label(self.left_frame, text="Matriz P", font=("Arial", 12, "bold")).pack(pady=5)

        matrix_frame = ttk.Frame(self.left_frame)
        matrix_frame.pack(pady=5)

        P_default = [[0.8, 0.2],[0.4, 0.6]]

        self.matrix_entries = []
        for i in range(2):
            row = []
            for j in range(2):
                e = ttk.Entry(matrix_frame, width=10, justify="center")
                e.grid(row=i, column=j, padx=5, pady=5)
                e.insert(0, str(P_default[i][j]))
                row.append(e)
            self.matrix_entries.append(row)

        # Parámetros
        etiquetas = [
            ("λ (tasa de llegada):", "5"),
            ("μ (tasa de servicio):", "4"),
            ("Estado 1 (c₁):", "2"),
            ("Estado 2 (c₂):", "1"),
            ("t (tiempo simulación, min):", "5")
        ]

        self.lambda_entry = self.agregar_entry(etiquetas[0])
        self.mu_entry     = self.agregar_entry(etiquetas[1])
        self.c1_entry     = self.agregar_entry(etiquetas[2])
        self.c2_entry     = self.agregar_entry(etiquetas[3])
        self.t_entry      = self.agregar_entry(etiquetas[4])

        ttk.Button(self.left_frame, text="Calcular", command=self.calculate).pack(pady=10)

    def agregar_entry(self, data):
        label, valor = data
        ttk.Label(self.left_frame, text=label).pack(anchor="w", pady=2)
        entry = ttk.Entry(self.left_frame)
        entry.insert(0, valor)
        entry.pack(fill="x", pady=2)
        return entry

    # -----------------------------------------------------
    # FUNCIÓN PRINCIPAL DE CÁLCULO
    # -----------------------------------------------------
    def calculate(self):
        try:
            # Obtener matriz P
            P = [[float(self.matrix_entries[i][j].get()) for j in range(2)] for i in range(2)]

            lam = float(self.lambda_entry.get())
            mu = float(self.mu_entry.get())
            c1 = int(self.c1_entry.get())
            c2 = int(self.c2_entry.get())
            total_minutes = float(self.t_entry.get())

            # ---- A) Calcular π ----
            pi = calculos.calcular_pi(P)

            # ---- B) Cálculos teóricos ----
            p1 = calculos.calcular_intensidades(lam, mu, c1)
            p2 = calculos.calcular_intensidades(lam, mu, c2)
            p_pond = pi[0]*p1 + pi[1]*p2

            l1 = calculos.calcular_clientes(lam, mu, p1, c1)
            l2 = calculos.calcular_clientes(lam, mu, p2, c2)
            L_pond = pi[0]*l1 + pi[1]*l2
            W_pond = L_pond / lam

            # Mostrar en cálculos
            self.result_label.config(text=
                f"π = [{pi[0]:.4f}, {pi[1]:.4f}]\n\n"
                f"p ponderado = {p_pond:.4f}\n"
                f"L ponderado = {L_pond:.4f}\n"
                f"W ponderado = {W_pond:.4f}\n"
                f"(Simulación con t = {total_minutes} min)"
            )

            # ---- Simulación ----
            texto_sim = simulacion.simular(lam, mu, P, c1, c2, total_minutes)

            # Limpiar tabla
            for item in self.sim_table.get_children():
                self.sim_table.delete(item)

            # Insertar registros
            for row in texto_sim:
                self.sim_table.insert("", "end", values=(
                    row["t"], row["N"], row["Lq"], row["estado"],
                    f"{row['W']:.4f}", f"{row['L']:.4f}",
                    f"{row['P0']:.4f}", f"{row['T_inestable']:.4f}"
                ))

        except Exception as e:
            self.result_label.config(text=f"⚠️ Error: {e}")


# --- Ejecutar aplicación ---
if __name__ == "__main__":
    root = tk.Tk()
    app = MarkovApp(root)
    root.mainloop()
