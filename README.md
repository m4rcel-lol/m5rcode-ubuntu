# m5rcode – The Unofficial Polyglot Programming Language

![Polyglot](https://img.shields.io/badge/language-Python%2FJS%2FPHP%2FC%23%2FC++-purple.svg)
![Status](https://img.shields.io/badge/status-experimental-orange.svg)

**m5rcode** is an experimental **polyglot programming language** written with a blend of **Python, JavaScript, PHP, C#, and C++**.  
It uses obfuscation and cross-language embedding to allow developers to write multi-language scripts in a single file (`.m5r`).  
The project includes a custom **REPL shell** (`m5rshell`) and an **interpreter** for `.m5r` files.  

---

## ✨ Features

- **Polyglot Language Core**
  - Mix **Python, JavaScript, PHP, CSS, C#, and C++** in a single `.m5r` file.
  - Interpreter extracts, executes, and blends code blocks.
  - Supports obfuscation for added challenge and uniqueness.

- **m5rshell – The REPL Shell**
  - Interactive REPL for testing code snippets.
  - Commands:  
    - `new`, `nano`, `run`, `fastfetch`, `credits`, `exit`, `cd`
  - Developer-friendly CLI for creating & running `.m5r` scripts.

- **.m5r File Runner (Interpreter)**
  - Executes `.m5r` polyglot files directly.
  - Efficient, multi-language-aware execution engine.
  - Provides fast output even for obfuscated code.

---

## 🔧 Requirements

- Python **3.8+**

---

## 📦 Installation

Clone this repository:

```bash
git clone https://github.com/m4rcel-lol/m5rcode.git
cd m5rcode
```

---

## ⚡ Quick Start

### Run the REPL shell
```bash
python3 m5rshell.py
```
---

## 📝 Example

Here’s a `hello.m5r` script that prints **Hello world** in all supported languages:

```m5r
<?py
# M5RCode Python Block: OBFUSCATED - 3D Hello World + Floating Rotating 3D Square

import tkinter as _tk
import math as _m
import time as _t

class _T:
    def __init__(self):
        self._rt=_tk.Tk()
        self._rt.title(''.join([chr(c) for c in [51,68,32,84,101,115,116]])) # 3D Test
        self._cv=_tk.Canvas(self._rt,width=420,height=260,bg='#181c22',highlightthickness=0)
        self._cv.pack()
        self._ang=0
        self._t=0
        self._run()
        self._rt.mainloop()

    def _run(self):
        self._cv.delete('all')
        # Draw "3D" shadowed Hello World text
        _s="".join([chr(c) for c in [72,101,108,108,111,32,119,111,114,108,100]])
        for _i in range(15,0,-3):
            self._cv.create_text(212+_i,90+_i,fill=f"#2a2a5{9-_i//3}",font=('Consolas',42,'bold'),text=_s)
        self._cv.create_text(212,90,fill="#ffe257",font=('Consolas',42,'bold'),text=_s)
        # Rotating & bouncing 3D square (pseudo-perspective)
        _a=self._ang
        _Y=130+_m.sin(self._t)*24
        _sz=70
        _pts=[]
        for _dx,_dy in [(-1,-1),(1,-1),(1,1),(-1,1)]:
            # 3D cube points, rotate a bit in Y, project to 2D
            _x=_dx*_sz*_m.cos(_a)
            _y=_dy*_sz*0.67
            _z=_dx*_sz*_m.sin(_a)
            _X=_x+_z*0.45
            _pts.append((212+_X,_Y+_y-_z*0.29))
        # Draw top face for 3D effect
        self._cv.create_polygon([_pts[i] for i in [0,1,2,3]],fill="#00ffae",outline="#222",width=3)
        # Draw floating shadow
        self._cv.create_oval(212-45,(_Y+_sz*1.03)+10,212+45,(_Y+_sz*1.24)+20,fill="#000",outline="")
        # Draw outline with depth
        for _offs in range(1,8):
            _offp=[(_x,_y+_offs*2) for _x,_y in _pts]
            self._cv.create_polygon(_offp,outline="#161413",fill="",width=1)
        # Animate: spin & up-down
        self._ang+=0.12
        self._t+=0.1
        self._rt.after(28,self._run)

_T()
?>
<?js
(function(){
    var x=[72,101,108,108,111,32,119,111,114,108,100];
    var s='';
    for(var i of x){ s+=String.fromCharCode(i); }
    console.log(s);
})();
?>
<?php
${a}=array(72,101,108,108,111,32,119,111,114,108,100);
echo implode(array_map('chr',${a})) . "\n";
?>
<?cs
// M5RCode C# Block: OBFUSCATED, illustrative
using System;
class S{
 static void Main(){
  Console.WriteLine(string.Join("", new int[] {72,101,108,108,111,32,119,111,114,108,100}.Select(c => (char)c)));
 }
}
?>
<?cpp
// M5RCode C++ Block: OBFUSCATED, illustrative
#include <iostream>
int main() {
 int arr[] = {72,101,108,108,111,32,119,111,114,108,100};
 for(int i = 0; i < 11; i++) std::cout << (char)arr[i];
 std::cout << std::endl;
 return 0;
}
?>
<?css
body { color: #ffe257; background: #1a1c1f; }
?>

```

---

## 📂 Project Structure

```
m5rcode/
├─ m5rshell.py         # The REPL shell
├─ m5r_interpreter.py              # The .m5r polyglot interpreter
├─ files/           # Sample m5rcode scripts
├─ utils/               # Handling everything
├─ commands # Commands handling
├─ version.txt # Version of m5rcode showing on fastfetch command
├─ requirements.txt # Modules u need to install for m5rcode to work.
└─ README.md
```

---

## 🤝 Contributing

Contributions are welcome!  
If you want to add support for more languages, open an issue or PR.

---

## 👥 Credits

- **Creator:** [m5rcel](https://github.com/m4rcel-lol)  
- **Contributors:** The m5rcode community  

---

## 📜 Where can I install m5rcode from?

You can install m5rcode from it's official website **pythonjs.cfd** hover over and copy paste to your browser.
