
<script lang="ts">
    import Header from "../dashboard/Header.svelte";
    import Sidebar from "../dashboard/Sidebar.svelte";


    export let username = "John Doe";
    export let notifications = 2;
</script>

<div class="flex h-screen bg-gray-50 dark:bg-gray-900">
    <Sidebar {username} />
    <div class="flex-1 ml-64">
        <Header {username} {notifications} />
        <main class="p-6 space-y-6">
            <slot />
        </main>
    </div>
</div>