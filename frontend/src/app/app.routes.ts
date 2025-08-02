import { Routes } from '@angular/router';
import { HomeComponent } from './features/home/home.component'
import { DetailsComponent } from './features/details/details.component'

const routeConfig: Routes = [
    {
        path: '',
        component: HomeComponent,
        title: 'Home page',
    },
    {
        path: 'details/:id',
        component: DetailsComponent,
        title: 'Home details',
    },
];

export default routeConfig;
