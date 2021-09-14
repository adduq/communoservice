<template>
	<div class="page-my-account">
		<div class="columns is-multiline">
			<div class="column is-12">
				<h1 class="title">Mon compte</h1>
			</div>

			<div class="column is-12">
				<button @click="logout()" class="button is-danger">Déconnexion</button>
			</div>

			<hr />
		</div>
	</div>
</template>

<script>
import axios from "axios";
export default {
	name: "MyAccount",
	data() {
		return {
			orders: [],
		};
	},
	mounted() {
		document.title = "Mon compte | Communoservice";
	},
	methods: {
		logout() {
			axios.defaults.headers.common["Authorization"] = "";
			localStorage.removeItem("token");
			localStorage.removeItem("username");
			localStorage.removeItem("userid");
			this.$store.commit("removeToken");
			this.$router.push("/");
		}
	},
};
</script>
