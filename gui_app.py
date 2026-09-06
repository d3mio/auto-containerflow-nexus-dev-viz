import tkinter as tk
from tkinter import ttk
import docker
import psutil
import time
import threading
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ContainerFlowNexus:
    def __init__(self, root):
        self.root = root
        self.root.title("ContainerFlow Nexus")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2d3436')
        
        # Docker client
        self.docker_client = docker.from_env()
        
        # Dark theme configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('.', background='#2d3436', foreground='#dfe6e9')
        self.style.configure('TFrame', background='#2d3436')
        self.style.configure('TLabel', background='#2d3436', foreground='#dfe6e9')
        self.style.configure('TButton', background='#3d4a52', foreground='#dfe6e9')
        self.style.map('TButton', background=[('active', '#4b5b66')])
        self.style.configure('TNotebook', background='#2d3436', borderwidth=0)
        self.style.configure('TNotebook.Tab', background='#3d4a52', foreground='#dfe6e9', padding=[10, 5])
        self.style.map('TNotebook.Tab', background=[('selected', '#4b5b66')])
        
        # Main layout
        self.create_widgets()
        
        # Start update thread
        self.running = True
        self.update_thread = threading.Thread(target=self.update_data, daemon=True)
        self.update_thread.start()
    
    def create_widgets(self):
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Dashboard tab
        self.dashboard_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_tab, text='Dashboard')
        self.create_dashboard_tab()
        
        # Containers tab
        self.containers_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.containers_tab, text='Containers')
        self.create_containers_tab()
        
        # Network tab
        self.network_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.network_tab, text='Network')
        self.create_network_tab()
        
        # Logs tab
        self.logs_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.logs_tab, text='Logs')
        self.create_logs_tab()
    
    def create_dashboard_tab(self):
        # Resource frames
        frame_resources = ttk.Frame(self.dashboard_tab)
        frame_resources.pack(fill=tk.X, padx=10, pady=10)
        
        # System stats
        stats_frame = ttk.LabelFrame(frame_resources, text='System Resources', padding=10)
        stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # CPU
        self.cpu_label = ttk.Label(stats_frame, text="CPU: 0%")
        self.cpu_label.pack(anchor='w')
        
        # Memory
        self.mem_label = ttk.Label(stats_frame, text="Memory: 0%")
        self.mem_label.pack(anchor='w')
        
        # Disk
        self.disk_label = ttk.Label(stats_frame, text="Disk: 0%")
        self.disk_label.pack(anchor='w')
        
        # Network
        self.net_label = ttk.Label(stats_frame, text="Network: 0 KB/s")
        self.net_label.pack(anchor='w')
        
        # Container status
        container_frame = ttk.LabelFrame(frame_resources, text='Container Status', padding=10)
        container_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.running_label = ttk.Label(container_frame, text="Running: 0")
        self.running_label.pack(anchor='w')
        
        self.stopped_label = ttk.Label(container_frame, text="Stopped: 0")
        self.stopped_label.pack(anchor='w')
        
        self.paused_label = ttk.Label(container_frame, text="Paused: 0")
        self.paused_label.pack(anchor='w')
        
        # Charts frame
        charts_frame = ttk.Frame(self.dashboard_tab)
        charts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Resource usage chart
        fig = Figure(figsize=(6, 4), dpi=100, facecolor='#2d3436')
        self.ax = fig.add_subplot(111)
        self.ax.set_facecolor('#2d3436')
        self.ax.tick_params(colors='#dfe6e9')
        for spine in self.ax.spines.values():
            spine.set_color('#dfe6e9')
        self.ax.set_xlabel('Time', color='#dfe6e9')
        self.ax.set_ylabel('Usage (%)', color='#dfe6e9')
        self.ax.set_title('Resource Usage', color='#dfe6e9')
        self.ax.set_ylim(0, 100)
        self.ax.grid(color='#636e72', linestyle='--')
        
        self.cpu_data = [0] * 30
        self.mem_data = [0] * 30
        self.line_cpu, = self.ax.plot(self.cpu_data, label='CPU', color='#e17055')
        self.line_mem, = self.ax.plot(self.mem_data, label='Memory', color='#0984e3')
        self.ax.legend(facecolor='#2d3436', labelcolor='#dfe6e9')
        
        chart_canvas = FigureCanvasTkAgg(fig, master=charts_frame)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def create_containers_tab(self):
        # Treeview for containers
        container_tree_frame = ttk.Frame(self.containers_tab)
        container_tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.tree = ttk.Treeview(container_tree_frame, columns=("ID", "Name", "Status", "Image", "Ports"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Image", text="Image")
        self.tree.heading("Ports", text="Ports")
        
        self.tree.column("ID", width=150, anchor='w')
        self.tree.column("Name", width=150, anchor='w')
        self.tree.column("Status", width=100, anchor='w')
        self.tree.column("Image", width=200, anchor='w')
        self.tree.column("Ports", width=200, anchor='w')
        
        scrollbar = ttk.Scrollbar(container_tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Container control buttons
        button_frame = ttk.Frame(self.containers_tab)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.start_btn = ttk.Button(button_frame, text="Start", command=self.start_container)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="Stop", command=self.stop_container)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.restart_btn = ttk.Button(button_frame, text="Restart", command=self.restart_container)
        self.restart_btn.pack(side=tk.LEFT, padx=5)
        
        self.remove_btn = ttk.Button(button_frame, text="Remove", command=self.remove_container)
        self.remove_btn.pack(side=tk.LEFT, padx=5)
        
        self.refresh_btn = ttk.Button(button_frame, text="Refresh", command=self.update_containers)
        self.refresh_btn.pack(side=tk.RIGHT, padx=5)
    
    def create_network_tab(self):
        # Network topology placeholder
        network_frame = ttk.Frame(self.network_tab)
        network_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.network_canvas = tk.Canvas(network_frame, bg='#2d3436', highlightthickness=0)
        self.network_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Network graph visualization will be added here
        self.draw_network_graph()
    
    def create_logs_tab(self):
        # Logs display
        logs_frame = ttk.Frame(self.logs_tab)
        logs_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.logs_text = tk.Text(logs_frame, bg='#2d3436', fg='#dfe6e9', insertbackground='#dfe6e9', 
                                 wrap=tk.WORD, font=('Courier', 10))
        scrollbar = ttk.Scrollbar(logs_frame, command=self.logs_text.yview)
        self.logs_text.configure(yscrollcommand=scrollbar.set)
        
        self.logs_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Log controls
        log_control_frame = ttk.Frame(self.logs_tab)
        log_control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.log_container_entry = ttk.Entry(log_control_frame, width=30)
        self.log_container_entry.pack(side=tk.LEFT, padx=5)
        
        self.log_follow_var = tk.IntVar()
        log_follow_check = ttk.Checkbutton(log_control_frame, text="Follow", variable=self.log_follow_var)
        log_follow_check.pack(side=tk.LEFT, padx=5)
        
        show_logs_btn = ttk.Button(log_control_frame, text="Show Logs", command=self.show_logs)
        show_logs_btn.pack(side=tk.LEFT, padx=5)
        
        clear_logs_btn = ttk.Button(log_control_frame, text="Clear", command=self.clear_logs)
        clear_logs_btn.pack(side=tk.RIGHT, padx=5)
    
    def draw_network_graph(self):
        # Simple network graph visualization
        width = self.network_canvas.winfo_width()
        height = self.network_canvas.winfo_height()
        
        if width < 10 or height < 10:
            return
        
        self.network_canvas.delete('all')
        
        # Draw center node (host)
        center_x = width // 2
        center_y = height // 2
        self.network_canvas.create_oval(center_x - 40, center_y - 40, center_x + 40, center_y + 40, 
                                       fill='#0984e3', outline='#dfe6e9')
        self.network_canvas.create_text(center_x, center_y, text="Host", fill='#dfe6e9')
        
        try:
            networks = self.docker_client.networks.list()
            containers = self.docker_client.containers.list(all=True)
            
            angle_step = 360 / max(1, len(containers))
            current_angle = 0
            
            for container in containers:
                x = center_x + int(200 * math.cos(math.radians(current_angle)))
                y = center_y + int(200 * math.sin(math.radians(current_angle)))
                
                # Draw container node
                color = '#00b894' if container.status == 'running' else '#ff7675'
                self.network_canvas.create_oval(x - 30, y - 30, x + 30, y + 30, fill=color, outline='#dfe6e9')
                self.network_canvas.create_text(x, y, text=container.name[:15], fill='#dfe6e9')
                
                # Draw connection to host
                self.network_canvas.create_line(center_x, center_y, x, y, fill='#636e72', width=2)
                
                current_angle += angle_step
        except Exception as e:
            print(f"Error drawing network graph: {e}")
    
    def update_data(self):
        last_net_io = psutil.net_io_counters()
        
        while self.running:
            try:
                # Update system stats
                cpu_percent = psutil.cpu_percent()
                mem_percent = psutil.virtual_memory().percent
                disk_percent = psutil.disk_usage('/').percent
                
                net_io = psutil.net_io_counters()
                net_speed = (net_io.bytes_sent + net_io.bytes_recv - 
                            last_net_io.bytes_sent - last_net_io.bytes_recv) / 1024
                last_net_io = net_io
                
                # Update UI
                self.cpu_label.config(text=f"CPU: {cpu_percent}%")
                self.mem_label.config(text=f"Memory: {mem_percent}%")
                self.disk_label.config(text=f"Disk: {disk_percent}%")
                self.net_label.config(text=f"Network: {net_speed:.2f} KB/s")
                
                # Update charts
                self.cpu_data.pop(0)
                self.cpu_data.append(cpu_percent)
                self.mem_data.pop(0)
                self.mem_data.append(mem_percent)
                
                self.line_cpu.set_ydata(self.cpu_data)
                self.line_mem.set_ydata(self.mem_data)
                
                # Redraw chart
                if hasattr(self, 'ax'):
                    self.ax.relim()
                    self.ax.autoscale_view()
                    self.ax.figure.canvas.draw_idle()
                
                # Update container stats
                self.update_containers()
                
                # Update network graph
                self.draw_network_graph()
                
            except Exception as e:
                print(f"Error updating data: {e}")
            
            time.sleep(2)
    
    def update_containers(self):
        try:
            containers = self.docker_client.containers.list(all=True)
            
            running = 0
            stopped = 0
            paused = 0
            
            # Clear tree
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            # Update container list
            for container in containers:
                status = container.status
                
                if status == 'running':
                    running += 1
                elif status == 'exited':
                    stopped += 1
                else:
                    paused += 1
                
                # Get ports
                ports = []
                if container.attrs['NetworkSettings']['Ports']:
                    for k, v in container.attrs['NetworkSettings']['Ports'].items():
                        if v:
                            ports.append(f"{k}→{v[0]['HostPort']}")
                        else:
                            ports.append(k)
                
                self.tree.insert("", tk.END, values=(
                    container.short_id,
                    container.name,
                    container.status,
                    container.image.tags[0] if container.image.tags else "",
                    ", ".join(ports)
                ))
            
            # Update status labels
            self.running_label.config(text=f"Running: {running}")
            self.stopped_label.config(text=f"Stopped: {stopped}")
            self.paused_label.config(text=f"Paused: {paused}")
            
        except Exception as e:
            print(f"Error updating containers: {e}")
    
    def start_container(self):
        selected = self.tree.focus()
        if not selected:
            return
        
        item = self.tree.item(selected)
        container_id = item['values'][0]
        
        try:
            container = self.docker_client.containers.get(container_id)
            container.start()
            self.update_containers()
        except Exception as e:
            print(f"Error starting container: {e}")
    
    def stop_container(self):
        selected = self.tree.focus()
        if not selected:
            return
        
        item = self.tree.item(selected)
        container_id = item['values'][0]
        
        try:
            container = self.docker_client.containers.get(container_id)
            container.stop()
            self.update_containers()
        except Exception as e:
            print(f"Error stopping container: {e}")
    
    def restart_container(self):
        selected = self.tree.focus()
        if not selected:
            return
        
        item = self.tree.item(selected)
        container_id = item['values'][0]
        
        try:
            container = self.docker_client.containers.get(container_id)
            container.restart()
            self.update_containers()
        except Exception as e:
            print(f"Error restarting container: {e}")
    
    def remove_container(self):
        selected = self.tree.focus()
        if not selected:
            return
        
        item = self.tree.item(selected)
        container_id = item['values'][0]
        
        try:
            container = self.docker_client.containers.get(container_id)
            container.remove(force=True)
            self.update_containers()
        except Exception as e:
            print(f"Error removing container: {e}")
    
    def show_logs(self):
        container_name = self.log_container_entry.get().strip()
        if not container_name:
            return
        
        try:
            container = self.docker_client.containers.get(container_name)
            logs = container.logs(tail=100, follow=False, stream=False).decode('utf-8')
            
            self.logs_text.delete(1.0, tk.END)
            self.logs_text.insert(tk.END, logs)
            self.logs_text.see(tk.END)
            
            if self.log_follow_var.get():
                # Start a thread to follow logs
                self.log_follow_thread = threading.Thread(
                    target=self.follow_logs, 
                    args=(container_name,), 
                    daemon=True
                )
                self.log_follow_thread.start()
                
        except Exception as e:
            self.logs_text.insert(tk.END, f"Error: {str(e)}\n")
    
    def follow_logs(self, container_name):
        try:
            container = self.docker_client.containers.get(container_name)
            for line in container.logs(stream=True, follow=True):
                line = line.decode('utf-8').rstrip()
                self.logs_text.insert(tk.END, line + "\n")
                self.logs_text.see(tk.END)
        except Exception as e:
            self.logs_text.insert(tk.END, f"Error following logs: {str(e)}\n")
    
    def clear_logs(self):
        self.logs_text.delete(1.0, tk.END)
    
    def on_closing(self):
        self.running = False
        if hasattr(self, 'update_thread') and self.update_thread.is_alive():
            self.update_thread.join(timeout=1)
        self.root.destroy()

if __name__ == "__main__":
    import math
    
    root = tk.Tk()
    app = ContainerFlowNexus(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()