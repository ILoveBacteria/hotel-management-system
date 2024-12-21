<!-- src/routes/admin/dashboard/+page.svelte -->
<script lang="ts">
  import { onMount } from "svelte";
  import type { UserProfile } from "$lib/types";
  import { goto } from "$app/navigation";
  import { PUBLIC_BASE_URL } from "$env/static/public";
  import {
    Hotel,
    Users,
    CalendarDays,
    BedDouble,
    Loader2,
  } from "lucide-svelte";
  import AdminLayout from "$lib/components/admin/AdminLayout.svelte";

  let user: UserProfile | null = null;
  let isLoading = true;
  let error: string | null = null;

  // Stats
  let stats = {
    totalRooms: 0,
    availableRooms: 0,
    totalReservations: 0,
    totalUsers: 0,
  };

  async function checkAdmin() {
    try {
      const response = await fetch(`${PUBLIC_BASE_URL}/users/profile/`, {
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error("Not authenticated");
      }

      const userProfile: UserProfile = await response.json();

      if (!userProfile.is_superuser) {
        throw new Error("Not authorized");
      }

      user = userProfile;
    } catch (err) {
      goto("/admin");
    }
  }

  // In a real application, these would be API calls
  async function fetchDashboardStats() {
    try {
      // Simulate API calls
      stats = {
        totalRooms: 50,
        availableRooms: 12,
        totalReservations: 156,
        totalUsers: 89,
      };
    } catch (err) {
      console.error("Failed to fetch stats:", err);
      error = "Failed to load dashboard statistics";
    } finally {
      isLoading = false;
    }
  }

  onMount(async () => {
    await checkAdmin();
    await fetchDashboardStats();
  });

  const statCards = [
    {
      name: "Total Rooms",
      value: stats.totalRooms,
      icon: Hotel,
      color: "text-blue-600",
      bgColor: "bg-blue-100",
    },
    {
      name: "Available Rooms",
      value: stats.availableRooms,
      icon: BedDouble,
      color: "text-green-600",
      bgColor: "bg-green-100",
    },
    {
      name: "Total Reservations",
      value: stats.totalReservations,
      icon: CalendarDays,
      color: "text-purple-600",
      bgColor: "bg-purple-100",
    },
    {
      name: "Total Users",
      value: stats.totalUsers,
      icon: Users,
      color: "text-orange-600",
      bgColor: "bg-orange-100",
    },
  ];

  const recentActivity = [
    {
      type: "reservation",
      message: "New reservation #1234 created",
      time: "5 minutes ago",
    },
    {
      type: "user",
      message: "New user John Doe registered",
      time: "10 minutes ago",
    },
    {
      type: "room",
      message: "Room 301 maintenance completed",
      time: "1 hour ago",
    },
    { type: "system", message: "System backup completed", time: "2 hours ago" },
  ];
</script>

{#if user}
  <AdminLayout {user}>
    <div class="space-y-6">
      <!-- Page Header -->
      <div class="flex items-center justify-between">
        <h1 class="text-2xl font-semibold text-gray-900 dark:text-white">
          Dashboard Overview
        </h1>
        <div class="text-sm text-gray-500 dark:text-gray-400">
          Last updated: {new Date().toLocaleTimeString()}
        </div>
      </div>

      {#if isLoading}
        <div class="flex items-center justify-center h-64">
          <Loader2 class="w-8 h-8 animate-spin text-blue-600" />
        </div>
      {:else if error}
        <div
          class="bg-red-50 dark:bg-red-900/50 text-red-600 dark:text-red-200 p-4 rounded-lg"
        >
          {error}
        </div>
      {:else}
        <!-- Stats Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {#each statCards as stat}
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="p-3 rounded-lg {stat.bgColor} {stat.color}">
                    <svelte:component this={stat.icon} class="w-6 h-6" />
                  </div>
                </div>
                <div class="ml-4">
                  <p
                    class="text-sm font-medium text-gray-600 dark:text-gray-400"
                  >
                    {stat.name}
                  </p>
                  <p
                    class="text-2xl font-semibold text-gray-900 dark:text-white"
                  >
                    {stat.value}
                  </p>
                </div>
              </div>
            </div>
          {/each}
        </div>

        <!-- Recent Activity -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow">
          <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <h2 class="text-lg font-medium text-gray-900 dark:text-white">
              Recent Activity
            </h2>
          </div>
          <div class="divide-y divide-gray-200 dark:divide-gray-700">
            {#each recentActivity as activity}
              <div class="px-6 py-4">
                <div class="flex items-center justify-between">
                  <div class="flex items-center">
                    <span class="text-gray-900 dark:text-white font-medium">
                      {activity.message}
                    </span>
                  </div>
                  <span class="text-sm text-gray-500 dark:text-gray-400">
                    {activity.time}
                  </span>
                </div>
              </div>
            {/each}
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4">
            Quick Actions
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button
              class="flex items-center justify-center gap-2 px-4 py-2 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200"
            >
              <Hotel class="w-5 h-5" />
              Add New Room
            </button>
            <button
              class="flex items-center justify-center gap-2 px-4 py-2 bg-green-100 text-green-700 rounded-lg hover:bg-green-200"
            >
              <CalendarDays class="w-5 h-5" />
              View Reservations
            </button>
            <button
              class="flex items-center justify-center gap-2 px-4 py-2 bg-purple-100 text-purple-700 rounded-lg hover:bg-purple-200"
            >
              <Users class="w-5 h-5" />
              Manage Users
            </button>
          </div>
        </div>
      {/if}
    </div>
  </AdminLayout>
{/if}
