import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {HomeComponent} from "./components/home/home.component";
import {PageNotFoundComponent} from "./components/page-not-found/page-not-found.component";
import {AuthGuard} from "./guards/authguard.guard";
import { AdminGuard } from "./guards/adminguard.guard";

const routes: Routes = [
  { path: '', component: HomeComponent},
  {
    path: 'parcel',
    loadChildren: ()=> import('../app/components/parcels/parcels.module').then(m => m.ParcelsModule),
    canActivate: [AuthGuard]
  },
  {
    path: 'backend',
    loadChildren: ()=> import('../app/components/admin/admin.module').then(m => m.AdminModule)
  },
  { path: '**', component: PageNotFoundComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
