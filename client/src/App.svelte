<script>
	let grid = [];
	let nGrid = 4;
	let nBombs = 0;

	let inputBomb = true;
	const resetGrid = () => {
		if (nGrid > 10) nGrid = 10;
		else if (nGrid < 4) nGrid = 4;
		nBombs = 0;
		grid = [];
		for (let i = 0; i < nGrid; i++) {
			grid[i] = new Array(nGrid);
			for (let j = 0; j < nGrid; j++) {
				grid[i][j] = {
					bomb: false,
					revealed: false,
					cnt: 0
				}
			}
		}
	}
	
	const toggleBomb = (i, j) => {
		if (!grid[i][j].bomb) nBombs++;
		else nBombs--;
		grid[i][j].bomb = !grid[i][j].bomb;
		cntAllTiles();
	}

	const dfs = (i, j) => {
		grid[i][j].revealed = true;
		if (grid[i][j].bomb) {
			for (let i = 0; i < nGrid; i++) {
				for (let j = 0; j < nGrid; j++) {
					if (grid[i][j].bomb) {
						grid[i][j].revealed = true;
					}
				}
			}
			return;
		}
		if (grid[i][j].cnt == 0) {
			for (let di = -1; di <= 1; di++) {
				for (let dj = -1; dj <= 1; dj++) {
					let ti = i + di, tj = j + dj;
					if (ti >= 0 && ti < nGrid && tj >= 0 && tj < nGrid) {
						if (!grid[ti][tj].revealed) {
							dfs(ti, tj);
						}
					}
				}
			}
		}
	}

	const cntBomb = (i, j) => {
		grid[i][j].cnt = 0;
		if (grid[i][j].bomb) return;
		for (let di = -1; di <= 1; di++) {
			for (let dj = -1; dj <= 1; dj++) {
				let ti = i + di, tj = j + dj;
				if (ti >= 0 && ti < nGrid && tj >= 0 && tj < nGrid) {
					if (grid[ti][tj].bomb) grid[i][j].cnt++;
				}
			}
		}
	}

	const cntAllTiles = () => {
		for (let i = 0; i < nGrid; i++) {
			for (let j = 0; j < nGrid; j++) {
				cntBomb(i, j);
			}
		}
	}
	
	const endBombInput = () => {
		inputBomb = false;
	}

	resetGrid();
</script>

<main>
	{#if inputBomb}
		<input type="number" bind:value={nGrid} on:change={resetGrid} min="4" max="10">
		<p>Grid size: {nGrid}</p>
		<p>Bombs: {nBombs}</p>
	{:else}
		<button on:click={() => {inputBomb = true, resetGrid()}}>Reset</button>
	{/if}
	<div class="board">
		{#each grid as row, i}
			{#each row as tile, j}
				<div
					class="tile"
					style="grid-row: {i + 1}; grid-column: {j + 1}"
					class:revealed={tile.revealed}
					class:bomb={tile.bomb && (tile.revealed || inputBomb)}
					on:click={() => inputBomb ? toggleBomb(i, j) : dfs(i, j) }
				>
					{#if inputBomb || tile.revealed}
						{tile.cnt ? tile.cnt : ''}
					{/if}
				</div>
			{/each}
		{/each}
	</div>
	{#if inputBomb}
		<button on:click={endBombInput}>End Bomb Input</button>
	{/if}
</main>

<style>
	@import url("https://fonts.googleapis.com/css?family=Inconsolata");

	:global(body) {
		font-family: 'Inconsolata';
	}

	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	.board {
		display: grid;
		width: fit-content;
		height: fit-content;
		margin: auto;
	}

	.tile {
		text-align: center;
		line-height: 50px;
		height: 50px;
		width: 50px;
		border: 1px solid #000;
		cursor: pointer;
	}

	.bomb:before {
		content: '';
		background: #000;
		position: absolute;
		transform: translate(-50%, 50%);
		width: 25px;
		height: 25px;
		border-radius: 50%;
	}

	.revealed {
		background: #555;
		color: white;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>