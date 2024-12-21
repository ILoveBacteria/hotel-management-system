
<script lang="ts">
    import { navigating } from "$app/stores";
    import { fade, fly } from "svelte/transition";
</script>

{#if $navigating}
    <div 
        class="fixed top-0 left-0 w-full z-50"
        in:fly={{ y: -10, duration: 200 }}
        out:fade={{ duration: 200 }}
    >
        <div class="w-full h-1 bg-blue-100">
            <div 
                class="h-1 bg-blue-600 transition-all duration-200 ease-in-out animate-loading-bar"
            />
        </div>
    </div>
{/if}

<style>
    @keyframes loading-bar {
        0% {
            width: 0%;
        }
        20% {
            width: 20%;
        }
        40% {
            width: 40%;
        }
        60% {
            width: 60%;
        }
        80% {
            width: 80%;
        }
        100% {
            width: 100%;
        }
    }

    .animate-loading-bar {
        animation: loading-bar 2s ease-in-out infinite;
    }
</style>