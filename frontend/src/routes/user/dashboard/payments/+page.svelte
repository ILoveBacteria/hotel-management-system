<!-- src/routes/dashboard/payments/+page.svelte -->
<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { PUBLIC_BASE_URL } from "$env/static/public";
  import type { UserProfile, Bill } from "$lib/types";
  import DashboardLayout from "$lib/components/layout/DashboardLayout.svelte";
  import {
    CreditCard,
    Calendar,
    Clock,
    AlertCircle,
    CheckCircle,
    XCircle,
  } from "lucide-svelte";

  let userProfile: UserProfile | null = null;
  let bills: Bill[] = [];
  let isLoading = true;
  let error: string | null = null;
  let currentPage = 1;
  let totalPages = 1;
  let totalBills = 0;

  // Payment statistics
  $: totalPaid = bills.reduce(
    (sum, bill) => (bill.status === "paid" ? sum + bill.amount : sum),
    0
  );
  $: totalPending = bills.reduce(
    (sum, bill) => (bill.status === "waiting" ? sum + bill.amount : sum),
    0
  );
  $: overdueBills = bills.filter((bill) => bill.status === "overdue").length;

  function formatAmount(amount: number): string {
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
    }).format(amount);
  }

  function formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString("en-IN", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  }

  function getStatusColor(status: string): string {
    switch (status) {
      case "paid":
        return "text-green-600 bg-green-100 dark:bg-green-900/20";
      case "waiting":
        return "text-yellow-600 bg-yellow-100 dark:bg-yellow-900/20";
      case "overdue":
        return "text-red-600 bg-red-100 dark:bg-red-900/20";
      default:
        return "text-gray-600 bg-gray-100 dark:bg-gray-900/20";
    }
  }

  function getStatusIcon(status: string) {
    switch (status) {
      case "paid":
        return CheckCircle;
      case "waiting":
        return Clock;
      case "overdue":
        return AlertCircle;
      default:
        return XCircle;
    }
  }

  async function loadBills(page = 1) {
    isLoading = true;
    error = null;

    try {
      const [profileResponse, billsResponse] = await Promise.all([
        fetch(`${PUBLIC_BASE_URL}/users/profile/`, {
          credentials: "include",
        }),
        fetch(`${PUBLIC_BASE_URL}/users/bills/?page=${page}`, {
          credentials: "include",
        }),
      ]);

      if (!profileResponse.ok) {
        goto("/");
        return;
      }

      userProfile = await profileResponse.json();

      if (billsResponse.ok) {
        const data = await billsResponse.json();
        bills = data.results;
        totalBills = data.count;
        totalPages = Math.ceil(data.count / 10); // Assuming 10 items per page
        currentPage = page;
      } else {
        throw new Error("Failed to fetch bills");
      }
    } catch (err) {
      console.error("Failed to load bills:", err);
      error = "Failed to load payment history";
    } finally {
      isLoading = false;
    }
  }

  async function handlePayment(billId: number) {
    // This would integrate with your payment gateway
    alert("Payment gateway integration would go here");
  }

  onMount(() => {
    loadBills();
  });
</script>

