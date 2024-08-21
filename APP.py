from flask import Flask, render_template, request
import subprocess
import csrf_tool  # Import the CSRF tool module
import xxe_tool_final  # Import the XXE tool module
import xss_tool  # Import the XSS tool module

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        selected_tool = request.form['tool']
        param = request.form.get('param', '')  # Get parameter for SQL Injection
        session_cookie = request.form.get('session_cookie', '')  # Get session cookie for XXE

        results = {
            'csrf': [],
            'ssrf': [],
            'xxe': [],
            'sql_injection': [],
            'xss': []
        }

        try:
            if selected_tool == '1':
                # Run CSRF Tool
                results['csrf'].append(csrf_tool.main(url))  # Call the main function directly
            elif selected_tool == '2':
                # Run SSRF Tool
                result = subprocess.run(['python', 'ssrf_tool.py', url], capture_output=True, text=True)
                results['ssrf'].extend(result.stdout.strip().split('\n'))  # Append results from stdout
            elif selected_tool == '3':
                # Run XXE Tool
                args = ['python', 'xxe_tool_final.py', '--url', url]
                if session_cookie:
                    args.extend(['--session_cookie', session_cookie])
                result = subprocess.run(args, capture_output=True, text=True)
                results['xxe'].extend(result.stdout.strip().split('\n'))  # Append results from stdout
            elif selected_tool == '4':
                # Run SQL Injection Tool
                result = subprocess.run(['python', 'sql_injection.py', '--url', url, '--param', param], capture_output=True, text=True)
                results['sql_injection'].extend(result.stdout.strip().split('\n'))  # Append results from stdout
            elif selected_tool == '5':
                # Run XSS Tool
                results['xss'].append(xss_tool.detect_xss(url))  # Call the XSS detection function
            elif selected_tool == '6':
                # Run All Tools
                results['csrf'].append(csrf_tool.main(url))  # Call the CSRF tool directly
                result = subprocess.run(['python', 'ssrf_tool.py', url], capture_output=True, text=True)
                results['ssrf'].extend(result.stdout.strip().split('\n'))  # Append results from stdout
                args = ['python', 'xxe_tool_final.py', '--url', url]
                if session_cookie:
                    args.extend(['--session_cookie', session_cookie])
                result = subprocess.run(args, capture_output=True, text=True)
                results['xxe'].extend(result.stdout.strip().split('\n'))  # Append results from stdout
                result = subprocess.run(['python', 'sql_injection.py', '--url', url, '--param', param], capture_output=True, text=True)
                results['sql_injection'].extend(result.stdout.strip().split('\n'))  # Append results from stdout
                results['xss'].append(xss_tool.detect_xss(url))  # Call the XSS detection function

            # Collect and handle results
            if result and result.stderr:  # Check if result is not None before accessing stderr
                results['errors'] = f"Error: {result.stderr.strip()}"  # Append any error messages
            else:
                results['errors'] = None

        except Exception as e:
            results['errors'] = f"Exception occurred: {str(e)}"

        # Pass results to the template
        return render_template('results.html', results=results)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
