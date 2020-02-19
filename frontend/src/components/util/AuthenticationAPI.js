class AuthenticationAPI {
  constructor(http) {
    this.http = http;
    this.urls = {
      registration: "/auth/registration/",
      login: "/api-token-auth/",
      account: "/auth/account"
    };
    this.error = null;
  }

  registration(username, email, passwd) {
    return new Promise((resolve, reject) => {
      this.http
        .post(this.urls.registration, {
          username: username,
          email: email,
          password: passwd
        })
        .then(response => {
          if (response.status === 200) {
            const errors = JSON.parse(response.data);
            this.getFirstError(errors);
            reject(this.error);
          } else if (response.status === 201) {
            resolve();
          }
        });
    });
  }

  getFirstError(errors) {
    if (errors.hasOwnProperty("username")) {
      this.error = errors.username[0];
    } else if (errors.hasOwnProperty("email")) {
      this.error = errors.email[0];
    }
  }

  login(username, passwd) {
    return new Promise((resolve, reject) => {
      this.http
        .post(this.urls.login, {
          username: username,
          password: passwd
        })
        .then(response => {
          if (response.status === 200 && "token" in response.data) {
            resolve(response.data.token);
          } else {
            reject("Váratlan hiba történt!");
          }
        })
        .catch(() => {
          reject("Helytelen felhasználónév vagy jelszó!");
        });
    });
  }

  getUserInformation() {
    return new Promise((resolve, reject) => {
      this.http
          .get("/auth/account")
          .then(response => {
            resolve(response.data);
          })
          .catch(err => {
            return reject(err);
          })
    });
  }
}

export default AuthenticationAPI;
