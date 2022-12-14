// TODO: Add SDKs for Firebase products that you want to use
    // https://firebase.google.com/docs/web/setup#available-libraries

    // Your web app's Firebase configuration
    // For Firebase JS SDK v7.20.0 and later, measurementId is optional
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
     // Comment out any lines corresponding to providers you did not check in
     // the Firebase console.
     firebase.auth.GoogleAuthProvider.PROVIDER_ID,
     firebase.auth.EmailAuthProvider.PROVIDER_ID,
     //firebase.auth.FacebookAuthProvider.PROVIDER_ID,
     //firebase.auth.TwitterAuthProvider.PROVIDER_ID,
     //firebase.auth.GithubAuthProvider.PROVIDER_ID,
     //firebase.auth.PhoneAuthProvider.PROVIDER_ID
     ],
     // Terms of service url.
     tosUrl: '<your-tos-url>'
     };
    
        // Initialize Firebase
       // Initialize Firebase
    firebase.initializeApp(firebaseConfig);
    firebase.analytics();
    const auth = firebase.auth();
    console.log(firebase);
    
    // https://dev.to/maasak/sign-up-login-logout-users-with-firebase-authentication-3oa9
    const signupBtn = document.querySelector('#signup-btn');
        signupBtn.addEventListener('click', e => {
        e.preventDefault();
    
        const email = document.querySelector('#email').value;
        const password = document.querySelector('#password').value;
    
        auth.createUserWithEmailAndPassword(email, password).then(cred => {
        console.log('User signed up!');
      });
    });
    
    
    const loginBtn = document.querySelector('#login-btn');
      loginBtn.addEventListener('click', e => {
    
      const email = document.querySelector('#email').value;
      const password = document.querySelector('#password').value;
    
      console.log(email);
      console.log(password);
    
    
      auth.signInWithEmailAndPassword(email, password)
        .then(cred => {
          console.log('Logged in user!');
        })
        .catch(error => {
          alert(error.message);
        })
    });
    
    auth.onAuthStateChanged(user => {
      if (user) {
        console.log(user.email + " is logged in!");
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
            url = window.location.href.slice(0, -5); // Remove login from end of url
            location.href = url + '/store'; // User's logged in, now load the store
        }); 
      } else {
        var ui = new firebaseui.auth.AuthUI(firebase.auth());
        // Show the Firebase login button.
        ui.start('#firebaseui-auth-container', uiConfig); 
        console.log('User is logged out!');
        document.cookie = "token=" + "; path=/";;
      }
    });