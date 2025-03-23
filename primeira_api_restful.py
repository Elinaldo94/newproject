from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Lista de músicas
musicas = [
    {"id": 1, "titulo": "Até que durou", "descricao": "Samba"},
    {"id": 2, "titulo": "Buquê de flores", "descricao": "Pagode"},
    {"id": 3, "titulo": "O poder do pretinho", "descricao": "Pagode"},
    {"id": 4, "titulo": "Leite consensado", "descricao": "Pagode"},
    {"id": 5, "titulo": "Lancinho", "descricao": "Pagode"},
    {"id": 6, "titulo": "Tá vendo aquela lua", "descricao": "Pagode"},
    {"id": 7, "titulo": "Robim Hood da paixão", "descricao": "Pagode"},
    {"id": 8, "titulo": "Fugidinha", "descricao": "Sertanejo"},
    {"id": 9, "titulo": "A praia", "descricao": "Forró"},
    {"id": 10, "titulo": "Anjo querubim", "descricao": "Forró"},
    {"id": 11, "titulo": "A saga de um vaqueiro", "descricao": "Forró"},
    {"id": 12, "titulo": "Rap do Silva", "descricao": "Funk"},
    {"id": 13, "titulo": "Som de preto", "descricao": "Funk"},
    {"id": 14, "titulo": "De bar em bar", "descricao": "Forró"},
    {"id": 15, "titulo": "Morto muito loko", "descricao": "Funk"}
]

# Página inicial
@app.route('/')
def home():
    return render_template_string('''
        <!doctype html>
        <html>
            <head>
                <title>Catálogo de Músicas</title>
            </head>
            <body>
                <h1>Bem-vindo à minha API!</h1>
                <form action="/musicas" method="get">
                    <label for="genero">Escolha um gênero musical:</label>
                    <select name="genero" id="genero">
                        <option value="todos">Todos</option>
                        <option value="samba">Samba</option>
                        <option value="pagode">Pagode</option>
                        <option value="sertanejo">Sertanejo</option>
                        <option value="forró">Forró</option>
                        <option value="funk">Funk</option>
                    </select>
                    <label for="formato">Formato:</label>
                    <select name="formato" id="formato">
                        <option value="html">HTML</option>
                        <option value="json">JSON</option>
                    </select>
                    <button type="submit">Filtrar</button>
                </form>
            </body>
        </html>
    ''')

# Rota para listar músicas com filtro e formato
@app.route('/musicas', methods=['GET'])
def listar_musicas():
    genero = request.args.get('genero', 'todos').lower()
    formato = request.args.get('formato', 'html').lower()

    if genero == 'todos':
        musicas_filtradas = musicas
    else:
        musicas_filtradas = [musica for musica in musicas if musica["descricao"].lower() == genero]

    if formato == 'json':
        return jsonify(musicas_filtradas)
    else:
        return render_template_string('''
            <!doctype html>
            <html>
                <head>
                    <title>Músicas Filtradas</title>
                </head>
                <body>
                    <h1>Músicas do gênero: {{ genero }}</h1>
                    <ul>
                        {% for musica in musicas %}
                            <li>{{ musica["id"] }} - {{ musica["titulo"] }} ({{ musica["descricao"] }})</li>
                        {% endfor %}
                    </ul>
                    <a href="/">Voltar</a>
                </body>
            </html>
        ''', genero=genero.capitalize(), musicas=musicas_filtradas)

# Rota para adicionar novas músicas
@app.route('/musicas', methods=['POST'])
def adicionar_musica():
    dados = request.json
    novo_id = max(musica["id"] for musica in musicas) + 1
    nova_musica = {"id": novo_id, "titulo": dados["titulo"], "descricao": dados["descricao"]}
    musicas.append(nova_musica)
    return jsonify({"mensagem": "Música adicionada com sucesso!", "musica": nova_musica}), 201

# Rota para deletar uma ou mais músicas
@app.route('/musicas', methods=['DELETE'])
def deletar_musicas():
    ids_para_deletar = request.json.get("ids", [])
    global musicas
    musicas = [musica for musica in musicas if musica["id"] not in ids_para_deletar]
    return jsonify({"mensagem": "Músicas deletadas com sucesso!", "musicas_restantes": musicas}), 200

# Rota para atualizar músicas existentes
@app.route('/musicas/<int:id>', methods=['PUT'])
def atualizar_musica(id):
    dados = request.json
    for musica in musicas:
        if musica["id"] == id:
            musica["titulo"] = dados.get("titulo", musica["titulo"])
            musica["descricao"] = dados.get("descricao", musica["descricao"])
            return jsonify({"mensagem": "Música atualizada com sucesso!", "musica": musica}), 200
    return jsonify({"erro": "Música não encontrada"}), 404

if __name__ == '__main__':
    app.run(port=5000)
