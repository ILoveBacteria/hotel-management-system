<!-- src/routes/admin/payments/+page.svelte 

This page provides a comprehensive view of payment management for administrators.
Key features:
- Overview of total waiting, paid, and overdue bills
- Filterable bill listing
- Ability to update bill status
- Pagination support
- Responsive design with dark mode support

Main components:
- Payment statistics cards
- Filterable bills table
- Pagination controls
-->

<script lang="ts">
    import { onMount } from 'svelte';
    
    import type { UserProfile, Bill } from '$lib/types';
    import { goto } from '$app/navigation';
    import { PUBLIC_BASE_URL } from '$env/static/public';
    import {
        Loader2,
        AlertTriangle,
        CreditCard,
        CheckCircle,
        Clock,
        XCircle,
    } from 'lucide-svelte';

    let user: UserProfile | null = null;
    let bills: Bill[] = [];
    let isLoading = true;
    let error: string | null = null;
    let currentPage = 1;
    let totalPages = 1;
    let totalBills = 0;

    // Filters
    let statusFilter: 'all' | 'waiting' | 'paid' | 'overdue' = 'all';

    // Computed stats
    $: totalWaiting = bills.filter(bill => bill.status === 'waiting').reduce((sum, bill) => sum + bill.amount, 0);
    $: totalPaid = bills.filter(bill => bill.status === 'paid').reduce((sum, bill) => sum + bill.amount, 0);
    $: totalOverdue = bills.filter(bill => bill.status === 'overdue').reduce((sum, bill) => sum + bill.amount, 0);

    // Filtered and sorted bills
    $: filteredBills = bills.filter(bill => 
        statusFilter === 'all' || bill.status === statusFilter
    ).sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());

    function formatAmount(amount: number): string {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
    }

    function formatDate(dateString: string): string {
        return new Date(dateString).toLocaleDateString('en-IN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    function getStatusColor(status: string): string {
        switch (status) {
            case 'paid': return 'bg-green-100 text-green-800';
            case 'waiting': return 'bg-yellow-100 text-yellow-800';
            case 'overdue': return 'bg-red-100 text-red-800';
            default: return 'bg-gray-100 text-gray-800';
        }
    }

    function getStatusIcon(status: string) {
        switch (status) {
            case 'paid': return CheckCircle;
            case 'waiting': return Clock;
            case 'overdue': return AlertTriangle;
            default: return XCircle;
        }
    }

    async function loadBills(page = 1) {
        isLoading = true;
        error = null;

        try {
            const [profileResponse, billsResponse] = await Promise.all([
                fetch(`${PUBLIC_BASE_URL}/users/profile/`, {
                    credentials: 'include'
                }),
                fetch(`${PUBLIC_BASE_URL}/payments/bills/?page=${page}`, {
                    credentials: 'include'
                })
            ]);

            if (!profileResponse.ok) {
                goto('/admin/login');
                return;
            }

            const userProfile: UserProfile = await profileResponse.json();

            if (!userProfile.is_superuser) {
                goto('/admin/login');
                return;
            }

            user = userProfile;

            if (billsResponse.ok) {
                const data = await billsResponse.json();
                bills = data.results;
                totalBills = data.count;
                totalPages = Math.ceil(data.count / 10); // Assuming 10 items per page
                currentPage = page;
            } else {
                throw new Error('Failed to fetch bills');
            }
        } catch (err) {
            console.error('Failed to load bills:', err);
            error = 'Failed to load payment history';
        } finally {
            isLoading = false;
        }
    }

    async function handleUpdateBillStatus(bill: Bill, newStatus: 'waiting' | 'paid' | 'overdue') {
        try {
            const response = await fetch(`${PUBLIC_BASE_URL}/payments/bills/${bill.id}/`, {
                method: 'PATCH',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ status: newStatus })
            });

            if (!response.ok) {
                throw new Error('Failed to update bill status');
            }

            // Update local state
            bills = bills.map(b => b.id === bill.id ? { ...b, status: newStatus } : b);
        } catch (err) {
            console.error('Failed to update bill status:', err);
            error = 'Failed to update bill status';
        }
    }

    onMount(() => {
        loadBills();
    });
</script>

