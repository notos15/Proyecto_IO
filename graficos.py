import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

class GraficoEstados:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.datos_simulacion = None
        
        # ---------- FRAME SCROLL ----------
        self.canvas_frame = tk.Canvas(self.parent_frame)
        self.scroll_y = tk.Scrollbar(self.parent_frame, orient="vertical", command=self.canvas_frame.yview)
        self.scroll_y.pack(side="right", fill="y")

        self.inner_frame = tk.Frame(self.canvas_frame)
        self.inner_frame.bind("<Configure>",
                              lambda e: self.canvas_frame.configure(scrollregion=self.canvas_frame.bbox("all")))
        self.canvas_frame.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.canvas_frame.configure(yscrollcommand=self.scroll_y.set)
        self.canvas_frame.pack(fill="both", expand=True)

        self.fig_list = []

    def actualizar_datos(self, datos):
        self.datos_simulacion = datos

    def generar_grafico(self):
        # Borrar gráficos previos
        for fig in self.fig_list:
            fig.get_tk_widget().destroy()
        self.fig_list.clear()

        if not self.datos_simulacion:
            return

        # Extraer datos
        t = [d["t"] for d in self.datos_simulacion]
        N = [d["N"] for d in self.datos_simulacion]
        Lq = [d["Lq"] for d in self.datos_simulacion]
        W = [d["W"] for d in self.datos_simulacion]
        L = [d["L"] for d in self.datos_simulacion]
        estados = [d["estado"] for d in self.datos_simulacion]

        # ========== GRAFICO 1: Porcentaje de tiempo en estados ==========
        fig1, ax1 = plt.subplots(figsize=(7, 4))
        self.fig_list.append(FigureCanvasTkAgg(fig1, master=self.inner_frame))

        pct1 = estados.count(1) / len(estados) * 100
        pct2 = estados.count(2) / len(estados) * 100

        ax1.bar(["Estado 1", "Estado 2"], [pct1, pct2],
                color=["#2E86AB", "#A23B72"], edgecolor="black")
        ax1.axhline(y=66.7, color="red", linestyle="--", label="Teórico 66.7%")
        ax1.axhline(y=33.3, color="blue", linestyle="--", label="Teórico 33.3%")

        ax1.set_title("Distribución del Tiempo en Cada Estado", fontsize=13)
        ax1.set_ylabel("Porcentaje (%)")
        ax1.grid(axis="y", alpha=0.3)
        ax1.legend()

        self.fig_list[-1].draw()
        self.fig_list[-1].get_tk_widget().pack(pady=5)

        # ========== GRAFICO 2: Lq(t) ==========
        fig2, ax2 = plt.subplots(figsize=(7, 4))
        self.fig_list.append(FigureCanvasTkAgg(fig2, master=self.inner_frame))

        ax2.plot(t, Lq, color="purple", linewidth=1.8)
        ax2.set_title("Lq(t): Largo de Cola en el Tiempo")
        ax2.set_xlabel("Tiempo (min)")
        ax2.set_ylabel("Lq(t)")
        ax2.grid(True, alpha=0.3)

        self.fig_list[-1].draw()
        self.fig_list[-1].get_tk_widget().pack(pady=5)

        # ========== GRAFICO 3: W(t) ==========
        fig3, ax3 = plt.subplots(figsize=(7, 4))
        self.fig_list.append(FigureCanvasTkAgg(fig3, master=self.inner_frame))

        ax3.plot(t, W, color="green", linewidth=1.8)
        ax3.set_title("W(t): Tiempo Promedio en Sistema")
        ax3.set_xlabel("Tiempo (min)")
        ax3.set_ylabel("W(t) (min)")
        ax3.grid(True, alpha=0.3)

        self.fig_list[-1].draw()
        self.fig_list[-1].get_tk_widget().pack(pady=5)

        # ========== GRAFICO 4: L(t) ==========
        fig4, ax4 = plt.subplots(figsize=(7, 4))
        self.fig_list.append(FigureCanvasTkAgg(fig4, master=self.inner_frame))

        ax4.plot(t, L, color="orange", linewidth=1.8)
        ax4.set_title("L(t): Número Promedio de Clientes en Sistema")
        ax4.set_xlabel("Tiempo (min)")
        ax4.set_ylabel("L(t)")
        ax4.grid(True, alpha=0.3)

        self.fig_list[-1].draw()
        self.fig_list[-1].get_tk_widget().pack(pady=5)

        # ========== GRAFICO 5: L(t) vs W(t) ==========
        fig5, ax5 = plt.subplots(figsize=(7, 4))
        self.fig_list.append(FigureCanvasTkAgg(fig5, master=self.inner_frame))

        ax5.plot(t, L, color="red", label="L(t)", linewidth=1.8)
        ax5.plot(t, W, color="blue", label="W(t)", linewidth=1.8)

        ax5.set_title("Comparación de L(t) y W(t)")
        ax5.set_xlabel("Tiempo (min)")
        ax5.set_ylabel("Valor")
        ax5.grid(True, alpha=0.3)
        ax5.legend()

        self.fig_list[-1].draw()
        self.fig_list[-1].get_tk_widget().pack(pady=5)

        # ========== GRAFICO 6: N(t) vs L(t) ==========
        fig6, ax6 = plt.subplots(figsize=(7, 4))
        self.fig_list.append(FigureCanvasTkAgg(fig6, master=self.inner_frame))

        ax6.plot(t, N, color="brown", label="N(t)", linewidth=1.8)
        ax6.plot(t, L, color="black", label="L(t)", linewidth=1.8)

        ax6.set_title("Comparación N(t) vs L(t)")
        ax6.set_xlabel("Tiempo (min)")
        ax6.set_ylabel("Valor")
        ax6.grid(True, alpha=0.3)
        ax6.legend()

        self.fig_list[-1].draw()
        self.fig_list[-1].get_tk_widget().pack(pady=5)
