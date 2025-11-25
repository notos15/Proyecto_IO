import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')

class GraficoEstados:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        self.canvas = None
        self.datos_simulacion = None
        
    def configurar_grafico(self):
        """Configura el aspecto inicial del gráfico"""
        self.ax.set_title('Porcentaje de tiempo en cada estado', fontsize=14, fontweight='bold')
        self.ax.set_xlabel('Estado Operativo', fontsize=12)
        self.ax.set_ylabel('Porcentaje del tiempo (%)', fontsize=12)
        self.ax.set_ylim(0, 100)
        self.ax.grid(True, alpha=0.3, axis='y')
        
    def calcular_porcentajes_estados(self, datos_simulacion):
        """Calcula el porcentaje de tiempo en cada estado"""
        if not datos_simulacion:
            return None, None
            
        # Contar ocurrencias de cada estado
        conteo_estado1 = 0
        conteo_estado2 = 0
        total_puntos = len(datos_simulacion)
        
        for registro in datos_simulacion:
            if registro['estado'] == 1:
                conteo_estado1 += 1
            else:
                conteo_estado2 += 1
        
        # Calcular porcentajes
        porcentaje_estado1 = (conteo_estado1 / total_puntos) * 100
        porcentaje_estado2 = (conteo_estado2 / total_puntos) * 100
        
        return porcentaje_estado1, porcentaje_estado2
        
    def actualizar_datos(self, datos_simulacion):
        """Actualiza los datos de la simulación para graficar"""
        self.datos_simulacion = datos_simulacion
        
    def generar_grafico(self):
        """Genera el gráfico de barras de porcentajes por estado"""
        if not self.datos_simulacion:
            self.ax.clear()
            self.ax.text(0.5, 0.5, 'Ejecuta la simulación primero\npara generar el gráfico', 
                        ha='center', va='center', transform=self.ax.transAxes, fontsize=12)
            self.ax.set_title('Porcentaje de tiempo en cada estado', fontsize=14, fontweight='bold')
            if self.canvas:
                self.canvas.draw()
            return
            
        # Limpiar el gráfico anterior
        self.ax.clear()
        
        # Calcular porcentajes
        pct_estado1, pct_estado2 = self.calcular_porcentajes_estados(self.datos_simulacion)
        
        if pct_estado1 is None:
            return
            
        # Datos para el gráfico de barras
        estados = ['Estado 1\n(2 servidores)', 'Estado 2\n(1 servidor)']
        porcentajes = [pct_estado1, pct_estado2]
        colores = ['#2E86AB', '#A23B72']  # Colores atractivos
        
        # Crear gráfico de barras
        barras = self.ax.bar(estados, porcentajes, color=colores, alpha=0.8, edgecolor='black', linewidth=1.2)
        
        # Configurar el gráfico
        self.ax.set_title('Distribución del Tiempo en Cada Estado', fontsize=14, fontweight='bold')
        self.ax.set_xlabel('Estado Operativo', fontsize=12)
        self.ax.set_ylabel('Porcentaje del Tiempo (%)', fontsize=12)
        self.ax.set_ylim(0, 100)
        self.ax.grid(True, alpha=0.3, axis='y')
        
        # Añadir valores en las barras
        for barra, porcentaje in zip(barras, porcentajes):
            altura = barra.get_height()
            self.ax.text(barra.get_x() + barra.get_width()/2., altura + 1,
                        f'{porcentaje:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        # Añadir línea de referencia teórica
        self.ax.axhline(y=66.7, color='red', linestyle='--', alpha=0.7, linewidth=1, label='Estado 1 teórico: 66.7%')
        self.ax.axhline(y=33.3, color='blue', linestyle='--', alpha=0.7, linewidth=1, label='Estado 2 teórico: 33.3%')
        
        # Añadir leyenda
        self.ax.legend(loc='upper right')
        
        # Añadir información adicional
        total_tiempo = self.datos_simulacion[-1]['t'] if self.datos_simulacion else 0
        self.ax.text(0.02, 0.98, f'Tiempo total: {total_tiempo} min\nMuestras: {len(self.datos_simulacion)}', 
                    transform=self.ax.transAxes, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
        
        # Redibujar el canvas si existe
        if self.canvas:
            self.canvas.draw()
    
    def crear_canvas(self):
        """Crea el canvas de matplotlib en el frame de tkinter"""
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            
        self.canvas = FigureCanvasTkAgg(self.fig, self.parent_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
    def limpiar_grafico(self):
        """Limpia el gráfico"""
        self.ax.clear()
        self.configurar_grafico()
        if self.canvas:
            self.canvas.draw()