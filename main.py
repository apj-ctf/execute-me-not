from flask import Flask, request, jsonify, render_template
from llm_gemini import generate_code

app = Flask(__name__)

@app.route("/")
def chat():
    return render_template("chat.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_prompt = request.json.get("prompt")

    # Check if the prompt is related to code
    if not any(keyword in user_prompt.lower() for keyword in ["python"]):
        # If it's a general question, return the Gemini response directly
        try:
            gemini_response = generate_code(user_prompt)
            return jsonify({
                "generated_code": None,
                "output": gemini_response
            })
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500


    code = generate_code(user_prompt)

    error=""
    try:
        output = {}
        #prepend the prompt as a comment
        code_with_comment = f"# Original prompt: {user_prompt}\n{code}"
        exec(code_with_comment, {"__builtins__": __builtins__}, output)
        result = output.get("result")
        if result is None:
            result = "No result found - you need to store the output in a variable called result"
        else:
            result = result + '\n' + code_with_comment
    except Exception as e:
        error = str(e)
        result = f"Error executing code: {error} \n\nResponse:\n{code}"


    return jsonify({
        "generated_code": code,
        "output": result
    })
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)