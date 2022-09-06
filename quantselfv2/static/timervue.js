const navbar=Vue.component('navbar',{
    props:['named'],
    template:`

    <nav class="navbar navbar-expand-lg navbar-light white" style="background-image: url(https://blog.redbubble.com/wp-content/uploads/2018/05/andywestface_keep-think-creative-banner.jpg);">
    <div class="container"> 
        <span class="navbar-brand" href="#"><h1>Hi {{named}}</h1></span>
        <ul class="navbar-nav mr-auto"></ul>
        <ul class="navbar-nav nav-flex-icons">
            <li class="nav-item">
            <a href="" class="nav-link btn-dark text-white rounded waves-effect mr-2">Logout</a>
            </li>
        </ul>
    </div>
    </nav>
    `,
})

var app=new Vue({
    el:'#app',
    data : {
        message : ''
    },
    methods : {
        send_message : function() {
            let data = {'text' : this.message}
            fetch('https://chat.googleapis.com/v1/spaces/AAAAiOGrH4I/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=PRCEzdw2CUOXU3KZRQJYAwdTfEDYbfZ3pCMFeiwPfQI%3D', {
                method : 'POST',
                body : JSON.stringify(data)
            }).then(r => r.json()
            ).then(d => console.log(d)
            ).catch(e => console.log("Some error occured:", e))
        }
    }
})