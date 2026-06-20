import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
import psutil

class FloatingHUD(App):
    def build(self):
        # Configure a small window size suitable for a mobile overlay widget
        Window.borderless = True
        Window.size = (450, 180)
        
        # UI Component layout with text formatting
        self.label = Label(
            text="Gathering performance metrics...",
            font_size='16sp',
            markup=True,
            halign='center'
        )
        
        # Update loop scheduled to trigger every 1.0 seconds
        Clock.schedule_interval(self.update_stats, 1.0)
        return self.label

    def update_stats(self, dt):
        # 1. Fallback method for CPU Load (Bypasses Android /proc/stat restriction)
        try:
            # Reads system load average over the last 1 minute
            with open("/proc/loadavg", "r") as f:
                load_1min = float(f.read().split()[0])
            
            # Convert load average to an approximate percentage based on an 8-core setup
            cpu_percent = min(int((load_1min / 8.0) * 100), 100)
            cpu_text = f"{cpu_percent}% (Load)"
        except Exception:
            cpu_percent = 0
            cpu_text = "N/A (Restricted)"

        # 2. Read live RAM metrics (This is allowed by Android)
        ram = psutil.virtual_memory()
        
        # Dynamic color coding based on load levels
        cpu_color = "FF3333" if cpu_percent > 85 else ("FFFF33" if cpu_percent > 50 else "33FF33")
        ram_color = "FF3333" if ram.percent > 85 else "33FFFF"
        
        # Render update string with Kivy BBCode markup text styling
        self.label.text = (
            f"[b][color=FFFFFF]Performance HUD[/color][/b]\n"
            f"[color=CCCCCC]CPU Load:[/color] [color={cpu_color}]{cpu_text}[/color]\n"
            f"[color=CCCCCC]RAM Used:[/color] [color={ram_color}]{ram.percent}%[/color]"
        )

if __name__ == '__main__':
    FloatingHUD().run()
