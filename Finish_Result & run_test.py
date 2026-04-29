from GUI import WeatherAppUI
from logic import WeatherController

app = WeatherAppUI(WeatherController)

if __name__ == "__main__":
    app.mainloop()