<script>
	let startGrid = [];
	let curGrid = [];
	let step = 0;
	let nGrid = 4;
	let nBombs = 0;
	let bombsFound = 0;

	const ONGOING = 0;
	const WIN = 1;
	const LOSE = 2 
	let gameStatus = ONGOING;
	
	let moves, agendas,facts;
	// moves stores array of (x, y, clickBomb) made by CLIPS
	// agendas stores.... the agenda.

	let inputBomb = true, waiting = false;

	const resetGrid = (size=4) => {
		if (size > 10) nGrid = 10;
		else if (size < 4) nGrid = 4;
		nBombs = 0;
		bombsFound = 0;
		curGrid = [];
		moves = agendas = [];
		step = 0;
		gameStatus = ONGOING;
		for (let i = 0; i < size; i++) {
			curGrid[i] = new Array(size);
			for (let j = 0; j < size; j++) {
				curGrid[i][j] = {
					bomb: false,
					revealed: false,
					flagged: false,
					cnt: 0
				}
			}
		}
	}
	
	const convertGridToConfig = (grid) => {
		let bombPos = []
		for (let i = 0; i < nGrid; i++) {
			for (let j = 0; j < nGrid; j++) {
				if (grid[i][j].bomb) {
					bombPos.push({x: i, y: j})
				}
			}
		}
		const ret = {
			nGrid, nBombs, bombPos
		}
		return ret;
	}

	const processConfig = () => {
		let configInput = document.getElementsByName("configInput")[0].value.split('\n');
		nGrid = parseInt(configInput[0])
		resetGrid(nGrid);
		nBombs = parseInt(configInput[1])

		for (let i = 2; i - 2 < nBombs; i++) {
			let pos = configInput[i].split(', ');
			curGrid[pos[0]][pos[1]].bomb = true;			
		}
		cntAllTiles();
	}

	const toggleBomb = (i, j) => {
		if (!curGrid[i][j].bomb) nBombs++;
		else nBombs--;
		curGrid[i][j].bomb = !curGrid[i][j].bomb;
		cntAllTiles();
	}

	const reveal = (i, j) => {
		if (curGrid[i][j].revealed) {
			return;
		}
		if (curGrid[i][j].bomb) {
			for (let i = 0; i < nGrid; i++) {
				for (let j = 0; j < nGrid; j++) {
					if (curGrid[i][j].bomb) {
						curGrid[i][j].revealed = true;
					}
				}
			}
			gameStatus = LOSE;
			return;
		}
		dfs(i, j);
	}

	// asumsi (i, j) blm di flag
	const flag = (i, j) => {
		curGrid[i][j].flagged = true;
		if (curGrid[i][j].bomb) {
			bombsFound++;
			if (bombsFound == nBombs) {
				gameStatus = WIN;
			}
		}
	}

	
	const dfs = (i, j) => {
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
		waiting = true;
		fetch('./initSolver',{
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(convertGridToConfig(curGrid))
		}).then(
			res => res.json()
		).then(
			res => {
				moves = [[-1, -1, 0], ...res[0]];
				agendas = ['Empty', ...res[1]];
				facts = ['Empty',...res[2]];
				startGrid = JSON.parse(JSON.stringify(curGrid));
				inputBomb = false;
				waiting = false;
				console.log(facts);
			}
		);
	}

	const simulateStep = (step) => {
		curGrid = JSON.parse(JSON.stringify(startGrid))
		bombsFound = 0;
		if (step == 0) return;
		for (let i = 1; i <= step; i++) {
			if (moves[i][2]) {
				flag(moves[i][0], moves[i][1]);
			} else {
				reveal(moves[i][0], moves[i][1]);
			}
		}
	}
	
	const prevState = () => {
		if (step > 0) {
			step--;
			simulateStep(step);
		}
	}

	const nextState = () => {
		if (step + 1 < moves.length) {
			step++;
			simulateStep(step);
		}
	}

	import Modal from './components/Modal.svelte'
	let textInputModal = Modal;
	let sizeInputModal = Modal;
	let gameFinishedModal = Modal;
	resetGrid();//size parameter default = 4
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

	.tile-small{
		height: 35px;
		width: 35px;
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

	.bomb-small:before{
		width: 17px;
		height: 17px;
	}

	.revealed {
		background: #555;
		color: white;
	}

	.flagged {
		background: pink;
	}
	.info-container{
		background-color: #fff;
		border: 1px solid black;
		width: 25%;
		height:100px;
		min-height: 80%;
		margin: auto 20px;
	}
	.f-container, .a-container {
		overflow: scroll;
		max-width: 25%;
	}

	.board-container{
		margin: 20px 0px;
	}
	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
	ol{
		text-align: left;
	}
</style>

<main style="display: grid; height: 100vh;">
	<div class="container" style="display: flex; flex-direction: row; justify-content:center">
		<div class="info-container f-container">
			<h3>Final Facts</h3>
			<!-- splice 2 to remove 'empty' and 'intial fact' -->
			{#if !inputBomb && !waiting}
				<ol>
					{#each (facts.splice(2)) as fact}  
					<li>
						{fact}
					</li>
					{/each}
				</ol>
			{/if}
		</div>
		<!-- <div style="margin: auto;" class="panel minesweeper"> -->
		<div class="info-container minesweeper" style="min-width: 40%  min-height: max-content">
			{#if waiting}
				<p>Waiting clips result...</p>
			{/if}
			<div class="board-container">
				{#if inputBomb}
					<button on:click={sizeInputModal.open}>Change size</button>
					<Modal title="Change grid size" bind:this={sizeInputModal}>
						<input type="number" bind:value={nGrid} on:change={()=>resetGrid(nGrid)} min="4" max="10" style="width: 100%;">
					</Modal>
	
					<p>Grid size: {nGrid}</p>
					<p>Bombs: {nBombs}</p>
					<button on:click={textInputModal.open}>Input config by text</button>
					<Modal title="Input by text" bind:this={textInputModal}>
						<div style="display: grid;">
							<textarea name="configInput" cols="30" rows="15" style="display: block; resize: none;"></textarea>
							<button on:click={() => {processConfig(), textInputModal.close()}}>Apply Input</button>
						</div>
					</Modal>
					<button on:click={endBombInput}>End Bomb Input</button>
				{:else if (gameStatus > ONGOING)}
					<Modal title="Game Finished" bind:this={gameFinishedModal} isOpen={true} backdropClickable={false}>
						<div style="display: grid;">
							<h1>You {gameStatus == WIN ? 'Won' : 'Lost'}!</h1>
							<button on:click={() => {resetGrid(), inputBomb = true, gameFinishedModal.close()}}>Reset</button>
						</div>
					</Modal>
				{:else}
					<button on:click={prevState} disabled={step == 0}>Prev</button>
					<button on:click={() => {inputBomb = true, resetGrid()}}>Reset</button>
					<button on:click={nextState} disabled={step == moves.length - 1}>Next</button>
				{/if}
			</div>
			<div class="board">
				{#each curGrid as row, i}
					{#each row as tile, j}
						<div
							class="tile {nGrid > 7 ? 'tile-small' : ''}"
							style="grid-row: {i + 1}; grid-column: {j + 1}"
							class:revealed={tile.revealed}
							class:flagged={tile.flagged}
							class:bomb={tile.bomb && (tile.revealed || inputBomb)}
							class:bomb-small= {nGrid > 7}
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
		<div class="info-container a-container">
			<h3>Agenda</h3>
			{#if !inputBomb && !waiting}
			<ol>
				{#each (agendas.splice(1)) as agenda}
					<li>
						{agenda}
					</li>
				{/each}
			</ol>
		{/if}
		</div>
	</div>
</main>