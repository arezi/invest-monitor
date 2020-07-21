

// <navbar-app :page="'portfolio'"></navbar-app>

Vue.component('navbar-app', {
    template: `
    <nav class="navbar navbar-expand-md navbar-dark bg-dark fixed-top">
        <span class="px-2 mr-4 navbar-brand" style="border: 1px solid #999; background-color: #444; border-radius: 5px;">Monitor</span>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarsDefault">
          <span class="navbar-toggler-icon"></span>
        </button>
      
        <div class="collapse navbar-collapse" id="navbarsDefault">
          <ul class="navbar-nav mr-auto">
            <li :class="['nav-item', { active: page === 'portfolio' }]">
              <a class="nav-link" href="portfolio.html">Portfolio</a>
            </li>
            <li :class="['nav-item', { active: page === 'performance' }]">
              <a class="nav-link" href="performance.html">Performance</a>
            </li>
          </ul>
        </div>
    </nav>
    `,
    props: ['page'],
});


