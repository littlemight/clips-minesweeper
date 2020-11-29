# Knowledge Based Agent for Minesweeper


![alt text](/minesweeper.png)



## File Structure
```bash
|- client
|- public
|- index.html
|- global.css
|- favicon.png

|- script
| - setupTypeScript.js
|- src
|- components
|- Modal.svelte
|- Tile.svelte
|- App.svelte
|- main.js
|- .gitignore
|- README.md
|- package-lock.json
|- package.json
|- rollup.config.js
|- test
|- README.md
|- app.py
|- board.py
|- bruteforce.py
|- constant.py
|- minesweeper.clp
|- requirements.txt
|- run.bat
|- solver.py
|- trace.bat
```

- File-file yang terdapat pada folder client adalah file untuk menjalankan frontend 
- File app.py berisi kode untuk mendefinisikan route pada server
- File board.py berisi class Board dan method-method yang digunakan
- File solver.py berisi kode program pemanggilan virtual environement clips dan beberapa fungsi yang akan digunakan untuk memudahkan proses - inferensi 
- File minesweeper.pl berisi definisi fakta dan rule yang akan dijadikan sebagai input pada CLIPS