<DashboardLayout username={userProfile?.username || "Guest"}>
  <div class="max-w-7xl mx-auto space-y-6">
    <!-- Page Header -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
      <h1
        class="text-2xl font-semibold text-gray-900 dark:text-white flex items-center"
      >
        <CreditCard class="w-6 h-6 mr-2" />
        Payments & Billing
      </h1>
      <p class="mt-2 text-gray-600 dark:text-gray-400">
        Manage your payments and view billing history
      </p>
    </div>

    <!-- Payment Statistics -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 dark:text-gray-400">Total Paid</p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">
              {formatAmount(totalPaid)}
            </p>
          </div>
          <div class="p-3 bg-green-100 dark:bg-green-900/20 rounded-full">
            <CheckCircle class="w-6 h-6 text-green-600" />
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              Pending Payments
            </p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">
              {formatAmount(totalPending)}
            </p>
          </div>
          <div class="p-3 bg-yellow-100 dark:bg-yellow-900/20 rounded-full">
            <Clock class="w-6 h-6 text-yellow-600" />
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              Overdue Bills
            </p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">
              {overdueBills}
            </p>
          </div>
          <div class="p-3 bg-red-100 dark:bg-red-900/20 rounded-full">
            <AlertCircle class="w-6 h-6 text-red-600" />
          </div>
        </div>
      </div>
    </div>

    <!-- Bills Table -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm">
      <div class="p-6 border-b border-gray-200 dark:border-gray-700">
        <h2 class="text-lg font-medium text-gray-900 dark:text-white">
          Payment History
        </h2>
      </div>

      {#if error}
        <div class="p-6">
          <div
            class="bg-red-50 dark:bg-red-900/50 text-red-600 dark:text-red-200 p-4 rounded-lg"
          >
            {error}
          </div>
        </div>
      {/if}

      {#if isLoading}
        <div class="p-6">
          <div class="flex items-center justify-center">
            <svg class="animate-spin h-8 w-8 text-blue-600" viewBox="0 0 24 24">
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
                fill="none"
              />
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
          </div>
        </div>
      {:else if bills.length === 0}
        <div class="p-6 text-center text-gray-500 dark:text-gray-400">
          No billing history found
        </div>
      {:else}
        <div class="overflow-x-auto">
          <table
            class="min-w-full divide-y divide-gray-200 dark:divide-gray-700"
          >
            <thead class="bg-gray-50 dark:bg-gray-700/50">
              <tr>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider"
                >
                  Bill ID
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider"
                >
                  Amount
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider"
                >
                  Due Date
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider"
                >
                  Status
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider"
                >
                  Payment Date
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider"
                >
                  Action
                </th>
              </tr>
            </thead>
            <tbody
              class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700"
            >
              {#each bills as bill}
                <tr>
                  <td
                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white"
                  >
                    #{bill.id}
                  </td>
                  <td
                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white"
                  >
                    {formatAmount(bill.amount)}
                  </td>
                  <td
                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white"
                  >
                    {formatDate(bill.due_date)}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium
                                                   {getStatusColor(
                        bill.status
                      )}"
                    >
                      <svelte:component
                        this={getStatusIcon(bill.status)}
                        class="w-4 h-4 mr-1"
                      />
                      {bill.status.charAt(0).toUpperCase() +
                        bill.status.slice(1)}
                    </span>
                  </td>
                  <td
                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white"
                  >
                    {bill.payment_date ? formatDate(bill.payment_date) : "-"}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm">
                    {#if bill.status === "waiting"}
                      <button
                        class="text-blue-600 hover:text-blue-700 font-medium"
                        on:click={() => handlePayment(bill.id)}
                      >
                        Pay Now
                      </button>
                    {:else if bill.status === "overdue"}
                      <button
                        class="text-red-600 hover:text-red-700 font-medium"
                        on:click={() => handlePayment(bill.id)}
                      >
                        Pay Overdue
                      </button>
                    {:else}
                      <span class="text-gray-400">Completed</span>
                    {/if}
                  </td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        {#if totalPages > 1}
          <div class="px-6 py-4 border-t border-gray-200 dark:border-gray-700">
            <div class="flex items-center justify-between">
              <div class="text-sm text-gray-500 dark:text-gray-400">
                Showing page {currentPage} of {totalPages}
              </div>
              <div class="flex space-x-2">
                <button
                  class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg
                                           text-sm font-medium text-gray-700 dark:text-gray-200
                                           hover:bg-gray-50 dark:hover:bg-gray-700
                                           disabled:opacity-50"
                  disabled={currentPage === 1}
                  on:click={() => loadBills(currentPage - 1)}
                >
                  Previous
                </button>
                <button
                  class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg
                                           text-sm font-medium text-gray-700 dark:text-gray-200
                                           hover:bg-gray-50 dark:hover:bg-gray-700
                                           disabled:opacity-50"
                  disabled={currentPage === totalPages}
                  on:click={() => loadBills(currentPage + 1)}
                >
                  Next
                </button>
              </div>
            </div>
          </div>
        {/if}
      {/if}
    </div>
  </div>
</DashboardLayout>
