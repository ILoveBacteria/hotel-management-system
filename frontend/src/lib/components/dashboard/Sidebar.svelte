<script lang="ts">
	import { goto } from '$app/navigation';
	import { PUBLIC_BASE_URL } from '$env/static/public';
	import {
		Home,
		Calendar,
		CreditCard,
		User,
		LogOut,
		BedDouble,
		ReceiptSwissFranc
	} from 'lucide-svelte';
	import { page } from '$app/stores';

	export let username: string;
	$: selected = $page.url.pathname.split('/').pop() || 'dashboard';

	async function logout() {
		try {
			await fetch(`${PUBLIC_BASE_URL}/auth/logout/`, {
				method: 'POST',
				credentials: 'include',
			});
			goto('/user/login');
		} catch (error) {
			console.error('Logout failed:', error);
		}
	}

	function handleNavigation(path: string, newSelected: string) {
		if (selected === newSelected) return;
		selected = newSelected;
		goto(path);
	}
</script>

<aside class="fixed inset-y-0 left-0 w-64 bg-white dark:bg-gray-800 shadow-lg">
	<div class="flex flex-col h-full">
		<div
			class="flex items-center justify-center h-16 border-b dark:border-gray-700"
		>
			<span class="text-xl font-bold text-blue-600">Bacteria Hotel</span>
		</div>

		<nav class="flex-1 p-4 space-y-2">
			<button
				on:click={() =>
					handleNavigation('/user/dashboard', 'dashboard')}
				class="flex items-center w-full px-4 py-2 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 {selected ===
				'dashboard'
					? 'bg-gray-100 dark:bg-gray-700'
					: ''}"
			>
				<Home class="w-5 h-5 mr-3" />
				Dashboard
			</button>

			<button
				on:click={() => handleNavigation('/user/dashboard/rooms', 'rooms')}
				class="flex items-center w-full px-4 py-2 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 {selected ===
				'rooms'
					? 'bg-gray-100 dark:bg-gray-700'
					: ''}"
			>
				<BedDouble class="w-5 h-5 mr-3" />
				Browse Rooms
			</button>


			<button
				on:click={() => handleNavigation('/user/dashboard/reservations/list', 'rooms')}
				class="flex items-center w-full px-4 py-2 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 {selected ===
				'rooms'
					? 'bg-gray-100 dark:bg-gray-700'
					: ''}"
			>
				<ReceiptSwissFranc class="w-5 h-5 mr-3" />
				Reservation List
			</button>

			<button
				on:click={() =>
					handleNavigation(
						'/user/dashboard/reservations',
						'reservations',
					)}
				class="flex items-center w-full px-4 py-2 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 {selected ===
				'reservations'
					? 'bg-gray-100 dark:bg-gray-700'
					: ''}"
			>
				<Calendar class="w-5 h-5 mr-3" />
				Reserve
			</button>

			<button
				on:click={() =>
					handleNavigation('/user/dashboard/payments', 'payments')}
				class="flex items-center w-full px-4 py-2 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 {selected ===
				'payments'
					? 'bg-gray-100 dark:bg-gray-700'
					: ''}"
			>
				<CreditCard class="w-5 h-5 mr-3" />
				Payments
			</button>

			<button
				on:click={() =>
					handleNavigation('/user/dashboard/profile', 'profile')}
				class="flex items-center w-full px-4 py-2 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 {selected ===
				'profile'
					? 'bg-gray-100 dark:bg-gray-700'
					: ''}"
			>
				<User class="w-5 h-5 mr-3" />
				Profile
			</button>
		</nav>

		<div class="p-4 border-t dark:border-gray-700">
			<button
				class="flex items-center w-full px-4 py-2 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
				on:click={logout}
			>
				<LogOut class="w-5 h-5 mr-3" />
				Logout
			</button>
		</div>
	</div>
</aside>
