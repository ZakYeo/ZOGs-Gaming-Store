const firebaseConfig = {
    apiKey: "AIzaSyAopZxjnk3TnQMPg9NUouUvC6aIsvtDCyo",
    authDomain: "ad-2021-03.firebaseapp.com",
    projectId: "ad-2021-03",
    storageBucket: "ad-2021-03.appspot.com",
    messagingSenderId: "243759511961",
    appId: "1:243759511961:web:8e19eab1cbf743c9d27b08",
    measurementId: "G-FKJT5126NC"
  };
  // FirebaseUI config.
  var uiConfig = {
    signInSuccessUrl: '/',
    signInOptions: [
    firebase.auth.GoogleAuthProvider.PROVIDER_ID,
    firebase.auth.EmailAuthProvider.PROVIDER_ID,
    ],
    tosUrl: ''
  };
  
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);
  firebase.analytics();
  const auth = firebase.auth();
  
  // https://dev.to/maasak/sign-up-login-logout-users-with-firebase-authentication-3oa9
  const signupBtn = document.querySelector('#signup-btn');
    signupBtn.addEventListener('click', e => {
    e.preventDefault();
  
    const email = document.querySelector('#email').value;
    const password = document.querySelector('#password').value;
  
    auth.createUserWithEmailAndPassword(email, password).then(cred => {
      alert('User signed up!');
    }).catch(error => {
      alert(error.message);
    });
  });
  
  
  
  
  auth.onAuthStateChanged(user => {
    if (user) {
      user.getIdToken().then(function (token) {
          // Add the token to the browser's cookies. The server will then be
          // able to verify the token against the API.
          document.cookie = "token=" + token + "; path=/";
          let xhr = new XMLHttpRequest();
          let url = window.location.href.split("login")[0];
          xhr.open("POST", `${url}/record` );
          xhr.setRequestHeader("Accept", "application/json");
          xhr.setRequestHeader("Content-Type", "application/json");
          xhr.send(`
          {"type": "login"}`
        );
          location.href = window.location.origin + '/store'; // User's logged in, now load the store
      }); 
    } else {
      var ui = new firebaseui.auth.AuthUI(firebase.auth());
      // Show the Firebase login button.
      ui.start('#firebaseui-auth-container', uiConfig); 
      document.cookie = "token=" + "; path=/";
    }
  });