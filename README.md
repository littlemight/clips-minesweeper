# Knowledge Based Agent for Minesweeper


![alt text](/minesweeper.png)


## How to Run
1. Buka cmd untuk menjalankan Server Python
2. Ketik python app.py  di folder terluar untuk menjalankan server
3. Buka cmd baru untuk menjalankan Client Svelte
4. Ketik npm install di dalam folder client untuk mendownload dependency dan library yang digunakan 
5. Ketik npm run watch untuk menjalankan frontend 
6. Buka browser dan localhost:5000


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
|- README.md
|- app.py
|- board.py
|- bruteforce.py
|- constant.py
|- minesweeper.clp
|- requirements.txt
|- solver.py

```

- File-file yang terdapat pada folder client adalah file untuk menjalankan frontend 
- File app.py berisi kode untuk mendefinisikan route pada server
- File board.py berisi class Board dan method-method yang digunakan
- File solver.py berisi kode program pemanggilan virtual environement clips dan beberapa fungsi yang akan digunakan untuk memudahkan proses - inferensi 
- File minesweeper.pl berisi definisi fakta dan rule yang akan dijadikan sebagai input pada CLIPS
