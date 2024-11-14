from flask import Flask, request, jsonify
import subprocess
import json
import os
app = Flask(__name__)

@app.after_request
def after_request(response):
    # 仅当请求是跨域的时才设置 Access-Control-Allow-Origin
    if request.headers.get('Origin'):
        response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
    else:
        response.headers['Access-Control-Allow-Origin'] = '*'  # 非跨域请求可以设置为 '*'
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/api/submit-contract', methods=['POST', 'OPTIONS'])
def submit_contract():
    if request.method == 'OPTIONS':
        # 处理OPTIONS请求，返回允许的方法
        return jsonify({'message': 'CORS preflight request successful'}), 200
    
    # 处理实际的POST请求
    data = request.get_json()
    contract_code = data.get('code')
    if not contract_code:
        return jsonify({'error': 'No contract code provided'}), 400

    # 处理智能合约代码
    print(contract_code)
    fname = "analyse.sol"
    outfile = open(fname,'w')
    outfile.write(contract_code)
    print("Output Successed!")
    outfile.close()
    
    try:
        # 调用Slither并获取输出
        result = subprocess.run(['slither', 'analyse.sol', '--json', 'output.json'], 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # 读取并解析JSON输出
        with open('output.json', 'r') as json_file:
            slither_output = json.load(json_file)
            
    except Exception as e:
        print(f"Error running Slither: {e}")
        slither_output = None
    
    if slither_output is None:
        print("No high impact vulnerability.")
    # 将发现格式化为JSON
    findings_json = []
    print("Detected vulnerabilities:")
    for issue in slither_output.get('results', {}).get('detectors', []):
        
        finding_dict = {
        "Title": issue.get('check'),
        "Description": issue.get('description')
        }
        findings_json.append(finding_dict)
        print(f"Title: {issue.get('check')}")
        print(f"Description: {issue.get('description')}")
        print()
    os.remove('output.json')
    return jsonify(findings_json)

   
if __name__ == '__main__':
    app.run(port=5173,debug=True)