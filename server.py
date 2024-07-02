from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import requests

class WeatherHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path.startswith('/weather'):
            query = parse_qs(urlparse(self.path).query)
            city = query.get('city', [''])[0]
            if city:
                weather_data = self.get_weather(city)
                if weather_data:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(weather_data.encode('utf-8'))
                else:
                    self.send_error(404, 'City not found')
            else:
                self.send_error(400, 'City parameter missing')

    def get_weather(self, city):
      url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=YOUR_API_KEY&units=metric'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            city_name = data['name']
            temperature = data['main']['temp']
            feels_like = data['main']['feels_like']
            min_temperature = data['main']['temp_min']
            max_temperature = data['main']['temp_max']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            description = data['weather'][0]['description']
            return f'''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Weather Result</title>
                    <style>
                        body {{
                            background-color: lightblue;
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding: 0;
                        }}
                        .container {{
                            max-width: 600px;
                            margin: 50px auto;
                            background-color: white;
                            padding: 20px;
                            border-radius: 10px;
                            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        }}
                        h2 {{
                            color: #333;
                        }}
                        p {{
                            margin: 10px 0;
                            color: #666;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h2>Weather in {city_name}</h2>
                        <p>Temperature: {temperature}°C</p>
                        <p>Feels Like: {feels_like}°C</p>
                        <p>Minimum Temperature: {min_temperature}°C</p>
                        <p>Maximum Temperature: {max_temperature}°C</p>
                        <p>Humidity: {humidity}%</p>
                        <p>Wind Speed: {wind_speed} km/hr</p>
                        <p>Description: {description}</p>
                        <a href="/">Back</a>
                    </div>
                </body>
                </html>
            '''
        else:
            return None

def run(server_class=HTTPServer, handler_class=WeatherHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server running on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
