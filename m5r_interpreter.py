import re
import subprocess
import tempfile
import os

def safe_run(cmd, timeout=8, **sub_kwargs):
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            **sub_kwargs
        )
        out = result.stdout
        err = result.stderr
        rc = result.returncode
    except subprocess.TimeoutExpired:
        return "", "[ERROR: timed out]", 1
    except FileNotFoundError:
        return "", f"[ERROR: Not installed: {cmd[0]}]", 1
    except Exception as e:
        return "", f"[ERROR: {e}]", 1
    else:
        return out, err, rc

def lang_header(name):
    return f"\n====== [{name.upper()} BLOCK] ======\n"

def interpret(source):
    outputs = []

    # Python blocks
    for segment in re.findall(r'<\?py(.*?)\?>', source, re.S):
        code = segment.strip()
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.py') as f:
            f.write(code)
            path = f.name
        out, err, rc = safe_run(['python3', path])
        outputs.append(lang_header("python") + out)
        if err or rc:
            outputs.append(f"[PYTHON ERROR]\n{err}")
        os.unlink(path)

    # JavaScript blocks
    for segment in re.findall(r'<\?js(.*?)\?>', source, re.S):
        code = segment.strip()
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.js') as f:
            f.write(code)
            path = f.name
        out, err, rc = safe_run(['node', path])
        outputs.append(lang_header("js") + out)
        if err or rc:
            outputs.append(f"[JS ERROR]\n{err}")
        os.unlink(path)

    # PHP blocks
    for segment in re.findall(r'<\?php(.*?)\?>', source, re.S):
        code = segment.strip()
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.php') as f:
            f.write("<?php\n" + code + "\n?>")
            path = f.name
        out, err, rc = safe_run(['php', path])
        outputs.append(lang_header("php") + out)
        if err or rc:
            outputs.append(f"[PHP ERROR]\n{err}")
        os.unlink(path)

    # CSS blocks (just return with header)
    for segment in re.findall(r'<\?css(.*?)\?>', source, re.S):
        css = segment.strip()
        outputs.append(lang_header("css") + "[CSS Styling Loaded]\n" + css + "\n")

    # Shell blocks
    for segment in re.findall(r'<\?sh(.*?)\?>', source, re.S):
        code = segment.strip()
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.sh') as f:
            f.write(code)
            path = f.name
        os.chmod(path, 0o700)
        out, err, rc = safe_run(['bash', path])
        outputs.append(lang_header("shell") + out)
        if err or rc:
            outputs.append(f"[BASH ERROR]\n{err}")
        os.unlink(path)

    # C# blocks
    for segment in re.findall(r'<\?cs(.*?)\?>', source, re.S):
        code = segment.strip()
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.cs') as f:
            f.write(f"using System; class Program {{ static void Main() {{ {code} }} }}")
            path = f.name
        exe_path = path.replace('.cs', '.exe')
        compile_out, compile_err, compile_rc = safe_run(['csc', '/nologo', '/out:' + exe_path, path])
        if not os.path.exists(exe_path) or compile_rc:
            outputs.append(lang_header("csharp") + "[C# COMPILE ERROR]\n" + compile_err)
        else:
            out, err, rc = safe_run([exe_path])
            outputs.append(lang_header("csharp") + out)
            if err or rc:
                outputs.append(f"[C# ERROR]\n{err}")
            os.unlink(exe_path)
        os.unlink(path)

    # C++ blocks
    for segment in re.findall(r'<\?cpp(.*?)\?>', source, re.S):
        code = segment.strip()
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.cpp') as f:
            f.write(f"#include <iostream>\nusing namespace std;\nint main() {{ {code} return 0; }}")
            path = f.name
        exe_path = path.replace('.cpp', '')
        compile_out, compile_err, compile_rc = safe_run(['g++', path, '-o', exe_path])
        if not os.path.exists(exe_path) or compile_rc:
            outputs.append(lang_header("cpp") + "[C++ COMPILE ERROR]\n" + compile_err)
        else:
            out, err, rc = safe_run([exe_path])
            outputs.append(lang_header("cpp") + out)
            if err or rc:
                outputs.append(f"[C++ ERROR]\n{err}")
            os.unlink(exe_path)
        os.unlink(path)

    print(''.join(outputs))

