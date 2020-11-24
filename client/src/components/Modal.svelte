<script>
    export let title;
    export let isOpen = false;
    export const open = () => {
        isOpen = true;
    }
    export const close = () => {
        isOpen = false;
    }
</script>

<style>
    .panel {
        z-index: 1000;
		position: fixed;
		left: 50%;
		top: 50%;
		transform: translateX(-50%) translateY(-50%);
		width: 200px;
    }
    
    .backdrop {
        position: fixed;
        top: 0;
        left: 0;
        z-index: 420;
        height: 100vh;
        width: 100vw;
        background: rgba(0, 0, 0, 40%);
    }
</style>

{#if isOpen}
    <div class="panel">
        <span>{title}</span>
        <button on:click={close}>X</button>
        <slot />
    </div>
    <div class="backdrop" on:click={close} />
{/if}