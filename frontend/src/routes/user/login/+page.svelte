<script lang="ts">
  import { goto } from "$app/navigation";
  import { PUBLIC_BASE_URL } from "$env/static/public";
  import type { LoginDto } from "$lib/dtos/requests/login-request.dto";
  import type { RegisterRequestDto } from "$lib/dtos/requests/register-request.dto";
  import axios from "axios";
  import { onMount } from "svelte";
  import { fade, fly } from "svelte/transition";

  let isLogin = true;
  let email = "";
  let password = "";
  let username = "";
  let firstname = "";
  let lastname = "";


  onMount(async () => {

    const result = await axios.get(
      PUBLIC_BASE_URL + "/users/profile/",
      {
        withCredentials : true
      }
    )

    if(result.status == 200) goto("/user/dashboard")
    

  });

  // @ts-ignore
  async function handleSubmit(e) {
    e.preventDefault();

    try {
      if (isLogin) {
        const loginRequest: LoginDto = { username, password };
        const request = await fetch(PUBLIC_BASE_URL + "/auth/login/",{
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(loginRequest),
            credentials: "include"
        });

        if (request.ok) {
            // You might want to handle the response before redirecting
            const response = await request.json();
            goto("/user/dashboard");
        }

      } else {
        const registerRequest: RegisterRequestDto = {
          email,
          password,
          username,
          first_name: firstname,
          last_name: lastname,
        };
        const result = await axios.post(
          PUBLIC_BASE_URL + "/auth/register/",
          registerRequest
        );
        if (result.status === 201) isLogin = true;
      }
    } catch (error) {
      console.error(error);
      alert(isLogin ? "Login failed!" : "Registration failed!");
    }
  }
</script>

<div
  class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8"
>
  <div
    class="max-w-md w-full space-y-8 bg-white dark:bg-gray-800 p-8 rounded-xl shadow-lg"
    in:fly={{ y: 50, duration: 1000 }}
    out:fade
  >
    <div class="text-center">
      <h2 class="mt-6 text-3xl font-extrabold text-gray-900 dark:text-white">
        Welcome to our hotel
      </h2>
      <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
        {isLogin ? "Please Login" : "Please Signup"}
      </p>
      <button
        class="mt-2 text-blue-600 hover:text-blue-500 text-sm font-medium"
        on:click={() => (isLogin = !isLogin)}
      >
        {isLogin
          ? "Need an account? Sign up"
          : "Already have an account? Login"}
      </button>
    </div>

    <form class="mt-8 space-y-6" on:submit={handleSubmit}>
      <div class="rounded-md shadow-sm space-y-4">
        <div>
          <label
            for="username"
            class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
          >
            Username
          </label>
          <input
            id="username"
            bind:value={username}
            type="text"
            required
            class="appearance-none relative block w-full px-3 py-2.5 border border-gray-300 dark:border-gray-600 placeholder-gray-500 text-gray-900 dark:text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 transition-all duration-300"
            placeholder="johndoe"
          />
        </div>

        {#if !isLogin}
          <div>
            <label
              for="email"
              class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
            >
              Email address
            </label>
            <input
              id="email"
              bind:value={email}
              type="email"
              required
              class="appearance-none relative block w-full px-3 py-2.5 border border-gray-300 dark:border-gray-600 placeholder-gray-500 text-gray-900 dark:text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 transition-all duration-300"
              placeholder="name@example.com"
            />
          </div>

          <div>
            <label
              for="firstname"
              class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
            >
              Firstname
            </label>
            <input
              id="firstname"
              bind:value={firstname}
              type="text"
              required
              class="appearance-none relative block w-full px-3 py-2.5 border border-gray-300 dark:border-gray-600 placeholder-gray-500 text-gray-900 dark:text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 transition-all duration-300"
              placeholder="John"
            />
          </div>

          <div>
            <label
              for="lastname"
              class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
            >
              Lastname
            </label>
            <input
              id="lastname"
              bind:value={lastname}
              type="text"
              required
              class="appearance-none relative block w-full px-3 py-2.5 border border-gray-300 dark:border-gray-600 placeholder-gray-500 text-gray-900 dark:text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 transition-all duration-300"
              placeholder="Doe"
            />
          </div>
        {/if}

        <div>
          <label
            for="password"
            class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
          >
            Password
          </label>
          <input
            id="password"
            bind:value={password}
            type="password"
            required
            class="appearance-none relative block w-full px-3 py-2.5 border border-gray-300 dark:border-gray-600 placeholder-gray-500 text-gray-900 dark:text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 transition-all duration-300"
            placeholder="••••••••"
          />
        </div>
      </div>

      <button
        type="submit"
        class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-300 transform hover:scale-[1.02]"
      >
        {isLogin ? "Sign in" : "Sign up"}
      </button>
    </form>
  </div>
</div>
