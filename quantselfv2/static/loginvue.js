Vue.component('login',{

    props:['message'],

    template:`
    <div class="container py-5 z-depth-1">
    <section class="px-md-5 mx-md-5 text-center text-lg-left dark-grey-text">
        <div class="row d-flex justify-content-center">
        <div class="col-md-6">
            <form class="text-center" method="POST" action="">
            <p class="h4 mb-4">Log In</p>
            <input type="text" id="defaultRegisterFormEmail" name="logusername" class="form-control mb-4" placeholder="Username">
            <input type="password" id="defaultRegisterFormPassword" name="logpassword" class="form-control" v-model="pass1" placeholder="Password" aria-describedby="defaultRegisterFormPasswordHelpBlock">
            <small id="defaultRegisterFormPhoneHelpBlock" class="form-text text-danger mb-4">{{message}}</small>
            <button class="btn btn-info my-4 btn-block" name="formpurpose" value="loginval" type="submit">Log in</button>
            </form>
        </div>
        </div>
    </section>
    </div>
    `
})



Vue.component('signup',{

    props:['message'],
    
    template:`
    <div class="container py-5 z-depth-1">
    <section class="px-md-5 mx-md-5 text-center text-lg-left dark-grey-text">
        <div class="row d-flex justify-content-center">
        <div class="col-md-6">
            <form class="text-center" method="POST" action="">
            <p class="h4 mb-4">Sign Up</p>
            <div class="form-row mb-4">
                <div class="col"><input type="text" id="defaultRegisterFormFirstName" name="naam" class="form-control" placeholder="First name"></div>
                <div class="col"><input type="text" id="defaultRegisterFormLastName" name="upnaam" class="form-control" placeholder="Last name"></div>
            </div>
            <input type="text" id="defaultRegisterFormEmail" name="sgnusername" class="form-control mb-4" placeholder="Username">
            <input type="email" id="defaultRegisterFormEmail" name="email" class="form-control mb-4" placeholder="Email">
            <input type="password" id="defaultRegisterFormPassword" name="sgnpassword" class="form-control" v-model="pass1" placeholder="Password" aria-describedby="defaultRegisterFormPasswordHelpBlock">
            <input type="password" id="defaultRegisterPhonePassword" name="repassword" class="form-control" v-model="pass2" placeholder="Re Enter Password" aria-describedby="defaultRegisterFormPhoneHelpBlock">
            <small id="defaultRegisterFormPasswordHelpBlock" class="form-text text-danger mb-4">{{ whatpwd }}</small>
            <button class="btn btn-info my-4 btn-block" :disabled='bulian' name="formpurpose" value="signupval" type="submit">Sign in</button>
            </form>
        </div>
        </div>
    </section>
    </div>
    `,

    data(){
        return{
            whatpwd:'',
            pass1:'',
            pass2:'',
            bulian:true,
        }
    },

    watch:{
        pass1(a){
            if(a.length<=8){
                this.whatpwd="Should contain atleast 8 Alphanumeric Characters!";
                this.bulian=true;
            }else{
                this.whatpwd="";
                if( this.pass1===this.pass2){
                    this.bulian=false;
                }else{
                    this.bulian=true;
                }
            }
        },
        pass2(a){
            if(a!=this.pass1){
                this.whatpwd="Passwords do not match!";
                this.bulian=true;
            }else{
                this.whatpwd="";
                if( this.pass1===this.pass2){
                    this.bulian=false;
                }
            }
        },
    },
    
})



var app=new Vue({

    el:'#app',

    data:{
        formtype:'Log In',
        nonform:'Sign Up',
        extra1:"Don't have an account?",
    },

    methods:{
        toggleform:function(){
            if (this.formtype=="Log In"){
                this.formtype="Sign Up";
                this.nonform='Log In';
                this.extra1="Already have an account?";
            }else{
                this.formtype='Log In';
                this.nonform="Sign Up";
                this.extra1="Don't have an account?";
            }
        },
    },

})