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

const begin=Vue.component('begin',{
    template:`
    <div>choos acshan</div>
    `,
})

const addt=Vue.component('addt',{

    template:`
        <div class="container z-depth-1 my-5 px-0">
        <section class="text-center">
        <form class="mb-5 mx-md-5" @submit.prevent="submit">
            <div class="row">
            <div class="col-md-6 mb-4"><input type="text" id="tablename" v-model="addname" class="form-control" placeholder="Table Name" readonly></div>
            <div class="col-md-6 mb-4"><input type="text" id="curtime" v-model="addtime" class="form-control" placeholder="Current Time" readonly></div>
            </div>
            <div class="row"><div class="col-md-12 mb-4"><input type="text" v-model="adddata" id="subject" class="form-control" placeholder="Enter Data"></div></div>
            <div class="row">
            <div class="col-md-12">
                <div class="form-group mb-4"><textarea class="form-control rounded" id="message" v-model="adddesc" rows="3" placeholder="Enter Description"></textarea></div>
                <div class="text-center"><button type="submit" class="btn btn-dark">Submit</button></div>
            </div>
            </div>
        </form>
        </section>
        </div>
    `,

    data(){
        return{
            addname:'',
            addtime:new Date().toLocaleString(),
            adddata:'',
            adddesc:'',
        }
    },

    created(){
        const field=document.querySelector("input[name=idlabeler]").value
        this.addname=field
    },

    methods: {
        submit() {
            alert(`submitted`)
        }
    }

})

const editt=Vue.component('editt',{
    template:`<div><h1>editt</h1></div>`,
})

const deletet=Vue.component('deletet',{
    template:`<div><h1>deletet</h1></div>`,
})
const exportt=Vue.component('exportt',{
    template:`<div><h1>exportt</h1></div>`,
})


const router = new VueRouter({
    routes:[{path: '/',component: begin},
            {path: '/addt',component: addt},
            {path: '/editt',component: editt,},
            {path: '/deletet',component: deletet,},
            {path: '/exportt',component: exportt,},
    ],
})

var app=new Vue({
    el:'#app',
    router:router,
    // data(){
    //     return{
    //         idlabel:''
    //     }
    // },
    // created () {
    //     const field=document.querySelector("input[name=idlabeler]").value
    //     this.idlabel=field
    //     alert(this.idlabel)
    // }
    
})