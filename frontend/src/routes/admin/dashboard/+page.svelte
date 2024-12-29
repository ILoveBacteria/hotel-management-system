<!-- src/routes/admin/dashboard/+page.svelte -->
<script lang="ts">
  import { onMount } from "svelte";
  import type { UserProfile, Room, Reserve, RoomType } from "$lib/types";
  import { goto } from "$app/navigation";
  import { PUBLIC_BASE_URL } from "$env/static/public";
  import {
    Hotel,
    Users,
    CalendarDays,
    BedDouble,
    Loader2,
    AlertTriangle,
  } from "lucide-svelte";
  import AdminLayout from "$lib/components/admin/AdminLayout.svelte";

  let user: UserProfile | null = null;
  let isLoading = true;
  let error: string | null = null;

  // Stats data
  let rooms: Room[] = [];
  let reservations: Reserve[] = [];
  let users: UserProfile[] = [];
  let roomTypes: RoomType[] = [];

  // Computed stats
  $: stats = {
    totalRooms: rooms.length,
    availableRooms: rooms.filter((r) => r.status === "available").length,
    totalReservations: reservations.length,
    totalUsers: users.length,
  };

  // Recent activity tracking with types
  interface ActivityItem {
    id: string;
    type: "reservation" | "user" | "room" | "system";
    message: string;
    time: string;
    timestamp: Date;
  }

  let recentActivity: ActivityItem[] = [];

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
      goto("/admin/login");
    }
  }

  async function fetchDashboardData() {
    try {
      const [roomsRes, reservationsRes, roomTypesRes] = await Promise.all([
        fetch(`${PUBLIC_BASE_URL}/rooms/inventories/`, {
          credentials: "include",
        }),
        fetch(`${PUBLIC_BASE_URL}/reservations/reserves/`, {
          credentials: "include",
        }),
        fetch(`${PUBLIC_BASE_URL}/rooms/types/`, { credentials: "include" }),
      ]);

      if (!roomsRes.ok || !reservationsRes.ok || !roomTypesRes.ok) {
        throw new Error("Failed to fetch dashboard data");
      }

      // Parse response data
      const roomsData = await roomsRes.json();
      const reservationsData = await reservationsRes.json();
      const roomTypesData = await roomTypesRes.json();

      rooms = roomsData.results;
      reservations = reservationsData.results;
      roomTypes = roomTypesData.results;

      // Add room type summary to activity
      const roomTypeSummary = roomTypes.map((type) => ({
        id: `type-${type.id}`,
        type: "room" as const,
        message: `${type.name}: ${rooms.filter((r) => r.room_type === type.id).length} rooms`,
        time: "Current status",
        timestamp: new Date(),
      }));

      // Generate recent activity from actual data
      const activity: ActivityItem[] = [
        ...reservations.slice(0, 3).map((res) => ({
          id: `res-${res.id}`,
          type: "reservation" as const,
          message: `New reservation #${res.id} created`,
          time: formatTimeAgo(new Date(res.created_at)),
          timestamp: new Date(res.created_at),
        })),
        ...rooms
          .filter((r) => r.status === "maintenance")
          .slice(0, 2)
          .map((room) => ({
            id: `room-${room.room_number}`,
            type: "room" as const,
            message: `Room ${room.room_number} under maintenance`,
            time: formatTimeAgo(
              room.last_maintained ? new Date(room.last_maintained) : new Date()
            ),
            timestamp: room.last_maintained
              ? new Date(room.last_maintained)
              : new Date(),
          })),
        ...roomTypeSummary,
      ];

      recentActivity = activity.sort(
        (a, b) => b.timestamp.getTime() - a.timestamp.getTime()
      );
    } catch (err) {
      console.error("Failed to fetch dashboard data:", err);
      error = "Failed to load dashboard statistics";
    } finally {
      isLoading = false;
    }
  }

  function formatTimeAgo(date: Date): string {
    const now = new Date();
    const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);

    if (diffInSeconds < 60) return "just now";
    if (diffInSeconds < 3600)
      return `${Math.floor(diffInSeconds / 60)} minutes ago`;
    if (diffInSeconds < 86400)
      return `${Math.floor(diffInSeconds / 3600)} hours ago`;
    return `${Math.floor(diffInSeconds / 86400)} days ago`;
  }

  // Quick actions handlers
  async function handleAddRoom() {
    goto("/admin/rooms/new");
  }

  async function handleViewReservations() {
    goto("/admin/reservations");
  }

  async function handleManageUsers() {
    goto("/admin/users");
  }

  const statCards = [
    {
      name: "Total Rooms",
      value: stats?.totalRooms || 0,
      icon: Hotel,
      color: "text-blue-600",
      bgColor: "bg-blue-100",
    },
    {
      name: "Available Rooms",
      value: stats?.availableRooms || 0,
      icon: BedDouble,
      color: "text-green-600",
      bgColor: "bg-green-100",
    },
    {
      name: "Total Reservations",
      value: stats?.totalReservations || 0,
      icon: CalendarDays,
      color: "text-purple-600",
      bgColor: "bg-purple-100",
    },
    {
      name: "Total Users",
      value: stats?.totalUsers || 0,
      icon: Users,
      color: "text-orange-600",
      bgColor: "bg-orange-100",
    },
  ];

  onMount(async () => {
    await checkAdmin();
    await fetchDashboardData();
  });
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
          class="bg-red-50 dark:bg-red-900/50 text-red-600 dark:text-red-200 p-4 rounded-lg flex items-center"
        >
          <AlertTriangle class="w-5 h-5 mr-2" />
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
              class="flex items-center justify-center gap-2 px-4 py-2 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors"
              on:click={handleAddRoom}
            >
              <Hotel class="w-5 h-5" />
              Add New Room
            </button>
            <button
              class="flex items-center justify-center gap-2 px-4 py-2 bg-green-100 text-green-700 rounded-lg hover:bg-green-200 transition-colors"
              on:click={handleViewReservations}
            >
              <CalendarDays class="w-5 h-5" />
              View Reservations
            </button>
            <button
              class="flex items-center justify-center gap-2 px-4 py-2 bg-purple-100 text-purple-700 rounded-lg hover:bg-purple-200 transition-colors"
              on:click={handleManageUsers}
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
