<!-- src/routes/admin/+page.svelte -->
<script lang="ts">
    import { goto } from "$app/navigation";
    import { PUBLIC_BASE_URL } from "$env/static/public";
    import type { UserProfile } from "$lib/types";
    import { Loader2 } from "lucide-svelte";

    let username = "";
    let password = "";
    let isLoading = false;
    let error: string | null = null;
    let showPassword = false;
    let rememberMe = false;

    async function handleLogin(e: SubmitEvent) {
        e.preventDefault();
        isLoading = true;
        error = null;

        try {
            const loginResponse = await fetch(`${PUBLIC_BASE_URL}/auth/login/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username, password }),
                credentials: "include",
            });

            if (!loginResponse.ok) {
                throw new Error("Invalid credentials");
            }

            const profileResponse = await fetch(`${PUBLIC_BASE_URL}/users/profile/`, {
                credentials: "include",
            });

            if (!profileResponse.ok) {
                throw new Error("Failed to fetch user profile");
            }

            const userProfile: UserProfile = await profileResponse.json();

            if (!userProfile.is_superuser) {
                throw new Error("Unauthorized: Admin access required");
            }

            goto("/admin/dashboard");

        } catch (err) {
            if (err instanceof Error) {
                error = err.message;
            } else {
                error = "An unexpected error occurred";
            }
        } finally {
            isLoading = false;
        }
    }
</script>

<div class="min-h-screen bg-[#f3f2f0]">
    <!-- Logo Section -->
    <header class="py-8">
        <h1 class="text-3xl text-blue-600 font-bold text-center">Admin Panel</h1>
    </header>

    <!-- Main Content -->
    <main class="max-w-[400px] mx-auto px-4">
        <!-- Sign in card -->
        <div class="bg-white rounded-lg p-6 shadow-sm">
            <h2 class="text-2xl font-semibold text-[#000000E6] mb-1">
                Sign in
            </h2>
            <p class="text-sm text-[#00000099] mb-6">
                Stay updated on hotel management system.
            </p>

            <form class="space-y-6" on:submit={handleLogin}>
                {#if error}
                    <div class="p-4 bg-red-50 text-red-700 text-sm rounded">
                        {error}
                    </div>
                {/if}

                <div class="space-y-4">
                    <input
                        type="text"
                        bind:value={username}
                        class="w-full px-3 py-[12px] text-[16px] border border-[#00000099] rounded focus:border-2 focus:border-blue-600 focus:outline-none placeholder:text-[#00000099]"
                        placeholder="Username"
                        required
                        disabled={isLoading}
                    />

                    <div class="relative">
                        <input
                            type={showPassword ? "text" : "password"}
                            bind:value={password}
                            class="w-full px-3 py-[12px] text-[16px] border border-[#00000099] rounded focus:border-2 focus:border-blue-600 focus:outline-none placeholder:text-[#00000099]"
                            placeholder="Password"
                            required
                            disabled={isLoading}
                        />
                        <button
                            type="button"
                            class="absolute right-3 top-1/2 -translate-y-1/2 text-blue-600 text-sm font-medium"
                            on:click={() => showPassword = !showPassword}
                        >
                            {showPassword ? 'Hide' : 'Show'}
                        </button>
                    </div>
                </div>

                <div class="flex items-center justify-between">
                    <label class="flex items-center">
                        <input
                            type="checkbox"
                            bind:checked={rememberMe}
                            class="w-4 h-4 border-[#00000099] rounded text-blue-600 focus:ring-blue-500"
                        />
                        <span class="ml-2 text-[16px] text-[#000000E6]">Keep me logged in</span>
                    </label>

                    <button 
                        type="button" 
                        class="text-blue-600 font-medium text-[16px] hover:underline"
                    >
                        Forgot password?
                    </button>
                </div>

                <button
                    type="submit"
                    class="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-full py-3 px-4 font-medium text-[16px] disabled:opacity-50 transition-colors"
                    disabled={isLoading}
                >
                    {#if isLoading}
                        <Loader2 class="w-5 h-5 animate-spin mx-auto" />
                    {:else}
                        Sign in
                    {/if}
                </button>
            </form>
        </div>

        <!-- Contact Info -->
        <div class="mt-4 text-center">
            <p class="text-sm text-[#00000099]">
                Don't have access? <a href="mailto:admin@hotel.com" class="text-blue-600 font-medium hover:underline">Contact administrator</a>
            </p>
        </div>
    </main>

    <!-- Footer -->
    <footer class="mt-8 text-center pb-8">
        <nav class="flex flex-wrap justify-center gap-x-3 gap-y-2 text-xs text-[#00000099]">
            <a href="#" class="hover:text-blue-600 hover:underline">User Agreement</a>
            <a href="#" class="hover:text-blue-600 hover:underline">Privacy Policy</a>
            <a href="#" class="hover:text-blue-600 hover:underline">Community Guidelines</a>
            <a href="#" class="hover:text-blue-600 hover:underline">Cookie Policy</a>
            <a href="#" class="hover:text-blue-600 hover:underline">Copyright Policy</a>
            <a href="#" class="hover:text-blue-600 hover:underline">Send Feedback</a>
            <span>Language</span>
        </nav>
    </footer>
</div>