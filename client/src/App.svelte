<script>
	let curGrid = [];
	let curStateId = 0;
	let grids = [];
	let nGrid = 4;
	let nBombs = 0;

	let inputBomb = true;
	const resetGrid = () => {
		if (nGrid > 10) nGrid = 10;
		else if (nGrid < 4) nGrid = 4;
		nBombs = 0;
		curGrid = [];
		grids = [];
		curStateId = 0;
		for (let i = 0; i < nGrid; i++) {
			curGrid[i] = new Array(nGrid);
			for (let j = 0; j < nGrid; j++) {
				curGrid[i][j] = {
					bomb: false,
					revealed: false,
					cnt: 0
				}
			}
		}
	}
	
	const toggleBomb = (i, j) => {
		if (!curGrid[i][j].bomb) nBombs++;
		else nBombs--;
		curGrid[i][j].bomb = !curGrid[i][j].bomb;
		cntAllTiles();
	}

	const reveal = (i, j) => {
		if (curGrid[i][j].revealed) {
			console.log('udah di reveal lur');
			return;
		}
		dfs(i, j);
		while (curStateId != grids.length - 1) {
			grids.pop();
		}
		grids.push(JSON.parse(JSON.stringify(curGrid)));
		curStateId++;
	}
	
	const dfs = (i, j) => {
		if (curGrid[i][j].bomb) {
			for (let i = 0; i < nGrid; i++) {
				for (let j = 0; j < nGrid; j++) {
					if (curGrid[i][j].bomb) {
						curGrid[i][j].revealed = true;
					}
				}
			}
			return;
		}
		curGrid[i][j].revealed = true;
		if (curGrid[i][j].cnt == 0) {
			for (let di = -1; di <= 1; di++) {
				for (let dj = -1; dj <= 1; dj++) {
					let ti = i + di, tj = j + dj;
					if (ti >= 0 && ti < nGrid && tj >= 0 && tj < nGrid) {
						if (!curGrid[ti][tj].revealed) {
							dfs(ti, tj);
						}
					}
				}
			}
		}
	}

	const cntBomb = (i, j) => {
		curGrid[i][j].cnt = 0;
		if (curGrid[i][j].bomb) return;
		for (let di = -1; di <= 1; di++) {
			for (let dj = -1; dj <= 1; dj++) {
				let ti = i + di, tj = j + dj;
				if (ti >= 0 && ti < nGrid && tj >= 0 && tj < nGrid) {
					if (curGrid[ti][tj].bomb) curGrid[i][j].cnt++;
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
		grids.push(JSON.parse(JSON.stringify(curGrid)));
	}

	const prevState = () => {
		if (curStateId > 0) {
			curStateId--;
		} else return;
		console.log(curGrid);
		curGrid = JSON.parse(JSON.stringify(grids[curStateId]))
	}

	const nextState = () => {
		if (curStateId + 1 < grids.length) {
			curStateId++;
		} else {
			//TODO: get clips (i, j) result
			return;
		}
		curGrid = JSON.parse(JSON.stringify(grids[curStateId]))
	}

	import Modal from './components/Modal.svelte'
	let textInputModal = Modal;
	let sizeInputModal = Modal;
	resetGrid();
</script>

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

<main style="display: grid; height: 100vh;">
	<div class="container" style="display: flex; flex-direction: row;">
		<div class="euy" style="margin: auto;">
			<textarea name="Facts" cols="30" rows="10"
				placeholder="F1 euy
				F2 euy"
				style="resize: none;"
			></textarea>
		</div>
		<div style="margin: auto;" class="panel minesweeper">
			<div>
				{#if inputBomb}
					<button on:click={sizeInputModal.open}>Change size</button>
					<Modal title="Change grid size" bind:this={sizeInputModal}>
						<input type="number" bind:value={nGrid} on:change={resetGrid} min="4" max="10" style="width: 100%;">
					</Modal>
	
					<p>Grid size: {nGrid}</p>
					<p>Bombs: {nBombs}</p>
					<button on:click={textInputModal.open}>Input config by text</button>
					<Modal title="Input by text" bind:this={textInputModal}>
						<div style="display: grid;">
							<textarea name="textinput" id="" cols="30" rows="15" style="display: block; resize: none;"></textarea>
							<button on:click={textInputModal.close}>Apply Input</button>
						</div>
					</Modal>
					<button on:click={endBombInput}>End Bomb Input</button>
				{:else}
					<button on:click={prevState} disabled={curStateId == 0}>Prev</button>
					<button on:click={() => {inputBomb = true, resetGrid()}}>Reset</button>
					<button on:click={() => {}} disabled>CLIPS</button>
					<button on:click={nextState} disabled={curStateId == grids.length - 1}>Next</button>
				{/if}
			</div>
			<div class="board">
				{#each curGrid as row, i}
					{#each row as tile, j}
						<div
							class="tile"
							style="grid-row: {i + 1}; grid-column: {j + 1}"
							class:revealed={tile.revealed}
							class:bomb={tile.bomb && (tile.revealed || inputBomb)}
							on:click={() => inputBomb ? toggleBomb(i, j) : reveal(i, j) }
						>
							{#if inputBomb || tile.revealed}
								{tile.cnt ? tile.cnt : ''}
							{/if}
						</div>
					{/each}
				{/each}
			</div>
		</div>
		<div class="euy2" style="margin: auto;">
			<textarea name="Agenda" id="" cols="30" rows="10"
				placeholder="R1 euy
				R2 euy"
				style="resize: none;"
			></textarea>
		</div>
	</div>
</main>