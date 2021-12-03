<template>
	<div class="page-sign-up">
		<div class="columns">
			<div class="column is-4 is-offset-4">
				<h1 class="title">Inscription</h1>

				<form @submit.prevent="submitForm">
					<div class="field">
						<label>Nom d'utilisateur</label>
						<div class="control">
							<input type="text" class="input" :class="this.usernameError ? 'is-danger': ''" v-model="this.username" @focus="this.usernameError = false" />
						</div>
					</div>

					<div class="field">
						<label>Mot de passe</label>
						<div class="control">
							<input type="password" class="input" :class="this.passwordError ? 'is-danger': ''" v-model="this.password" @focus="this.passwordError = false"/>
						</div>
					</div>

					<div class="field">
						<label>Répéter le mot de passe</label>
						<div class="control">
							<input type="password" class="input" :class="this.password2Error ? 'is-danger': ''" v-model="this.password2" @focus="this.checkPasswordMatch" @input="this.checkPasswordMatch"/>
						</div>
					</div>

					<div class="notification is-danger" v-if="errors.length">
						<p v-for="error in errors" v-bind:key="error">{{ error }}</p>
					</div>

					<div class="field">
						<div class="control">
							<button class="button is-dark">Inscription</button>
						</div>
					</div>

					<hr />

					Ou <router-link to="/connexion">me connecter !</router-link>
				</form>
			</div>
		</div>
	</div>
</template>

<script>
import axios from "axios";
import { toast } from "bulma-toast";

export default {
	name: "SignUp",
	data() {
		return {
			username: "",
			usernameError: false,
			password: "",
			passwordError: false,
			password2: "",
			password2Error: false,
			errors: [],
		};
	},
	mounted() {
		document.title = "Inscription | Communoservice";
	},
	methods: {
		submitForm() {
			const formData = {
				username: this.username,
				password: this.password,
			};

			if(this.validateFormData(formData)){
				axios
					.post("/api/v1/users/", formData)
					.then((response) => {
						toast({
							message: "Compte créé, connectez-vous!",
							type: "is-success",
							dismissible: true,
							pauseOnHover: true,
							duration: 2000,
							position: "bottom-right",
						});

						this.$router.push("/connexion");
					})
					.catch((error) => {
						if (error.response.status === 400) {
							for (const property in error.response.data) {
								switch (property) {
									case "username":
										error.response.data["username"].forEach(usernameErr => this.errors.push(usernameErr));
										this.usernameError = true;
										break;
									case "password":
										error.response.data["password"].forEach(passwordErr => this.errors.push(passwordErr));
										this.passwordError = true;
										this.password2Error = true;
									break;
								}
							}
						} else {
							this.errors.push("Une erreur est survenue");
							console.log(error);
						}
					});	
			}
		},
		validateFormData(formData){
			this.errors.splice(0);
			let validUsername = true, validPasswords = true;

			if(!formData.username.trim()){
				this.errors.push("Le nom d'utilisateur est invalide");
				this.usernameError = true;
				validUsername = false;
			}
			if(formData.password.trim().length < 8){
				this.errors.push("Le mot de passe doit contenir au minimum 8 caractères");
				validPasswords = false;
				this.passwordError = true;
				this.password2Error = true;
			}
			else if(formData.password.trim() != this.password2.trim()){
				this.errors.push("Les mots de passe ne correspondent pas")
				validPasswords = false;
				this.passwordError = true;
				this.password2Error = true;
			}

			return validUsername && validPasswords;
		},
		checkPasswordMatch(e){
			if(e.target.value != this.password){
				this.password2Error = true;
			}else{
				this.password2Error = false;
			}
		}
	},
};
</script>
