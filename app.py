from flask import Flask, render_template, request, jsonify
from miniasm_assembler import assemble

app = Flask(__name__)

SAMPLE = open("sample_program.asm").read()

@app.route("/")
def index():
    return render_template("index.html", sample=SAMPLE)

@app.route("/assemble", methods=["POST"])
def run_assemble():
    source = request.json.get("source", "")
    sym_table, intermediate, machine_code, errors = assemble(source)
    return jsonify({
        "symbols": [{"name": k, "address": v} for k, v in sym_table.items()],
        "intermediate": [
            {"line": ln, "addr": addr, "label": lbl or "", "tokens": " ".join(tok)}
            for ln, addr, lbl, tok in intermediate
        ],
        "machine_code": [
            {"addr": addr, "code": code, "annotation": ann}
            for addr, code, ann in machine_code
        ],
        "errors": [{"line": ln, "msg": msg} for ln, msg in errors],
    })

if __name__ == "__main__":
    app.run(debug=True)
