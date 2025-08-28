from flask import Flask, request, Response, jsonify
import graphviz

app = Flask(__name__)

EDITOR_HTML = """<!doctype html>
<meta charset="utf-8">
<title>DotEditor Flask</title>
<style>textarea{width:48%;height:80vh} iframe{width:48%;height:80vh;border:1px solid #ccc}</style>
<form id=f method=post action="/render" target="v">
    <textarea name=dot id=dot>digraph{a->b}</textarea>
    <div>
        <button type=submit>Render</button>
        <select name=format form=f>
            <option value=svg selected>svg</option>
            <option value=png>png</option>
            <option value=pdf>pdf</option>
        </select>
    </div>
</form>
<iframe name="v"></iframe>
"""

@app.get("/")
def index():
    return EDITOR_HTML

@app.post("/render")
def render_dot():
    dot = request.form.get("dot", "")
    fmt = request.form.get("format", "svg")
    if not dot or fmt not in {"svg", "png", "pdf"}:
        return jsonify(error="invalid input"), 400
    try:
        src = graphviz.Source(dot, format=fmt)
        data = src.pipe()
    except Exception as e:
        return jsonify(error=str(e)), 400
    if fmt == "svg":
        return Response(data, mimetype="image/svg+xml")
    if fmt == "png":
        return Response(data, mimetype="image/png")
    return Response(data, mimetype="application/pdf")

if __name__ == "__main__":
    app.run(debug=True)
