## PyAutoHotKey

# DEPREACATED: Because of limitation of the package i'm using this project will not be working on anymore

PyAutoHotKey is an AutoHotKey-like in python with it's own syntax

---

### Usage

```
ttest k(space)
k(shift) [ test k(space) maj ]
t(1000) m(right) t(1000) k(down) t(1000) k(down) t(1000) k(enter) t(1000)
m(2000, 500)
```

To run a script simply do:
`python3 src/main.py /path/to/script/`

---

### Doc

---

#### Normal string:
A normal string will press each of the key in quick succession.

Example:
```
testing testing2
```
It will write "testing" and "testing2" ignoring the space.

---

#### Special keys:
Special keys are a wait to press more complex keys like space, arrow keys and shift. </br>
Syntax: `k(key_name)`

Example:
```
testing k(space) testing2
```
It will write the same as for the example for normal string but with a space in the middle.

---

#### Key hold:
Key hold are a way to hold a key while doing other things. </br>
Syntax: `holded_key [ instructions ]`

Example:
```
k(shift) [ testing ]
```
It will write "testing" while pressing the shift key making the text upper-case.

---

#### Mouse instruction:
Mouse instruction can do two thing, move the mouse and click with the mouse, </br>
clicking is simple you just need to tell it which button to use (left, right, ...). </br>
For moving the mouse you need to give the instruction the new mouse position on the x and y axis. </br>
Syntax: `m(button_name | x, y)`

Example:
```
m(1250, 750)
m(right)
m(1300, 800)
m(left)
```
It will move the mouse to x: 1250 and y: 750, right click, go to x: 1300 and y: 800 to then left click.

---

#### Time wait instruction:
Time wait instruction can be used to wait a certain amount of milliseconds. </br>
Syntax: `t(milliseconds)`

Example:
```
before
t(2000)
after
```
It will write "before" then wait 2 seconds and after those write "after".

---

#### Keybind/Hotkeys:
Keybinds are a way to automate some action under a key sequence. </br>
To have some keybinds like `ctrl+t` you use key holds </br>
Syntax: `trigger_key { instruction }` </br>
Syntax with key hold: `hold_key[ trigger_key ] { instruction }`

Example:
```
k(ctrl) [ k(shift) [ f ] ] { t(1000) testing }
```
When `ctrl+shift+f` is pressed it will wait 1s and then write testing.