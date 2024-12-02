<script lang="ts">
  import Dashboard from "$lib/components/Dashboard.svelte";
  import Header from "$lib/components/Header.svelte";
  import NewBooking from "$lib/components/NewBooking.svelte";
  import Sidebar from "$lib/components/Sidebar.svelte";
  import { onMount } from "svelte";

  let currentPage = "dashboard";

  // @ts-ignore
  function handleNavigation(event) {
    currentPage = event.detail;
  }
</script>

<div class="flex h-screen bg-gray-100">
  <!-- Sidebar Component -->
  <Sidebar {currentPage} on:navigate={handleNavigation} />

  <!-- Main Content -->
  <div class="flex-1 flex flex-col overflow-hidden">
    <Header />

    <main class="flex-1 overflow-y-auto bg-gray-100 p-4">
      {#if currentPage === "dashboard"}
        <Dashboard />
      {:else if currentPage === "bookings-new-booking"}
        <NewBooking />
      {:else}
        <p>Content for {currentPage}</p>
      {/if}
    </main>
  </div>
</div>
