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
    addtime:new Date().toLocaleString(),
})