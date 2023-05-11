import subprocess
import os
import time
from flask import Flask, request, jsonify


file_path = os.path.abspath('stockfishEXE')
process = subprocess.Popen([file_path], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
startedMsg = process.stdout.readline().decode('utf-8')
print(startedMsg.encode("utf-8"))
app = Flask(__name__)

def getBestMove(fen: str, depth: str):
    # run the executable program
    fenString = f"position fen {fen}\n"
    depthString = f"go depth {depth}\n"
    process.stdin.write(fenString.encode("utf-8"))
    process.stdin.write(depthString.encode("utf-8"))
    process.stdin.flush()
    # read the output continuously
    while True:
        output = process.stdout.readline().decode('utf-8')
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output)
            if output.split(" ")[0] == "bestmove":
                return output.split(" ")[1]

    # get the return code of the process
    return_code = process.poll()
    return return_code

# Define a route to handle POST requests
@app.route('/getBestMove', methods=['POST'])
def getBestMoveAPI():
    print(request.json)
    depth = request.json['depth']
    fen = request.json['fen']
    bestMove = getBestMove(fen, depth)
    response = {
        'move' : bestMove 
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=3030)