<svelte:head>
    <title>Payment Management - Bacteria Hotel Admin</title>
    <meta name="description" content="Manage and track bills, payments, and financial transactions in the Bacteria Hotel admin panel" />
</svelte:head>

{#if user}
    <div class="space-y-6">
        <!-- Page Header -->
        <div class="flex justify-between items-center">
            <h1 class="text-2xl font-semibold text-gray-900 dark:text-white">
                Payment Management
            </h1>
        </div>

        {#if error}
            <div class="bg-red-50 dark:bg-red-900/50 text-red-600 dark:text-red-200 p-4 rounded-lg flex items-center">
                <AlertTriangle class="w-5 h-5 mr-2" />
                {error}
            </div>
        {/if}

        <!-- Payment Statistics -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-gray-500 dark:text-gray-400">Total Waiting</p>
                        <p class="text-2xl font-semibold text-gray-900 dark:text-white">
                            {formatAmount(totalWaiting)}
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
                        <p class="text-sm text-gray-500 dark:text-gray-400">Total Overdue</p>
                        <p class="text-2xl font-semibold text-gray-900 dark:text-white">
                            {formatAmount(totalOverdue)}
                        </p>
                    </div>
                    <div class="p-3 bg-red-100 dark:bg-red-900/20 rounded-full">
                        <AlertTriangle class="w-6 h-6 text-red-600" />
                    </div>
                </div>
            </div>
        </div>

        <!-- Bills Table Section -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm">
            <div class="p-6 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
                <h2 class="text-lg font-medium text-gray-900 dark:text-white">
                    Billing History
                </h2>
                <div class="flex items-center space-x-4">
                    <label class="text-sm text-gray-500 dark:text-gray-400">
                        Filter by Status:
                    </label>
                    <select 
                        bind:value={statusFilter}
                        class="rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                    >
                        <option value="all">All Bills</option>
                        <option value="waiting">Waiting</option>
                        <option value="paid">Paid</option>
                        <option value="overdue">Overdue</option>
                    </select>
                </div>
            </div>

            {#if isLoading}
                <div class="flex items-center justify-center h-64">
                    <Loader2 class="w-8 h-8 animate-spin text-blue-600" />
                </div>
            {:else if filteredBills.length === 0}
                <div class="p-6 text-center text-gray-500 dark:text-gray-400">
                    No bills found.
                </div>
            {:else}
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                        <thead class="bg-gray-50 dark:bg-gray-700">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                    Bill ID
                                </th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                    Reservation
                                </th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                    Amount
                                </th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                    Due Date
                                </th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                    Payment Date
                                </th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                    Status
                                </th>
                                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                    Actions
                                </th>
                            </tr>
                        </thead>
                        <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                            {#each filteredBills as bill}
                                <tr>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                                        #{bill.id}
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                                        {bill.reserve}
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                                        {formatAmount(bill.amount)}
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                                        {formatDate(bill.due_date)}
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                                        {bill.payment_date ? formatDate(bill.payment_date) : '-'}
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span 
                                            class={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(bill.status)}`}
                                        >
                                            <svelte:component 
                                                this={getStatusIcon(bill.status)} 
                                                class="w-4 h-4 mr-1" 
                                            />
                                            {bill.status.charAt(0).toUpperCase() + bill.status.slice(1)}
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                        <div class="flex justify-end gap-2">
                                            {#if bill.status === 'waiting'}
                                                <button 
                                                    class="text-green-600 hover:text-green-900 dark:hover:text-green-400"
                                                    on:click={() => handleUpdateBillStatus(bill, 'paid')}
                                                >
                                                    Mark Paid
                                                </button>
                                                <button 
                                                    class="text-red-600 hover:text-red-900 dark:hover:text-red-400"
                                                    on:click={() => handleUpdateBillStatus(bill, 'overdue')}
                                                >
                                                    Mark Overdue
                                                </button>
                                            {/if}
                                        </div>
                                    </td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>

                <!-- Pagination -->
                {#if totalPages > 1}
                    <div class="px-6 py-4 border-t border-gray-200 dark:border-gray-700 flex items-center justify-between">
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
                {/if}
            {/if}
        </div>
    </div>
{/if}