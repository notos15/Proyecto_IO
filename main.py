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

        # Pestaña simulación
        self.simulacion_output = tk.Text(self.tab_simulacion, width=70, height=22)
        self.simulacion_output.pack(padx=10, pady=10)

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

        # MATRIZ POR DEFECTO
        P_default = [
            [0.8, 0.2],
            [0.4, 0.6]
        ]

        self.matrix_entries = []
        for i in range(2):
            row = []
            for j in range(2):
                e = ttk.Entry(matrix_frame, width=10, justify="center")
                e.grid(row=i, column=j, padx=5, pady=5)
                e.insert(0, str(P_default[i][j]))
                row.append(e)
            self.matrix_entries.append(row)

        # --- Otros datos ---
        ttk.Label(self.left_frame, text="λ (tasa de llegada):").pack(anchor="w", pady=2)
        self.lambda_entry = ttk.Entry(self.left_frame)
        self.lambda_entry.insert(0, "5")
        self.lambda_entry.pack(fill="x", pady=2)

        ttk.Label(self.left_frame, text="μ (tasa de servicio):").pack(anchor="w", pady=2)
        self.mu_entry = ttk.Entry(self.left_frame)
        self.mu_entry.insert(0, "4")
        self.mu_entry.pack(fill="x", pady=2)

        ttk.Label(self.left_frame, text="Estado 1 (c₁):").pack(anchor="w")
        self.c1_entry = ttk.Entry(self.left_frame)
        self.c1_entry.insert(0, "2")
        self.c1_entry.pack(fill="x", pady=2)

        ttk.Label(self.left_frame, text="Estado 2 (c₂):").pack(anchor="w")
        self.c2_entry = ttk.Entry(self.left_frame)
        self.c2_entry.insert(0, "1")
        self.c2_entry.pack(fill="x", pady=2)

        # ----------- NUEVO CAMPO: TIEMPO t -----------
        ttk.Label(self.left_frame, text="t (tiempo simulación, min):").pack(anchor="w", pady=2)
        self.t_entry = ttk.Entry(self.left_frame)
        self.t_entry.insert(0, "5")  # valor por defecto
        self.t_entry.pack(fill="x", pady=2)

        # Botón calcular
        ttk.Button(self.left_frame, text="Calcular", command=self.calculate).pack(pady=10)


    # -----------------------------------------------------
    # FUNCIÓN PRINCIPAL DE CÁLCULO
    # -----------------------------------------------------
    def calculate(self):
        try:
            # Obtener matriz P
            P = [[float(self.matrix_entries[i][j].get()) for j in range(2)] for i in range(2)]

            # Parámetros
            lam = float(self.lambda_entry.get())
            mu = float(self.mu_entry.get())
            c1 = int(self.c1_entry.get())
            c2 = int(self.c2_entry.get())
            total_minutes = float(self.t_entry.get())

            # ---------- A) Calcular π ----------
            pi = calculos.calcular_pi(P)

            # ---------- B.1) Intensidad ----------
            p1 = calculos.calcular_intensidades(lam, mu, c1)
            p2 = calculos.calcular_intensidades(lam, mu, c2)
            p_ponderado = pi[0] * p1 + pi[1] * p2

            # ---------- B.2) L ponderado ----------
            l1 = calculos.calcular_clientes(lam, mu, p1, c1)
            l2 = calculos.calcular_clientes(lam, mu, p2, c2)
            L_pond = pi[0] * l1 + pi[1] * l2

            # ---------- B.3) W ponderado ----------
            W_pond = L_pond / lam

            # ---------- Mostrar en Cálculos ----------
            texto = (
                f"π = [{pi[0]:.4f}, {pi[1]:.4f}]\n\n"
                f"p ponderado = {p_ponderado:.4f}\n"
                f"L ponderado = {L_pond:.4f}\n"
                f"W ponderado = {W_pond:.4f}\n"
                f"(Simulación con t = {total_minutes} min)"
            )
            self.result_label.config(text=texto)

            # ---------- Ejecutar simulación ----------
            texto_sim = simulacion.simular(
                lam=lam,
                mu=mu,
                P=P,
                c1=c1,
                c2=c2,
                total_minutes=total_minutes
            )

            # Mostrar salida simulación
            self.simulacion_output.delete("1.0", tk.END)
            self.simulacion_output.insert(tk.END, texto_sim)

        except Exception as e:
            self.result_label.config(text=f"⚠️ Error: {e}")


# --- Ejecutar aplicación ---
if __name__ == "__main__":
    root = tk.Tk()
    app = MarkovApp(root)
    root.mainloop()
