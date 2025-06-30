import http.server
import socketserver
import os

PORT = 8000

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        http.server.SimpleHTTPRequestHandler.end_headers(self)

# Создаем пустой файл tasks.json, если он не существует
if not os.path.exists('tasks.json'):
    with open('tasks.json', 'w') as f:
        f.write('[]')

# Запускаем сервер
Handler = MyHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print(f"Сервер запущен на порту {PORT}")
print(f"Откройте index.html в браузере")
httpd.serve_forever() 